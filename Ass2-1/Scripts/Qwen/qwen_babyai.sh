#!/bin/bash
set -e

export OPENAI_API_KEY="ollama"
export OLLAMA_URL="http://$(ip route show default | awk '{print $3}'):11434/v1"

python eval.py \
    agent.type=naive \
    agent.max_image_history=0 \
    agent.max_text_history=16 \
    eval.output_dir="Ass2-1/Results" \
    eval.num_workers=4 \
    eval.num_episodes.babyai=10 \
    envs.names=babyai \
    envs.env_kwargs.seed=20 \
    'tasks.babyai_tasks=[BabyAI-MixedTrainLocal-v0/goto]' \
    client.client_name=openai \
    client.model_id=qwen2.5:3b \
    client.base_url="$OLLAMA_URL" \
    client.generate_kwargs.max_tokens=1024 \
    client.timeout=120 \
    client.max_retries=3 

    


