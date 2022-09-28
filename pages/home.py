#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_mantine_components as dmc

from dash import register_page

layout=dmc.Container(
    children=[
    ]
)

register_page(
    __name__,
    path="/",
    title="Home | SigFi",
    description="Charts for open, high, low, close and volume data.",
    layout=layout
)
