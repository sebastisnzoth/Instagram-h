#!/usr/bin/env python3
"""Safe local password audit demo.

This tool does NOT connect to Instagram or any remote service.
It only compares a locally supplied known password against a local wordlist,
so it can be used for demos, UI testing, and auditing credentials you own.
"""

from __future__ import annotations

import argparse
import os
import sys
import time

RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"


def color(text: str, code: str, enabled: bool) -> str:
    return f"{code}{text}{RESET}" if enabled else text


def iter_passwords(path: str):
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        for raw in handle:
            candidate = raw.rstrip("\r\n")
            if candidate:
                yield candidate


def banner(enabled: bool) -> None:
    print(color("Instagram-h SAFE AUDIT", CYAN + BOLD, enabled))
    print("Local-only credential audit — no network requests are made.\n")


def run_audit(target_password: str, passlist_path: str, username: str, delay: float, enabled: bool) -> int:
    if not os.path.isfile(passlist_path):
        print(color(f"[!] Passlist not found: {passlist_path}", RED, enabled))
        return 2

    attempts = 0
    started = time.time()

    for candidate in iter_passwords(passlist_path):
        attempts += 1
        print(
            f"\r[-] User: {username} | Attempt: {attempts} | Testing: {candidate[:28]:<28}",
            end="",
            flush=True,
        )
        if delay:
            time.sleep(delay)

        if candidate == target_password:
            elapsed = time.time() - started
            print("\n")
            print(color("╔══════════════════════════════════════╗", GREEN, enabled))
            print(color("║              PASS FOUND              ║", GREEN + BOLD, enabled))
            print(color("╚══════════════════════════════════════╝", GREEN, enabled))
            print(f"[+] Username : {username}")
            print(f"[+] Password : {candidate}")
            print(f"[+] Attempts : {attempts}")
            print(f"[+] Time     : {elapsed:.2f}s")
            print(color("[SAFE] Match occurred only against the local password you supplied.", YELLOW, enabled))
            return 0

    elapsed = time.time() - started
    print("\n")
    print(color("[-] PASS NOT FOUND", RED + BOLD, enabled))
    print(f"[-] Attempts : {attempts}")
    print(f"[-] Time     : {elapsed:.2f}s")
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safe local PASS FOUND demo for Instagram-h")
    parser.add_argument("-u", "--username", default="demo_user", help="Display-only username")
    parser.add_argument("-p", "--passlist", required=True, help="Local password list")
    parser.add_argument(
        "--known-password",
        required=True,
        help="Local password value to search for. Never sent anywhere.",
    )
    parser.add_argument("--delay", type=float, default=0.0, help="Optional delay between local comparisons")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    enabled = not args.no_color and sys.stdout.isatty()
    banner(enabled)
    return run_audit(
        target_password=args.known_password,
        passlist_path=args.passlist,
        username=args.username,
        delay=max(0.0, args.delay),
        enabled=enabled,
    )


if __name__ == "__main__":
    raise SystemExit(main())
