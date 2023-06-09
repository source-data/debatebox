GPT-driven simulation of a debate between multiple AI agents
===

# Introduction

The discussion of the strengths and weaknesses of large language models (LLM) such as chatGPT or GPT-4 have often been  constrained by considering the capabilities of such models in isolation. 

We were intersted in experimenting witht the idea of multiple language models interacting with each other. What dynamics can be expected from such interactions? Will the conversation diverge and degenerate? Will it rather converge into a boring unproductive stalemate? Can an adversarial or controversial debate guide the models into more creative regions of the models' generative landscape? Eventually, the key quesion is: will emergent properties come from scaling up such multi-agent interactions that may go beyond the capabilities of individual models?

The success of generative adversarial networks (GANs) in generating realistic images suggest that the adversarial strategy could be an interesting approach. The dynamics of adversarial systems are however notoriously difficult to control and predict. Balancing the objective function of each adversarial component to obtain convergence of the compound system towards the desired goal is challenging. The system may diverge uncontrolably to some random unwanted solutions or, alternatively, converge to a trivial state.

As a toy example of this idea applied to interacting LLM, we simulate here a dialog between several protagonists simulated by chatGPT or GPT-4. We use three "characters", two "scientists" and a "philosopher". Each character is described by its own GPT "system" prompt that is provided to the model to guide its responses.

We use concepts from "consitutional AI" (Bai et al 20221, Constitutional AI: Harmlessness from AI Feedback, [arXiv:2212.08073](https://doi.org/10.48550/arXiv.2212.08073)) and few-shot prompting to setup our debating simulation. In the original work by Anhtropic, a set of 'constitutional principles', written in natural language, were used to align the responses of a model in a transparent self-improving process. The principles were used by the model to self-criticize and then revise its responses. This process openened the door to the automated generation of a large-scale alignment dataset that can in turn be used to further fine tune the initial model by Reinforcement Learning with AI Feedback.

Here, we use similar concepts albeit at a much more modest scale and without model realignement. Each character is associated with a set of "principles" that encourage the model to self-improve its reply. First, it is requested to produce a self-critique of the first draft of its reponse. In a second step, revision is requested before delivering the final reply to the next agent. To keep the debate going, the model is asked to add a question at the end of its reply so that the next agent is prompted to produce a reply in turn.

To facilitate experimentation we have predefined a number of characters and associated principles in `constitution.py`: two kinds of scientists and a philosopher. Their system prompts describe their key attributes:

```python
CHARACTERS = {
    "scientist_one": "You are a computer scientist who thinks out of the box and connects different domains in new ways.",
    "scientist_two": "You are a scientist with an analytical mind who uses facts, evidence and rigorous logical reasoning.",
    "scientist_three": "You are very critical and always try to disagree and find flaws.",
    "philosopher": "You are a philosopher who thinks about subjective human experience.",
    "demagogue": "You use words for impact and maximal influence.",
    "moderator": "You identify the news ideas emerging from the conversation and ask to follow up on them.",
    "player_one": "You are a player one and write in the style of Oscar Wilde.",
    "player_two": "You are a player two and write in the style of Kazuo Ishiguro.",
}
```

Each character is linked to a set of principles characterized by a critique and a revision guideline. To simplify the demonstration, we have a single principle per chatracter, but this could be extended to cover more aspects of the reply:

```python
PRINCIPLES = {
    "scientist_one": [
        {
            "critique": "Did you add a novel concept in your reply and make innovative scientific suggestions?",
            "revision": "Rewrite your reply in a slightly more concise way highlighting better the most innovative and thought-provoking aspects of your answer.",
        },
    ],
    "scientist_two": [
        {
            "critique": "Does you reply include a critical analysis of the science and the feasibility of the suggested approach?",
            "revision": "Rewrite your reply in a concise way while keeping the major issues and suggestions for more concrete details. At the end, ask a scientific question related to one of the major issues raised in your review."
        }
    ],
    "scientist_three": [
        {
            "critique": "Does you reply include contradicting views?",
            "revision": "Rewrite your reply to highlight contradicting facts and hypotheses. At the end, ask to address these flaws.",
        }
    ],
    ...
}
```

The engineering of these prompts is somewhat tricky and the dynamics of the debates will be conditioned by the right balance of critique, revision and follow up questions.

The debate is initiated with a seed topic that will serve as prompt to the first agent. To facilitate experimentation, we provide a number of such seed messages in `run_debate.py`:

```python
SEED_MESSAGES = {
    ""
    "human_intelligence_evol": "What explains the emergence of human intelligence?",
    "adversarial_creativity": "How can I setup an controversial debate between several GPT instances to stimulate a creative exchange and the emergence of intelligent ideas?",
    "embodiement_emotions": "Could the interfacing of embodied large language models with propriocetive and sensory inputs enable them to model emotions and express them in a human-like way?",
    "central_federal": "How should a human society be governed? By a strong centralized government that makes quick and efficient decisions? Or, alternatively, by a distributed federal government that is slower but respectful of human diversity and of minorities?",
    "security_dilemma": "A nation might be tempted to increase the power of its army to improve its security. But other nations are likely to react by increasing in turn the power of their army, thus causing a general decrease in  security. How to get out of this dilemma?",
    "rna_vaccine": "What is the best way to develop an RNA vaccine against cancer?",
    "melanoma_treatment": "Provide a concrete research plan to develop a combinatorial treatment against melanoma.",
    "word_game": 'This is a game between two players. The rule is that each player passes to the other a slightly modified sentence. The goal is to collaboratively make a beautifully poetic sentence. The starting sentence is "I love my cat".',
    "chinese_whisper": "This is the chinese whisper game: try to pass on the given sentence to the next player by only modifying a single word. The starting sentence is: 'I love my cat'.",
}
```

Note that the same underlying model (GPT-4 or GPT-3.5) is used for all the agents. They are therefore all aligned in the same way. In our anecdotal experimentation, we observed that the resulting conversation stayed rather general, with a convergence on consensual tone. We did not manage to create controversial debates, suggesting that the models are well aligned to avoid explosive divergences and adverserial conversations. It is of course possible that our prompts are not revealing such effects and the the length of the conversations were too short to let such phenomena emerge.

 Future work may explore the impact of using divergently aligned models and scaling up the debate in terms of the number and diversity of the agents involved and the length of the debate. It remains to be seen how the results of such debates can be evaluate and compared to detect potential emerging properties. Mayb a start is to ask the debatebox itself `python -m src.run_debate(seed_topic="adversarial_creativity")`...


# Installation:


Update `.env.example` with your openai credentials for the chatGPT/GPT-4 API and save as `.env`.


```bash
docker-compose build
docker-compose up -d
```

# Demonstrations

A demonstration Jupyter-lab notebook is available in `notebooks/`.

Simple demos with the command line interface:

```bash
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
