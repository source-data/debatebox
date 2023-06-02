from argparse import ArgumentParser

from .debate import Debate
from .config import SEED_MESSAGES, DEFAULT_CONTEXT_LENGTH

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--seed_content", type=str, help="The seed content to frame the debate")
    parser.add_argument("--seed_topic", type=str, choices=SEED_MESSAGES.keys(), default="human_intelligence_evol", help=f"The seed topic to frame the debate (alternative to seed_content, availaible choice:{SEED_MESSAGES.keys()}, default: human_intelligence_evolution)")
    parser.add_argument("--max_rounds", type=int, default=1, help="The maximum number of rounds of debating.")
    parser.add_argument("--steps", type=str, nargs="+", default=[], help="The steps of the debate (default 'critique revision')")
    parser.add_argument("--verbose", default=False, action="store_true", help="Whether to print the internal working of the critique/revision steps (default False).")
    parser.add_argument("--protagonists", type=str, nargs="+", default=["scientist_one", "scientist_two"], help="The protagonists of the debate (default 'scientist_one scientist_two').")
    parser.add_argument("--run_dir", type=str, default="/runs", help="The directory where to save the run (default '/runs').")
    parser.add_argument("--context_length", type=int, default=DEFAULT_CONTEXT_LENGTH, help="The number of messages to use as context (default 4).")
    parser.add_argument('--mode', type=str, choices=["sequential", "random_no_repeat", "random_with_replacement"], default="sequential", help="The mode of the debate (default 'sequential').")
    args = parser.parse_args()

    steps = args.steps
    if steps == [""]:
        steps = []

    debate = Debate(
        args.protagonists,
        run_dir=args.run_dir,
    )

    debate.run(
        seed_content=SEED_MESSAGES[args.seed_topic] if args.seed_content is None else args.seed_content,
        max_rounds=args.max_rounds,
        steps=steps,
        verbose=args.verbose,
        context_length=args.context_length,
        mode=args.mode
    )
