# Assignment 2 — Exercise 1: BALROG Benchmark

## Overview

This excercise evaluates the standard BALROG naive agent on different LLMs on the babyAI and Crafter benchmark
The LLMs both contain local and cloud models

## Requirements
- Python 3.10 (recommended by BALROG; tested with Python 3.12)
- Ollama for the local hosted models
- Acces to the Ollama API key for running the cloud-model GPT-Oss
- BALROG base directory
- WSL Ubuntu (used for our experiments)

## Installation

The experiments were conducted using Python 3.12 in a WSL Ubuntu environment.

From the BALROG project root:

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install -e .
balrog-post-install
```

after this you can put the scripts handed in with this assignment in the directory
you also need to replace the client.py file with the file added to this admission

### local models

The local models can be downloaded through Ollama throught the following command in a terminal after downloading Ollama:

```bash
ollama pull qwen2.5:3b
ollama pull llama3.2:3b
ollama pull gemma4:e4b
```

Make sure the Ollama servers are running before starting the evaluation

### cloud model

For the cloud model code to run, you need to set up an API key.
You can do that with the following command in the wsl terminal:

```bash
OLLAMA_API_KEY=<Apikey>
```

replace '<APIKEY>' with the API key that you created on the site: https://ollama.com/settings/keys

## Running the experiments

You can run the evaluations scripts from the repistory root with the following command

```bash
bash Deliverables/Ass2-1/Scripts/<filename>.sh

```

You can replace '<filename>' with the name of the file you want to run

## Models evaluated

The following models were evaluated during Exercise 1:

| Model | Size | Context | Input | Hosting |
|---|---|---|---|---|
| Qwen2.5:3b | 1.9 GB | 32K | Text | Local (Ollama) |
| Llama3.2:3b | 2.0 GB | 128K | Text | Local (Ollama) |
| Gemma4:e4b | 9.5 GB | 128K | Text, Image | Local (Ollama) |
| gpt-oss:20b-cloud | 14 GB | 128K | Text | Cloud (Ollama) |

## Benchmarks

- BabyAI: Instruction-following and object-interaction tasks
- Crafter: Exploration, survival and achievemnet progression

## Results

## Limitations 

Gemma4 was evaluaed only on one BabyAI seed due to computational constraints

GPT-Oss completed only one Crafter epsiode because of repeated API errors that could not be fixed, Therefore, this single episode is not a reliable estimate of its average Crafter performance.