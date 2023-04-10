from typing import List, Dict
from .chatbox import ChatBox
from .constitution import MODEL
from .utils import wrapped_print


class Debate:
    def __init__(self, protagonists: List[str]):
        # initialize the chat boxes
        self.protagonists = [ChatBox(character=p) for p in protagonists]
        # a default seed message content for demo
        self.seed_content = {
            "role": "user",
            "content": "What is the most likely explanation for the emergence of human intelligence?"
        }

    def run(self, seed_content: str = "", max_rounds: int = 2, steps: List[str] = ["critique", "revision"], verbose: bool = False):
        # set level of verbosity
        for p in self.protagonists:
            p.verbose = verbose
        # initialize the first message that will trigger the debate
        msg = {
            "role": "user",
            "content": seed_content if seed_content else self.seed_content
        }
        print(f"This debate is run with: {MODEL}\n")
        wrapped_print("framing", seed_content)
        self.debating_loop(msg, max_rounds, steps)

    def debating_loop(self, seed_message, max_rounds, steps):
        # frame the debate with the seed message
        msg = seed_message
        for _ in range(max_rounds):
            # sequential strategy to invoke protagonists
            # Maybe a little randomness or asking them first if they wish to comment could be alternative strategies.
            for idx, debater in enumerate(self.protagonists):
                msg = self.debating_step(msg, debater, steps)  # the reply has the role "assistant", it will be changed to "user" when fed to the other protagonist
                wrapped_print(f'{debater.character}_{idx}', msg["content"])

    def debating_step(self, input_msg: Dict[str, str], character: ChatBox, steps) -> Dict[str, str]:
        # from the point of view of the current character, the input is from "user" and the reply will be from "assistant"
        # since the input message come from the previous round is has likely role "assistant" and needs to be update to "user"
        # to reflect the change of perspective.
        input_msg["role"] = "user"
        output_msg = character.reply(input_msg, steps=steps)
        return output_msg

    def dump(self, idx: int):
        chat_box = self.protagonists[idx]
        print(chat_box.character)
        print(chat_box.principles)
        for message in chat_box.chat:
            wrapped_print(message["role"], message["content"])
