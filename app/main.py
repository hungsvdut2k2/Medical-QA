import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import chat
from app.core.llms import HuggingFaceLLM
from app.core.memories import ConversationMemory
from app.core.settings import app_settings
from app.core.vector_stores import QdrantVectorStore
from app.schemas import InferenceParams, InitParams
from app.services import ConversationManager

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_params = InitParams(
    model_path_or_repo_id=app_settings.model_path_or_repo_id,
    model_file=app_settings.model_file,
    model_type=app_settings.model_type,
    context_length=app_settings.context_length,
    gpu_layers=app_settings.gpu_layers,
)
inference_params = InferenceParams(
    top_k=app_settings.top_k, top_p=app_settings.top_p, temperature=app_settings.temperature, stream=app_settings.stream
)

conversation_memory = ConversationMemory(top_k=app_settings.memory_top_k)
vector_store = QdrantVectorStore(
    host_url=app_settings.host_url,
    model_name=app_settings.model_name,
    collection_name=app_settings.collection,
)
llm = HuggingFaceLLM(int_parameters=init_params, inference_parameters=inference_params)
conversation_manager = ConversationManager(llm=llm, vector_store=vector_store, memory=conversation_memory)

app.state.conversation_manager = conversation_manager


@app.get("/")
async def root():
    return {"detail": "Hello World"}


app.include_router(chat.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
