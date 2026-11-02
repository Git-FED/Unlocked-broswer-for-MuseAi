#!/usr/bin/env python3
"""Run an authorized HTTP smoke test or a Playwright Chromium session."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.core.browser import BrowserSession
from src.network.fetch import fetch
from src.network.proxy import ProxyPool
from src.stealth.fingerprint import default_profile
from src.ui.sidebar import show_status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--proxy", action="append", default=[])
    parser.add_argument("--browser", action="store_true", help="Use JavaScript-capable Chromium via Playwright")
    parser.add_argument("--headed", action="store_true", help="Show the Chromium window in browser mode")
    parser.add_argument("--profile-dir", default=".browser-data", help="Persistent cookie/session directory")
    parser.add_argument("--click", help="CSS selector to click after navigation")
    parser.add_argument("--type", dest="type_spec", help="Fill a field as SELECTOR=TEXT after navigation")
    parser.add_argument("--screenshot", help="Save a full-page PNG screenshot")
    parser.add_argument("--wait-for-human", action="store_true", help="Pause for a human CAPTCHA/security-check handoff")
    args = parser.parse_args()

    if not args.browser:
        status, body = fetch(args.url, default_profile().user_agent, proxy=ProxyPool(args.proxy).next())
        show_status(args.url, status, len(body))
        return 0

    with BrowserSession(
        proxies=ProxyPool(args.proxy),
        user_data_dir=Path(args.profile_dir),
        headless=not args.headed,
    ) as session:
        result = session.navigate(args.url)
        if args.type_spec:
            selector, separator, text = args.type_spec.partition("=")
            if not separator or not selector:
                parser.error("--type must be formatted as SELECTOR=TEXT")
            session.type(selector, text)
        if args.click:
            session.click(args.click)
        if args.wait_for_human:
            session.wait_for_human()
        if args.screenshot:
            session.screenshot(args.screenshot)
        show_status(result.url, result.status, len(result.html.encode("utf-8")))
        print(f"Title: {result.title}")
        print(f"Persistent profile: {Path(args.profile_dir).expanduser()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
