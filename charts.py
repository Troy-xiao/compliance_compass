def market_share_bar(market: str):
    """中企在主要市场的份额对比（条形图）"""
    data = {
        "东南亚": 24, "欧洲": 16, "美国": 10, "中东": 18, "拉美": 15,
    }
    names = list(data.keys())
    values = [data[n] for n in names]
    return {
        "title": {"text": "中企样本行业海外市场份额（2026）", "left": "center", "textStyle": {"fontSize": 14}},
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category", "data": names, "axisLabel": {"fontSize": 11}},
        "yAxis": {"type": "value", "name": "%", "max": 30},
        "series": [{
            "type": "bar",
            "data": [{"value": v, "itemStyle": {"color": "#6EE7B7" if n == market else "#93C5FD"}} for n, v in zip(names, values)],
            "barWidth": "50%",
            "label": {"show": True, "position": "top", "formatter": "{c}%"},
        }],
        "grid": {"left": "12%", "right": "8%", "bottom": "15%", "top": "18%"},
    }


def risk_gauge(market: str):
    """合规风险等级仪表盘"""
    mapping = {"美国": 85, "欧洲": 78, "东南亚": 52, "中东": 48, "拉美": 60}
    value = mapping.get(market, 50)
    color = "#F87171" if value >= 70 else ("#FBBF24" if value >= 50 else "#34D399")
    return {
        "title": {"text": f"{market} · 合规风险指数", "left": "center", "textStyle": {"fontSize": 13}},
        "series": [{
            "type": "gauge",
            "min": 0, "max": 100,
            "progress": {"show": True, "width": 18},
            "axisLine": {"lineStyle": {"width": 18, "color": [[1, "#E5E7EB"]]}},
            "axisTick": {"show": False},
            "splitLine": {"show": False},
            "axisLabel": {"show": False},
            "pointer": {"show": False},
            "detail": {"valueAnimation": True, "fontSize": 24, "offsetCenter": [0, "0%"], "color": color},
            "data": [{"value": value, "itemStyle": {"color": color}}],
        }],
    }


def opportunity_matrix():
    """区域机会矩阵：市场规模 vs 中企份额（散点图）"""
    return {
        "title": {"text": "区域机会矩阵（气泡大小=5年CAGR）", "left": "center", "textStyle": {"fontSize": 13}},
        "tooltip": {"trigger": "item", "formatter": "{b}<br/>市场规模: {c} 十亿美元"},
        "xAxis": {"name": "中企份额（%）", "type": "value", "min": 0, "max": 30},
        "yAxis": {"name": "市场规模（十亿美元）", "type": "value"},
        "series": [{
            "type": "scatter",
            "data": [
                {"name": "东南亚", "value": [24, 320], "symbolSize": 38},
                {"name": "欧洲", "value": [16, 1850], "symbolSize": 26},
                {"name": "美国", "value": [10, 2400], "symbolSize": 20},
                {"name": "中东", "value": [18, 210], "symbolSize": 34},
                {"name": "拉美", "value": [15, 480], "symbolSize": 30},
            ],
            "label": {"show": True, "formatter": "{b}", "position": "top", "fontSize": 11},
            "itemStyle": {"color": "#93C5FD"},
        }],
    }