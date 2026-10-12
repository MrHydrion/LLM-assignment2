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
    eval.output_dir="Ass2-1/Results/minihack_corridor_groq" \
    eval.num_workers=1 \
    eval.num_episodes.minihack=3 \
    eval.max_steps_per_episode=15 \
    eval.save_trajectories=true \
    envs.names=minihack \
    envs.env_kwargs.seed=20 \
    'tasks.minihack_tasks=[MiniHack-Corridor-R3-v0]' \
    client.client_name=openai \
    client.model_id=openai/gpt-oss-120b \
    client.base_url="https://api.groq.com/openai/v1" \
    client.generate_kwargs.max_tokens=4096 \
    client.timeout=120 \
    client.max_retries=3
