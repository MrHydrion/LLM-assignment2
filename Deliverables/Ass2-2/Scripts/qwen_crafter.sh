#!/bin/bash
set -e

export OPENAI_API_KEY="ollama"
export OLLAMA_URL="http://$(ip route show default | awk '{print $3}'):11434/v1"

echo "Ollama URL: $OLLAMA_URL"

# Test whether Ollama is reachable
curl --fail --show-error "$OLLAMA_URL/models"
echo

for SEED in 20 21 22; do
    python -u eval.py \
        agent.type=custom_A2 \
        agent.max_image_history=0 \
        agent.max_text_history=16 \
        eval.output_dir="Ass2-2/Results/Qwen_crafter_final" \
        eval.num_workers=1 \
        eval.num_episodes.crafter=5 \
        envs.names=crafter \
        envs.crafter_kwargs.seed="$SEED" \
        envs.env_kwargs.seed="$SEED" \
        envs.crafter_kwargs.max_episode_steps=1000 \
        client.client_name=openai \
        client.model_id=qwen2.5:3b \
        client.base_url="$OLLAMA_URL" \
        client.generate_kwargs.max_tokens=1024 \
        client.timeout=120 \
        client.max_retries=3
done
