"""
Chart Builder — SmartQuery AI
Author: Abhay Sharma | github.com/KAZURIKAFU
Auto-generates best-fit Plotly charts from query results
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLORS = {
    "bg":       "#0d1117",
    "card":     "#161b22",
    "blue":     "#58a6ff",
    "green":    "#3fb950",
    "orange":   "#f78166",
    "yellow":   "#e3b341",
    "purple":   "#bc8cff",
    "text":     "#e6edf3",
    "subtext":  "#8b949e",
    "border":   "#30363d",
}

PALETTE = [COLORS["blue"], COLORS["green"], COLORS["orange"],
           COLORS["yellow"], COLORS["purple"], "#79c0ff",
           "#56d364", "#ffa657", "#ff7b72", "#d2a8ff"]

LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORS["text"], family="Segoe UI, Arial"),
    margin=dict(l=20, r=20, t=50, b=60),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["subtext"])),
    xaxis=dict(showgrid=False, color=COLORS["subtext"],
               tickfont=dict(size=11), title_font=dict(color=COLORS["subtext"])),
    yaxis=dict(showgrid=True, gridcolor=COLORS["border"],
               color=COLORS["subtext"], title_font=dict(color=COLORS["subtext"])),
)


def build_chart(result: dict, height: int = 420) -> go.Figure:
    """Build appropriate chart based on query result type."""
    if not result.get("success") or result["data"].empty:
        return _empty_chart("No data to display")

    df = result["data"]
    chart_type = result.get("chart_type", "bar")
    title = result.get("title", "Query Results")
    x_col = result.get("x")
    y_col = result.get("y")
    color_col = result.get("color")

    try:
        if chart_type == "bar":
            fig = _bar_chart(df, x_col, y_col, title, color_col)
        elif chart_type == "line":
            fig = _line_chart(df, x_col, y_col, title, color_col)
        elif chart_type == "pie":
            fig = _pie_chart(df, x_col, y_col, title)
        elif chart_type == "scatter":
            fig = _scatter_chart(df, x_col, y_col, title, color_col)
        else:
            fig = _bar_chart(df, x_col, y_col, title, color_col)

        fig.update_layout(**LAYOUT_BASE, height=height,
                          title=dict(text=title, font=dict(size=15, color=COLORS["text"]),
                                     x=0.01, xanchor="left"))
        return fig
    except Exception as e:
        return _empty_chart(f"Chart error: {str(e)}")


def _bar_chart(df, x, y, title, color=None):
    if color and color in df.columns:
        fig = px.bar(df, x=x, y=y, color=color,
                     color_discrete_sequence=PALETTE, barmode="group")
    else:
        fig = px.bar(df, x=x, y=y, color_discrete_sequence=[COLORS["blue"]])
        fig.update_traces(marker_color=PALETTE[:len(df)], marker_line_width=0)
    fig.update_traces(opacity=0.9)
    return fig


def _line_chart(df, x, y, title, color=None):
    if color and color in df.columns:
        fig = px.line(df, x=x, y=y, color=color,
                      color_discrete_sequence=PALETTE,
                      markers=False, line_shape="spline")
        fig.update_traces(line=dict(width=2.5))
    else:
        fig = px.line(df, x=x, y=y, line_shape="spline",
                      color_discrete_sequence=[COLORS["blue"]])
        fig.update_traces(line=dict(width=2.5, color=COLORS["blue"]),
                          fill="tozeroy", fillcolor="rgba(88,166,255,0.1)")
    return fig


def _pie_chart(df, names, values, title):
    fig = px.pie(df, names=names, values=values,
                 color_discrete_sequence=PALETTE, hole=0.45)
    fig.update_traces(textfont=dict(color=COLORS["text"]),
                      marker=dict(line=dict(color=COLORS["bg"], width=2)))
    fig.update_layout(showlegend=True)
    return fig


def _scatter_chart(df, x, y, title, color=None):
    if color and color in df.columns:
        fig = px.scatter(df, x=x, y=y, color=color,
                         color_discrete_sequence=PALETTE, size_max=12)
    else:
        fig = px.scatter(df, x=x, y=y,
                         color_discrete_sequence=[COLORS["blue"]])
    fig.update_traces(marker=dict(size=8, opacity=0.8))
    return fig


def _empty_chart(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, xref="paper", yref="paper",
                       x=0.5, y=0.5, showarrow=False,
                       font=dict(size=16, color=COLORS["subtext"]))
    fig.update_layout(**LAYOUT_BASE, height=420)
    return fig


def build_stats_cards(df: pd.DataFrame, y_col: str) -> dict:
    """Generate summary statistics for the result dataframe."""
    if df.empty or y_col not in df.columns:
        return {}
    col = df[y_col]
    return {
        "count": f"{len(df):,}",
        "mean": f"{col.mean():,.2f}",
        "max": f"{col.max():,.2f}",
        "min": f"{col.min():,.2f}",
        "total": f"{col.sum():,.2f}",
    }
