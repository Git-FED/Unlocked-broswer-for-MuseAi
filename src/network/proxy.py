"""Proxy selection for explicitly authorized test proxies."""

from dataclasses import dataclass
from itertools import cycle
from typing import Iterable, Optional


@dataclass
class ProxyPool:
    proxies: Iterable[str]

    def __post_init__(self) -> None:
        values = [p.strip() for p in self.proxies if p and p.strip()]
        self._cycle = cycle(values) if values else None

    def next(self) -> Optional[str]:
        """Return the next configured proxy, or None when none were supplied."""
        return next(self._cycle) if self._cycle else None
