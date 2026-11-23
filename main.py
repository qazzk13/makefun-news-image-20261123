"""Write the 23 November 2026 world-news image to the output directory.

The image is bundled in this repository as ``entry.jpg``. It is a
1024x1024 JPEG (249,925 bytes) that sums up Monday 23 November 2026:
the COP31 climate talks in Antalya collapsing with no deal, oil
tankers hit in the Strait of Hormuz, a deadly factory fire in
Indonesia, and a magnitude 6.7 earthquake in Peru.

This program copies the bundled image byte-for-byte to
``<output>/entry.png`` (the name stays ``entry.png`` even though the
bytes are JPEG, as the bounty rules allow), as required by the make.fun
news-image-20261123 bounty. It uses only the standard library and
makes no network calls, so repeated runs produce identical output.
Before writing, it validates the bundled file: JPEG magic bytes, the
1 MiB size cap, and the expected SHA-256, so a corrupted bundle fails
loudly instead of shipping a bad entry.
"""

import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.jpg")
EXPECTED_SHA256 = "9706f65cb84a3bef2d0c0165e4b86867b983a73ade87f3c0287031be094ba9af"
MAX_BYTES = 1_048_576
JPEG_MAGIC = b"\xff\xd8\xff"


def _validate(data: bytes) -> None:
    """Fail loudly if the bundled image is not the expected JPEG."""
    if not data.startswith(JPEG_MAGIC):
        raise SystemExit("entry.jpg is not a JPEG (bad magic bytes)")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.jpg is {len(data)} bytes, over the 1 MiB cap")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"entry.jpg sha256 mismatch: {digest}")


def main() -> int:
    with open(SOURCE, "rb") as fh:
        data = fh.read()
    _validate(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(data)
    written = open(dest, "rb").read()
    assert written == data, "output differs from the bundled image"
    print(f"wrote {dest} ({len(data)} bytes, sha256 {EXPECTED_SHA256})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
