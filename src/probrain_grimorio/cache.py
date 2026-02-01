from __future__ import annotations

import copy
import time
from typing import Any, Dict, Optional, Tuple


def _now_s() -> float:
    return time.time()


class TTLCache:
    # COST: cache reduz repetição de GET e custo de execução
    def __init__(self):
        self._store: Dict[str, Tuple[float, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        item = self._store.get(key)
        if not item:
            return None
        expires_at, value = item
        if _now_s() >= expires_at:
            self._store.pop(key, None)
            return None
        return copy.deepcopy(value)

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        expires_at = _now_s() + ttl_seconds
        self._store[key] = (expires_at, copy.deepcopy(value))

    def invalidate_prefix(self, prefix: str) -> None:
        keys = list(self._store.keys())
        for k in keys:
            if k.startswith(prefix):
                self._store.pop(k, None)

    def clear(self) -> None:
        self._store.clear()


CACHE = TTLCache()


class FixedWindowRateLimiter:
    # COST: rate limit simples para reduzir abuso e custos
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._buckets: Dict[str, Tuple[int, float]] = {}

    def allow(self, client_id: str) -> bool:
        now = _now_s()
        count, window_start = self._buckets.get(client_id, (0, now))

        if now - window_start >= self.window_seconds:
            count, window_start = 0, now

        if count >= self.max_requests:
            self._buckets[client_id] = (count, window_start)
            return False

        self._buckets[client_id] = (count + 1, window_start)
        return True

    def reset(self) -> None:
        self._buckets.clear()


RATE_LIMITER = FixedWindowRateLimiter(max_requests=60, window_seconds=60)
