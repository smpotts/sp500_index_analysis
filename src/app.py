"""
Stock Market Analysis
"""
__author__ = "Shelby Potts"
__version__ = "0.0.0"

import src.sp500_data as sp
import plotly.express as px
from dash import Dash, html, dash_table, dcc, Input, Output, callback
import dash_mantine_components as dmc
import pandas as pd


external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)


company_list = sp.load_companies_data()
financials = sp.load_company_financials()
industrials = financials[financials["Sector"] == "Industrials"]


app.layout = html.Div([
    dmc.Title('Stock Market Analysis', color="black", size="h1"),
    dmc.Space(h=20),

    # table listing s&p 500 companies
    dmc.Text("S&P 500 Companies", size="xl", align="left"),
    dmc.Space(h=10),

    # dash_table.DataTable(data=company_list.to_dict('records'), page_size=10,
    #                      style_cell={'textAlign': 'left'}),
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

    # dcc.Graph(px.scatter(financials[financials["Sector"] == "Industrials"], x="Name", y="Price",
    #                      title='Stock Prices for Industrials', color="Sector")),

    dcc.Graph(figure=px.violin(financials, x="Sector", y="Price", color="Sector", hover_data=["Name"],
                                title="Stock Prices by Sector"), style={'height': '100vh'}),

    # html.Div(className='row', children=[
    #     html.Div(className='six columns', children=[
    #         dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Industrials"], x="Name", y="Price",
    #                              title='Stock Prices for Industrials', color="Sector"),
    #                   style={'width': '50%', 'display': 'inline-block'}),
    #         html.Div(className='six columns', children=[
    #             dcc.Graph(figure=px.scatter(financials[financials["Sector"] == "Health Care"], x="Name", y="Price",
    #                                  title='Stock Prices for Health Care', color="Sector"),
    #                       style={'width': '50%', 'display': 'inline-block'}),
    #     ]),
    # ]),

    # dcc.Graph(figure=px.scatter(financials["Sector"], x=financials["Name"], y="Price", color=sec)),


    # box plot showing earnings/share by sector
    dmc.Text("Earnings/Share by Sector", size="xl", align="left"),
    dmc.Space(h=10),
    dcc.Graph(figure=px.box(financials, x="Sector", y="Earnings/Share", color="Sector", hover_data=["Name"]),
              style={'height': '100vh'}),

    # 3D scatter plot
    dmc.Text("Price by Price/Earnings by Earnings/Share", size="xl", align="left"),
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
    dmc.Text("Dividend Yield by Sector", size="xl", align="left"),
    dmc.Space(h=10),
    dcc.Graph(figure=px.box(financials, x="Sector", y="Dividend Yield", color="Sector", hover_data=["Name"])),



    # dcc.Graph(figure=px.bar(financials.sort_values("Name"), x="Name", y="Market Cap",
    #                         title="Market Cap by Company")),

    # ])
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
    # print(financials[financials["Sector"] == "Industrials"])