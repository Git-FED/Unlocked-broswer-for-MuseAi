"""Stable, transparent client metadata for reproducible authorized tests."""

from dataclasses import dataclass
import platform
import sys


@dataclass(frozen=True)
class ClientProfile:
    """A truthful profile used to make test runs reproducible."""

    name: str = "authorized-test-client"
    version: str = "0.1"
    platform: str = platform.system().lower()

    @property
    def user_agent(self) -> str:
        return f"{self.name}/{self.version} ({self.platform}; Python {sys.version_info.major}.{sys.version_info.minor})"


def default_profile() -> ClientProfile:
    return ClientProfile()
