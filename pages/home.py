#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_mantine_components as dmc

from dash_iconify import DashIconify
from dash import register_page

layout = dmc.Container(
    id="wrapper",
    children=[
        dmc.Container(
            pl=8,
            pr=8,
            style={"marginTop": 30, "marginBottom": 20},
            children=[
                dmc.Text(
                    "SigFi Suite",
                    align="center",
                    style={"fontSize": 30}
                ),
                dmc.Text(
                    "A collection of crypto tools.",
                    align="center"
                )
            ]
        ),
        dmc.Grid(
            gutter="xl",
            children=[
                dmc.Col(
                    children=[
                        dmc.Anchor(
                            children=[
                                dmc.Paper(
                                    withBorder=True,
                                    p="lg",
                                    children=[
                                        dmc.Group(
                                            direction="column",
                                            align="center",
                                            children=[
                                                dmc.ThemeIcon(
                                                    DashIconify(icon="ic:outline-candlestick-chart", height=20),
                                                    size=40,
                                                    radius=40,
                                                    variant="light"
                                                ),
                                                dmc.Text(
                                                    "Product Candles",
                                                    weight=500,
                                                    style={"marginTop": 15, "marginBottom": 5}
                                                ),
                                                dmc.Text(
                                                    color="dimmed",
                                                    size="sm",
                                                    align="center",
                                                    style={"lineHeight": 1.6, "marginBottom": 10},
                                                    children=[
                                                        "Tools for monitoring and measuring cryptocurrency ",
                                                        "pairs. This includes RSI, SMA, Volume, and Bollinger ",
                                                        "measurements."
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ],
                            href="/candles"
                        )
                    ]
                )
            ]
        )
    ]
)

register_page(
    __name__,
    path="/",
    title="Home | SigFi",
    description="Charts for open, high, low, close and volume data.",
    layout=layout
)
