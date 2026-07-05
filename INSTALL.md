# 📥 GHOSTEYE — Installation Multi-OS

> *Du silence naît la lumière.*

---

## Prérequis globaux

| Composant | Version | Pourquoi |
|-----------|---------|----------|
| Python 3 | 3.8+ | Runtime du proxy |
| ffmpeg | 4.0+ | Transcodage RTSP → HLS |
| Git | 2.0+ | Clone du repo |
| Navigateur moderne | Firefox 80+, Chrome 80+ | Dashboard |

---

## 🐧 Kali Linux / Debian / Ubuntu

```bash
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg git firefox
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
firefox http://localhost:8082
```

**Vérification :**
```bash
python3 --version    # >= 3.8
ffmpeg -version      # >= 4.0
curl -s http://localhost:8082/health
# → {"status":"ok","version":"3.0","streams":0,"uptime":0}
```

---

## 🏔️ Arch Linux / Manjaro

```bash
sudo pacman -Syu python ffmpeg git firefox
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
```

---

## 🍎 macOS

```bash
# Install Homebrew si pas déjà fait
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install python3 ffmpeg git
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
open http://localhost:8082
```

---

## 🪟 Windows 10/11 (WSL2)

```powershell
# PowerShell admin
wsl --install -d Ubuntu
wsl --set-default Ubuntu
```

```bash
# Dans WSL Ubuntu
sudo apt update
sudo apt install -y python3 python3-pip ffmpeg git
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
```

**Accès depuis Windows :** `http://localhost:8082` (automatique)

---

## 📱 Termux (Android)

```bash
# Install Termux depuis F-Droid (PAS Google Play — version obsolète)
pkg update && pkg upgrade
pkg install python ffmpeg git

git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
```

**Accès depuis le cell :** Ouvre `http://localhost:8082` dans Chrome mobile.

**Accès depuis un autre cell/PC en 4G :**
```bash
# Sur Termux
curl -sL https://github.com/ekzhang/bore/releases/download/v0.5.2/bore-v0.5.2-x86_64-unknown-linux-musl.tar.gz | tar xz -C /tmp/
mv /tmp/bore $PREFIX/bin/
bore local 8082 --to bore.pub
# → http://bore.pub:XXXXX → autre cell
```

---

## 🐳 Docker (one-liner)

```bash
docker run -d -p 8082:8082 --name ghosteye --restart unless-stopped 187ghost101/ghosteye
firefox http://localhost:8082
```

**Build local :**
```bash
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
docker build -t ghosteye .
docker run -d -p 8082:8082 ghosteye
```

---

## ☁️ Replit (one-click cloud)

1. Va sur https://replit.com/github/187Ghost101/ghosteye
2. Click "Import from GitHub"
3. Click "Run"
4. URL publique auto-générée → ouvre dans ton browser

---

## ☁️ GitHub Codespaces

1. Va sur https://github.com/187Ghost101/ghosteye
2. Click "Code" → "Codespaces" → "Create codespace"
3. Terminal : `python3 ghosteye_proxy.py 8082`
4. Onglet "Ports" → forward 8082

---

## 🧪 Vérification post-install

```bash
# 1. Proxy répond
curl -s http://localhost:8082/health

# 2. Dashboard s'affiche
curl -s http://localhost:8082/ | head -20

# 3. ONVIF discover fonctionne
curl -s -X POST http://localhost:8082/onvif/discover -H 'Content-Type: application/json' -d '{}'

# 4. RTSP brute répond
curl -s -X POST http://localhost:8082/rtsp/brute -H 'Content-Type: application/json' -d '{"ip":"10.0.0.77"}'
```

Si les 4 commandes passent → **installation OK**.

---

## 🔧 Troubleshooting

### `Address already in use`
```bash
# Trouve le zombie
ss -tlnp | grep 8082
# ou
lsof -i :8082
# Kill
pkill -f ghosteye_proxy
```

### `ffmpeg: command not found`
```bash
sudo apt install -y ffmpeg       # Debian/Ubuntu
brew install ffmpeg              # macOS
pkg install ffmpeg               # Termux
sudo pacman -S ffmpeg            # Arch
```

### `ModuleNotFoundError: No module named 'aiohttp'`
Le proxy utilise **uniquement la stdlib Python**. Aucun pip install nécessaire. Si erreur, vérifie que tu utilises `python3` (pas python 2).

### Dashboard chargé mais boutons ne réagissent pas
1. F12 → Console → copier erreurs rouges
2. F12 → Network → tester `/health`
3. Vérifier que proxy tourne : `ps aux | grep ghosteye`

### Permission denied sur Termux
```bash
chmod +x ghosteye_proxy.py
```

### Le stream RTSP ne se charge pas
1. Vérifier l'URL : `ffprobe rtsp://IP:554/path`
2. Tester sans firewall : `iptables -F` (root only)
3. Essayer TCP forcé : `rtsp_transport=tcp` dans la query

---

## 📦 Mise à jour

```bash
cd ghosteye
git pull origin main
pkill -f ghosteye_proxy
python3 ghosteye_proxy.py 8082
```

---

## 🗑️ Désinstallation

```bash
pkill -f ghosteye_proxy
rm -rf ghosteye
# Docker
docker rm -f ghosteye
```

---

<div align="center">

**L'ÉVEIL NOCTURNE** · [ghost1o1](https://github.com/187Ghost101) — 2026

*There is no lock.*

</div>
