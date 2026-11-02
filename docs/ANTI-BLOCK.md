# Responsible automation guidance

The original project concept mentioned “anti-block” behavior. This repository intentionally narrows that concept to reliable, polite automation in environments where you have permission.

## Allowed practices

- Use documented APIs when available.
- Identify your client honestly with a descriptive User-Agent.
- Keep a stable client profile during a session so tests are reproducible.
- Apply conservative delays, bounded retries, and exponential backoff.
- Stop on `401`, `403`, repeated `429`, or explicit opt-out signals.
- Use proxies only when they are owned, authorized, and configured for the test.
- Keep credentials and proxy URLs out of source control.

## Do not implement

- CAPTCHA solving or CAPTCHA bypass.
- Browser fingerprint spoofing intended to impersonate users.
- Header, cookie, or TLS tricks intended to defeat bot detection.
- Proxy scraping, residential proxy abuse, or IP-ban evasion.
- Credential stuffing, scraping private data, or bypassing authentication.

## Operational checklist

1. Confirm written authorization and scope.
2. Prefer a staging environment or a supplied test endpoint.
3. Set a low request rate and a clear stop condition.
4. Log request outcomes without storing sensitive payloads.
5. Remove secrets from logs and commit history.
6. Stop immediately when the owner asks you to stop.
