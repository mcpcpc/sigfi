#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from datetime import timezone
from typing import List

from utilities.exchange import Action
from utilities.exchange import Endpoint
from utilities.exchange import Exchange


@dataclass
class Options(Action):
    """Options action."""

    default: List[str] = field(
        default_factory=lambda: [
            "Moving Average (MA)"
        ]
    )
    allowed: List[dict] = field(
        default_factory=lambda: [
            {"label": "Moving Average (MA)", "value": "ma"},
            {"label": "EMA", "value": "ema"},
            {"label": "Relative Strength Index (RSI)", "value": "rsi"},
            {"label": "Volume", "value": "vol"},
            {"label": "Bollinger Bands", "value": "boll"},
            {"label": "MACD", "value": "macd"}
        ]
    )


@dataclass
class Candles(Action):
    """Candles action."""

    default: str = "86400"
    allowed: List[dict] = field(
        default_factory=lambda: [
            {"label": "1m", "value": "60"},
            {"label": "5m", "value": "300"},
            {"label": "15m", "value": "900"},
            {"label": "1h", "value": "3600"},
            {"label": "6h", "value": "2160"},
            {"label": "1d", "value": "86400"}
        ]
    )


@dataclass
class Products(Action):
    """Products action."""
    
    default: str = "BTC-USD"
    allowed: List[dict] = field(
        default_factory=lambda: []
    )


@dataclass
class Coinbase(Exchange):
    """Coinbase exchange."""

    name: str = "Coinbase"
    endpoint: Endpoint = Endpoint("https://api.exchange.coinbase.com")
    products: Action = Products()
    candles: Action = Candles()
    options: Action = Options()

    def get_products(self, params: dict = None) -> List[dict]:
        """Get available Coinbase trading pairs."""
        products = self.endpoint.get(
            endpoint="/products",
            params=params
        )
        return products
    
    def get_candles(self, product: str, params: dict = None) -> List[dict]:
        """Get open, high, low, close and volume Coinbase data."""
        records = self.endpoint.get(
            endpoint=f"/products/{product}/candles",
            params=params
        )
        to_ohlcv = lambda record: dict(
            timestamp=datetime.fromtimestamp(int(record[0]), timezone.utc),
            low=float(record[1]),
            high=float(record[2]),
            open=float(record[3]),
            close=float(record[4]),
            volume=float(record[5]),
        )
        ohlcv = list(map(to_ohlcv, records))
        ohlcv_sorted = sorted(ohlcv, key=lambda d: d["timestamp"])
        return ohlcv_sorted