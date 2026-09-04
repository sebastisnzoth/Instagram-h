from pathlib import Path

from safe_audit import run_audit


def test_pass_found(tmp_path: Path):
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("alpha\nsecret123\nomega\n", encoding="utf-8")

    result = run_audit(
        target_password="secret123",
        passlist_path=str(wordlist),
        username="demo",
        delay=0.0,
        enabled=False,
    )

    assert result == 0


def test_pass_not_found(tmp_path: Path):
    wordlist = tmp_path / "words.txt"
    wordlist.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")

    result = run_audit(
        target_password="missing",
        passlist_path=str(wordlist),
        username="demo",
        delay=0.0,
        enabled=False,
    )

    assert result == 1


def test_missing_wordlist(tmp_path: Path):
    result = run_audit(
        target_password="anything",
        passlist_path=str(tmp_path / "missing.txt"),
        username="demo",
        delay=0.0,
        enabled=False,
    )

    assert result == 2
