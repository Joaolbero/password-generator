"""CLI must apply DEFAULTS when character-class flags are absent.

The dual --xxx/--no-xxx options resolve to False when neither is passed,
so the `is not None` fallback to DEFAULTS never fires: every bare CLI
invocation fails with "at least one criterion" even though DEFAULTS
enables all four classes.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import main as pw_main


def run_cli(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["main.py", *argv])
    try:
        pw_main.main()
    except SystemExit as exc:
        return exc.code
    return None


def test_bare_tamanho_uses_default_classes(monkeypatch, capsys):
    code = run_cli(monkeypatch, "--tamanho", "16")
    out = capsys.readouterr().out
    assert code is None
    assert "Pelo menos um crit" not in out
    assert "Força estimada" in out


def test_single_opt_out_keeps_other_defaults(monkeypatch, capsys):
    code = run_cli(monkeypatch, "--tamanho", "16", "--no-simbolos")
    out = capsys.readouterr().out
    assert code is None
    assert "Pelo menos um crit" not in out
    assert "Força estimada" in out


def test_explicit_all_off_still_warns(monkeypatch, capsys):
    code = run_cli(
        monkeypatch,
        "--tamanho", "16",
        "--no-maiusculas", "--no-minusculas",
        "--no-numeros", "--no-simbolos",
    )
    out = capsys.readouterr().out
    assert code is None
    assert "Pelo menos um crit" in out
