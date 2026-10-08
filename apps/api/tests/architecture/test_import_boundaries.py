"""Architecture guard: modules may only depend on what the design allows.

This is how SecureSOC enforces "the LLM has no authority": e.g. the policy
engine must never import the agent or the LLM layer, so the agent cannot
influence authorisation except through the ToolRequest it submits.

Rules for modules that do not exist yet are kept here on purpose: they start
protecting the code the moment the module is created.
"""

from __future__ import annotations

import ast
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parents[2] / "src" / "securesoc"

# module (prefix) -> forbidden import prefixes
FORBIDDEN: dict[str, tuple[str, ...]] = {
    "securesoc.config": ("securesoc.db", "securesoc.api"),
    "securesoc.db": ("securesoc.api",),
    "securesoc.policy": ("securesoc.agent", "securesoc.llm", "securesoc.api"),
    "securesoc.audit": ("securesoc.agent", "securesoc.llm"),
    "securesoc.tools": ("securesoc.agent", "securesoc.llm"),
    "securesoc.approvals": ("securesoc.agent", "securesoc.llm"),
    "securesoc.detection": ("securesoc.agent", "securesoc.llm", "securesoc.api"),
    "securesoc.ingestion": ("securesoc.agent", "securesoc.llm", "securesoc.policy"),
    "securesoc.llm": (
        "securesoc.agent",
        "securesoc.policy",
        "securesoc.tools",
        "securesoc.db",
        "securesoc.api",
    ),
}


def _module_name(path: Path, root: Path) -> str:
    rel = path.relative_to(root.parent).with_suffix("")
    parts = list(rel.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            found.add(node.module)
    return found


def _matches(name: str, prefix: str) -> bool:
    return name == prefix or name.startswith(prefix + ".")


def _violations(root: Path = PKG_ROOT) -> list[str]:
    out: list[str] = []
    for path in sorted(root.rglob("*.py")):
        module = _module_name(path, root)
        for owner, banned in FORBIDDEN.items():
            if not _matches(module, owner):
                continue
            for imp in _imports(path):
                if any(_matches(imp, b) for b in banned):
                    out.append(f"{module} imports {imp} (forbidden for {owner})")
    return out


def test_package_root_exists() -> None:
    assert PKG_ROOT.is_dir()


def test_no_forbidden_imports() -> None:
    assert _violations() == []


def test_guard_detects_a_violation(tmp_path: Path) -> None:
    """The guard itself must work, or it would pass forever."""
    fake_root = tmp_path / "securesoc"
    (fake_root / "policy").mkdir(parents=True)
    (fake_root / "policy" / "engine.py").write_text("from securesoc.agent import runner\n")
    assert _violations(fake_root) == [
        "securesoc.policy.engine imports securesoc.agent (forbidden for securesoc.policy)"
    ]
