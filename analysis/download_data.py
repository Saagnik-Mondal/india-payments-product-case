"""Download PhonePe's open Pulse dataset (JSON files) into ./data/pulse.

Dataset: https://github.com/PhonePe/pulse, licensed CDLA-Permissive-2.0. It holds anonymised,
aggregated data on payments in India (transactions, registered users, registered merchants) by
state and district, per quarter. The raw files are not stored in this repo.
"""

from __future__ import annotations

import io
import urllib.request
import zipfile
from pathlib import Path

URL = "https://codeload.github.com/PhonePe/pulse/zip/refs/heads/main"


def main(dest: Path = Path("data/pulse")) -> None:
    if (dest / "aggregated").exists():
        print("Pulse data already present in", dest)
        return
    print("Downloading PhonePe Pulse (about 50 MB) ...")
    with urllib.request.urlopen(URL, timeout=180) as resp:  # noqa: S310 (fixed https URL)
        blob = resp.read()
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        for member in zf.namelist():
            marker = "/data/"
            if marker in member and not member.endswith("/"):
                target = dest / member.split(marker, 1)[1]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zf.read(member))
    print("Data ready in", dest.resolve())


if __name__ == "__main__":
    main()
