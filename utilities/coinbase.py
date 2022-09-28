#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from datetime import timezone

from utilities.exchange import Action
from utilities.exchange import Endpoint
from utilities.exchange import Exchange

@dataclass
class Candles(Action):
    """Candles action."""

    default: int = 60
    allowed: List[dict] = field(
        default_factory=lambda: [
            {"label": "1m", "value": 60},
            {"label": "5m", "value": 300},
            {"label": "15h", "value": 900},
            {"label": "1h", "value": 3600},
            {"label": "6h", "value": 2160},
            {"label": "1d", "value": 86400}
        ]
    )

    def verify(self, value) -> bool:
        is_allowed = value in allowed
        return is_allowed

@dataclass
class Coinbase(Exchange):
    """Coinbase exchange."""

    name: str
    endpoint: Endpoint("https://api.exchange.coinbase.com")
    candles: Action = Candles

    def products(self, params: dict = None) -> List[dict]:
        """Get available Coinbase trading pairs."""
        products = self.endpoint.get(
            endpoint="/products",
            params=params
        )
        return products
    
    def candles(self, product: str, params: dict = None) -> List[dict]:
        """Get open, high, low, close and volume Coinbase data."""
        records = self.endpoint.get(
            endpoint=f"/products/{product}/candles",
            params=params
        )
        to_ohlcv = lambda record: dict(
            timestamp=datetime.fromtimestamp(int(record[0]), timezone.utc),
            open=float(record[1]),
            high=float(record[2]),
            low=float(record[3]),
            close=float(record[4]),
            volume=float(record[5]),
        )
        ohlcv = list(map(to_ohlcv, records))
        return ohlcv