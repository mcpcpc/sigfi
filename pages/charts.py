#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_mantine_components as dmc

from dash import register_page

layout=dmc.Container(
    children=[
        dmc.Navbar(
            id="tools-nabar",
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
                        description="Available Token pairs",
                        searchable=True,
                        nothingFound="Invalid product",
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
                dcc.Graph(id="charts", config={"displayModeBar": False})
            ]
        )
    ]
)

register_page(
    __name__,
    path="/charts/",
    title="Charts | SigFi",
    description="Charts for open, high, low, close and volume data.",
    layout=layout
)