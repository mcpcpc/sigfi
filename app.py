#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dash import dash
from dash import page_registry

from layout.default import layout


app = Dash(__name__, use_pages=True)
values =  page_registry.values()
app.layout = layout(values)
server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)