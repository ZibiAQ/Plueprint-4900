import hashlib
import json
import os
import secrets
from dataclasses import dataclass


def _app_data_dir():
    path = os.path.abspath(os.path.join(os.getcwd(), "data_users"))
    os.makedirs(path, exist_ok=True)
    return path


def _users_file():
    return os.path.join(_app_data_dir(), "users.json")


def _normalize_username(username: str) -> str:
    username = (username or "").strip()
    if not username:
        raise ValueError("Username cannot be empty.")
    if len(username) > 64:
        raise ValueError("Username is too long.")
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")
    if any(ch not in allowed for ch in username):
        raise ValueError("Username can only contain letters, numbers, _ and -.")
    return username


def _pbkdf2_sha256(password: str, salt: bytes, iterations: int = 200_000) -> str:
    if password is None:
        password = ""
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return dk.hex()


@dataclass(frozen=True)
class UserRecord:
    username: str
    salt_hex: str
    pw_hash_hex: str


def load_users() -> dict[str, UserRecord]:
    path = _users_file()
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f) or {}
    users: dict[str, UserRecord] = {}
    for username, rec in raw.get("users", {}).items():
        if not isinstance(rec, dict):
            continue
        salt_hex = rec.get("salt_hex", "")
        pw_hash_hex = rec.get("pw_hash_hex", "")
        if not salt_hex or not pw_hash_hex:
            continue
        users[username] = UserRecord(username=username, salt_hex=salt_hex, pw_hash_hex=pw_hash_hex)
    return users


def save_users(users: dict[str, UserRecord]) -> None:
    path = _users_file()
    payload = {
        "schema_version": 1,
        "users": {
            u: {"salt_hex": r.salt_hex, "pw_hash_hex": r.pw_hash_hex}
            for u, r in sorted(users.items(), key=lambda kv: kv[0].lower())
        },
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)


def create_user(username: str, password: str) -> None:
    username = _normalize_username(username)
    users = load_users()
    if username in users:
        raise ValueError("User already exists.")
    if not password:
        raise ValueError("Password cannot be empty.")
    salt = secrets.token_bytes(16)
    pw_hash_hex = _pbkdf2_sha256(password, salt)
    users[username] = UserRecord(username=username, salt_hex=salt.hex(), pw_hash_hex=pw_hash_hex)
    save_users(users)


def verify_login(username: str, password: str) -> bool:
    username = (username or "").strip()
    users = load_users()
    rec = users.get(username)
    if rec is None:
        return False
    salt = bytes.fromhex(rec.salt_hex)
    return _pbkdf2_sha256(password, salt) == rec.pw_hash_hex


def reset_password(username: str, new_password: str) -> None:
    username = _normalize_username(username)
    if not new_password:
        raise ValueError("Password cannot be empty.")
    users = load_users()
    if username not in users:
        raise ValueError("User does not exist.")
    salt = secrets.token_bytes(16)
    pw_hash_hex = _pbkdf2_sha256(new_password, salt)
    users[username] = UserRecord(username=username, salt_hex=salt.hex(), pw_hash_hex=pw_hash_hex)
    save_users(users)


def user_data_file(username: str) -> str:
    username = _normalize_username(username)
    user_dir = os.path.join(_app_data_dir(), username)
    os.makedirs(user_dir, exist_ok=True)
    return os.path.join(user_dir, "data.json")

