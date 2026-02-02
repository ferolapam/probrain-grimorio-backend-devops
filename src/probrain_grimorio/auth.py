from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class AuthClaims:
    sub: str
    role: str


def verify_bearer_token(
    authorization_header: Optional[str],
) -> Tuple[bool, Optional[AuthClaims], str]:
    # SEC: validação fake no formato "Bearer valid:<sub>:<role>"
    if not authorization_header:
        return False, None, "missing_authorization"

    parts = authorization_header.split(" ", 1)
    if len(parts) != 2 or parts[0] != "Bearer":
        return False, None, "invalid_authorization_format"

    token = parts[1].strip()
    if not token.startswith("valid:"):
        return False, None, "invalid_token"

    pieces = token.split(":")
    if len(pieces) != 3:
        return False, None, "invalid_token_shape"

    _, sub, role = pieces
    if role not in {"reader", "writer", "admin"}:
        return False, None, "invalid_role"

    return True, AuthClaims(sub=sub, role=role), "ok"
