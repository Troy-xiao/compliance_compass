import os
from dataclasses import dataclass

@dataclass
class ModelConfig:
    base_url: str = "https://agentrs.jd.com/api/saas/openai-u/v1"  # 兼容OpenAI协议
    api_key: str = ""
    model_name: str = "glm-4-flash"  # 可按实际可用模型替换

def load_config(api_key: str, base_url: str = "", model_name: str = "") -> ModelConfig:
    return ModelConfig(
        base_url=base_url or ModelConfig.base_url,
        api_key=api_key,
        model_name=model_name or ModelConfig.model_name,
    )