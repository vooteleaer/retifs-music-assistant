#!/bin/sh
# Builds retifsd, retifs and retifs-extractd for Linux x86_64 from ../retifs
# (next to this repo) into dev/retifs/bin. Run on Linux (or in WSL).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
RETIFS=$(cd "$HERE/../../retifs" && pwd)
export CARGO_TARGET_DIR=${CARGO_TARGET_DIR:-$HOME/retifs-target-rel}
cargo build --release --manifest-path "$RETIFS/Cargo.toml" -p retifs-node -p retifs-extract
mkdir -p "$HERE/retifs/bin"
for f in retifsd retifs retifs-extractd; do cp "$CARGO_TARGET_DIR/release/$f" "$HERE/retifs/bin/"; done
ls -la "$HERE/retifs/bin"
