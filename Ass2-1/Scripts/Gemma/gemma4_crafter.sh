#!/bin/bash
set -e

export OPENAI_API_KEY="ollama"

for SEED in 20; do
    python eval.py \
        agent.type=naive \
        agent.max_image_history=0 \
        agent.max_text_history=16 \
        eval.output_dir="Ass2-1/Results/llama_crafter" \
        eval.num_workers=1 \
        eval.save_trajectories=true \
        eval.num_episodes.crafter=5 \
        envs.names=crafter \
        envs.crafter_kwargs.seed="$SEED" \
        envs.env_kwargs.seed="$SEED" \
        envs.crafter_kwargs.max_episode_steps=1000 \
        client.client_name=openai \
        client.model_id=gemma4:e4b \
        client.base_url=http://localhost:11434/v1 \
        client.generate_kwargs.max_tokens=1024 \
        client.timeout=120 \
        client.max_retries=3 
done
