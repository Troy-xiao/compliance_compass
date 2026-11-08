# import os
# from dataclasses import dataclass

# @dataclass
# class ModelConfig:
#     base_url: str = "https://agentrs.jd.com/api/saas/openai-u/v1"  # 兼容OpenAI协议
#     api_key: str = ""
#     model_name: str = "glm-4-flash"  # 可按实际可用模型替换

# def load_config(api_key: str, base_url: str = "", model_name: str = "") -> ModelConfig:
#     return ModelConfig(
#         base_url=base_url or ModelConfig.base_url,
#         api_key=api_key,
#         model_name=model_name or ModelConfig.model_name,
#     )

# #
# OPENAI_API_KEY = os.getenv("JD_API_KEY", "  ") # 优先从系统环境变量读取
# OPENAI_BASE_URL = "https://modelservice.jdcloud.com/v1"
# MODEL_NAME = "DeepSeek-V4-Flash-0731"

import os
import streamlit as st

# 尝试从 Streamlit 的 Secrets 中读取，如果本地跑没配置 Secrets，就回退到系统环境变量
def get_config(key, default=""):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default)

OPENAI_API_KEY = get_config("OPENAI_API_KEY", "sk-109a0ea95c654ee584cf86555df91266")
OPENAI_BASE_URL = get_config("OPENAI_BASE_URL", "https://modelservice.jdcloud.com/v1")
MODEL_NAME = get_config("MODEL_NAME", "DeepSeek-V4-Flash-0731")
