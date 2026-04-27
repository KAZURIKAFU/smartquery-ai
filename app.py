"""
SmartQuery AI — Natural Language Data Analysis Dashboard
Author: Abhay Sharma | github.com/KAZURIKAFU
Google Cloud BigQuery + Gemini AI Powered Analytics
"""

import dash
from dash import dcc, html, Input, Output, State, ctx
import pandas as pd
import json
from gemini_engine import execute_query, get_suggested_queries, DATASETS
from chart_builder import build_chart, build_stats_cards

# ── App Init ─────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, title="SmartQuery AI | Abhay Sharma",
                meta_tags=[{"name":"viewport","content":"width=device-width,initial-scale=1"}],
                suppress_callback_exceptions=True)

# ── Colors ────────────────────────────────────────────────────────────────────
C = {"bg":"#0d1117","card":"#161b22","card2":"#1c2128","blue":"#58a6ff",
     "green":"#3fb950","orange":"#f78166","yellow":"#e3b341","purple":"#bc8cff",
     "text":"#e6edf3","sub":"#8b949e","border":"#30363d"}

suggestions = get_suggested_queries()

# ── Layout ────────────────────────────────────────────────────────────────────
app.layout = html.Div(style={"backgroundColor":C["bg"],"minHeight":"100vh",
                              "fontFamily":"'Segoe UI',Arial,sans-serif","color":C["text"]}, children=[

    # ── Header ──
    html.Div(style={"background":"linear-gradient(135deg,#0d1117 0%,#1a1f35 50%,#0d2137 100%)",
                    "padding":"20px 40px","borderBottom":f"1px solid {C['border']}",
                    "boxShadow":"0 2px 20px rgba(88,166,255,0.1)"}, children=[
        html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"center"}, children=[
            html.Div(children=[
                html.Div(style={"display":"flex","alignItems":"center","gap":"12px"}, children=[
                    html.Span("🤖", style={"fontSize":"28px"}),
                    html.Div(children=[
                        html.H1("SmartQuery AI",
                                style={"margin":"0","fontSize":"24px","fontWeight":"700",
                                       "color":"#ffffff","letterSpacing":"-0.5px"}),
                        html.P("Natural Language Data Analysis · Google BigQuery · Gemini AI",
                               style={"margin":"2px 0 0 0","fontSize":"11px","color":C["blue"]}),
                    ])
                ])
            ]),
            html.Div(style={"display":"flex","gap":"8px","flexWrap":"wrap"}, children=[
                html.Span("☁️ BigQuery", style={"backgroundColor":"rgba(88,166,255,0.15)",
                                                "color":C["blue"],"padding":"4px 10px",
                                                "borderRadius":"20px","fontSize":"11px",
                                                "border":f"1px solid {C['blue']}"}),
                html.Span("🤖 Gemini AI", style={"backgroundColor":"rgba(63,185,80,0.15)",
                                                  "color":C["green"],"padding":"4px 10px",
                                                  "borderRadius":"20px","fontSize":"11px",
                                                  "border":f"1px solid {C['green']}"}),
                html.Span("📊 5 Datasets", style={"backgroundColor":"rgba(188,140,255,0.15)",
                                                   "color":C["purple"],"padding":"4px 10px",
                                                   "borderRadius":"20px","fontSize":"11px",
                                                   "border":f"1px solid {C['purple']}"}),
            ]),
        ])
    ]),

    # ── Main Layout ──
    html.Div(style={"display":"grid","gridTemplateColumns":"300px 1fr","minHeight":"calc(100vh - 80px)"}, children=[

        # ── LEFT SIDEBAR ──
        html.Div(style={"backgroundColor":C["card"],"borderRight":f"1px solid {C['border']}",
                        "padding":"20px","overflowY":"auto"}, children=[

            # Datasets
            html.H3("📁 Datasets", style={"margin":"0 0 12px 0","fontSize":"13px",
                                           "color":C["sub"],"textTransform":"uppercase","letterSpacing":"1px"}),
            html.Div(id="dataset-cards", children=[
                html.Div(style={"padding":"10px 12px","marginBottom":"8px","borderRadius":"8px",
                                "border":f"1px solid {C['border']}","cursor":"pointer",
                                "backgroundColor":C["card2"],"transition":"all 0.2s"}, children=[
                    html.Div(style={"display":"flex","alignItems":"center","gap":"8px"}, children=[
                        html.Span(DATASETS[k]["icon"], style={"fontSize":"18px"}),
                        html.Div(children=[
                            html.P(k.replace("_"," ").title(),
                                   style={"margin":"0","fontSize":"12px","fontWeight":"600",
                                          "color":C["text"]}),
                            html.P(DATASETS[k]["description"],
                                   style={"margin":"0","fontSize":"10px","color":C["sub"]}),
                        ])
                    ])
                ]) for k in DATASETS
            ]),

            html.Hr(style={"border":f"1px solid {C['border']}","margin":"16px 0"}),

            # Suggestions
            html.H3("💡 Example Queries", style={"margin":"0 0 12px 0","fontSize":"13px",
                                                   "color":C["sub"],"textTransform":"uppercase","letterSpacing":"1px"}),
            html.Div(children=[
                html.Div(s, id={"type":"suggestion","index":i},
                         style={"padding":"8px 10px","marginBottom":"6px","borderRadius":"6px",
                                "cursor":"pointer","fontSize":"11px","color":C["sub"],
                                "backgroundColor":C["card2"],"border":f"1px solid {C['border']}",
                                "lineHeight":"1.4","transition":"all 0.2s"},
                         className="suggestion-item")
                for i,s in enumerate(suggestions)
            ]),

            html.Hr(style={"border":f"1px solid {C['border']}","margin":"16px 0"}),

            # Query History
            html.H3("🕓 Query History", style={"margin":"0 0 12px 0","fontSize":"13px",
                                                "color":C["sub"],"textTransform":"uppercase","letterSpacing":"1px"}),
            html.Div(id="query-history-display",
                     style={"fontSize":"11px","color":C["sub"]},
                     children=[html.P("No queries yet", style={"margin":"0","fontStyle":"italic"})]),

            # Author card
            html.Hr(style={"border":f"1px solid {C['border']}","margin":"16px 0"}),
            html.Div(style={"padding":"12px","backgroundColor":C["card2"],"borderRadius":"8px",
                             "border":f"1px solid {C['border']}"}, children=[
                html.P("👨‍💻 Abhay Sharma",
                       style={"margin":"0 0 4px 0","fontSize":"12px","fontWeight":"600","color":C["text"]}),
                html.P("Manipal University Jaipur",
                       style={"margin":"0 0 4px 0","fontSize":"10px","color":C["sub"]}),
                html.P("🔗 github.com/KAZURIKAFU",
                       style={"margin":"0","fontSize":"10px","color":C["blue"]}),
            ]),
        ]),

        # ── RIGHT MAIN PANEL ──
        html.Div(style={"padding":"24px","overflowY":"auto"}, children=[

            # Query Input Box
            html.Div(style={"backgroundColor":C["card"],"borderRadius":"12px","padding":"20px",
                             "border":f"1px solid {C['border']}","marginBottom":"20px",
                             "boxShadow":"0 4px 20px rgba(0,0,0,0.3)"}, children=[
                html.H2("Ask a question about your data",
                        style={"margin":"0 0 6px 0","fontSize":"18px","fontWeight":"700","color":C["text"]}),
                html.P("Type in plain English — powered by Gemini AI & Google BigQuery",
                       style={"margin":"0 0 16px 0","fontSize":"12px","color":C["sub"]}),
                html.Div(style={"display":"flex","gap":"10px","alignItems":"center"}, children=[
                    dcc.Input(id="query-input", type="text", debounce=False,
                              placeholder="e.g.  Show top 10 most polluted cities in the world ...",
                              style={"flex":"1","backgroundColor":C["card2"],"border":f"1px solid {C['border']}",
                                     "borderRadius":"8px","padding":"12px 16px","color":C["text"],
                                     "fontSize":"14px","outline":"none"}),
                    html.Button("🔍 Analyze", id="run-query-btn", n_clicks=0,
                                style={"backgroundColor":C["blue"],"color":"#0d1117","border":"none",
                                       "borderRadius":"8px","padding":"12px 20px","fontSize":"14px",
                                       "fontWeight":"700","cursor":"pointer","whiteSpace":"nowrap"}),
                    html.Button("🗑️", id="clear-btn", n_clicks=0,
                                style={"backgroundColor":C["card2"],"color":C["sub"],"border":f"1px solid {C['border']}",
                                       "borderRadius":"8px","padding":"12px","fontSize":"14px","cursor":"pointer"}),
                ]),
                # Quick filters
                html.Div(style={"marginTop":"12px","display":"flex","gap":"8px","flexWrap":"wrap"}, children=[
                    html.Span(f"{DATASETS[k]['icon']} {k.replace('_',' ').title()}",
                              id={"type":"dataset-filter","index":k},
                              style={"padding":"4px 10px","borderRadius":"20px","fontSize":"11px",
                                     "cursor":"pointer","color":C["sub"],"border":f"1px solid {C['border']}",
                                     "backgroundColor":C["card2"]})
                    for k in DATASETS
                ]),
            ]),

            # Results area
            html.Div(id="results-area", children=[
                # Default welcome state
                html.Div(style={"textAlign":"center","padding":"60px 20px"}, children=[
                    html.Span("🤖", style={"fontSize":"64px"}),
                    html.H2("SmartQuery AI is ready",
                            style={"margin":"16px 0 8px 0","fontSize":"22px","color":C["text"]}),
                    html.P("Type a question above or click an example query on the left to get started.",
                           style={"margin":"0 0 24px 0","fontSize":"14px","color":C["sub"]}),
                    html.Div(style={"display":"flex","justifyContent":"center","gap":"16px","flexWrap":"wrap"}, children=[
                        html.Div(style={"backgroundColor":C["card"],"border":f"1px solid {C['border']}",
                                        "borderRadius":"10px","padding":"16px 20px","width":"160px"}, children=[
                            html.P(icon, style={"margin":"0 0 4px 0","fontSize":"28px"}),
                            html.P(label, style={"margin":"0","fontSize":"12px","color":C["sub"]})
                        ]) for icon, label in [
                            ("☁️", "Google BigQuery"),("🤖","Gemini AI"),("📊","5 Datasets"),
                            ("💬","Natural Language"),("⚡","Instant Results"),("📤","CSV Export")]
                    ])
                ])
            ]),
        ]),
    ]),

    # ── Hidden stores ──
    dcc.Store(id="query-history-store", data=[]),
    dcc.Store(id="last-result-store", data={}),
    dcc.Store(id="selected-query-store", data=""),

    # Footer
    html.Div(style={"textAlign":"center","padding":"16px","borderTop":f"1px solid {C['border']}",
                    "backgroundColor":C["card"],"color":C["sub"],"fontSize":"11px"}, children=[
        html.P("SmartQuery AI · Built by Abhay Sharma · Manipal University Jaipur · "
               "github.com/KAZURIKAFU · linkedin.com/in/abhay-sharma-426702208",
               style={"margin":"0"})
    ])
])


# ── Callbacks ─────────────────────────────────────────────────────────────────

# Handle suggestion clicks → fill input
@app.callback(
    Output("query-input","value"),
    Output("selected-query-store","data"),
    Input({"type":"suggestion","index":dash.ALL},"n_clicks"),
    Input("clear-btn","n_clicks"),
    State("query-input","value"),
    prevent_initial_call=True
)
def handle_suggestion_or_clear(suggestion_clicks, clear_clicks, current_val):
    triggered = ctx.triggered_id
    if triggered == "clear-btn":
        return "", ""
    if isinstance(triggered, dict) and triggered.get("type") == "suggestion":
        idx = triggered["index"]
        query_text = suggestions[idx].split(" ", 1)[1] if " " in suggestions[idx] else suggestions[idx]
        return query_text, query_text
    return current_val or "", ""


# Run query and render results
@app.callback(
    Output("results-area","children"),
    Output("query-history-store","data"),
    Output("last-result-store","data"),
    Output("query-history-display","children"),
    Input("run-query-btn","n_clicks"),
    State("query-input","value"),
    State("query-history-store","data"),
    prevent_initial_call=True
)
def run_query(n_clicks, query, history):
    if not query or not query.strip():
        return dash.no_update, history, {}, dash.no_update

    # Execute
    result = execute_query(query)

    # Update history
    history = history or []
    history.insert(0, {"query": query, "success": result["success"],
                        "rows": result.get("row_count", 0)})
    history = history[:10]

    # History display
    history_elements = [
        html.Div(style={"padding":"6px 8px","marginBottom":"4px","borderRadius":"6px",
                         "backgroundColor":C["card2"],"border":f"1px solid {C['border']}"}, children=[
            html.P(h["query"][:40]+("..." if len(h["query"])>40 else ""),
                   style={"margin":"0","fontSize":"10px","color":C["text"]}),
            html.P(f"{'✅' if h['success'] else '❌'} {h['rows']} rows",
                   style={"margin":"2px 0 0 0","fontSize":"9px","color":C["sub"]}),
        ]) for h in history
    ] or [html.P("No queries yet", style={"margin":"0","fontStyle":"italic"})]

    if not result["success"]:
        content = html.Div(style={"backgroundColor":"rgba(247,129,102,0.1)",
                                   "border":f"1px solid {C['orange']}","borderRadius":"10px","padding":"20px"}, children=[
            html.P(f"⚠️ Error: {result.get('error','Unknown error')}",
                   style={"margin":"0","color":C["orange"]})
        ])
        return content, history, {}, history_elements

    df = result["data"]
    fig = build_chart(result, height=420)
    stats = build_stats_cards(df, result.get("y",""))

    # Stats row
    stat_items = []
    labels = {"count":"Rows","mean":"Average","max":"Maximum","min":"Minimum","total":"Total"}
    colors_list = [C["blue"],C["green"],C["yellow"],C["orange"],C["purple"]]
    for i,(k,v) in enumerate(stats.items()):
        stat_items.append(
            html.Div(style={"backgroundColor":C["card"],"borderRadius":"8px","padding":"12px 16px",
                             "border":f"1px solid {C['border']}","borderTop":f"2px solid {colors_list[i]}",
                             "flex":"1","minWidth":"100px"}, children=[
                html.P(labels.get(k,k), style={"margin":"0 0 4px 0","fontSize":"10px",
                                                "color":C["sub"],"textTransform":"uppercase"}),
                html.P(v, style={"margin":"0","fontSize":"18px","fontWeight":"700","color":C["text"]}),
            ])
        )

    # Preview table (first 8 rows)
    preview_df = df.head(8)
    table_header = [html.Th(col, style={"padding":"8px 12px","textAlign":"left","fontSize":"11px",
                                         "color":C["sub"],"borderBottom":f"1px solid {C['border']}",
                                         "textTransform":"uppercase"})
                    for col in preview_df.columns]
    table_rows = []
    for _, row in preview_df.iterrows():
        table_rows.append(html.Tr(children=[
            html.Td(str(val), style={"padding":"7px 12px","fontSize":"12px","color":C["text"],
                                      "borderBottom":f"1px solid {C['border']}"})
            for val in row.values
        ]))

    content = html.Div(children=[
        # Query info bar
        html.Div(style={"backgroundColor":C["card"],"borderRadius":"10px","padding":"12px 16px",
                         "marginBottom":"16px","border":f"1px solid {C['border']}",
                         "display":"flex","justifyContent":"space-between","alignItems":"center"}, children=[
            html.Div(children=[
                html.Span("🤖 Query: ", style={"fontSize":"12px","color":C["sub"]}),
                html.Span(f'"{query}"', style={"fontSize":"12px","color":C["blue"],"fontWeight":"600"}),
            ]),
            html.Div(children=[
                html.Span(f"📊 Dataset: {result['dataset'].replace('_',' ').title()}  ",
                          style={"fontSize":"11px","color":C["sub"]}),
                html.Span(f"✅ {result['row_count']} rows returned",
                          style={"fontSize":"11px","color":C["green"]}),
            ]),
        ]),

        # Stats row
        html.Div(style={"display":"flex","gap":"10px","marginBottom":"16px","flexWrap":"wrap"},
                 children=stat_items),

        # Chart
        html.Div(style={"backgroundColor":C["card"],"borderRadius":"12px","padding":"20px",
                         "border":f"1px solid {C['border']}","marginBottom":"16px"}, children=[
            dcc.Graph(figure=fig, config={"displayModeBar":True,
                                          "modeBarButtonsToRemove":["pan2d","select2d","lasso2d"],
                                          "displaylogo":False})
        ]),

        # Data table
        html.Div(style={"backgroundColor":C["card"],"borderRadius":"12px","padding":"20px",
                         "border":f"1px solid {C['border']}"}, children=[
            html.Div(style={"display":"flex","justifyContent":"space-between","alignItems":"center",
                             "marginBottom":"12px"}, children=[
                html.H3(f"📋 Data Preview (first {len(preview_df)} of {len(df)} rows)",
                        style={"margin":"0","fontSize":"14px","color":C["text"]}),
                html.Span(f"Total: {len(df)} rows",
                          style={"fontSize":"11px","color":C["sub"],"backgroundColor":C["card2"],
                                 "padding":"4px 10px","borderRadius":"20px","border":f"1px solid {C['border']}"}),
            ]),
            html.Div(style={"overflowX":"auto"}, children=[
                html.Table(style={"width":"100%","borderCollapse":"collapse"}, children=[
                    html.Thead(html.Tr(table_header)),
                    html.Tbody(table_rows)
                ])
            ])
        ])
    ])

    return content, history, {"query": query, "rows": len(df)}, history_elements


if __name__ == "__main__":
    print("\n🚀 SmartQuery AI Starting...")
    print("📊 Loading datasets...")
    print("🌐 Open: http://localhost:8051\n")
    app.run(debug=True, port=8051)
