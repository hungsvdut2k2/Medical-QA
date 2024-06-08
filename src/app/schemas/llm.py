from typing import Optional

from pydantic import BaseModel, Field

__all__ = ["InitParams", "InferenceParams"]


class InitParams(BaseModel):
    model_path_or_repo_id: Optional[str] = Field(default=None, title="Model Name", description="Model name or path")
    model_file: Optional[str] = Field(default=None, title="Model File Path", description="Model File path")
    model_type: Optional[str] = Field(default=None, title="Model Type Name", description="Model Type name")
    context_length: Optional[int] = Field(default=None, title="Context Length", description="Context length")
    gpu_layers: Optional[int] = Field(default=None, title="GPU Layers", description="Number of GPU layers")


class InferenceParams(BaseModel):
    top_k: Optional[int] = Field(default=None, title="Top K", description="Top K")
    top_p: Optional[float] = Field(default=None, title="Top P", description="Top P")
    temperature: Optional[float] = Field(default=None, title="Temperature", description="Temperature")
    stream: Optional[bool] = Field(default=None, title="Stream", description="Stream")
