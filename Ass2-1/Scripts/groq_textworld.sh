#!/bin/bash
set -e

if [ -z "${GROQ_API_KEY:-}" ]; then
    echo "Error: GROQ_API_KEY is not set."
    exit 1
fi

export OPENAI_API_KEY="$GROQ_API_KEY"

python eval.py \
    agent.type=naive \
    agent.max_image_history=0 \
    agent.max_text_history=16 \
    eval.output_dir="Ass2-1/Results/textworld_coin_groq" \
    eval.num_workers=1 \
    eval.num_episodes.textworld=5 \
    eval.save_trajectories=true \
    envs.names=textworld \
    envs.env_kwargs.seed=20 \
    'tasks.textworld_tasks=[coin_collector]' \
    client.client_name=openai \
    client.model_id=openai/gpt-oss-120b \
    client.base_url="https://api.groq.com/openai/v1" \
    client.generate_kwargs.max_tokens=4096 \
    client.timeout=120 \
    client.max_retries=3
