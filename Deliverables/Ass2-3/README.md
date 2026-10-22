# Assignment 2 — Exercise 3: Self-Reflection

## Overview

In this exercise, we implemented a custom BALROG agent using
a self-reflection agent. The agent uses action selection and
self evaluation to try and perform better than the Naive agent.

The goal was to implement the self-reflection agent in a way that
it would outperform the Naive agent on the BabyAI and Crafter 
benchmarks because of its reasoning capability.

## Requirements

- Python 3.12 (used in our experiments)
- BALROG installed and configured
- Ollama for running locally hosted LLMs
- WSL Ubuntu (used for our experiments)

## Installation

Follow the installation instructions in Ass2-1/README.md to set up BALROG and the Python environment.

Place the Ass2-3 folder in the BALROG repository root, alongside eval.py.

Replace the original balrog/client.py and balrog/agents/custom.py files with the corresponding modified files included in this deliverable.
The modified client.py allows the evaluation scripts to connect to the Ollama API, while custom.py contains our custom agent implementation.

The evaluation scripts use agent.type=custom to select our agent through BALROG's original agent factory.

## Self-reflection Agent

The self reflection agent has tow main roles. Reflection, where the agent looks back at
the previous action and tries to learn lessons from its outcome. And action selection,
where it uses the current observation and sotred lesson to choos the next action.

Reflection takes into account the previous observation, the previous action, the current observation and the lessons it has learned so far. In a reflection prompt, these are all provided to the agent, which is then asked to analyze the transition between observations. It does this by examining the differences between observations, the outcome of the previous action, whether the action influenced the observed result, and whether it learned something. It is then told how to format these in the response. If the agent learned something, the lesson will be saved in memory with the other lessons, up to a maximum of the 5 most recent lessons.

The agent will then use this reflection to select the next action. The agent has specific reflection instructions in which the lesson memory is given. The instructions tell the agent how to choose its next action by identifying the task objective, determining if the last outcome was successful, using the available lessons, revising its plan, and then selecting an action. It then tells the agent how to format its response. From this, an action will be extracted based on the observation and the possible actions. The new observation from this action becomes the new reference point for the next reflection. 

## Models and Benchmarks


| Model | Hosting | Benchmarks
|---|---|---|
| Qwen2.5:3b | Local (Ollama) | BabyAI, Crafter |
| Llama3.2:3b | Local (Ollama) | BabyAI, Crafter |

The evaluations use two seeds: 20 and 21.

For BabyAI, five episodes were evaluated per task type, giving 25 episodes per seed.

For Crafter, five episodes were evaluated per seed.

## Running the Experiments

download the required models in a terminal with the following bash commands

```bash
ollama pull qwen2.5:3b
ollama pull llama3.2:3b
```

The evaluation scripts can be run from the BALROG repository root:

```bash
bash Ass2-2/Scripts/<filename>.sh
```

Replace <filename> with the name of the evaluation script.

## Results

The custom agent was compared against the standard BALROG naive agent using the same benchmarks and models.

BabyAI performance is measured by the percentage of successfully completed episodes.

Crafter performance is measured by the percentage of 22 distinct achievements completed.

## Baseline Results

Where applicable, the baseline evaluations from Exercise 1 are used for comparison.

These results are available in the corresponding Ass2-1 and are not duplicated here

## limitations

Computation speed is highly dependent on which models is used. Larger models with
more parameters are likely to have faster compute times. Also better hardware will
reduce the total time to compute.

The self-reflection agent tried to perform many invalid actions, which resulted in
long compute times and low scores. This is likely due to the way in which the
action selection and reflection instructions are set up

The results, limitations, and possible improvements are discussed in more detail in the assignment report.