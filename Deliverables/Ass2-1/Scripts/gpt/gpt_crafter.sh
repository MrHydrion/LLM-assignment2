#!/bin/bash
set -e

if [ -z "${OLLAMA_API_KEY:-}" ]; then
    echo "Error: OLLAMA_API_KEY is not set."
    exit 1
fi

export OPENAI_API_KEY="$OLLAMA_API_KEY"

# code for one seed tht was succesfull, it didnt 
for SEED in 20; do
    python eval.py \
        agent.type=naive \
        agent.max_image_history=0 \
        agent.max_text_history=16 \
        eval.output_dir="Ass2-1/Results/Ollama_crafter_250_low" \
        eval.num_workers=1 \
        eval.save_trajectories=true \
        eval.num_episodes.crafter=3 \
        eval.max_steps_per_episode=250 \
        envs.names=crafter \
        envs.crafter_kwargs.seed="$SEED" \
        envs.env_kwargs.seed="$SEED" \
        envs.crafter_kwargs.max_episode_steps=250 \
        client.client_name=openai \
        client.model_id=gpt-oss:20b-cloud \
        client.base_url="https://ollama.com/v1" \
        client.generate_kwargs.max_tokens=4096 \
        +client.generate_kwargs.reasoning_effort=low \
        client.timeout=120 \
        client.max_retries=3 
done
