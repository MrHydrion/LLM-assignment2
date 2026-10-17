#!/bin/bash
set -e

export OPENAI_API_KEY="ollama"
export OLLAMA_URL="http://$(ip route show default | awk '{print $3}'):11434/v1"

echo "Ollama URL: $OLLAMA_URL"

# Test whether Ollama is reachable
curl --fail --show-error "$OLLAMA_URL/models"
echo

# Test the Python OpenAI client
# python - <<'PY'
# import os
# from openai import OpenAI

# client = OpenAI(
#     api_key="ollama",
#     base_url=os.environ["OLLAMA_URL"],
#     timeout=30,
# )

# response = client.chat.completions.create(
#     model="qwen2.5:3b",
#     messages=[{"role": "user", "content": "Say hello"}],
#     max_tokens=30,
# )

# print("Python client response:", response.choices[0].message.content)
# PY

# Run BALROG
python eval.py \
    agent.type=custom_A2 \
    agent.max_image_history=0 \
    agent.max_text_history=16 \
    envs.names=babyai \
    eval.output_dir="Ass2-2/Results/Qwen_babyai" \
    eval.num_episodes.babyai=1 \
    eval.max_steps_per_episode=10 \
    eval.num_workers=1 \
    client.client_name=openai \
    client.model_id=qwen2.5:3b \
    client.base_url="$OLLAMA_URL" \
    client.generate_kwargs.max_tokens=1024 \
