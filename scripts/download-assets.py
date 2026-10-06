#!/usr/bin/env python3
"""Download pinned upstream assets and verify SHA-256 before installation."""
import hashlib
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
assets = json.loads((ROOT / "scripts/assets.json").read_text())
for asset in assets:
    target = ROOT / asset["path"]
    if target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest() == asset["sha256"]:
        print("Verified:", asset["path"])
        continue
    print("Downloading:", asset["url"])
    request = urllib.request.Request(asset["url"], headers={"User-Agent": "shuibowen-asset-setup/1"})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != asset["sha256"]:
        raise SystemExit("SHA-256 mismatch: " + asset["path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(target)
    print("Installed:", asset["path"])
print("All runtime assets are ready.")
