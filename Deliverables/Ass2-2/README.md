# Assignment 2 — Exercise 2: Implement Own Reasoning Agent

## Overview

In this exercise, we implemented a custom BALROG agent using observation-aware short term memory, repetition detection and targeted feedback.

The aim was to investigate whether these mechanisms could support the LLM's sequential reasoning and decision-making by helping it recognize potentially ineffective action patterns, reconsider its actions, and improve task performance on the BabyAI and Crafter benchmarks.

## Requirements

- Python 3.12 (used in our experiments)
- BALROG installed and configured
- Ollama for running locally hosted LLMs
- WSL Ubuntu (used for our experiments)

## Installation

Follow the installation instructions in Ass2-1/README.md to set up BALROG and the Python environment.

Place both the Ass2-1 and Ass2-2 folders in the BALROG repository root

Replace the original balrog/client.py and balrog/agents/custom.py files with the corresponding modified files included in this deliverable.
The modified client.py allows the evaluation scripts to connect to the Ollama API, while custom.py contains our custom agent implementation.

The evaluation scripts use agent.type=custom to select our agent through BALROG's original agent factory.

## Custom Agent

We modified the original BALROG CustomAgent by replacing its plan-based approach with observation-aware short-term memory, repetition detection, and targeted feedback.

- Short-term memory: Stores the last 10 actions and their resulting observations.
- Repetition detection: Uses six rule-based mechanisms to identify potentially ineffective action patterns.
- Targeted feedback: Adds a warning to the LLM's prompt when potentially ineffective behavior is detected.

We also reused the action-output instructions from BALROG's NaiveAgent instead of the original CustomAgent's planning instructions. 
This allowed us to focus on the effects of short-term memory, repetition detection, and targeted feedback without introducing an additional planning mechanism. 
Additionally, we added action sanitization to remove unsupported characters from the generated output.

The agent does not force a different action when a pattern is detected; the LLM remains responsible for selecting its next action.

## Models and Benchmarks

| Model | Hosting | Benchmarks
|---|---|---|
| Qwen2.5:3b | Local (Ollama) | BabyAI, Crafter |
| Llama3.2:3b | Local (Ollama) | BabyAI, Crafter |

The evaluations use three seeds: 20, 21, and 22.

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

## Naive results

The naive-agent results used for comparison are stored in the Ass2-2/Results/Naive/ directory and the reused results from Exercise 1 can be found in Ass2-1/Results/.

## Limitations

The repetition detection mechanisms identify potentially ineffective action patterns but cannot directly determine whether the agent is making progress towards its objective. 
Furthermore, receiving feedback does not guarantee that the LLM will select a better action.

The experimental results, limitations, and possible improvements are discussed in more detail in the assignment report.