import json
import os
from typing import Any, Dict, List, Optional

import chainlit as cl
from chainlit import ThreadDict, logger
from chainlit.cli import run_chainlit
from dotenv import load_dotenv

from ui.utils.request_util import create_request, send_request

load_dotenv()


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.User]:
    valid_password = os.getenv("USER_CHAINLIT_PASSWORD", os.getenv("CHAINLIT_AUTH_SECRET"))

    if username.endswith("@gmail.com") and password == valid_password:
        return cl.User(identifier=username, metadata={"role": "user", "provider": "credentials"})

    return None


@cl.on_chat_resume
async def load_chat_history(thread: ThreadDict):
    primary_messages = [message for message in thread["steps"] if message.get("parentId") is None]
    cl.user_session.set("memory", primary_messages)


@cl.on_message
async def on_message(message: cl.Message) -> None:
    user = cl.user_session.get("user")
    conversation_id = cl.user_session.get("id")

    data = create_request(conversation_id=conversation_id, role="user", content=message.content)

    response = send_request(url=os.getenv("API_ENDPOINT"), user_message=data)

    await cl.Message(response["response"]).send()


if __name__ == "__main__":
    run_chainlit(__file__)
