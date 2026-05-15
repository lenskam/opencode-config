#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== OpenCode Config Setup ==="
echo ""

cd "$SCRIPT_DIR"

# 1. Init & update submodules
echo "[1/6] Initializing git submodules..."
git submodule init
git submodule update
echo "  OK"

# 2. Setup .env from template if missing
echo "[2/6] Checking .env file..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "  Created .env from .env.example"
else
  echo "  .env already exists"
fi
echo "  OK"

# 3. Install OpenCode plugin deps
echo "[3/6] Installing OpenCode dependencies..."
bun install
echo "  OK"

# 4. Build mcp-image-gen
echo "[4/6] Building mcp-image-gen..."
cd mcp-servers/mcp-image-gen
npm install && npm run build
cd "$SCRIPT_DIR"
echo "  OK"

# 5. Build modelcontextprotocol servers
echo "[5/6] Building modelcontextprotocol servers..."
cd mcp-servers/servers
npm install && npm run build
cd "$SCRIPT_DIR"
echo "  OK"

# 6. Install mcp-servers root deps (puppeteer)
if [ -f mcp-servers/package.json ]; then
  echo "[6/6] Installing mcp-servers root dependencies..."
  cd mcp-servers && npm install && cd "$SCRIPT_DIR"
  echo "  OK"
fi

# ---- .bashrc / .zshrc loader ----
LOADER_LINE='if [ -f ~/.config/opencode/.env ]; then set -a; source ~/.config/opencode/.env; set +a; fi'

detected_rc=""
if [ -f "$HOME/.bashrc" ]; then
  detected_rc="$HOME/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
  detected_rc="$HOME/.zshrc"
fi

if [ -n "$detected_rc" ]; then
  if grep -q "opencode/.env" "$detected_rc" 2>/dev/null; then
    echo ""
    echo "  .env loader already present in $detected_rc"
  else
    {
      echo ""
      echo "# Load OpenCode secrets from .env"
      echo "$LOADER_LINE"
    } >> "$detected_rc"
    echo ""
    echo "  Added .env loader to $detected_rc"
  fi
else
  echo ""
  echo "  WARNING: no .bashrc or .zshrc found."
  echo "  Add this to your shell rc file manually:"
  echo "    $LOADER_LINE"
fi

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "  1. Edit ~/.config/opencode/.env — fill in your real secrets"
echo "  2. Run: source ~/.bashrc"
echo "  3. For Pencil MCP: install High Agency VS Code extension"
echo "     on this machine and update the 'pencil' path in opencode.json"
