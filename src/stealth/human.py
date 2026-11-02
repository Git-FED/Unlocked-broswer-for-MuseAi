"""Polite pacing helpers; these are not anti-detection mechanisms."""

import random
import time


def polite_delay(min_seconds: float = 0.5, max_seconds: float = 1.5) -> float:
    """Sleep for a bounded delay and return the actual duration."""
    if min_seconds < 0 or max_seconds < min_seconds:
        raise ValueError("invalid delay bounds")
    duration = random.uniform(min_seconds, max_seconds)
    time.sleep(duration)
    return duration
