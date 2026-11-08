import streamlit as st
from streamlit_echarts import st_echarts
from config import load_config
from agents import run_agent
from charts import market_share_bar, risk_gauge, opportunity_matrix

st.set_page_config(page_title="合规罗盘 · 出海AI智能体", page_icon="🧭", layout="wide")

st.markdown("""
<style>
.big-title {font-size: 28px; font-weight: 700; margin-bottom: 4px;}
.sub-title {color: #6B7280; font-size: 14px; margin-bottom: 18px;}
.trace-box {background: #F8FAFC; border-left: 3px solid #93C5FD; padding: 10px 14px; border-radius: 6px; font-size: 13px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🧭 合规罗盘</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">出海市场洞察与合规风控多智能体 · 演示原型</div>', unsafe_allow_html=True)

with st.sidebar:
    st.subheader("⚙️ 模型配置")
    api_key = st.text_input("API Key", type="password")
    base_url = st.text_input("Base URL", value="https://agentrs.jd.com/api/saas/openai-u/v1")
    model_name = st.text_input("模型名称", value="glm-4-flash")
    st.caption("可替换为任意 OpenAI 兼容接口。无 Key 时智能体自动降级为规则引擎输出，仍可演示。")

col1, col2, col3 = st.columns([1.1, 1, 1])
with col1:
    market = st.selectbox("目标市场", ["东南亚", "欧洲", "美国", "中东", "拉美"])
with col2:
    sector = st.text_input("行业/产品（可选）", placeholder="如：消费电子、SaaS")
with col3:
    st.write("")
    st.write("")
    run = st.button("▶ 启动智能体分析", use_container_width=True, type="primary")

if run:
    cfg = load_config(api_key, base_url, model_name)
    with st.spinner("Leader 正在派发任务，三个专业Agent并行工作中……"):
        result = run_agent({"market": market, "sector": sector}, cfg)
    st.session_state["result"] = result
    st.session_state["market"] = market

if "result" in st.session_state:
    result = st.session_state["result"]
    mk = st.session_state["market"]

    st.markdown("### 📌 决策摘要")
    st.info(result["final_report"])

    st.markdown("### 📊 可视化驾驶舱")
    c1, c2, c3 = st.columns(3)
    with c1:
        st_echarts(market_share_bar(mk), height="280px")
    with c2:
        st_echarts(risk_gauge(mk), height="280px")
    with c3:
        st_echarts(opportunity_matrix(), height="280px")

    with st.expander("🔍 市场分析详情", expanded=False):
        st.text(result["market_report"])
    with st.expander("⚠️ 合规扫描详情", expanded=False):
        st.text(result["compliance_report"])
    with st.expander("🌐 本地化适配详情", expanded=False):
        st.text(result["localization_report"])

    st.markdown("### 🧾 Agent 执行轨迹（审计证据链）")
    for t in result["trace"]:
        st.markdown(f'<div class="trace-box">{t}</div>', unsafe_allow_html=True)
else:
    st.caption("在左侧选择目标市场后点击“启动智能体分析”。可视化驾驶舱将同步呈现市场机会与合规风险。")


# 兼容“本地/云端”
import streamlit as st
import os

def get_config(key, default=""):
    # 优先级：Streamlit Secrets > 本地环境变量 > 默认值
    return st.secrets.get(key, os.environ.get(key, default))

api_key = get_config("OPENAI_API_KEY")
base_url = get_config("OPENAI_BASE_URL", "https://modelservice.jdcloud.com/v1")
model_name = get_config("MODEL_NAME", "DeepSeek-V4-Flash-0731")

# 侧边栏依然保留手动输入作为降级方案
st.sidebar.text_input("API Key", value=api_key, type="password")
