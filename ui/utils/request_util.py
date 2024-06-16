from typing import Any, Optional

import requests

from ui.schemas import MessageBase


def create_request(**kwargs):
    return MessageBase(**kwargs)


def send_request(url: Optional[str], user_message: Optional[Any]):
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    data = user_message.model_dump()

    response = requests.post(url, headers=headers, json=data)

    return response.json()
