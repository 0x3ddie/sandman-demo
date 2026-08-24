from pathlib import Path


def test_incident_workflow_supports_one_click_and_modal_fallback() -> None:
    workflow = Path(".github/workflows/sandman.yml").read_text(encoding="utf-8")

    assert "workflow_dispatch:" in workflow
    assert "Open or reuse the demo incident pull request" in workflow
    assert "Generate bounded candidate with Codex" in workflow
    assert "Run three real Modal Sandbox probes" in workflow
    assert "Run deterministic three-lane demo verification" in workflow
    assert "openai/codex-action@86365089eb2b84e0a8fb0717b304f8bdcb13b20e" in workflow
    assert "--ignore-rules" not in workflow

    notify = workflow.split("\n  notify:\n", maxsplit=1)[1]
    assert "permissions:\n      issues: write\n      pull-requests: write" in notify
