"""Session façade for simple, authorized browser checks."""

from dataclasses import dataclass, field
from src.network.fetch import fetch
from src.network.proxy import ProxyPool
from src.stealth.fingerprint import ClientProfile, default_profile


@dataclass
class BrowserSession:
    profile: ClientProfile = field(default_factory=default_profile)
    proxies: ProxyPool = field(default_factory=lambda: ProxyPool([]))

    def open(self, url: str) -> tuple[int, bytes]:
        proxy = self.proxies.next()
        return fetch(url, self.profile.user_agent, proxy=proxy)
