#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_mantine_components as dmc

from dataclasses import dataclass
from typing import List
from typing import Optional
from plotly import graph_objects
from plotly import subplots

def hex_to_rgb(value: str) -> tuple:
    """Convert hexidecimal string to RGB tuple."""
    red = int(value[1:3], 16)
    green = int(value[3:5], 16)
    blue = int(value[5:7], 16)
    return (red, green, blue)

def rgb_to_rgba(rgb: str, alpha:float) -> str:
    """Compute RGBA string from RGB tuple."""
    red, green, blue = rgb
    rgba = f"rgba({red}, {green}, {blue}, {alpha})"
    return rgba


@dataclass
class CandlesFigures:
    """Generates candlestick figure objects."""

    data: List[dict]
    figure: Optional[graph_objects.Figure] = None
    timestamp: Optional[List] = None
    low: Optional[List] = None
    high: Optional[List] = None
    open: Optional[List] = None
    close: Optional[List] = None

    def create_figure(self) -> None:
        """Create Plotly figure."""
        rgb = hex_to_rgb(dmc.theme.DEFAULT_COLORS["indigo"][6])
        rgba = rgb_to_rgba(rgb, 0.5)
        figure = subplots.make_subplots(
            specs=[[{"secondary_y": True}]],
            rows=1,
            cols=1
        )
        figure.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_family="Inter, sans-serif",
            xaxis_rangeslider_visible=False,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        figure.update_yaxes(
            gridcolor=rgba,
            row=1,
            col=1
        )
        figure.update_xaxes(
            gridcolor=rgba,
            row=1,
            col=1
        )
        self.figure = figure
    
    def add_candles(self) -> None:
        """Add Candles data to figure."""
        if self.figure == None:
            return
        self.timestamp = [x["timestamp"] for x in self.data]
        self.open = [x["open"] for x in self.data]
        self.high = [x["high"] for x in self.data]
        self.low = [x["low"] for x in self.data]
        self.close = [x["close"] for x in self.data]
        self.figure.add_trace(
            graph_objects.Candlestick(
                name="Candles",
                x=self.timestamp,
                low=self.low,
                high=self.high,
                open=self.open,
                close=self.close,
                increasing_line_color=dmc.theme.DEFAULT_COLORS["indigo"][6],
                increasing_line_width=2,
                increasing_fillcolor="rgba(0,0,0,0)",
                decreasing_line_color=dmc.theme.DEFAULT_COLORS["indigo"][6],
                decreasing_line_width=2,
                decreasing_fillcolor=dmc.theme.DEFAULT_COLORS["indigo"][6]
            ),
            row=1,
            col=1,
            secondary_y=False
        )
    
    def add_volume(self) -> None:
        """Add Volume data to figure."""
        if self.figure == None:
            return
        self.volume = [x["volume"] for x in self.data]
        self.figure.add_trace(
            graph_objects.Bar(
                name="Volume",
                x=self.timestamp,
                y=self.volume,
                marker={"line": {"width": 0}},
                opacity=0.3,
                marker_color=dmc.theme.DEFAULT_COLORS["indigo"][6]
            ),
            row=1,
            col=1,
            secondary_y=True
        )
        self.figure.update_yaxes(
            range=[0.0, max(self.volume) * 2],
            secondary_y=True,
            visible=False
        )

    def add_moving_average(self, period: int) -> None:
        """Add simle moving average to figure."""
        ma = []
        for i, _ in enumerate(self.close):
            window = self.close[i-period:i]
            if len(window) > 0:
                ma_ = sum(window) / len(window)
            else:
                ma_ = None
            ma.append(ma_)
        self.figure.add_trace(
            graph_objects.Scatter(
                name="MA" + str(period),
                x=self.timestamp,
                y=ma,
                line_color=dmc.theme.DEFAULT_COLORS["yellow"][6],
                line = {"width": 1}
            ),
            row=1,
            col=1,
            secondary_y=False
        )



    def get_figure(self) -> None:
        """Return Plotly figure."""
        return self.figure