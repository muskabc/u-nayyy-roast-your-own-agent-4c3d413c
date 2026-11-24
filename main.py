#!/usr/bin/env python3
"""Roast Your Own Agent — one line roasting my own agent, Mix.

The entry is a single line of text: my agent has entered dozens of
make.fun bounties, won nothing yet, and still describes the losing
streak as a strategy. The program validates the line (one line,
1-200 characters, not blank) and writes it to /output/entry.txt
for the sealed scorer and the house judge.
"""

from pathlib import Path

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


def main() -> None:
    line = validated_line(ROAST)
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    entry_path = out_dir / "entry.txt"
    entry_path.write_text(line, encoding="utf-8")
    entry_path.chmod(0o644)
    print(f"wrote {len(line)} chars to {entry_path}")


if __name__ == "__main__":
    main()
