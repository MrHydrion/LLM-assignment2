#!/bin/bash
set -e

export OPENAI_API_KEY="ollama"
export OLLAMA_URL="http://$(ip route show default | awk '{print $3}'):11434/v1"

echo "Ollama URL: $OLLAMA_URL"
curl --fail --show-error "$OLLAMA_URL/models"
echo

# BabyAI seed 21 only
echo "Running BabyAI seed 21"

python -u eval.py \
    agent.type=custom_A3 \
    agent.max_image_history=0 \
    agent.max_text_history=16 \
    envs.names=babyai \
    envs.env_kwargs.seed=21 \
    eval.output_dir="Ass2-3/Results/BabyAI/Qwen_babyai_seed21" \
    eval.num_episodes.babyai=5 \
    eval.num_workers=1 \
    client.client_name=openai \
    client.model_id=qwen2.5:3b \
    client.base_url="$OLLAMA_URL" \
    client.generate_kwargs.max_tokens=1024 \
    client.timeout=120 \
    client.max_retries=3

# Crafter seeds 20 and 21
for SEED in 20 21; do

    echo "Running Crafter seed $SEED"

    python -u eval.py \
        agent.type=custom_A3 \
        agent.max_image_history=0 \
        agent.max_text_history=16 \
        envs.names=crafter \
        envs.crafter_kwargs.seed="$SEED" \
        envs.env_kwargs.seed="$SEED" \
        envs.crafter_kwargs.max_episode_steps=1000 \
        eval.output_dir="Ass2-3/Results/Crafter/Qwen_crafter_seed${SEED}" \
        eval.num_episodes.crafter=5 \
        eval.num_workers=1 \
        client.client_name=openai \
        client.model_id=qwen2.5:3b \
        client.base_url="$OLLAMA_URL" \
        client.generate_kwargs.max_tokens=1024 \
        client.timeout=120 \
        client.max_retries=3

done

echo "All remaining evaluations completed."