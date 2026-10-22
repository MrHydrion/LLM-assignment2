#!/bin/bash
set -e

export OPENAI_API_KEY="ollama"
export OLLAMA_URL="http://$(ip route show default | awk '{print $3}'):11434/v1"
SEEDS=(20 21)

for SEED in "${SEEDS[@]}"; do
    echo "Running seed $SEED"

    python eval.py \
        agent.type=custom_A3 \
        agent.max_image_history=0 \
        agent.max_text_history=16 \
        eval.output_dir="Ass2-3/Results/BabyAI/Llama_babyai_seed${SEED}" \
        eval.num_workers=1 \
        eval.num_episodes.babyai=5 \
        eval.save_trajectories=true \
        envs.names=babyai \
        envs.env_kwargs.seed=${SEED} \
        client.model_id=llama3.2:3b \
        client.base_url="$OLLAMA_URL" \
        client.generate_kwargs.max_tokens=1024 \
        client.timeout=120 \
        client.max_retries=3
done
