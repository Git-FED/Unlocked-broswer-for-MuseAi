#!/usr/bin/env python3
"""Run a single authorized smoke-test request."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.core.browser import BrowserSession
from src.network.proxy import ProxyPool
from src.ui.sidebar import show_status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--proxy", action="append", default=[])
    args = parser.parse_args()
    status, body = BrowserSession(proxies=ProxyPool(args.proxy)).open(args.url)
    show_status(args.url, status, len(body))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
