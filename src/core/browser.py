"""Authorized browser session backed by Playwright Chromium.

This module deliberately does not spoof fingerprints or bypass CAPTCHA/security
checks. A human can take over when a site requests a challenge or confirmation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from src.network.proxy import ProxyPool
from src.stealth.fingerprint import ClientProfile, default_profile


class BrowserUnavailableError(RuntimeError):
    """Raised when Playwright or its Chromium browser is unavailable."""


@dataclass
class BrowserResult:
    status: int
    title: str
    url: str
    html: str


@dataclass
class BrowserSession:
    """A persistent Chromium context for an authorized test session.

    The profile directory stores cookies, local storage, and other browser state
    between runs. Keep it outside source control and never share it publicly.
    """

    profile: ClientProfile = field(default_factory=default_profile)
    proxies: ProxyPool = field(default_factory=lambda: ProxyPool([]))
    user_data_dir: Path = Path(".browser-data")
    headless: bool = True
    timeout_ms: int = 30_000
    _playwright: object | None = field(default=None, init=False, repr=False)
    _context: object | None = field(default=None, init=False, repr=False)
    _page: object | None = field(default=None, init=False, repr=False)

    def start(self) -> "BrowserSession":
        """Start a persistent Chromium context with JavaScript enabled."""
        if self._context is not None:
            return self
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise BrowserUnavailableError(
                "Playwright is not installed. Run: pip install -r requirements.txt"
            ) from exc

        self.user_data_dir = Path(self.user_data_dir).expanduser()
        self.user_data_dir.mkdir(parents=True, exist_ok=True)
        proxy = self.proxies.next()
        try:
            self._playwright = sync_playwright().start()
            launch_options = {
                "headless": self.headless,
                "user_agent": self.profile.user_agent,
                "viewport": {"width": 1440, "height": 900},
            }
            if proxy:
                launch_options["proxy"] = {"server": proxy}
            self._context = self._playwright.chromium.launch_persistent_context(
                str(self.user_data_dir), **launch_options
            )
            self._context.set_default_timeout(self.timeout_ms)
            self._page = self._context.pages[0] if self._context.pages else self._context.new_page()
        except Exception as exc:
            self.close()
            raise BrowserUnavailableError(f"Could not start Chromium: {exc}") from exc
        return self

    @property
    def page(self):
        if self._page is None:
            self.start()
        return self._page

    def navigate(self, url: str, wait_until: str = "domcontentloaded") -> BrowserResult:
        """Navigate a JavaScript-capable page and return its current content."""
        if not url.startswith(("http://", "https://", "file://", "data:")):
            raise ValueError("supported URLs must use http(s), file, or data schemes")
        response = self.page.goto(url, wait_until=wait_until)
        return BrowserResult(
            status=response.status if response else 0,
            title=self.page.title(),
            url=self.page.url,
            html=self.page.content(),
        )

    def open(self, url: str) -> tuple[int, bytes]:
        """Compatibility method returning status and rendered HTML bytes."""
        result = self.navigate(url)
        return result.status, result.html.encode("utf-8")

    def click(self, selector: str) -> None:
        """Click a CSS/text selector in the current page."""
        self.page.locator(selector).click()

    def type(self, selector: str, text: str, clear: bool = True) -> None:
        """Fill a form field without attempting to bypass any challenge."""
        locator = self.page.locator(selector)
        if clear:
            locator.fill(text)
        else:
            locator.press_sequentially(text)

    def screenshot(self, path: str | Path, full_page: bool = True) -> Path:
        """Save a screenshot of the current page."""
        destination = Path(path).expanduser()
        destination.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(destination), full_page=full_page)
        return destination

    def wait_for_human(self, message: str = "Complete any site verification in the browser, then press Enter") -> None:
        """Pause for a human when a CAPTCHA or security check appears."""
        print(f"MANUAL HANDOFF: {message}")
        input()

    def close(self) -> None:
        """Close the context; persistent cookies are written to user_data_dir."""
        try:
            if self._context is not None:
                self._context.close()
        finally:
            self._context = None
            self._page = None
            if self._playwright is not None:
                self._playwright.stop()
            self._playwright = None

    def __enter__(self) -> "BrowserSession":
        return self.start()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
