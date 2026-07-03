#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════
# GHOSTEYE v12.0 — NOCTURNE · Universal installer
# ghost1o1 · "There is no lock."
# ════════════════════════════════════════════════════════════════════
set -e
APP="ghosteye"
APP_NAME="GHOSTEYE v12.0 — Nocturne"
INSTALL_DIR="${GHOSTEYE_DIR:-$HOME/$APP}"
BOLD="\033[1m"; RED="\033[0;31m"; CYAN="\033[0;36m"; VIOLET="\033[0;35m"; GREEN="\033[0;32m"; NC="\033[0m"

logo() {
cat << 'EOF'

   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
   █  ╔═╗╦ ╦╔═╗╦ ╔═╗╔═╗╔╦╗╔═╗╦ ╦  █
   █  ║ ╦╠═╣║╣ ║ ║ ║╠═╝ ║ ╠═╣╚╦╝  █
   █  ╚═╝╩ ╩╚  ╩ ╚═╝╩   ╩ ╩ ╩ ╩   █
   █  ███████╗██╗  ██╗ ██████╗ ███████╗████████╗  █
   █  ██╔════╝██║  ██║██╔═══██╗██╔════╝╚══██╔══╝  █
   █  ██║     ███████║██║   ██║███████╗   ██║     █
   █  ██║     ██╔══██║██║   ██║╚════██║   ██║     █
   █  ███████╗██║  ██║╚██████╔╝███████║   ██║     █
   █  ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝     █
   █                  v12.0 — NOCTURNE                       █
   █              "There is no lock." — ghost1o1            █
   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

EOF
}

detect_os() {
  case "$(uname -s 2>/dev/null)" in
    Linux)
      if [ -f /etc/os-release ]; then . /etc/os-release; echo "$ID"
      elif [ -d /system ]; then echo "termux"
      else echo "linux"; fi ;;
    Darwin) echo "macos" ;;
    *) echo "unknown" ;;
  esac
}

OS=$(detect_os)
echo -e "${VIOLET}${BOLD}→ Detected OS: ${CYAN}$OS${NC}"

mkdir -p "$INSTALL_DIR"
echo -e "${VIOLET}${BOLD}→ Install dir: ${CYAN}$INSTALL_DIR${NC}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo .)"

# Copy files
for f in index.html ghosteye.css ghosteye.js ghosteye_proxy.py ghost1o1.css ghost1o1.js; do
  if [ -f "$SCRIPT_DIR/$f" ]; then
    cp "$SCRIPT_DIR/$f" "$INSTALL_DIR/"
    echo -e "${GREEN}✓${NC} Copied $f"
  fi
done

# v3.0 backward compat
[ -f "$SCRIPT_DIR/ghosteye.html" ] && cp "$SCRIPT_DIR/ghosteye.html" "$INSTALL_DIR/"

# Renommer index.html → ghosteye.html pour v3.0 compat
[ -f "$INSTALL_DIR/index.html" ] && [ ! -f "$INSTALL_DIR/ghosteye.html" ] && cp "$INSTALL_DIR/index.html" "$INSTALL_DIR/ghosteye.html"

# Launcher
cat > "$INSTALL_DIR/launch.sh" << 'LAUNCH'
#!/usr/bin/env bash
# GHOSTEYE launcher
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${GHOSTEYE_PORT:-8082}"

# Check ffmpeg
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "[!] ffmpeg not installed. Run: sudo apt install ffmpeg"
fi

# Check python
if ! command -v python3 >/dev/null 2>&1; then
  echo "[✗] python3 not found"
  exit 1
fi

# Kill any previous instance
pkill -f ghosteye_proxy 2>/dev/null
sleep 0.5

echo "[+] Launching GHOSTEYE v12.0 — Nocturne on :$PORT"
echo "[+] Dashboard: http://localhost:$PORT"
python3 "$DIR/ghosteye_proxy.py" "$PORT"
LAUNCH
chmod +x "$INSTALL_DIR/launch.sh"
echo -e "${GREEN}✓${NC} Created launcher"

# Desktop entry
if [ "$OS" = "kali" ] || [ "$OS" = "debian" ] || [ "$OS" = "ubuntu" ] || [ "$OS" = "parrot" ]; then
  mkdir -p "$HOME/.local/share/applications"
  cat > "$HOME/.local/share/applications/ghosteye.desktop" << EOF
[Desktop Entry]
Type=Application
Name=GHOSTEYE v12.0
Comment=Nocturne — Camera & IoT Pentest Dashboard
Exec=bash $INSTALL_DIR/launch.sh
Icon=utilities-system-monitor
Categories=Security;Education;Development;
Terminal=true
StartupNotify=true
EOF
  [ -x /usr/bin/update-desktop-database ] && update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
  echo -e "${GREEN}✓${NC} Desktop entry created"
fi

# Termux
if [ "$OS" = "termux" ] && [ -n "$PREFIX" ] && [ -d "$PREFIX/bin" ]; then
  ln -sf "$INSTALL_DIR/launch.sh" "$PREFIX/bin/ghosteye" 2>/dev/null && \
    echo -e "${GREEN}✓${NC} Added 'ghosteye' command (Termux)"
fi

# Done
echo
echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════${NC}"
echo -e "${VIOLET}${BOLD}  ✓ $APP_NAME — Installed${NC}"
echo -e "${CYAN}${BOLD}═══════════════════════════════════════════════════════${NC}"
echo
echo -e "  ${BOLD}Path:${NC}    $INSTALL_DIR"
echo -e "  ${BOLD}Launch:${NC}  bash $INSTALL_DIR/launch.sh"
echo -e "  ${BOLD}Then:${NC}    open http://localhost:8082"
echo
if [ "$OS" = "termux" ]; then
  echo -e "  ${BOLD}Command:${NC} ghosteye"
fi
echo -e "  ${RED}${BOLD}\"There is no lock.\"${NC} ${VIOLET}— ghost1o1${NC}"
echo
