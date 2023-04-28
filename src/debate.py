from typing import List, Dict
from datetime import datetime
import json
import random
from .chatbox import ChatBox
from .config import MODEL
from .lib.utils import wrapped_print


class Debate:
    def __init__(self, protagonists: List[str], run_dir: str = "/runs"):
        # initialize the chat boxes
        self.protagonists = [ChatBox(character=p) for p in protagonists]
        self.run_dir = run_dir  # where to save the runs
        self.j_run = {
            "chatboxes": {},
            "model": MODEL,
            "max_rounds": None,
            "steps": None,
            "timestamp": None,
            "seed_message": None
        }

    def run(
        self,
        seed_content: str,
        max_rounds: int = 2,
        steps: List[str] = ["critique", "revision"],
        verbose: bool = False,
        context_length: int = 4,
        mode: str = "sequential",
    ):
        # set level of verbosity
        for p in self.protagonists:
            p.verbose = verbose
            p.context_length = context_length
        self.j_run["max_rounds"] = max_rounds
        self.j_run["steps"] = steps
        self.j_run["mode"] = mode
        debate_start = datetime.isoformat(datetime.now())
        self.j_run["timestamp"] = debate_start
        # initialize the first message that will trigger the debate
        msg = {
            "role": "user",
            "content": seed_content
        }
        self.j_run["seed_message"] = msg
        wrapped_print("framing", seed_content)
        self.debating_loop(msg, max_rounds, steps, mode)
        self.dump(self.run_dir)

    def debating_loop(self, seed_message, max_rounds, steps, mode):
        # the first pretagonist will receive the seed message and will reply
        # the seed message should be added to the chat of the other protagonists
        # so that its serves as context to the reply of the first protagonist
        for debater in self.protagonists[1:]:
            debater.append_to_chat(seed_message)
        # frame the debate with the seed message
        msg = seed_message
        for _ in range(max_rounds):
            if mode == "sequential":
                # sequential strategy to invoke protagonists
                debaters = self.protagonists
            elif mode == "random_no_repeat":
                # random strategy to invoke protagonists without repetition
                debaters = random.sample(self.protagonists, k=len(self.protagonists))
            elif mode == "random_with_replacement":
                # ranom sample with replacement
                debaters = random.choices(self.protagonists, k=len(self.protagonists))
            else:
                raise ValueError(f"mode {mode} not supported")
            for debater in debaters:
                msg = self.debating_step(msg, debater, steps)  # the reply has the role "assistant", it will be changed to "user" when fed to the other protagonist
                wrapped_print(f'{debater.character}', msg["content"])

    def debating_step(self, input_msg: Dict[str, str], character: ChatBox, steps) -> Dict[str, str]:
        # from the point of view of the current character, the input is from "user" and the reply will be from "assistant"
        # since the input message come from the previous round is has likely role "assistant" and needs to be update to "user"
        # to reflect the change of perspective.
        input_msg["role"] = "user"
        output_msg = character.reply(input_msg, steps=steps)
        return output_msg

    def dump(self, run_dir: str, include_chat: bool = False):
        for chat_box in self.protagonists:
            self.j_run["chatboxes"][chat_box.character] = chat_box.to_dict()
            print(chat_box.character)
            print(chat_box.model)
            print(chat_box.system_content)
            print(chat_box.principles)
        with open(f'{run_dir}/run_{self.j_run["timestamp"]}.json', 'w') as f:
            json.dump(self.j_run, f, indent=4)
