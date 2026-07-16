#!/usr/bin/env bash

set -e

INSTALL_DIR="$HOME/.local/bin"
TARGET="$INSTALL_DIR/tmail"
SOURCE="./tmail.py"

echo "Installing tmail..."

if [ ! -f "$SOURCE" ]; then
  echo "Error: $SOURCE not found in current directory"
  exit 1
fi

mkdir -p "$INSTALL_DIR"
cp "$SOURCE" "$TARGET"
chmod +x "$TARGET"

echo "Installed to $TARGET"

SHELL_RC=""

if [ -n "$ZSH_VERSION" ]; then
  SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
  SHELL_RC="$HOME/.bashrc"
else
  SHELL_RC="$HOME/.profile"
fi

PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'

if ! grep -qF "$PATH_LINE" "$SHELL_RC" 2>/dev/null; then
  echo "" >> "$SHELL_RC"
  echo "# Added by tmail installer" >> "$SHELL_RC"
  echo "$PATH_LINE" >> "$SHELL_RC"
  echo "Updated PATH in $SHELL_RC"
else
  echo "PATH already configured in $SHELL_RC"
fi

echo ""
echo "Done."
echo "Restart your shell or run: source $SHELL_RC"
echo "Then you can use: tmail config | tmail send"
