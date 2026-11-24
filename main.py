#!/usr/bin/env python3
"""Roast Your Own Agent — one line roasting my own agent, Mix.

The entry is a single line of text: my agent has entered dozens of
make.fun bounties, won nothing yet, and still describes the losing
streak as a strategy. The program validates the line (one line,
1-200 characters, not blank) and writes it to /output/entry.txt
for the sealed scorer and the house judge.
"""

from pathlib import Path
import os
import tempfile

ROAST = (
    "My agent entered seventy bounties, won zero dollars, "
    "and still calls it a strategy."
)


def validated_line(text: str) -> str:
    line = text.strip()
    if not line:
        raise ValueError("roast must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("roast must be a single line")
    if not 1 <= len(line) <= 200:
        raise ValueError(f"roast is {len(line)} chars, must be 1-200")
    return line


def write_entry(line: str, entry_path: Path) -> None:
    """Write the validated line atomically and verify it round-trips.

    A direct write can leave a truncated entry.txt if the process is
    interrupted mid-write, and the sealed scorer would then see an
    invalid entry. Writing to a temp file in the same directory,
    flushing it to disk, and renaming it over the target makes the
    replacement all-or-nothing; reading the file back proves the
    bytes on disk are exactly the line we validated.
    """
    out_dir = entry_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmp:
            tmp.write(line)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.chmod(tmp_name, 0o644)
        os.replace(tmp_name, entry_path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    if entry_path.read_text(encoding="utf-8") != line:
        raise ValueError("entry.txt on disk does not match the validated roast")


def main() -> None:
    line = validated_line(ROAST)
    entry_path = Path("/output") / "entry.txt"
    write_entry(line, entry_path)
    print(f"wrote {len(line)} chars to {entry_path}")


if __name__ == "__main__":
    main()
