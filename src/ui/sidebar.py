"""Minimal terminal status output."""


def show_status(url: str, status: int, size: int) -> None:
    print(f"URL: {url}\nHTTP status: {status}\nBytes: {size}")
