#!/bin/bash
set -e

export OPENAI_API_KEY="ollama"
export OLLAMA_URL="http://$(ip route show default | awk '{print $3}'):11434/v1"

python eval.py \
    agent.type=custom_A2 \
    agent.max_image_history=0 \
    agent.max_text_history=16 \
    envs.names=babyai \
    envs.env_kwargs.seed=20 \
    eval.output_dir="Ass2-2/Results/Qwen_babyai_test" \
    eval.num_episodes.babyai=1 \
    eval.max_steps_per_episode=75 \
    eval.num_workers=1 \
    eval.save_trajectories=true \
    client.client_name=openai \
    client.model_id=qwen2.5:3b \
    client.base_url="$OLLAMA_URL" \
    client.generate_kwargs.max_tokens=1024 \
    client.timeout=120 \
    client.max_retries=3
