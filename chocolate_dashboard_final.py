import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load & Clean Data
df = pd.read_csv("Chocolate Sales.csv")

df["Amount"] = df["Amount"].replace(r'[\$,]', '', regex=True).astype(float)
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)
df["Year"] = df["Date"].dt.year

# App Setup
app = Dash(__name__)
app.title = "Chocolate Sales Analytics Dashboard"

countries = sorted(df["Country"].unique())
products = sorted(df["Product"].unique())

year_min = df["Year"].min()
year_max = df["Year"].max()

# Styles
CARD_STYLE = {
    "backgroundColor": "#4E342E",
    "color": "white",
    "padding": "22px",
    "borderRadius": "18px",
    "boxShadow": "0 6px 18px rgba(0,0,0,0.15)",
    "textAlign": "center",
    "flex": "1",
}

GRAPH_CARD = {
    "backgroundColor": "white",
    "padding": "20px",
    "borderRadius": "18px",
    "boxShadow": "0 6px 18px rgba(0,0,0,0.08)",
    "marginBottom": "24px",
}

# Layout
app.layout = html.Div(
    style={
        "fontFamily": "Segoe UI, Arial, sans-serif",
        "backgroundColor": "#F8F5F2",
        "minHeight": "100vh",
        "padding": "0",
        "margin": "0",
    },
    children=[
        # Header
        html.Div(
            style={
                "backgroundColor": "#3E2723",
                "color": "white",
                "padding": "36px 50px",
            },
            children=[
                html.H1(
                    "Chocolate Sales Analytics Dashboard",
                    style={"margin": "0", "fontSize": "40px"},
                ),
                html.P(
                    "Interactive analysis of global chocolate sales performance from 2022 to 2024",
                    style={"marginTop": "10px", "fontSize": "18px", "color": "#D7CCC8"},
                ),
            ],
        ),

        html.Div(
            style={"padding": "30px 50px"},
            children=[
                # Filters
                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "22px",
                        "borderRadius": "18px",
                        "boxShadow": "0 6px 18px rgba(0,0,0,0.08)",
                        "marginBottom": "28px",
                    },
                    children=[
                        html.H3("Filters", style={"marginTop": "0", "color": "#3E2723"}),

                        html.Div(
                            style={
                                "display": "grid",
                                "gridTemplateColumns": "1fr 1fr",
                                "gap": "24px",
                            },
                            children=[
                                html.Div([
                                    html.Label("Select Countries", style={"fontWeight": "600"}),
                                    dcc.Dropdown(
                                        id="country-filter",
                                        options=[{"label": c, "value": c} for c in countries],
                                        value=countries,
                                        multi=True,
                                        placeholder="Select countries",
                                    ),
                                ]),

                                html.Div([
                                    html.Label("Select Products", style={"fontWeight": "600"}),
                                    dcc.Dropdown(
                                        id="product-filter",
                                        options=[{"label": p, "value": p} for p in products],
                                        value=[],
                                        multi=True,
                                        placeholder="Optional: select products, or leave blank for all",
                                    ),
                                ]),
                            ],
                        ),

                        html.Div(
                            style={"marginTop": "26px"},
                            children=[
                                html.Label("Select Year", style={"fontWeight": "600"}),
                                dcc.Slider(
                                    id="year-slider",
                                    min=year_min,
                                    max=year_max,
                                    step=1,
                                    value=year_min,
                                    marks={y: str(y) for y in range(year_min, year_max + 1)},
                                ),
                            ],
                        ),
                    ],
                ),

                # KPI Cards
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(4, 1fr)",
                        "gap": "20px",
                        "marginBottom": "28px",
                    },
                    children=[
                        html.Div(id="kpi-sales", style=CARD_STYLE),
                        html.Div(id="kpi-boxes", style=CARD_STYLE),
                        html.Div(id="kpi-product", style=CARD_STYLE),
                        html.Div(id="kpi-country", style=CARD_STYLE),
                    ],
                ),

                # Main Trend
                html.Div(
                    style=GRAPH_CARD,
                    children=[
                        html.Div(
                            id="flag-display",
                            style={
                                "fontSize": "22px",
                                "marginBottom": "6px",
                                "color": "#3E2723",
                                "display": "flex",
                                "alignItems": "center",
                                "gap": "6px",
                                "flexWrap": "wrap",
                            },
                        ),
                        html.Div(
                            style={
                                "display": "flex",
                                "justifyContent": "flex-end",
                                "marginBottom": "10px",
                            },
                            children=[
                                dcc.RadioItems(
                                    id="line-chart-topn",
                                    options=[
                                        {"label": " Top 5",  "value": 5},
                                        {"label": " Top 10", "value": 10},
                                        {"label": " All",    "value": 0},
                                    ],
                                    value=5,
                                    inline=True,
                                    style={"fontSize": "14px", "color": "#3E2723"},
                                    inputStyle={
                                        "marginRight": "4px",
                                        "marginLeft": "12px",
                                        "accentColor": "#4E342E",
                                    },
                                )
                            ],
                        ),
                        dcc.Graph(id="line-chart"),
                    ],
                ),

                # Two-chart analysis
                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "24px",
                    },
                    children=[
                        html.Div(style=GRAPH_CARD, children=[dcc.Graph(id="country-chart")]),

                        # Salesperson chart card with click-to-pie swap
                        html.Div(
                            style=GRAPH_CARD,
                            children=[
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "justifyContent": "space-between",
                                        "alignItems": "center",
                                        "marginBottom": "0px",
                                    },
                                    children=[
                                        html.Button(
                                            "← Back to Top 10",
                                            id="salesperson-back-btn",
                                            n_clicks=0,
                                            style={
                                                "display": "none",
                                                "background": "none",
                                                "border": "none",
                                                "color": "#6D4C41",
                                                "fontSize": "13px",
                                                "cursor": "pointer",
                                                "fontWeight": "600",
                                                "padding": "0",
                                            },
                                        ),
                                    ],
                                ),
                                # Bar chart (default view)
                                dcc.Graph(id="salesperson-chart"),
                                # Pie chart (hidden by default)
                                html.Div(
                                    id="salesperson-pie-container",
                                    style={"display": "none"},
                                    children=[dcc.Graph(id="salesperson-pie")],
                                ),
                                html.P(
                                    "Click a bar to see product breakdown",
                                    id="salesperson-hint",
                                    style={
                                        "fontSize": "12px",
                                        "color": "#8D6E63",
                                        "margin": "8px 0 0 0",
                                        "fontStyle": "italic",
                                        "textAlign": "right",
                                    }
                                ),
                            ],
                        ),
                    ],
                ),

                # Bubble chart
                html.Div(
                    style=GRAPH_CARD,
                    children=[
                        dcc.Graph(id="bubble-chart"),
                    ],
                ),
            ],
        ),
    ],
)

# Callback
@app.callback(
    Output("line-chart", "figure"),
    Output("country-chart", "figure"),
    Output("salesperson-chart", "figure"),
    Output("bubble-chart", "figure"),
    Output("kpi-sales", "children"),
    Output("kpi-boxes", "children"),
    Output("kpi-product", "children"),
    Output("kpi-country", "children"),
    Output("flag-display", "children"),
    Input("country-filter", "value"),
    Input("product-filter", "value"),
    Input("year-slider", "value"),
    Input("line-chart-topn", "value"),
)
def update_dashboard(selected_countries, selected_products, selected_year, topn):
    COUNTRY_FLAGS = {
        "Australia":   "🇦🇺",
        "Canada":      "🇨🇦",
        "India":       "🇮🇳",
        "New Zealand": "🇳🇿",
        "UK":          "🇬🇧",
        "USA":         "🇺🇸",
    }

    active_countries = selected_countries if selected_countries else list(COUNTRY_FLAGS.keys())
    flag_children = [
        html.Span(COUNTRY_FLAGS.get(c, ''),
                  style={"fontSize": "14px", "backgroundColor": "#F0EAE6",
                         "padding": "3px 10px", "borderRadius": "20px",
                         "color": "#3E2723", "fontWeight": "500"})
        for c in sorted(active_countries)
    ]
    flag_display = [
        html.Span("Showing: ", style={"fontSize": "13px", "color": "#8D6E63", "marginRight": "4px"}),
        *flag_children,
    ]

    dff = df.copy()

    if selected_countries:
        dff = dff[dff["Country"].isin(selected_countries)]

    if selected_products:
        dff = dff[dff["Product"].isin(selected_products)]

    year_df = dff[dff["Year"] == selected_year]

    # KPI
    total_sales = year_df["Amount"].sum()
    total_boxes = year_df["Boxes Shipped"].sum()

    if not year_df.empty:
        best_product = (
            year_df.groupby("Product")["Amount"]
            .sum()
            .idxmax()
        )
        top_country = (
            year_df.groupby("Country")["Amount"]
            .sum()
            .idxmax()
        )
    else:
        best_product = "N/A"
        top_country = "N/A"

    kpi_sales = [
        html.Div("Total Revenue", style={"fontSize": "14px", "color": "#D7CCC8"}),
        html.Div(f"${total_sales:,.0f}", style={"fontSize": "28px", "fontWeight": "700"}),
    ]

    kpi_boxes = [
        html.Div("Boxes Shipped", style={"fontSize": "14px", "color": "#D7CCC8"}),
        html.Div(f"{total_boxes:,.0f}", style={"fontSize": "28px", "fontWeight": "700"}),
    ]

    kpi_product = [
        html.Div("Best Product", style={"fontSize": "14px", "color": "#D7CCC8"}),
        html.Div(best_product, style={"fontSize": "22px", "fontWeight": "700"}),
    ]

    kpi_country = [
        html.Div("Top Market", style={"fontSize": "14px", "color": "#D7CCC8"}),
        html.Div(top_country, style={"fontSize": "22px", "fontWeight": "700"}),
    ]

    # Main Line Chart: Top N Products
    all_products_ranked = (
        dff.groupby("Product")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    if topn == 0:
        selected_line_products = all_products_ranked.index
        line_title = "Sales Trend Over Time: All Products"
    else:
        selected_line_products = all_products_ranked.head(topn).index
        line_title = f"Sales Trend Over Time: Top {topn} Products"

    line_df = (
        dff[dff["Product"].isin(selected_line_products)]
        .groupby(["Year", "Product"])["Amount"]
        .sum()
        .reset_index()
    )

    fig_line = px.line(
        line_df,
        x="Year",
        y="Amount",
        color="Product",
        markers=True,
        title=line_title,
        category_orders={"Product": list(selected_line_products)},
    )

    # Country Chart
    country_df = (
        year_df.groupby("Country")["Amount"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig_country = px.bar(
        country_df,
        x="Amount",
        y="Country",
        orientation="h",
        title=f"Sales by Country ({selected_year})",
        text_auto=".2s",
    )
    fig_country.update_traces(marker_color="#6D4C41")

    # Salesperson Chart — Total Revenue Bar
    top10_sales_people = (
        year_df.groupby("Sales Person")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .index
    )

    sp_total = (
        year_df[year_df["Sales Person"].isin(top10_sales_people)]
        .groupby("Sales Person")["Amount"]
        .sum()
        .sort_values(ascending=True)
    )
    sp_order = sp_total.index.tolist()

    simple_df = sp_total.reset_index()
    fig_product = px.bar(
        simple_df,
        x="Amount",
        y="Sales Person",
        orientation="h",
        title=f"Top 10 Sales People by Revenue ({selected_year})",
        text_auto=".2s",
        category_orders={"Sales Person": sp_order},
    )
    fig_product.update_traces(
        marker_color="#8D6E63",
        selected_marker_color="#3E2723",
    )

    # Bubble Chart — aggregated by Product (Each bubble size = Revenue per Box)
    bubble_df = (
        year_df[year_df["Boxes Shipped"] > 0]
        .groupby("Product")
        .agg(
            Total_Amount=("Amount", "sum"),
            Total_Boxes=("Boxes Shipped", "sum"),
        )
        .reset_index()
    )
    bubble_df["Revenue per Box"] = bubble_df["Total_Amount"] / bubble_df["Total_Boxes"]
    # Amplify size differences by squaring
    bubble_df["Bubble Size"] = bubble_df["Revenue per Box"] ** 2

    fig_bubble = px.scatter(
        bubble_df,
        x="Total_Amount",
        y="Total_Boxes",
        size="Bubble Size",
        color="Product",
        hover_name="Product",
        hover_data={
            "Total_Amount": ":,.0f",
            "Total_Boxes": ":,.0f",
            "Revenue per Box": ":.2f",
            "Product": False,
        },
        labels={
            "Total_Amount": "Total Revenue ($)",
            "Total_Boxes": "Total Boxes Shipped",
            "Revenue per Box": "Revenue per Box ($)",
        },
        title=f"Product Performance Overview ({selected_year})",
        size_max=55,
    )

    # Shared Chart Styling
    for fig in [fig_line, fig_country, fig_product, fig_bubble]:
        fig.update_layout(
            plot_bgcolor="#F8F5F2",
            paper_bgcolor="white",
            font=dict(color="#3E2723"),
            title_font=dict(size=20, color="#3E2723"),
            margin=dict(l=40, r=40, t=70, b=40),
        )

    fig_line.update_xaxes(dtick=1)

    return (
        fig_line,
        fig_country,
        fig_product,
        fig_bubble,
        kpi_sales,
        kpi_boxes,
        kpi_product,
        kpi_country,
        flag_display,
    )


# Callback: click bar -> swap to pie; back button -> swap back
@app.callback(
    Output("salesperson-pie", "figure"),
    Output("salesperson-pie-container", "style"),
    Output("salesperson-chart", "style"),
    Output("salesperson-back-btn", "style"),
    Output("salesperson-hint", "style"),
    Input("salesperson-chart", "clickData"),
    Input("salesperson-back-btn", "n_clicks"),
    Input("country-filter", "value"),
    Input("product-filter", "value"),
    Input("year-slider", "value"),
)
def swap_salesperson_view(clickData, n_clicks, selected_countries, selected_products, selected_year):
    from dash import ctx

    HIDE = {"display": "none"}
    SHOW_BLOCK = {"display": "block"}
    BACK_BTN_VISIBLE = {
        "display": "inline-block",
        "background": "none",
        "border": "none",
        "color": "#6D4C41",
        "fontSize": "13px",
        "cursor": "pointer",
        "fontWeight": "600",
        "padding": "0",
    }
    HINT_VISIBLE = {
        "fontSize": "12px",
        "color": "#8D6E63",
        "margin": "8px 0 0 0",
        "fontStyle": "italic",
        "textAlign": "right",
    }

    triggered = ctx.triggered_id

    # Reset to bar view if back button clicked or filters changed
    if triggered in ("salesperson-back-btn", "country-filter", "product-filter", "year-slider") or not clickData:
        return {}, HIDE, SHOW_BLOCK, HIDE, HINT_VISIBLE

    # Build pie
    person = clickData["points"][0]["y"]

    dff = df.copy()
    if selected_countries:
        dff = dff[dff["Country"].isin(selected_countries)]
    if selected_products:
        dff = dff[dff["Product"].isin(selected_products)]

    person_df = dff[
        (dff["Sales Person"] == person) &
        (dff["Year"] == selected_year)
    ].groupby("Product")["Amount"].sum().sort_values(ascending=False).reset_index()

    # Group products below 2% into "Others"
    total = person_df["Amount"].sum()
    person_df["pct"] = person_df["Amount"] / total
    main_df = person_df[person_df["pct"] >= 0.02].copy()
    small_df = person_df[person_df["pct"] < 0.02].copy()

    if not small_df.empty:
        others_sum = small_df["Amount"].sum()
        import pandas as pd
        others_row = pd.DataFrame([{"Product": "Others", "Amount": others_sum, "pct": others_sum / total}])
        person_df = pd.concat([main_df, others_row], ignore_index=True)
    else:
        person_df = main_df

    person_df = person_df.drop(columns=["pct"])

    fig_pie = px.pie(
        person_df,
        values="Amount",
        names="Product",
        title=f"{person} — Product Breakdown ({selected_year})",
        color_discrete_sequence=px.colors.sequential.Oranges_r,
        hole=0.35,
    )
    fig_pie.update_traces(
        textposition="inside",
        textinfo="percent+label",
        insidetextorientation="radial",
    )
    fig_pie.update_layout(
        plot_bgcolor="#F8F5F2",
        paper_bgcolor="white",
        font=dict(color="#3E2723", size=12),
        title_font=dict(size=18, color="#3E2723"),
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True,
        legend=dict(
            font=dict(size=11, color="#3E2723"),
            bgcolor="rgba(0,0,0,0)",
        ),
    )

    return fig_pie, SHOW_BLOCK, HIDE, BACK_BTN_VISIBLE, HIDE




if __name__ == "__main__":
    app.run(debug=True)