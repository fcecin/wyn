#!/usr/bin/env bash
# WYN installer. Requires Python 3; no third-party Python packages.
set -euo pipefail
WYN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
exec python3 "$WYN_ROOT/skills/wyn/scripts/install.py" "$@"
