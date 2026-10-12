#!/bin/bash
set -e

# Check Groq API key
if [ -z "${GROQ_API_KEY:-}" ]; then
    echo "Error: GROQ_API_KEY is not set."
    exit 1
fi

export OPENAI_API_KEY="$GROQ_API_KEY"

# export GROQ_API_KEY="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"

python eval.py \
    agent.type=naive \
    agent.max_image_history=0 \
    agent.max_text_history=16 \
    eval.output_dir="Ass2-1/Results/babyai_goto_groq_gptoss" \
    eval.num_workers=1 \
    eval.num_episodes.babyai=10 \
    eval.save_trajectories=true \
    envs.names=babyai \
    envs.env_kwargs.seed=20 \
    'tasks.babyai_tasks=[BabyAI-MixedTrainLocal-v0/goto]' \
    client.client_name=openai \
    client.model_id=openai/gpt-oss-120b \
    client.base_url="https://api.groq.com/openai/v1" \
    client.generate_kwargs.max_tokens=4096 \
    client.timeout=120 \
    client.max_retries=3