# Unblocked Browser

A small, authorization-first browser automation skeleton for testing websites you own or are explicitly permitted to assess. It now includes a real Playwright Chromium engine alongside the lightweight HTTP fetcher.

> This project does not attempt to defeat CAPTCHAs, access controls, rate limits, bot protections, or account security. Do not use it to evade protections or access systems without permission.

## Structure

- `src/core/browser.py` — real Chromium engine with JavaScript, persistent cookies, clicks, typing, screenshots, and human handoff
- `src/network/fetch.py` — bounded HTTP fetching with retries
- `src/network/proxy.py` — explicit, user-supplied proxy rotation for test environments
- `src/stealth/fingerprint.py` — stable, transparent client profile metadata
- `src/stealth/human.py` — conservative pacing helpers for polite automation
- `src/ui/sidebar.py` — minimal CLI status view
- `docs/donations.html` — separated, age-gated support and donation cards
- `docs/thank-you.html` and `docs/leave.html` — local HTML destinations for redirects
- `docs/community-invite.html` — standalone FedPromptly community invite widget
- `docs/assets/` — favicon and clean PNG promotion assets
- Public FED-OS footer links — ecosystem, membership, storefront, contact, media, and support destinations
- `scripts/run.py` — example entry point
- `requirements.txt` — Playwright dependency
- `.gitignore` — excludes persistent sessions and local artifacts
- `tests/test_stealth.py` — unit tests
- `docs/ANTI-BLOCK.md` — safety and operating guidance

## Quick start

```bash
# Lightweight HTTP mode
python3 scripts/run.py --url https://example.com

# Install the browser dependency and Chromium
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium

# Real JavaScript-capable Chromium mode
python3 scripts/run.py --browser --headed --url https://example.com

# Interact with a page and save a screenshot
python3 scripts/run.py --browser --headed \
  --url https://example.com \
  --type 'input[name=q]=example' \
  --click 'button[type=submit]' \
  --screenshot artifacts/example.png

python3 -m unittest discover -s tests -v
```

Browser mode uses a persistent `.browser-data/` profile by default. Cookies, local storage, and other session state survive across runs; the directory is ignored by Git and must never be committed or shared. Use `--profile-dir` to select a separate profile for an authorized test account.

When a site presents a CAPTCHA or Google/security verification, use `--headed --wait-for-human`. The script pauses so a human can complete the check in the visible Chromium window. It does not solve, bypass, or automate those checks.

Open `docs/donations.html` in a browser to preview the support page. It uses relative asset and page links, so it can be served from GitHub Pages or Cloudflare Pages without a server-side build. The age confirmation is only an advisory front-end gate; it is not identity or legal-age verification. Payment credentials, provider configuration, and compliance requirements should be managed through the respective payment providers.

The public footer intentionally excludes private Matrix rooms, private channels, personal/internal profiles, and other restricted destinations. Those should be handled behind an appropriate login, age, country, or invite flow rather than exposed in public navigation.

The lightweight HTTP mode uses only the standard library. Browser mode requires Playwright and its Chromium install. Always follow the target site's terms, robots guidance, rate limits, and API policies.
