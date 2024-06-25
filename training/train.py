import wandb
import torch

from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from trl import SFTTrainer
from unsloth import FastLanguageModel

if __name__ == '__main__':

    base_model = "Viet-Mistral/Vistral-7B-Chat"
    dataset_name = "hungsvdut2k2/raft-vietnamese-meadow-wikidoc"

    wandb.login(key=wandb_api_key)
    wandb.init(
        entity="hungsvdut",
        project="medical-qa",
        name="vistral-raft-qa"
    )

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=base_model,
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit,
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model)

    dataset = load_dataset(dataset_name)["train"]

    model = FastLanguageModel.get_peft_model(
        model,
        r=16,  # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj", ],
        lora_alpha=16,
        lora_dropout=0,  # Supports any, but = 0 is optimized
        bias="none",  # Supports any, but = "none" is optimized
        use_gradient_checkpointing="unsloth",  # 4x longer contexts auto supported!
        random_state=3407,
        use_rslora=False,  # We support rank stabilized LoRA
        loftq_config=None,  # And LoftQ
    )

    dataset = dataset.map(lambda x: {"formatted_chat": tokenizer.apply_chat_template(x["conversation"], tokenize=False,
                                                                                     add_generation_prompt=False)})
    tokenizer.padding_side = 'right'

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        dataset_text_field="formatted_chat",
        max_seq_length=4096,
        dataset_num_proc=2,
        packing=False,  # Can make training 5x faster for short sequences.
        args=TrainingArguments(
            num_train_epochs=1,
            save_strategy="epoch",
            per_device_train_batch_size=4,
            gradient_accumulation_steps=16,
            warmup_steps=0.1,
            learning_rate=2e-5,
            fp16=not torch.cuda.is_bf16_supported(),
            bf16=torch.cuda.is_bf16_supported(),
            logging_steps=1,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="cosine",
            seed=42,
            output_dir="outputs",
            report_to="wandb",
        ),
    )

    trainer_stats = trainer.train()
    model.push_to_hub_merged("hungsvdut2k2/medical-qa-qwen-2", tokenizer, save_method="merged_16bit")