#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_mantine_components as dmc

from dash import callback
from dash import dcc
from dash import register_page
from dash import no_update
from dash import Input
from dash import Output
from dash_iconify import DashIconify
from plotly import subplots
from plotly import graph_objects

from utilities.coinbase import Coinbase

layout=dmc.Container(
    children=[
        dmc.Navbar(
            id="tools-navbar",
            fixed=True,
            position={"top": 70, "right": 0},
            width={"base": 300},
            style={"paddingRight": 20},
            children=dmc.Group(
                direction="column",
                grow=True,
                children=[
                    dmc.Select(
                        id="exchange",
                        label="Exchange",
                        description="i.e. Coinbase, FTX, etc."
                    ),
                    dmc.Select(
                        id="products",
                        label="Products",
                        description="Available token pairs",
                        searchable=True,
                        nothingFound="Invalid product option",
                        icon=[DashIconify(icon="radix-icons:magnifying-glass")]
                    ),
                    dmc.Select(
                        id="timeframe",
                        label="Timeframe",
                        description="i.e. 1m, 5m, 1h, 1d, etc."
                    ),
                    dmc.MultiSelect(
                        id="options",
                        label="Options",
                        maxSelectedValues=5
                    )
                ]
            )
        ),
        dmc.LoadingOverlay(
            loaderProps={"variant": "bars"},
            children=[
                dcc.Graph(id="candles", config={"displayModeBar": False})
            ]
        ),
        dcc.Interval(id="live_update", max_intervals=1)
    ]
)

@callback(
    Output("exchange", "data"),
    Output("exchange", "value"),
    Input("live_update", "n_intervals"))
def update_exchanges(n_intervals):
    data = [
        {"label": "Coinbase", "value": "COINBASE"},
        {"label": "BitFenix", "value": "BITFENIX"},
    ]
    value = "COINBASE"
    return data, value

@callback(
    Output("products", "data"),
    Output("products", "value"),
    Input("exchange", "value"))
def update_products(exchange_value):
    if exchange_value == "COINBASE":
        exchange = Coinbase()
    else:
        return no_update, no_update
    products = exchange.get_products()
    data = [dict(label=x["id"], value=x["id"]) for x in products]
    data_sorted = sorted(data, key=lambda d: d["label"])
    value = data_sorted[0]["value"]
    return data_sorted, value

@callback(
    Output("timeframe", "data"),
    Output("timeframe", "value"),
    Input("exchange", "value"))
def update_timeframe(exchange_value):
    if exchange_value == "COINBASE":
        exchange = Coinbase()
    else:
        return no_update, no_update
    data = exchange.candles.allowed
    value = exchange.candles.default
    return data, value

@callback(
    Output("options", "data"),
    Output("options", "value"),
    Input("exchange", "value"))
def update_options(exchange_value):
    if exchange_value == "COINBASE":
        exchange = Coinbase()
    else:
        return no_update, no_update
    allowed = exchange.options.allowed
    data = [x["label"] for x in allowed]
    value = exchange.options.default
    return data, value 

@callback(
    Output("candles", "figure"),
    Input("exchange", "value"),
    Input("products", "value"),
    Input("timeframe", "value"),
    Input("options", "value"))
def update_candles(exchange, product, timeline, options):
    if exchange == "COINBASE":
        exchange = Coinbase()
    else:
        return no_update, no_update
    df = exchange.get_candles(product)
    fig = subplots.make_subplots()
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_family="Inter, sans-serif"
    )
    return fig

register_page(
    __name__,
    path="/candles/",
    title="Candles | SigFi",
    description="Charts for OHLCV (open, high, low, close and volume) data.",
    layout=layout
)