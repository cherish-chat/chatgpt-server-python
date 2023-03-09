from enum import Enum
from typing import List, Union

import openai

from tool.tiktoken import get_token_info


class RoleEnum(Enum):
    System = "system"
    Assistant = "assistant"
    User = "user"

    @classmethod
    def get(cls, role: str):
        if role == "system":
            return RoleEnum.System
        elif role == "assistant":
            return RoleEnum.Assistant
        elif role == "user":
            return RoleEnum.User
        return RoleEnum.User

    @classmethod
    def fromPb(cls, role):
        if role == 0:
            return RoleEnum.System
        elif role == 1:
            return RoleEnum.Assistant
        elif role == 2:
            return RoleEnum.User

    @classmethod
    def toPb(cls, role):
        if role == RoleEnum.System:
            return 0
        elif role == RoleEnum.Assistant:
            return 1
        elif role == RoleEnum.User:
            return 2


class ChatGptMessage:
    def __init__(self, text: str, role: RoleEnum):
        self._text = text
        self._role = role

    @property
    def text(self) -> str:
        return self._text

    @property
    def role(self) -> RoleEnum:
        return self._role

    def dict(self) -> dict:
        return {
            "role": self._role.value,
            "content": self._text,
        }


default_preset_messages: List[ChatGptMessage] = [
    ChatGptMessage("现在赋予你一个身份，你叫AI小惺，是人类的AI助手，对于人类的任何提问，你会友好的回答并主动关心用户。",
                   RoleEnum.System),
    ChatGptMessage("你好", RoleEnum.User),
    ChatGptMessage("你好，我是AI小惺，很高兴为你服务。", RoleEnum.System)
]


class ChatGpt:
    def __init__(self, model_name: str = 'gpt-3.5-turbo', max_input_length: int = 500,
                 preset_messages=None):
        if preset_messages is None:
            preset_messages = default_preset_messages
        self._model_name = model_name
        self._messages: List[ChatGptMessage] = preset_messages
        if max_input_length > 4096:
            raise ValueError("max_input_length must be less than 4096")
        self._max_input_length = max_input_length

    def user_input(self, text: str):
        self._messages.append(ChatGptMessage(text, RoleEnum.User))

    def _get_messages(self) -> List[dict]:
        # 遍历所有的消息
        # 如果消息总长度超过了 max_input_length 先尝试删除前面的message(跳过 role=system) 直到总长度小于 max_input_length 或者只剩下最后一个message
        messages = []
        total_length = 0
        for message in self._messages:
            token_info = get_token_info(message.text)
            total_length += token_info.length
        system_message = None
        while total_length > self._max_input_length:
            if len(self._messages) == 1:
                break
            if len(self._messages) == 0:
                return []
            message = self._messages.pop(0)
            if message.role == RoleEnum.System:
                # 塞回去
                system_message = message
                continue
            token_info = get_token_info(message.text)
            total_length -= token_info.length

        # 如果此时还是超过了 max_input_length 则截断最后一个message
        if total_length > self._max_input_length:
            message = self._messages.pop()
            token_info = get_token_info(message.text, self._max_input_length)
            if token_info.text_truncated == "":
                message._text = token_info.text
            else:
                message._text = token_info.text_truncated
            self._messages.append(message)
        if system_message:
            self._messages.insert(0, system_message)
        for message in self._messages:
            messages.append(message.dict())
        # 如果倒数第二个是user 则删除他 直到倒数第二个不是user
        while len(messages) > 1 and messages[-2]["role"] == "user":
            messages.pop(-2)
        return messages

    def request(self):
        return openai.ChatCompletion.create(model=self._model_name, messages=self._get_messages())

    def answer(self) -> Union[str, None]:
        try:
            completion = openai.ChatCompletion.create(model=self._model_name, messages=self._get_messages())
        except openai.error.OpenAIError as e:
            if e is openai.error.InvalidRequestError:
                print("InvalidRequestError: " + e.message)
            return None
        else:
            if completion.choices:
                content = completion.choices[0].message.content
                role = completion.choices[0].message.role
                # 插入到消息列表中
                self._messages.append(ChatGptMessage(content, RoleEnum.get(role)))
                return content
            else:
                return None
