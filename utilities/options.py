#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_mantine_components as dmc

from dataclasses import dataclass
from typing import List
from typing import Optional
from plotly import graph_objects
from plotly import subplots


@dataclass
class CandlesFigures:
    """Generates Candlestick Figure Objects."""

    data: List[dict]
    figure: Optional[graph_objects.Figure] = None
    timestamp: Optional[List] = None
    open: Optional[List] = None
    high: Optional[List] = None
    low: Optional[List] = None
    close: Optional[List] = None

    def _compute_moving_average(self, x: List[float], period: int = 20) -> List[float]:
        ma = []
        for i, _ in enumerate(x):
            window = x[(i - period):i]
            if len(window) > 0:
                ma.append(sum(window) / len(window))
            else:
                ma.append(None)
        return ma


    def create_figure(self) -> None:
        """Create Plotly figure."""
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
            #margin=dict(l=0, r=0, t=0, b=0),
            #showlegend=False
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
                open=self.open,
                high=self.high,
                low=self.low,
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
                name="Volume"
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

    def get_figure(self) -> None:
        """Return Plotly figure."""
        return self.figure