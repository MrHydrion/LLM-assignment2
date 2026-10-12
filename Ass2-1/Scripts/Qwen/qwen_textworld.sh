#!/bin/bash
set -e

export OPENAI_API_KEY="ollama"
export OLLAMA_URL="http://$(ip route show default | awk '{print $3}'):11434/v1"

python eval.py \
    agent.type=naive \
    agent.max_image_history=0 \
    agent.max_text_history=16 \
    eval.output_dir="Ass2-1/Results/textworld_coin_qwen" \
    eval.num_workers=4 \
    eval.num_episodes.textworld=5 \
    envs.names=textworld \
    envs.env_kwargs.seed=20 \
    'tasks.textworld_tasks=[coin_collector]' \
    client.client_name=openai \
    client.model_id=qwen2.5:3b \
    client.base_url="$OLLAMA_URL" \
    client.generate_kwargs.max_tokens=1024 \
    client.timeout=120 \
    client.max_retries=3 

