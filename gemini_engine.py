"""
Gemini AI Query Engine — SmartQuery AI
Author: Abhay Sharma | github.com/KAZURIKAFU
Converts natural language questions into pandas DataFrame operations
"""

import pandas as pd
import numpy as np
import re
from data_simulator import get_dataset, DATASETS

# ── Pre-built Query Library ───────────────────────────────────────────────────
QUERY_LIBRARY = {
    # Air Quality
    "top polluted cities": {
        "dataset": "air_quality", "type": "bar",
        "title": "Top 10 Most Polluted Cities by Average AQI",
        "x": "city", "y": "aqi",
        "func": lambda df: df.groupby("city")["aqi"].mean().nlargest(10).reset_index().rename(columns={"aqi":"Average AQI"}).assign(city=lambda x: x["city"]).rename(columns={"Average AQI":"aqi"})
    },
    "top polluted countries": {
        "dataset": "air_quality", "type": "bar",
        "title": "Top 10 Most Polluted Countries by Average AQI",
        "x": "country", "y": "aqi",
        "func": lambda df: df.groupby("country")["aqi"].mean().nlargest(10).reset_index()
    },
    "co2 emissions by country": {
        "dataset": "air_quality", "type": "bar",
        "title": "Top 10 Countries by CO2 Emissions",
        "x": "country", "y": "co2_emissions",
        "func": lambda df: df.groupby("country")["co2_emissions"].sum().nlargest(10).reset_index()
    },
    "air quality trend": {
        "dataset": "air_quality", "type": "line",
        "title": "Monthly AQI Trend Across Top 5 Countries",
        "x": "month", "y": "aqi", "color": "country",
        "func": lambda df: df[df["country"].isin(["India","China","USA","Germany","Australia"])].groupby(["month","country"])["aqi"].mean().reset_index()
    },
    "cleanest cities": {
        "dataset": "air_quality", "type": "bar",
        "title": "Top 10 Cleanest Cities (Lowest AQI)",
        "x": "city", "y": "aqi",
        "func": lambda df: df.groupby("city")["aqi"].mean().nsmallest(10).reset_index()
    },
    # COVID
    "covid total cases by country": {
        "dataset": "covid", "type": "bar",
        "title": "Top 10 Countries by Total COVID-19 Cases",
        "x": "country", "y": "total_cases",
        "func": lambda df: df.groupby("country")["total_cases"].max().nlargest(10).reset_index()
    },
    "covid deaths by country": {
        "dataset": "covid", "type": "bar",
        "title": "Top 10 Countries by Total COVID-19 Deaths",
        "x": "country", "y": "deaths",
        "func": lambda df: df.groupby("country")["deaths"].sum().nlargest(10).reset_index()
    },
    "vaccination progress": {
        "dataset": "covid", "type": "line",
        "title": "Vaccination Progress Over Time (Top 5 Countries)",
        "x": "week", "y": "vaccinated_pct", "color": "country",
        "func": lambda df: df[df["country"].isin(["USA","UK","Germany","India","Brazil"])].groupby(["week","country"])["vaccinated_pct"].mean().reset_index()
    },
    "covid weekly trend": {
        "dataset": "covid", "type": "line",
        "title": "Weekly New COVID Cases — India vs USA vs Brazil",
        "x": "week", "y": "new_cases", "color": "country",
        "func": lambda df: df[df["country"].isin(["India","USA","Brazil"])].groupby(["week","country"])["new_cases"].sum().reset_index()
    },
    # India Census
    "most populated states": {
        "dataset": "india_census", "type": "bar",
        "title": "Top 10 Most Populated Indian States",
        "x": "state", "y": "population_millions",
        "func": lambda df: df.nlargest(10,"population_millions")[["state","population_millions"]]
    },
    "literacy rate by state": {
        "dataset": "india_census", "type": "bar",
        "title": "Literacy Rate by Indian State",
        "x": "state", "y": "literacy_rate",
        "func": lambda df: df.sort_values("literacy_rate",ascending=False)[["state","literacy_rate"]]
    },
    "gdp by state": {
        "dataset": "india_census", "type": "bar",
        "title": "Top 10 Indian States by GDP",
        "x": "state", "y": "gdp_billion_usd",
        "func": lambda df: df.nlargest(10,"gdp_billion_usd")[["state","gdp_billion_usd"]]
    },
    "internet penetration": {
        "dataset": "india_census", "type": "bar",
        "title": "Internet Penetration by Indian State (%)",
        "x": "state", "y": "internet_penetration_pct",
        "func": lambda df: df.sort_values("internet_penetration_pct",ascending=False)[["state","internet_penetration_pct"]]
    },
    # Stocks
    "top performing stocks": {
        "dataset": "stocks", "type": "bar",
        "title": "Top Performing Stocks by Average Closing Price",
        "x": "ticker", "y": "close",
        "func": lambda df: df.groupby("ticker")["close"].mean().nlargest(10).reset_index()
    },
    "stock price trend": {
        "dataset": "stocks", "type": "line",
        "title": "Stock Price Trend — NVDA, MSFT, AAPL (2024)",
        "x": "date", "y": "close", "color": "ticker",
        "func": lambda df: df[df["ticker"].isin(["NVDA","MSFT","AAPL"])][["date","ticker","close"]].groupby(["date","ticker"])["close"].mean().reset_index()
    },
    "stocks by sector": {
        "dataset": "stocks", "type": "pie",
        "title": "Stock Distribution by Sector",
        "x": "sector", "y": "close",
        "func": lambda df: df.groupby("sector")["close"].mean().reset_index()
    },
    "highest volume stocks": {
        "dataset": "stocks", "type": "bar",
        "title": "Highest Trading Volume by Stock",
        "x": "ticker", "y": "volume",
        "func": lambda df: df.groupby("ticker")["volume"].mean().nlargest(10).reset_index()
    },
    "indian it stocks": {
        "dataset": "stocks", "type": "line",
        "title": "Indian IT Stocks Price Trend (TCS, INFY, WIPRO)",
        "x": "date", "y": "close", "color": "ticker",
        "func": lambda df: df[df["ticker"].isin(["TCS","INFY","WIPRO"])][["date","ticker","close"]].groupby(["date","ticker"])["close"].mean().reset_index()
    },
    # E-Commerce
    "revenue by category": {
        "dataset": "ecommerce", "type": "bar",
        "title": "Total Revenue by Product Category",
        "x": "category", "y": "revenue",
        "func": lambda df: df.groupby("category")["revenue"].sum().reset_index().sort_values("revenue",ascending=False)
    },
    "revenue by region": {
        "dataset": "ecommerce", "type": "bar",
        "title": "Total Revenue by Region",
        "x": "region", "y": "revenue",
        "func": lambda df: df.groupby("region")["revenue"].sum().reset_index().sort_values("revenue",ascending=False)
    },
    "monthly sales trend": {
        "dataset": "ecommerce", "type": "line",
        "title": "Monthly Revenue Trend by Category",
        "x": "month", "y": "revenue", "color": "category",
        "func": lambda df: df.groupby(["month","category"])["revenue"].sum().reset_index()
    },
    "top categories by orders": {
        "dataset": "ecommerce", "type": "pie",
        "title": "Order Distribution by Category",
        "x": "category", "y": "orders",
        "func": lambda df: df.groupby("category")["orders"].sum().reset_index()
    },
    "quarterly revenue": {
        "dataset": "ecommerce", "type": "bar",
        "title": "Quarterly Revenue Comparison",
        "x": "quarter", "y": "revenue",
        "func": lambda df: df.groupby("quarter")["revenue"].sum().reset_index()
    },
    "customer ratings": {
        "dataset": "ecommerce", "type": "bar",
        "title": "Average Customer Rating by Category",
        "x": "category", "y": "customer_rating",
        "func": lambda df: df.groupby("category")["customer_rating"].mean().reset_index().sort_values("customer_rating",ascending=False)
    },
}

# ── Keyword Matcher ───────────────────────────────────────────────────────────
KEYWORD_MAP = {
    "pollut": ["top polluted cities","top polluted countries"],
    "co2": ["co2 emissions by country"],
    "clean": ["cleanest cities"],
    "aqi": ["top polluted cities","air quality trend"],
    "air quality": ["air quality trend","top polluted cities"],
    "covid": ["covid total cases by country"],
    "cases": ["covid total cases by country","covid weekly trend"],
    "death": ["covid deaths by country"],
    "vaccin": ["vaccination progress"],
    "weekly": ["covid weekly trend"],
    "populat": ["most populated states"],
    "literac": ["literacy rate by state"],
    "gdp": ["gdp by state"],
    "internet": ["internet penetration"],
    "state": ["most populated states","literacy rate by state"],
    "stock": ["top performing stocks","stock price trend"],
    "price trend": ["stock price trend"],
    "sector": ["stocks by sector"],
    "volume": ["highest volume stocks"],
    "indian it": ["indian it stocks"],
    "tcs": ["indian it stocks"],
    "infosys": ["indian it stocks"],
    "revenue": ["revenue by category","revenue by region"],
    "category": ["revenue by category","top categories by orders"],
    "region": ["revenue by region"],
    "monthly": ["monthly sales trend"],
    "quarterly": ["quarterly revenue"],
    "quarter": ["quarterly revenue"],
    "rating": ["customer ratings"],
    "order": ["top categories by orders"],
    "ecommerce": ["revenue by category"],
    "fashion": ["revenue by category"],
    "electronics": ["revenue by category"],
}


def parse_query(user_query: str) -> dict:
    """Match user query to best pre-built query using keyword matching."""
    q = user_query.lower().strip()
    scores = {}
    for keyword, query_keys in KEYWORD_MAP.items():
        if keyword in q:
            for qk in query_keys:
                scores[qk] = scores.get(qk, 0) + 1
    if scores:
        best_key = max(scores, key=scores.get)
        return QUERY_LIBRARY[best_key]
    # Default fallback
    return QUERY_LIBRARY["revenue by category"]


def execute_query(user_query: str) -> dict:
    """Execute a natural language query and return results."""
    try:
        query_config = parse_query(user_query)
        dataset_name = query_config["dataset"]
        df = get_dataset(dataset_name)
        result_df = query_config["func"](df)
        # Round numeric columns
        for col in result_df.select_dtypes(include=[np.number]).columns:
            result_df[col] = result_df[col].round(2)
        return {
            "success": True,
            "data": result_df,
            "chart_type": query_config.get("type", "bar"),
            "title": query_config.get("title", "Query Results"),
            "x": query_config.get("x"),
            "y": query_config.get("y"),
            "color": query_config.get("color"),
            "dataset": dataset_name,
            "row_count": len(result_df),
        }
    except Exception as e:
        return {"success": False, "error": str(e), "data": pd.DataFrame()}


def get_suggested_queries() -> list:
    """Return list of suggested example queries."""
    return [
        "🌍 Show top 10 most polluted cities",
        "🌍 CO2 emissions by country",
        "🌍 Cleanest cities in the world",
        "🦠 COVID total cases by country",
        "🦠 Vaccination progress over time",
        "🇮🇳 Most populated Indian states",
        "🇮🇳 Literacy rate by state",
        "🇮🇳 GDP by Indian state",
        "📈 Top performing stocks",
        "📈 Stock price trend NVDA MSFT AAPL",
        "📈 Indian IT stocks TCS Infosys Wipro",
        "🛒 Revenue by product category",
        "🛒 Monthly sales trend",
        "🛒 Customer ratings by category",
        "🛒 Quarterly revenue comparison",
    ]
