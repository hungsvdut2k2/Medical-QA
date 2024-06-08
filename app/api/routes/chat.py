from typing import Optional

from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import MessageBase

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/completion", status_code=status.HTTP_200_OK)
async def get_completion(message: Optional[MessageBase], request: Request):
    conversation_manager = request.app.state.conversation_manager

    if len(message.content) == 0:
        raise HTTPException(status_code=400, detail="Message is empty")

    response = conversation_manager.handle_conversation(message=message)

    return {"response": response}
