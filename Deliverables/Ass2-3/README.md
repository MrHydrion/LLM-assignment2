# Assignment 2 — Exercise 3: Self-Reflection

## Overview


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

## Models and Benchmarks


| Model | Hosting | Benchmarks
|---|---|---|
| Qwen2.5:3b | Local (Ollama) | BabyAI, Crafter |
| Llama3.2:3b | Local (Ollama) | BabyAI, Crafter |

The evaluations use three seeds: 20 and 21.

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