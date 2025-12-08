import os
import requests
from requests.adapters import HTTPAdapter, Retry


class OpenAIProxyClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "demo-key")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai-proxy.org/v1")
        
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=frozenset(["POST"]),
            raise_on_status=False,
        )
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def summarize_topic(self, topic: str) -> dict:
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": f"用不超过100字总结这个课程主题: {topic}",
                }
            ],
            "temperature": 0.2,
            "max_tokens": 120,
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}

        resp = self.session.post(f"{self.base_url}/chat/completions", json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        raw = resp.json()
        content = raw["choices"][0]["message"]["content"].strip()
        return {
            "topic": topic,
            "summary": content,
            "provider": "openai",
        }
