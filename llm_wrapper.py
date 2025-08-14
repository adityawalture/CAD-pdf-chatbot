import os
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("LLM_MODEL", "phi")

def generate_summary(text: str, max_tokens: int = 512) -> str:
    prompt = (
        "You are a senior mechanical design analyst. Based on the following extracted "
        "information from a CAD drawing, write a concise summary covering purpose, key "
        "components, notable dimensions, and any design considerations.\n\n" + text[:3000]
    )

    response = requests.post(
        f"{OLLAMA_HOST}/api/chat",
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        },
        timeout=300,
    )
    response.raise_for_status()
    return response