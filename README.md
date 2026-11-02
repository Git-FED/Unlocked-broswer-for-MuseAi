# Unblocked Browser

A small, authorization-first browser automation skeleton for testing websites you own or are explicitly permitted to assess.

> This project does not attempt to defeat CAPTCHAs, access controls, rate limits, bot protections, or account security. Do not use it to evade protections or access systems without permission.

## Structure

- `src/core/browser.py` — browser-session abstraction and site profiles
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
- `tests/test_stealth.py` — unit tests
- `docs/ANTI-BLOCK.md` — safety and operating guidance

## Quick start

```bash
python3 scripts/run.py --url https://example.com
python3 -m unittest discover -s tests -v
```

Open `docs/donations.html` in a browser to preview the support page. It uses relative asset and page links, so it can be served from GitHub Pages or Cloudflare Pages without a server-side build. The age confirmation is only an advisory front-end gate; it is not identity or legal-age verification. Payment credentials, provider configuration, and compliance requirements should be managed through the respective payment providers.

The public footer intentionally excludes private Matrix rooms, private channels, personal/internal profiles, and other restricted destinations. Those should be handled behind an appropriate login, age, country, or invite flow rather than exposed in public navigation.

The example uses the standard library only. For production browser automation, integrate an approved browser driver and follow the target site's terms, robots guidance, and API policies.
