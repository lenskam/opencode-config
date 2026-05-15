#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== OpenCode Config Setup ==="
echo ""

cd "$SCRIPT_DIR"

# 1. Init & update submodules
echo "[1/5] Initializing git submodules..."
git submodule init
git submodule update
echo "  OK"

# 2. Install OpenCode plugin deps
echo "[2/5] Installing OpenCode dependencies..."
bun install
echo "  OK"

# 3. Build mcp-image-gen
echo "[3/5] Building mcp-image-gen..."
cd mcp-servers/mcp-image-gen
npm install && npm run build
cd "$SCRIPT_DIR"
echo "  OK"

# 4. Build modelcontextprotocol servers (sequential-thinking etc.)
echo "[4/5] Building modelcontextprotocol servers..."
cd mcp-servers/servers
npm install && npm run build
cd "$SCRIPT_DIR"
echo "  OK"

# 5. Install mcp-servers root deps (puppeteer)
if [ -f mcp-servers/package.json ]; then
  echo "[5/5] Installing mcp-servers root dependencies..."
  cd mcp-servers && npm install && cd "$SCRIPT_DIR"
  echo "  OK"
fi

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "  1. Set required env vars (see .env.example)"
echo "  2. For Pencil MCP: install High Agency VS Code extension"
echo "     and update the 'pencil' path in opencode.json"
