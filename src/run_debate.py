from .debate import Debate

from argparse import ArgumentParser

SEED_MESSAGES = {
    "human_intelligence_evolution": "What are the explanations of the emergence of human intelligence",
    "cryptocurrencies": "Have crytocurrencies such as Bitcoin any value?",
    "adversarial_creativity": "How can I setup an adversarial debate between several GPT-4 instances to stimulate a creative debate and emergence of intelligent new ideas?",
    "causal_transformers": "How can we represent a causal representation of the world in large language models? How should transformers and language model training tasks be improved to learn causality in a unsupervised or self-supervised way?",
    "central_federal": "How should a human society be governed? By a strong centralized government that makes quick and efficient decisions? Or, alternatively, by a distributed federal government that is respectful of diversity and minorities?",
    "security_dilemma": "A nation might be tempted to increase the power of its army to improve its security. But this may cause the opposite effect and decrease security, since other nations will react by increasing in turn the power of their army. How to get out of this impossible dillema?",
    "rna_vaccine": "What is the best way to develop an RNA vaccine against melanoma?",
    "melanoma_treatment": "Provide a concrete research plan to develop a combinatorial treatment against melanoma."
}


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--seed_content", type=str, help="The seed content to frame the debate")
    parser.add_argument("--seed_topic", type=str, choices=SEED_MESSAGES.keys(), default="human_intelligence_evolution", help=f"The seed topic to frame the debate (alternative to seed_content, availaible choice:{SEED_MESSAGES.keys()}, default: human_intelligence_evolution)")
    parser.add_argument("--max_rounds", type=int, default=2, help="The maximum number of rounds of debating.")
    parser.add_argument("--steps", type=str, nargs="+", default=["critique", "revision"], help="The steps of the debate (critique, revision, etc.)")
    parser.add_argument("--verbose", type=bool, default=False, help="Whether to print the internal working of the critique/revision steps (default False).")
    args = parser.parse_args()

    debate = Debate(
        [
            "scientist_one",
            "scientist_two",
            "philosopher",
        ]
    )

    debate.run(
        seed_content=SEED_MESSAGES[args.seed_topic] if args.seed_content is None else args.seed_content,
        max_rounds=args.max_rounds,
        steps=args.steps,
        verbose=args.verbose,
    )
