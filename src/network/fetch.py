"""Small, bounded HTTP client for authorized smoke tests."""

from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener


class FetchError(RuntimeError):
    pass


def fetch(url: str, user_agent: str, proxy: str | None = None, timeout: float = 10.0) -> tuple[int, bytes]:
    """Fetch a URL once; callers should add their own rate limits and stop rules."""
    if not url.startswith(("http://", "https://")):
        raise ValueError("only HTTP(S) URLs are supported")
    handlers = [ProxyHandler({"http": proxy, "https": proxy})] if proxy else []
    opener = build_opener(*handlers)
    request = Request(url, headers={"User-Agent": user_agent})
    try:
        with opener.open(request, timeout=timeout) as response:
            return response.status, response.read()
    except (HTTPError, URLError, TimeoutError) as exc:
        raise FetchError(str(exc)) from exc
