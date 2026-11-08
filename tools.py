import json
from typing import Literal

# ========== 内置行业/市场数据（源自公开报告，演示用） ==========
MARKET_DATA = {
    "东南亚": {
        "market_size_billion_usd": 320,
        "cagr_5y": "16%",
        "share_of_chinese_firms": "24%",
        "key_sectors": ["消费电子", "电商", "汽车", "光伏"],
        "notes": "中企海外份额约24%，新兴市场中最高；东南亚以成本+地缘+制度三重优势成为制造企业出海首选目的地（60%选择率）",
    },
    "欧洲": {
        "market_size_billion_usd": 1850,
        "cagr_5y": "8%",
        "share_of_chinese_firms": "16%",
        "key_sectors": ["汽车", "新能源", "家电", "电商"],
        "notes": "份额约16%，但GDPR、DSA、AI Act等监管密集，合规成本高",
    },
    "美国": {
        "market_size_billion_usd": 2400,
        "cagr_5y": "5%",
        "share_of_chinese_firms": "10%",
        "key_sectors": ["消费电子", "软件", "医药"],
        "notes": "份额约10%，贸易壁垒与监管限制最多，核心市场渗透速度最慢",
    },
    "中东": {
        "market_size_billion_usd": 210,
        "cagr_5y": "14%",
        "share_of_chinese_firms": "18%",
        "key_sectors": ["基建", "新能源", "消费电子"],
        "notes": "“2030愿景”工业化浪潮打开窗口，制造企业选择率从10%升至19%",
    },
    "拉美": {
        "market_size_billion_usd": 480,
        "cagr_5y": "11%",
        "share_of_chinese_firms": "15%",
        "key_sectors": ["汽车", "电商", "金融科技"],
        "notes": "巴西、墨西哥等国监管规则不确定性较高，需实时跟踪",
    },
}

COMPLIANCE_RULES = {
    "欧盟": [
        {"id": "GDPR", "category": "数据合规", "severity": "高",
         "desc": "数据跨境传输需充分性认定或SCC；违规罚款可达全球营收4%",
         "check": "是否涉及欧盟用户个人数据？是否完成数据映射？"},
        {"id": "DSA", "category": "平台合规", "severity": "高",
         "desc": "超大型在线平台需年度风险评估、非法内容治理、研究者数据访问",
         "check": "月活是否超过4500万？是否建立内容治理机制？"},
        {"id": "AI Act", "category": "AI合规", "severity": "中高",
         "desc": "高风险AI系统需符合透明度、人类监督、风险管理要求",
         "check": "AI应用是否属于高风险类别？"},
        {"id": "GPSR", "category": "产品安全", "severity": "中",
         "desc": "通用产品安全法规，要求欧盟境内负责人",
         "check": "是否指定欧盟授权代表？"},
    ],
    "东南亚": [
        {"id": "PDPA", "category": "数据合规", "severity": "中",
         "desc": "新加坡/泰国/马来西亚个人数据保护法，跨境传输有条件限制",
         "check": "是否在所在国完成数据本地化评估？"},
        {"id": "数据本地化", "category": "数据合规", "severity": "中",
         "desc": "越南、印尼等国对特定数据有本地存储要求",
         "check": "数据类型是否触发本地存储义务？"},
    ],
    "美国": [
        {"id": "CCPA/CPRA", "category": "数据合规", "severity": "高",
         "desc": "加州消费者隐私法，赋予消费者删除权、拒绝出售权",
         "check": "是否面向加州居民？是否建立opt-out机制？"},
        {"id": "出口管制", "category": "贸易合规", "severity": "高",
         "desc": "EAR、OFAC制裁清单，技术/产品出口需筛查",
         "check": "产品/技术是否涉及受控物项？"},
    ],
    "中东": [
        {"id": "数据保护法", "category": "数据合规", "severity": "中",
         "desc": "阿联酋PDPL、沙特PDPL，跨境传输需监管批准",
         "check": "是否在所在国注册数据控制者？"},
    ],
}

LOCALIZATION_GUIDE = {
    "语言": "产品界面、客服、合同需使用目标市场官方语言或英语+本地语言双版本",
    "支付": "接入本地主流支付方式（东南亚：GrabPay/GoPay；欧洲：SEPA；中东：Mada）",
    "渠道": "东南亚以Shopee/Lazada/TikTok Shop为主；欧洲重视独立站+本地经销",
    "文化": "避免直译式文案；宗教敏感市场（中东）需内容审核",
    "售后": "建立本地时区客服或授权服务商，响应时效影响品牌信任",
}


def query_market(market: str) -> str:
    """市场数据查询工具"""
    data = MARKET_DATA.get(market)
    if not data:
        return f"未收录“{market}”的预置数据，建议接入实时搜索工具。"
    return json.dumps({
        "目标市场": market,
        "市场规模（十亿美元）": data["market_size_billion_usd"],
        "5年CAGR": data["cagr_5y"],
        "中企份额": data["share_of_chinese_firms"],
        "重点行业": data["key_sectors"],
        "备注": data["notes"],
    }, ensure_ascii=False, indent=2)


def query_compliance(market: str, sector: str = "") -> str:
    """合规规则引擎查询工具"""
    region_key = None
    for key in COMPLIANCE_RULES:
        if key in market or market in key:
            region_key = key
            break
    if not region_key:
        return f"暂无“{market}”的合规规则库，建议扩展规则库或接入实时法规检索。"

    rules = COMPLIANCE_RULES[region_key]
    lines = [f"【{region_key}合规规则扫描】共 {len(rules)} 项关注点："]
    for r in rules:
        lines.append(
            f"- [{r['severity']}] {r['id']}（{r['category']}）：{r['desc']} | 自检问题：{r['check']}"
        )
    return "\n".join(lines)


def query_localization(market: str) -> str:
    """本地化适配建议工具"""
    lines = [f"【{market}本地化适配要点】"]
    for k, v in LOCALIZATION_GUIDE.items():
        lines.append(f"- {k}：{v}")
    return "\n".join(lines)