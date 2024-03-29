"""
S&P 500 Index Analysis
"""
__author__ = "Shelby Potts"
__version__ = "0.0.0"

import src.financial_data as sp
import plotly.express as px
from dash import Dash, html, dash_table, dcc, Input, Output, callback
import dash_mantine_components as dmc
import pandas as pd


external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)


company_list = sp.load_companies_data()
financials = sp.load_company_financials()
vix = sp.load_cboe_volatility()


app.layout = html.Div([
    dmc.Title('S&P 500 Index Analysis', color="black", size="h1"),
    dmc.Space(h=20),
    dmc.Text("The S&P 500 Index (Standard and Poor's 500), is a stock market index tracking the stock performance of "
             "500 of the largest companies listed on stock exchanges in the United States. This is using publicly "
             "available data sets from datahub.io and visualizing the companies and their financials."),
    dmc.Space(h=10),

    # table listing s&p 500 companies
    dmc.Text("S&P 500 Companies", size="xl", align="left", weight=500),
    dmc.Space(h=10),
    dmc.Text("All 500 companies listed on the S&P 500 index. Each of the columns in the table can be filtered to look "
             "at specific data points"),
    dmc.Space(h=10),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in company_list.columns
        ],
        data=company_list.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Div(id='datatable-interactivity-container'),

    dmc.Text("VIX Volatility Index Close by Date", size="xl", weight=500),
    dmc.Space(h=10),
    dmc.Text("The VIX Volatility Index is a measurement of market volatility for companies listed on the S&P 500. The "
             "VIX is a reflection of the market risks and investor's sentiments over time. The VIX typically spikes "
             "when the stock market crashes, which also makes it an indicator of market volume. This graph shows the "
             "VIX closing price over time."),
    dmc.Text("The large spikes in the graph can be attributed to the Housing Market crash "
             "in 2008 and the Coronavirus Pandemic in 2020."),
    dcc.Graph(figure=px.line(vix, x="Date", y="VIX Close", hover_data=["Date"])),
    dmc.Space(h=10),

    # violin plot showing earnings/share by sector
    dmc.Text("Earnings/Share by Sector", size="xl", align="left", weight=500),
    dmc.Space(h=10),
    dmc.Text("Earnings per share is a metric investors use to determine the value of a company because it is a ratio "
             "of profitability per share. This graph shows how those metrics fluctuate per sector."),
    dmc.Space(h=10),
    dcc.Graph(figure=px.violin(financials, x="Sector", y="Earnings/Share", color="Sector", hover_data=["Name"])
              .update_layout(yaxis_range=[-30,45]),
              style={'height': '100vh'}),

    # box plot showing earnings/share by sector
    dmc.Text("Dividend Yield by Sector", size="xl", align="left", weight=500),
    dmc.Space(h=10),
    dmc.Text("The dividend yield is how much money in dividends a company pays out to shareholders relative to the "
             "stock price. This box plot shows the distribution of the dividend yields per sector."),
    dmc.Space(h=10),
    dcc.Graph(figure=px.box(financials, x="Sector", y="Dividend Yield", color="Sector", hover_data=["Name"])),

    # 3D scatter plot
    dmc.Text("Price by Price/Earnings by Earnings/Share", size="xl", align="left", weight=500),
    dmc.Space(h=10),
    dmc.Text("A 3D graph showing how price, price/earnings, and earnings/share relate to each other. The slider range "
             "at the bottom can be used to look at companies where ther stock price is within a certain range."),
    dmc.Space(h=10),
    html.Div(
        [
            dcc.Graph(id="graph"),
            html.P("Stock Price:"),
            dcc.RangeSlider(
                id="range-slider",
                min=0,
                max=2000,
                step=0.1,
                marks={0: "0", 1600: "1600"},
                value=[0, 2000],
            ),
        ]),

    # box plot showing earnings/share by sector
    dmc.Text("Best Price/Book for Top Companies with Largest Market Cap", size="xl", align="left", weight=500),
    dmc.Space(h=10),
    dmc.Text("Price/ book is a ratio of a company's market capitalization to book value. It is a metric investors use "
             "to determine whether a company is undervalued. P/B values under 3 are typically seen as a good investment"
             "."),
    dcc.Graph(figure=px.bar(financials.sort_values("Market Cap").where(financials["Price/Book"] <= 5).head(30), x="Name", y="Price/Book", color="Sector")
              .update_layout(yaxis_range=[0,5])
              ,style={'height': '100vh'}),

    dmc.Text("Prices per Sector", size="xl", align="left", weight=500),
    dmc.Space(h=10),
    dmc.Text("Scatter plots of stock prices for each sector."),
    dmc.Space(h=10),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Industrials"], x="Name", y="Price",
                                 title='Stock Prices for Industrials', color="Sector").update_layout(showlegend=False),
                      style={'width': '50%', 'display': 'inline-block', 'height': '75vh'}),
                dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Health Care"], x="Name", y="Price",
                                     title='Stock Prices for Health Care', color="Sector").update_layout(showlegend=False),
                          style={'width': '50%', 'display': 'inline-block', 'height': '75vh'}),
        html.Div(className='six columns', children=[
            dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Information Technology"], x="Name", y="Price",
                                        title='Stock Prices for Information Technology', color="Sector").update_layout(showlegend=False),
                      style={'width': '50%', 'display': 'inline-block', 'height': '75vh'}),
            dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Consumer Discretionary"], x="Name", y="Price",
                                        title='Stock Prices for Consumer Discretionary', color="Sector").update_layout(showlegend=False),
                      style={'width': '50%', 'display': 'inline-block', 'height': '75vh'}),
            dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Utilities"], x="Name", y="Price",
                                        title='Stock Prices for Utilities', color="Sector").update_layout(showlegend=False),
                      style={'width': '50%', 'display': 'inline-block', 'height': '75vh'}),
            dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Financials"], x="Name", y="Price",
                                        title='Stock Prices for Financials', color="Sector").update_layout(showlegend=False),
                      style={'width': '50%', 'display': 'inline-block', 'height': '75vh'}),
            dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Materials"], x="Name", y="Price",
                                        title='Stock Prices for Materials', color="Sector").update_layout(
                showlegend=False), style={'width': '50%', 'display': 'inline-block', 'height': '75vh'}),
            dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Real Estate"], x="Name", y="Price",
                                        title='Stock Prices for Real Estate', color="Sector").update_layout(
                showlegend=False), style={'width': '50%', 'display': 'inline-block', 'height': '75vh'}),
            dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Consumer Staples"], x="Name", y="Price",
                                        title='Stock Prices for Consumer Staples', color="Sector").update_layout(
                showlegend=False), style={'width': '50%', 'display': 'inline-block', 'height': '75vh'}),
            dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Energy"], x="Name", y="Price",
                                        title='Stock Prices for Energy', color="Sector").update_layout(
                showlegend=False), style={'width': '50%', 'display': 'inline-block', 'height': '75vh'}),
            dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Telecommunication Services"], x="Name", y="Price",
                                        title='Stock Prices for Telecommunication Services', color="Sector").update_layout(
                showlegend=False), style={'width': '50%', 'display': 'inline-block', 'height': '55vh'}),
            ])
        ]),
    ]),
])

@callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


@callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = company_list if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["Name"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["Price", "Market Cap", "52 Week Low", "52 Week High"] if column in dff
    ]


@app.callback(
    Output("graph", "figure"),
    Input("range-slider", "value"),
)
def update_chart(slider_range):
    low, high = slider_range
    mask = (financials.Price > low) & (financials.Price < high)

    fig = px.scatter_3d(
        financials[mask],
        x="Price/Earnings",
        y="Earnings/Share",
        z="Price",
        color="Sector",
        hover_data=["Name"],
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)