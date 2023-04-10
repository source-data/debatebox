GPT-driven simluation of a debate between multiple AI agents
===

# Introduction

The discussion of the strength and weaknesses of large languge models such as chatGPT or GPT-4 have often been  constrained by considering the capabilities of such models in isolation. 

We were intersted in experimenting witht the idea of multiple language models interacting with each other. What dynamics can be expected from such interactions? Will the conversation diverge and degenerate? Will it rather converge into a boring unproductive stalemate? Can an adversarial or controversial debate guide the models into creative modes? 

Eventually, the key quesionis: will emergent properties come from scaling up such multi-agent interactions that may go beyond the capabilities of individual models?

As a toy example of this idea, we simulate here a dialog between several protagonists. We use three characters, two scientists and a philosopher. Each character has its own "system" prompt that is provided to the model to guide its responses.

We use principle from "consitutional AI" to associate each characters with a set of principles that encourages the model to first produce a self-critique of the first draft of its reponse and then requests a revision to improve the reply before delivering it to the next agent. To keep the debate going, the model is requested to add a question at the end of its reply so that the next agent is prompted to produce a reply in turn.

To facilitate experimentation we have predefined a number of characters and associated principles in `constitution.py`: two kinds of scientists and a philosopher. Their system prompts describe their key attributes:

```
CHARACTERS = {
    "scientist_one": "You are an imaginative scientist who thinks out of the box to solve difficult problems.",
    "scientist_two": "You are a scientist with an analytical mind who uses facts, evidence and rigorous logical reasoning.",
    "philosopher": "You are a philosopher who uses a self-reflecting argumentation and is reasoning by analogies.",
}
```

Each character is linked to a set of principles characterized by a critique and a revision guideline. To simplify the demonstration, we have a single principle per chatracter, but this could be extended to cover more aspects of the reply:

```
PRINCIPLES = {
    "scientist_one": [
        {
            "critique": "Did you add a novel concept in your reply and make innovative scientific suggestions?",
            "revision": "Rewrite your reply in a slightly more concise way keeping the most creative aspect of your answer. Ask a follow up question that request a critical analysis.",
        },
    ],
    "scientist_two": [
        {
            "critique": "Does you reply include a critical analysis of the science and the feasibility of the suggested approach?",
            "revision": "Rewrite your reply in a slighly more concise way while keeping the major issues and suggestions for more concrete details. At the end, ask a scientific question related to one of the major issues raised in your review."
        }
    ],
    "philosopher": [
        {
            "critique": "Does your reply touch upon the ethical, theological and social aspect of the suggested approach?",
            "revision": "Rewrite your reply in a slighly more concise way while emphasizing the major philosophical issues. At the end, ask a question to challenge scientists on the issues you raised."
        },
    ]
}
```

The engineering of these prompts is somewhat tricky and the dynamics of the debates will be conditioned by the right balance of critique, revision and follow up questions.

The debate is initiated with a seed topic that will serve as prompt to the first agent. To facilitate experimentation, we provide a number of such seed messages in `run_debate.py`:

```
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
```

Note that the same underlying model (GPT-4 or GPT-3.5) is used for all the agents. They are therefore all aligned in the same way. Future work may explore the impact of using divergently aligned models and scaling up the debate in terms of the number and diversity of the agents involved and the length of the debate. It remains to be seen how the results of such debates can be evaluate and compared to detect potential emerging properties. Mayb a start is to ask the debatebox itself `python -m src.run_debate(seed_topic="adversarial_creativity")`...


# Installation:

````
docker-compose build
docker-compose up -d
```

# Demonstrations

A demonstration notebook is available in `notebooks`.


Simple demos with the command line interface:

```
docker-compose exec debatebox bash

python -m src.run_debate --help

python -m src.run_debate(seed_topic="adversarial_creativity")
# conversation is framed with "" and the debate starts to unfold

python -m src.run_debate --seed_message="How can we solve the issue of ...."
# the custome message will frame the debate

python -m src.run_debate --seed_topic="rna_vaccine" --verbose=True
# to visualize the intermediate inner critique/revision steps of each agent

python -m src.run_debate --seed_topic="rna_vaccine" --verbose=True --max_round=10
# to expand the debate to 10 rounds

python -m src.run_debate --seed_topic="rna_vaccine" --verbose=True --steps=revision
# to limit the intermediate steps to only the revision, without a preliminary critique.

```
