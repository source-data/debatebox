from typing import List, Dict
from datetime import datetime
from .chatbox import ChatBox
from .constitution import MODEL
from .lib.utils import wrapped_print


class Debate:
    def __init__(self, protagonists: List[str]):
        # initialize the chat boxes
        self.protagonists = [ChatBox(character=p) for p in protagonists]

    def run(self, seed_content, max_rounds: int = 2, steps: List[str] = ["critique", "revision"], verbose: bool = False):
        # set level of verbosity
        for p in self.protagonists:
            p.verbose = verbose
        # initialize the first message that will trigger the debate
        msg = {
            "role": "user",
            "content": seed_content
        }
        print(f"{datetime.isoformat(datetime.now())}: This debate is run with: {MODEL}\n")
        wrapped_print("framing", seed_content)
        self.debating_loop(msg, max_rounds, steps)
        for p in self.protagonists:
            self.dump(p)

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

    def dump(self, chat_box: ChatBox, include_chat: bool = False):
        print(chat_box.character)
        print(chat_box.system_content)
        print(chat_box.principles)
        print("\n------------------\n")
        if include_chat:
            for m in chat_box.chat:
                wrapped_print(m["role"], m["content"])
