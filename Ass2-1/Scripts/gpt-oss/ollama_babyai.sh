
#!/bin/bash
set -e

if [ -z "${OLLAMA_API_KEY:-}" ]; then
    echo "Error: OLLAMA_API_KEY is not set."
    exit 1
fi

export OPENAI_API_KEY="$OLLAMA_API_KEY"

python eval.py \
    agent.type=naive \
    agent.max_image_history=0 \
    agent.max_text_history=16 \
    eval.output_dir="Ass2-1/Results/babyai_goto_ollama_cloud" \
    eval.num_workers=1 \
    eval.num_episodes.babyai=1 \
    eval.save_trajectories=true \
    envs.names=babyai \
    envs.env_kwargs.seed=20 \
    'tasks.babyai_tasks=[BabyAI-MixedTrainLocal-v0/goto]' \
    client.client_name=openai \
    client.model_id=gpt-oss:120b-cloud \
    client.base_url="https://ollama.com/v1" \
    client.generate_kwargs.max_tokens=4096 \
    client.timeout=120 \
    client.max_retries=3
