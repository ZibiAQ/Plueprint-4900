import json
import os
import secrets
from dataclasses import dataclass

from .user_store import _normalize_username


def _user_dir(username: str) -> str:
    username = _normalize_username(username)
    base = os.path.abspath(os.path.join(os.getcwd(), "data_users", username))
    os.makedirs(base, exist_ok=True)
    return base


def _datasets_dir(username: str) -> str:
    path = os.path.join(_user_dir(username), "datasets")
    os.makedirs(path, exist_ok=True)
    return path


def _datasets_file(username: str) -> str:
    return os.path.join(_user_dir(username), "datasets.json")


@dataclass(frozen=True)
class DatasetRecord:
    dataset_id: str
    name: str


def _load_raw(username: str) -> dict:
    path = _datasets_file(username)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f) or {}


def _save_raw(username: str, raw: dict) -> None:
    path = _datasets_file(username)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(raw, f, indent=4, ensure_ascii=False)


def ensure_user_datasets(username: str) -> None:
    username = _normalize_username(username)
    _datasets_dir(username)

    raw = _load_raw(username)
    datasets = raw.get("datasets") if isinstance(raw.get("datasets"), list) else None
    current = raw.get("current_dataset_id")

    if not datasets:
        default_id = "default"
        raw = {
            "schema_version": 1,
            "current_dataset_id": default_id,
            "datasets": [{"id": default_id, "name": "Default"}],
        }
        _save_raw(username, raw)
        current = default_id

    # move old per-user data into the default dataset once
    legacy_path = os.path.join(_user_dir(username), "data.json")
    default_path = dataset_data_file(username, current or "default")
    if os.path.exists(legacy_path) and not os.path.exists(default_path):
        os.makedirs(os.path.dirname(default_path), exist_ok=True)
        try:
            os.replace(legacy_path, default_path)
        except Exception:
            import shutil

            shutil.copy2(legacy_path, default_path)

    # ensure the current dataset has a usable data.json
    current_id = (current or raw.get("current_dataset_id") or "default").strip() or "default"
    current_path = dataset_data_file(username, current_id)
    os.makedirs(os.path.dirname(current_path), exist_ok=True)
    if not os.path.exists(current_path):
        with open(current_path, "w", encoding="utf-8") as f:
            json.dump({"members": [], "tasks": []}, f, indent=4, ensure_ascii=False)


def list_datasets(username: str) -> list[DatasetRecord]:
    ensure_user_datasets(username)
    raw = _load_raw(username)
    out: list[DatasetRecord] = []
    for item in raw.get("datasets", []):
        if not isinstance(item, dict):
            continue
        did = (item.get("id") or "").strip()
        name = (item.get("name") or "").strip()
        if did and name:
            out.append(DatasetRecord(dataset_id=did, name=name))
    return out


def get_current_dataset_id(username: str) -> str:
    ensure_user_datasets(username)
    raw = _load_raw(username)
    did = (raw.get("current_dataset_id") or "").strip()
    if did:
        return did
    ds = list_datasets(username)
    return ds[0].dataset_id


def set_current_dataset(username: str, dataset_id: str) -> None:
    ensure_user_datasets(username)
    raw = _load_raw(username)
    dataset_id = (dataset_id or "").strip()
    ids = {d.dataset_id for d in list_datasets(username)}
    if dataset_id not in ids:
        raise ValueError("Dataset not found.")
    raw["current_dataset_id"] = dataset_id
    _save_raw(username, raw)


def create_dataset(username: str, name: str) -> DatasetRecord:
    ensure_user_datasets(username)
    name = (name or "").strip()
    if not name:
        raise ValueError("Dataset name cannot be empty.")
    if len(name) > 64:
        raise ValueError("Dataset name is too long.")
    existing = list_datasets(username)
    if any(d.name.lower() == name.lower() for d in existing):
        raise ValueError("A dataset with the same name already exists.")

    dataset_id = secrets.token_hex(8)
    raw = _load_raw(username)
    raw.setdefault("datasets", [])
    raw["datasets"].append({"id": dataset_id, "name": name})
    raw["current_dataset_id"] = dataset_id
    _save_raw(username, raw)

    path = dataset_data_file(username, dataset_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"members": [], "tasks": []}, f, indent=4, ensure_ascii=False)

    return DatasetRecord(dataset_id=dataset_id, name=name)


def rename_dataset(username: str, dataset_id: str, new_name: str) -> None:
    ensure_user_datasets(username)
    dataset_id = (dataset_id or "").strip()
    new_name = (new_name or "").strip()
    if not new_name:
        raise ValueError("Dataset name cannot be empty.")
    raw = _load_raw(username)
    datasets = raw.get("datasets", [])
    if any(
        isinstance(d, dict)
        and (d.get("name") or "").strip().lower() == new_name.lower()
        and (d.get("id") or "").strip() != dataset_id
        for d in datasets
    ):
        raise ValueError("A dataset with the same name already exists.")
    found = False
    for d in datasets:
        if isinstance(d, dict) and (d.get("id") or "").strip() == dataset_id:
            d["name"] = new_name
            found = True
            break
    if not found:
        raise ValueError("Dataset not found.")
    _save_raw(username, raw)


def delete_dataset(username: str, dataset_id: str) -> None:
    ensure_user_datasets(username)
    dataset_id = (dataset_id or "").strip()
    raw = _load_raw(username)
    datasets = [d for d in raw.get("datasets", []) if isinstance(d, dict)]
    if len(datasets) <= 1:
        raise ValueError("Cannot delete the last dataset.")

    if not any((d.get("id") or "").strip() == dataset_id for d in datasets):
        raise ValueError("Dataset not found.")

    raw["datasets"] = [d for d in datasets if (d.get("id") or "").strip() != dataset_id]
    if (raw.get("current_dataset_id") or "").strip() == dataset_id:
        raw["current_dataset_id"] = (raw["datasets"][0].get("id") or "").strip()
    _save_raw(username, raw)

    path = dataset_data_file(username, dataset_id)
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def dataset_data_file(username: str, dataset_id: str) -> str:
    username = _normalize_username(username)
    dataset_id = (dataset_id or "").strip()
    if not dataset_id:
        raise ValueError("Dataset id cannot be empty.")
    return os.path.join(_datasets_dir(username), dataset_id, "data.json")


def dataset_name(username: str, dataset_id: str) -> str:
    for d in list_datasets(username):
        if d.dataset_id == dataset_id:
            return d.name
    raise ValueError("Dataset not found.")

