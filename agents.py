from typing import TypedDict, Annotated, List
from operator import add
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from tools import query_market, query_compliance, query_localization
from config import ModelConfig


class AgentState(TypedDict):
    user_input: dict
    market_report: str
    compliance_report: str
    localization_report: str
    final_report: str
    trace: Annotated[List[str], add]


def _llm(cfg: ModelConfig, temperature: float = 0.2):
    return ChatOpenAI(
        model=cfg.model_name,
        api_key=cfg.api_key,
        base_url=cfg.base_url,
        temperature=temperature,
    )


def _safe_call(llm, system: str, user: str) -> str:
    try:
        resp = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])
        return resp.content if hasattr(resp, "content") else str(resp)
    except Exception as e:
        return f"[Agent调用异常，已降级为规则引擎输出] {e}"


def market_agent(state: AgentState, cfg: ModelConfig) -> dict:
    market = state["user_input"]["market"]
    raw = query_market(market)
    llm = _llm(cfg)
    report = _safe_call(
        llm,
        "你是出海市场分析师。基于给定数据，用中文写一段120字以内的市场机会评估，指出机会大小、中企份额含义和1个关键风险。不要编造数据。",
        f"目标市场：{market}\n数据：{raw}",
    )
    return {
        "market_report": f"{report}\n\n原始数据：\n{raw}",
        "trace": [f"[市场分析Agent] 查询{market}市场数据"],
    }


def compliance_agent(state: AgentState) -> dict:
    market = state["user_input"]["market"]
    sector = state["user_input"].get("sector", "")
    raw = query_compliance(market, sector)
    lines = raw.split("\n")
    high = sum(1 for l in lines if "[高]" in l)
    mid = sum(1 for l in lines if "[中高]" in l or "[中]" in l)
    risk_level = "高" if high >= 2 else ("中高" if high >= 1 else "中")
    return {
        "compliance_report": f"风险等级判定：{risk_level}（高危{high}项，中危{mid}项）\n{raw}",
        "trace": [f"[合规扫描Agent] 扫描{market}规则库，高危{high}项，中危{mid}项"],
    }


def localization_agent(state: AgentState) -> dict:
    market = state["user_input"]["market"]
    raw = query_localization(market)
    return {
        "localization_report": raw,
        "trace": [f"[本地化适配Agent] 生成{market}适配要点"],
    }


def leader_aggregate(state: AgentState, cfg: ModelConfig) -> dict:
    llm = _llm(cfg)
    user = (
        f"用户输入：{state['user_input']}\n\n"
        f"市场分析：{state['market_report']}\n\n"
        f"合规扫描：{state['compliance_report']}\n\n"
        f"本地化适配：{state['localization_report']}\n\n"
        "请用中文输出一份结构化决策摘要，严格按四段：①机会结论（2句）；"
        "②合规红线（列2-3条最关键的）；③本地化优先动作（2条）；④下一步建议（1条）。"
        "总字数不超过280字。不要重复原始数据，只给判断。"
    )
    final = _safe_call(
        llm,
        "你是出海战略负责人，擅长把多源信息压缩为可执行决策。",
        user,
    )
    return {"final_report": final, "trace": ["[Leader] 汇总三路输出并压缩为决策摘要"]}


def build_graph(cfg: ModelConfig):
    graph = StateGraph(AgentState)
    graph.add_node("市场分析", lambda s: market_agent(s, cfg))
    graph.add_node("合规扫描", compliance_agent)
    graph.add_node("本地化适配", localization_agent)
    graph.add_node("汇总", lambda s: leader_aggregate(s, cfg))

    graph.set_entry_point("市场分析")
    graph.add_edge("市场分析", "合规扫描")
    graph.add_edge("合规扫描", "本地化适配")
    graph.add_edge("本地化适配", "汇总")
    graph.add_edge("汇总", END)
    return graph.compile()


def run_agent(user_input: dict, cfg: ModelConfig) -> dict:
    app = build_graph(cfg)
    init: AgentState = {
        "user_input": user_input,
        "market_report": "",
        "compliance_report": "",
        "localization_report": "",
        "final_report": "",
        "trace": [],
    }
    return app.invoke(init)