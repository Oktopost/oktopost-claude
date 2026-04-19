#!/bin/sh
# install.sh — Oktopost Claude Skill Installer
# POSIX-compatible (sh). No bash-specific syntax.
#
# Usage:
#   sh install.sh                                       Install skill + example preset
#   sh install.sh --with-mcp KEY ACCOUNT_ID [REGION]    Install + configure MCP server
#   sh install.sh --uninstall                            Remove installed files

set -e

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SKILL_NAME="oktopost"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_SRC="${REPO_DIR}/skills/${SKILL_NAME}"
PRESET_SRC="${REPO_DIR}/skills/${SKILL_NAME}/presets/oktopost-example.json"

SKILL_DEST="${HOME}/.claude/skills/${SKILL_NAME}"
PRESET_DIR="${HOME}/.oktopost/presets"
PRESET_DEST="${PRESET_DIR}/oktopost-example.json"

MCP_CONFIG="${HOME}/.claude/settings.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
info()  { printf "\033[1;34m[info]\033[0m  %s\n" "$1"; }
ok()    { printf "\033[1;32m[ok]\033[0m    %s\n" "$1"; }
warn()  { printf "\033[1;33m[warn]\033[0m  %s\n" "$1"; }
err()   { printf "\033[1;31m[error]\033[0m %s\n" "$1" >&2; exit 1; }

detect_os() {
  case "$(uname -s)" in
    Darwin*) OS="macOS" ;;
    Linux*)  OS="Linux" ;;
    *)       err "Unsupported operating system: $(uname -s). Only macOS and Linux are supported." ;;
  esac
  info "Detected OS: ${OS}"
}

check_claude_cli() {
  if command -v claude >/dev/null 2>&1; then
    ok "Claude Code CLI found: $(command -v claude)"
  else
    warn "Claude Code CLI not found in PATH."
    warn "Install it from https://docs.anthropic.com/en/docs/claude-code and re-run this script."
    warn "Continuing anyway — files will be placed in ~/.claude/skills/."
  fi
}

# ---------------------------------------------------------------------------
# Install
# ---------------------------------------------------------------------------
do_install() {
  detect_os
  check_claude_cli

  # 1. Copy skill directory
  info "Installing skill to ${SKILL_DEST} ..."
  if [ ! -d "${SKILL_SRC}" ]; then
    err "Skill source not found at ${SKILL_SRC}. Are you running this from the repo root?"
  fi
  mkdir -p "$(dirname "${SKILL_DEST}")"
  if [ -d "${SKILL_DEST}" ]; then
    warn "Skill directory already exists — overwriting."
    rm -rf "${SKILL_DEST}"
  fi
  cp -R "${SKILL_SRC}" "${SKILL_DEST}"
  ok "Skill installed."

  # 2. Create presets directory (empty — we do NOT auto-copy the example,
  #    which contains REPLACE_WITH_PROFILE_ID placeholders that would block
  #    the skill's runtime validator until edited).
  info "Creating presets directory at ${PRESET_DIR} (empty)..."
  mkdir -p "${PRESET_DIR}"
  ok "Presets directory ready."
  info "Reference template lives at ${SKILL_DEST}/presets/oktopost-example.json"
  info "Copy it to ${PRESET_DIR}/<your-brand>.json and edit when you're ready."

  # 4. MCP setup (optional)
  if [ "${SETUP_MCP}" = "1" ]; then
    do_mcp_setup
  fi

  # 5. Success
  printf "\n"
  ok "Oktopost Claude skill installed successfully!"
  printf "\n"
  info "Next steps:"
  printf "  1. Open Claude Code (no restart needed for the skill).\n"
  printf "  2. Run:  /oktopost setup\n"
  printf "     Claude will walk you through connecting your Oktopost account\n"
  printf "     conversationally -- no shell commands required.\n"
  printf "  3. Try it:  /oktopost publish \"Draft a LinkedIn post about employee advocacy\"\n"
  if [ "${SETUP_MCP}" != "1" ]; then
    printf "\n"
    printf "  Advanced (skip /oktopost setup and configure non-interactively):\n"
    printf "     sh install.sh --with-mcp YOUR_API_KEY ACCOUNT_ID [us|eu]\n"
  fi
  printf "\n"
}

# ---------------------------------------------------------------------------
# MCP setup
# ---------------------------------------------------------------------------
do_mcp_setup() {
  info "Registering oktopost MCP server via 'claude mcp add' ..."

  if [ -z "${MCP_KEY}" ] || [ -z "${MCP_ACCOUNT_ID}" ]; then
    err "--with-mcp requires at least two arguments: KEY ACCOUNT_ID [REGION]"
  fi

  if ! command -v claude >/dev/null 2>&1; then
    err "Claude Code CLI ('claude') is required for MCP setup. Install it from https://docs.anthropic.com/en/docs/claude-code and re-run."
  fi

  if ! command -v npx >/dev/null 2>&1; then
    err "'npx' (Node.js 20+) is required to run the oktopost-mcp server. Install Node.js and re-run."
  fi

  # Probe that the oktopost-mcp package is published before registering.
  # Tolerates offline mode — we just warn instead of blocking the install.
  if command -v npm >/dev/null 2>&1; then
    if ! npm view oktopost-mcp version >/dev/null 2>&1; then
      warn "Could not find 'oktopost-mcp' on the npm registry (offline, or package not yet published)."
      warn "Continuing — 'claude mcp add' will attempt to install on first run."
    fi
  fi

  # Remove any prior registration so re-runs are idempotent.
  claude mcp remove oktopost >/dev/null 2>&1 || true

  if [ -n "${MCP_REGION}" ]; then
    claude mcp add oktopost \
      -e "OKTOPOST_ACCOUNT_ID=${MCP_ACCOUNT_ID}" \
      -e "OKTOPOST_API_KEY=${MCP_KEY}" \
      -e "OKTOPOST_ACCOUNT_REGION=${MCP_REGION}" \
      -- npx oktopost-mcp
  else
    claude mcp add oktopost \
      -e "OKTOPOST_ACCOUNT_ID=${MCP_ACCOUNT_ID}" \
      -e "OKTOPOST_API_KEY=${MCP_KEY}" \
      -- npx oktopost-mcp
  fi

  ok "MCP server 'oktopost' registered. Claude Code should hot-load it within a few seconds; if tools don't appear, restart once."
}

# ---------------------------------------------------------------------------
# Uninstall
# ---------------------------------------------------------------------------
do_uninstall() {
  detect_os
  info "Uninstalling Oktopost Claude skill ..."

  if [ -d "${SKILL_DEST}" ]; then
    rm -rf "${SKILL_DEST}"
    ok "Removed ${SKILL_DEST}"
  else
    warn "Skill directory not found at ${SKILL_DEST} — nothing to remove."
  fi

  # Remove empty dirs (but not user presets)
  if [ -d "${PRESET_DIR}" ] && [ -z "$(ls -A "${PRESET_DIR}" 2>/dev/null)" ]; then
    rmdir "${PRESET_DIR}" 2>/dev/null || true
    rmdir "${HOME}/.oktopost" 2>/dev/null || true
    ok "Removed empty ${PRESET_DIR}"
  else
    warn "Presets directory ${PRESET_DIR} still contains files — leaving in place."
  fi

  # Remove MCP server registration if the CLI is available
  if command -v claude >/dev/null 2>&1; then
    if claude mcp remove oktopost >/dev/null 2>&1; then
      ok "Removed MCP server 'oktopost'"
    fi
  fi

  printf "\n"
  ok "Oktopost Claude skill uninstalled."
  printf "\n"
}

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
SETUP_MCP=0
MCP_KEY=""
MCP_ACCOUNT_ID=""
MCP_REGION=""

case "${1:-}" in
  --uninstall)
    do_uninstall
    exit 0
    ;;
  --with-mcp)
    if [ $# -lt 3 ]; then
      err "Usage: sh install.sh --with-mcp API_KEY ACCOUNT_ID [REGION]"
    fi
    SETUP_MCP=1
    MCP_KEY="$2"
    MCP_ACCOUNT_ID="$3"
    MCP_REGION="${4:-}"
    do_install
    exit 0
    ;;
  --help|-h)
    printf "Oktopost Claude Skill Installer\n\n"
    printf "Usage:\n"
    printf "  sh install.sh                                       Install skill + example preset\n"
    printf "  sh install.sh --with-mcp KEY ACCOUNT_ID [REGION]    Install + configure MCP server\n"
    printf "  sh install.sh --uninstall                            Remove installed files\n"
    printf "  sh install.sh --help                                 Show this message\n"
    printf "\nREGION defaults to 'us'. Pass 'eu' for EU accounts.\n"
    exit 0
    ;;
  "")
    do_install
    exit 0
    ;;
  *)
    err "Unknown option: $1. Run 'sh install.sh --help' for usage."
    ;;
esac
