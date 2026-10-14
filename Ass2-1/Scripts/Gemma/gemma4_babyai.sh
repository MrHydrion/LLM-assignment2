#!/bin/bash
set -e

python eval.py \
    agent.type=naive \
    agent.max_image_history=0 \
    agent.max_text_history=16 \
    eval.output_dir="Ass2-1/Results/babyai_goto_gemma_local" \
    eval.num_workers=1 \
    eval.num_episodes.babyai=1 \
    eval.save_trajectories=true \
    envs.names=babyai \
    envs.env_kwargs.seed=20 \
    'tasks.babyai_tasks=[BabyAI-MixedTrainLocal-v0/goto]' \
    client.client_name=vllm \
    client.model_id=gemma4:e4b \
    client.base_url=http://localhost:11434/v1 \
    client.generate_kwargs.max_tokens=256 \
    client.timeout=120 \
    client.max_retries=3