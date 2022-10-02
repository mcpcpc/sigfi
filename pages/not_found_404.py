#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash
import dash_mantine_components as dmc

layout = dmc.Group(
    direction="column",
    align="center",
    children=[
        dmc.Text(
            [
                "If you think this page should exist, create an issue ",
                dmc.Anchor(
                    "here",
                    underline=False,
                    href="https://github.com/mcpcpc/sigfi/issues/new",
                ),
                ".",
            ]
        ),
        dmc.Anchor("Go back to home ->", href="/", underline=False),
    ],
)

dash.register_page(
    __name__,
    path="/404",
    layout=layout
)