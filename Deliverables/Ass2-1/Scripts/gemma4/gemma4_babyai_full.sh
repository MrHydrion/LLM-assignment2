#!/bin/bash
set -e

for SEED in 20; do
    python eval.py \
        agent.type=naive \
        agent.max_image_history=0 \
        agent.max_text_history=16 \
        eval.output_dir="Ass2-1/Results/babyai_full_gemma_local" \
        eval.num_workers=1 \
        eval.num_episodes.babyai=5 \
        eval.save_trajectories=true \
        envs.names=babyai \
        envs.env_kwargs.seed="$SEED" \
        'tasks.babyai_tasks=["BabyAI-MixedTrainLocal-v0/goto","BabyAI-MixedTrainLocal-v0/pickup","BabyAI-MixedTrainLocal-v0/open","BabyAI-MixedTrainLocal-v0/putnext","BabyAI-MixedTrainLocal-v0/pick_up_seq_go_to"]' \
        client.client_name=vllm \
        client.model_id=gemma4:e4b \
        client.base_url=http://localhost:11434/v1 \
        client.generate_kwargs.max_tokens=1024 \
        client.timeout=120 \
        client.max_retries=3
done
