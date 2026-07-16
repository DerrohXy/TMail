#!/usr/bin/env bash

set -e

INSTALL_DIR="$HOME/.local/bin"
TARGET="$INSTALL_DIR/tmail"

echo "Uninstalling tmail..."

if [[ -f "$TARGET" ]]; then
  rm "$TARGET"
  echo "tmail uninstalled."
else
  echo "tmail installation not found."
fi
