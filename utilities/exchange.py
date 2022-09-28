#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from requests import get
from typing import List
from typing import Optional


@dataclass
class Endpoint:
    """API endpoint interface."""

    api: str
    headers: Optional[dict] = field(
        default_factory=lambda: {
            "accept": "application/json"
        }
    )

    def get(self, endpoint: str, params: dict = None) -> List[dict]:
        response = get(
            self.api + endpoint,
            headers=self.headers,
            params=params
        )
        return response.json()


@dataclass
class Action(ABC):
    """Representation of an exchange's endpoint properties."""

    allowed: List[dict]
    default: str

    @abstractmethod
    def verify(self, value: str) -> bool:
        ...


@dataclass
class Exchange(ABC):
    """Representation of a financial exchange."""

    name: str
    endpoint: Endpoint
    products: Optional[Action] = None
    candles: Optional[Action] = None

    @abstractmethod
    def get_products(self) -> List[dict]:
        ...
    
    @abstractmethod
    def get_candles(self) -> List[dict]:
        ...