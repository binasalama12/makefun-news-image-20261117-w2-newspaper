"""Wallet 2 entry for news-image-20261117: the newspaper front page.

Picture summary: a broadsheet called "The Daily World", dated Tuesday,
November 17, 2026. The banner headline announces Ukraine blowing a span
out of Putin's Crimea bridge. Six columns follow: Iranian drones over
Bahrain, the end of measles-free America, Israel's parliament turning,
Japanese jets scrambling, 146,000 people marching in France, and five
arrests over an Iran-linked assassination plot in Greece.

This publisher treats the picture like a newspaper plate: it checks
that the file ends the way a complete image should end (the IEND chunk
of a PNG, or the EOI marker of a JPEG), copies it in two passes over a
temporary name, and only then gives the output its final name.
"""
import os
import sys

FOLDER = os.path.dirname(os.path.abspath(__file__))
PLATE = os.path.join(FOLDER, "entry.png")
PNG_TRAILER = b"IEND\xaeB`\x82"
JPEG_TRAILER = b"\xff\xd9"


def plate_is_complete(path):
    """True when the file carries a proper image ending."""
    with open(path, "rb") as handle:
        handle.seek(0, os.SEEK_END)
        length = handle.tell()
        handle.seek(max(0, length - 16))
        tail = handle.read()
    return tail.endswith(PNG_TRAILER) or tail.endswith(JPEG_TRAILER)


def run():
    if not plate_is_complete(PLATE):
        raise SystemExit("plate looks truncated: no image ending found")
    out_folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_folder, exist_ok=True)
    final_name = os.path.join(out_folder, "entry.png")
    staging_name = os.path.join(out_folder, "entry.png.part")
    with open(PLATE, "rb") as fin, open(staging_name, "wb") as fout:
        first_half = fin.read(os.path.getsize(PLATE) // 2)
        fout.write(first_half)
        fout.write(fin.read())
    os.replace(staging_name, final_name)
    print(f"two-pass print finished, first pass carried {len(first_half)} bytes")
    plate_size = os.path.getsize(PLATE)
    printed_size = os.path.getsize(final_name)
    if printed_size != plate_size:
        raise SystemExit(f"printed {printed_size} bytes from a {plate_size} plate")
    print(f"front page printed cleanly: {printed_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(run())
