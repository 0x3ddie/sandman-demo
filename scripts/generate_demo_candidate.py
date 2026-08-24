from __future__ import annotations

import argparse
from pathlib import Path
from typing import Final

BUGGY_CONFIG: Final = '    "ca": ("CAD", 0),'
FIXED_CONFIG: Final = '    "CA": ("CAD", 0),'


def generate_candidate(source_path: Path) -> None:
    source = source_path.read_text(encoding="utf-8")
    occurrences = source.count(BUGGY_CONFIG)
    if occurrences != 1:
        raise ValueError(
            f"demo generator expected exactly one lowercase Canada pricing key; found {occurrences}"
        )
    source_path.write_text(source.replace(BUGGY_CONFIG, FIXED_CONFIG), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the deterministic, explicitly simulated Sandman demo candidate."
    )
    parser.add_argument("source", type=Path, help="storefront source file to patch")
    arguments = parser.parse_args()
    generate_candidate(arguments.source)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
