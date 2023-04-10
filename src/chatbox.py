from typing import List, Dict
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt

from .constitution import (
    MODEL,
    CHARACTERS,
    PRINCIPLES,
    CONTEXT_LENGTH,
)
from .lib.utils import wrapped_print


class ChatBox():

    model: str = MODEL
    engine = openai.ChatCompletion

    def __init__(self, model: str = MODEL, character: str = "", verbose: bool = False):
        self.model = model
        self.character = character
        self.principles: List[Dict[str, str]] = PRINCIPLES[self.character]
        self.system_content: str = CHARACTERS[self.character] if self.character else ""
        self.chat = [
            {"role": "system", "content": self.system_content},
        ]
        self.context_length = CONTEXT_LENGTH  # forwared only last N entries of the chat otherwise quickly running out of tokens
        self.verbose = verbose  # whether the inner critique and revisions are displayed

    def reply(self, user_msg: Dict[str, str], steps: List[str] = ["critique", "revision"]):
        assert steps == [] or "revision" in steps, f"Critique without revision is not supported (steps={steps})."
        self.chat_step(user_msg)  # chat_step automatically logs messages and reponses in the chat
        refined_response = self.self_improve(steps)  # type: ignore
        return refined_response

    def chat_step(self, user_msg: Dict[str, str]):
        # the message and its response are logged in the chat
        self.append_to_chat(user_msg)  # message should include a field for the role of the message producer, e.g. "scientist", "philosopher"
        if self.verbose:
            wrapped_print(f'INTERNAL INPUT: {self.chat[-1]["role"]}', self.chat[-1]["content"], indent=4)
        # figure out the entry point in the chat to provide context
        idx = max(len(self.chat) - self.context_length, 0)
        context = self.chat[idx:]
        response = self.call_model(context)
        # extract the content of the response
        content = self.process_response(response)  # type: ignore
        # log the response in the chat
        self.append_to_chat(content)
        if self.verbose:
            wrapped_print(f'INTERNAL OUTPUT: {self.chat[-1]["role"]}', self.chat[-1]["content"], indent=4)
        return content

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def call_model(self, context: List[Dict[str, str]]):
        response = self.engine.create(
            model=self.model,
            messages=context
        )
        return response

    def self_improve(self, steps: List[str]) -> Dict[str, str]:
        # Simple implementation of 'constitutional AI. 
        # cycles through critiques and revisions to self improve the last item in the chat
        # according to the principles of the character
        # the last revision is returned as result
        for principle in self.principles:
            # requesting a critique first, as first step of a chain-of-thought approach
            if "critique" in steps:
                request_critique = {
                    "role": "user",
                    "content": principle["critique"]
                }
                self.chat_step(request_critique)
            # requesting a revision to integrate the principle, this can be done without the intermediate critique
            if "revision" in steps:
                request_revision = {
                    "role": "user",
                    "content": principle["revision"]
                }
                self.chat_step(request_revision)
        last_response = self.chat[-1]
        return last_response

    def process_response(self, response: Dict):
        content = response['choices'][0]['message']['content']
        role = response['choices'][0]['message']['role']
        reply_message = {
            "role": role,
            "content": content,
        }
        return reply_message

    def append_to_chat(self, message: Dict[str, str]):
        self.chat.append(message)
