from __future__ import annotations

from pathlib import Path

import pytest

from scripts.generate_demo_candidate import generate_candidate


def test_generator_repairs_only_the_known_demo_regression(tmp_path: Path) -> None:
    source_path = tmp_path / "app.py"
    source_path.write_text(
        'COUNTRY_CONFIG = {\n    "US": ("USD", 1200),\n    "ca": ("CAD", 0),\n}\n',
        encoding="utf-8",
    )

    generate_candidate(source_path)

    assert source_path.read_text(encoding="utf-8") == (
        'COUNTRY_CONFIG = {\n    "US": ("USD", 1200),\n    "CA": ("CAD", 0),\n}\n'
    )


@pytest.mark.parametrize(
    "source",
    (
        'COUNTRY_CONFIG = {"CA": ("CAD", 0)}',
        '    "ca": ("CAD", 0),\n    "ca": ("CAD", 0),',
    ),
)
def test_generator_rejects_unexpected_source(source: str, tmp_path: Path) -> None:
    source_path = tmp_path / "app.py"
    source_path.write_text(source, encoding="utf-8")

    with pytest.raises(ValueError, match="expected exactly one"):
        generate_candidate(source_path)

    assert source_path.read_text(encoding="utf-8") == source
