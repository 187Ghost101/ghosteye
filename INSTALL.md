# 📥 GHOSTEYE v12.0 — Guide d'installation

> Multi-plateforme · 5 minutes · 0 cloud.

## 🎯 Prérequis

| Item | Requis | Note |
|------|--------|------|
| **OS** | Kali / Debian / Ubuntu / macOS / Termux | Linux recommandé |
| **Python** | 3.10+ | Vérifie : `python3 --version` |
| **ffmpeg** | 4.0+ | Requis pour HLS transcode |
| **RAM** | 100 MB | Léger |
| **Disque** | 5 MB | |
| **Réseau** | Port 8082 (par défaut) | Modifiable |

## ⚡ Méthode 1 — Installateur universel (recommandée)

```bash
# 1. Clone
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye

# 2. Permissions
chmod +x install.sh ghosteye_proxy.py

# 3. Install
./install.sh
```

Le script :
1. Vérifie Python 3.10+
2. Installe `ffmpeg` si manquant (via apt/brew)
3. Installe dépendances Python (aiohttp)
4. Crée `~/ghosteye/` avec raccourcis
5. Lance le proxy

## 🔧 Méthode 2 — Manuel

### 2.1 Installer ffmpeg

```bash
# Debian/Ubuntu/Kali
sudo apt update && sudo apt install -y ffmpeg python3-pip

# macOS
brew install ffmpeg python3

# Termux
pkg install ffmpeg python

# Windows (chocolatey)
choco install ffmpeg python3
```

### 2.2 Cloner le repo

```bash
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
```

### 2.3 Installer Python deps

```bash
pip3 install -r requirements.txt
# OU
pip3 install aiohttp
```

### 2.4 Lancer

```bash
python3 ghosteye_proxy.py 8082
```

Output attendu :
```
╔═══════════════════════════════════════════╗
║  GHOSTEYE Stream Proxy v12.0              ║
║  RTSP → HLS + 5 RECON ENDPOINTS          ║
╠═══════════════════════════════════════════╣
║  Dashboard: http://0.0.0.0:8082          ║
║  /health    : status                     ║
║  /streams   : list                       ║
║  /onvif/*   : ONVIF recon                ║
║  /scan/ports: port scanner               ║
║  /rtsp/brute: 55 paths brute             ║
╚═══════════════════════════════════════════╝
```

## 🐧 Kali Linux (full setup)

```bash
# 1. Update
sudo apt update && sudo apt full-upgrade -y

# 2. Install deps
sudo apt install -y ffmpeg python3-pip git curl

# 3. Clone + install
cd ~
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
chmod +x install.sh ghosteye_proxy.py
./install.sh

# 4. Lancer
python3 ghosteye_proxy.py 8082

# 5. Firefox
firefox http://localhost:8082 &

# 6. (Optionnel) Tunnel externe
ngrok http 8082
# OU
bore local 8082 --to bore.pub
```

## 🍎 macOS

```bash
# 1. Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Deps
brew install ffmpeg python3 git

# 3. Clone
cd ~
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye

# 4. Python deps
pip3 install aiohttp

# 5. Lancer
python3 ghosteye_proxy.py 8082

# 6. Navigateur
open http://localhost:8082
```

## 📱 Termux (Android)

```bash
# 1. Setup Termux
pkg update && pkg upgrade -y
pkg install python ffmpeg git

# 2. Clone
cd ~
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye

# 3. Deps
pip install aiohttp

# 4. Lancer (en background)
nohup python3 ghosteye_proxy.py 8082 > ghosteye.log 2>&1 &

# 5. Accès via navigateur Android
# (utilise :8082 dans l'IP de Termux, ex: 127.0.0.1:8082)
```

## 🪟 Windows (WSL2 recommandé)

```powershell
# WSL2 (recommandé)
wsl --install
wsl --set-default-version 2

# Puis dans WSL Ubuntu :
sudo apt install ffmpeg python3-pip git
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
pip3 install aiohttp
python3 ghosteye_proxy.py 8082
```

Ou via Python natif :
```powershell
# Python natif Windows
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
pip install aiohttp
python ghosteye_proxy.py 8082
```

## 🌐 Accès réseau (cell/remote)

### Option A : bore.pub (gratuit, instant)

```bash
# Install bore
curl -sL https://github.com/ekzhang/bore/releases/download/v0.5.2/bore-v0.5.2-x86_64-unknown-linux-musl.tar.gz | tar xz -C /tmp/
sudo mv /tmp/bore /usr/local/bin/

# Tunnel
bore local 8082 --to bore.pub
# Output: listening at bore.pub:XXXXX
```

### Option B : ngrok

```bash
ngrok config add-authtoken TON_TOKEN
ngrok http 8082
# Output: https://xxxx.ngrok-free.app
```

### Option C : SSH tunnel (LAN)

```bash
# Kali
sudo systemctl start ssh
ip addr show  # note l'IP

# Cell (via Termux)
ssh -L 8082:localhost:8082 kali@KALI_IP
# Ouvre http://localhost:8082 sur le cell
```

## ✅ Vérification

```bash
# Test health endpoint
curl http://localhost:8082/health
# Output attendu: {"status":"ok","version":"12.0","uptime":...}

# Test HTML
curl -I http://localhost:8082/
# Output attendu: HTTP/1.1 200 OK, Content-Type: text/html
```

Dans le navigateur :
1. Ouvre `http://localhost:8082`
2. Tu dois voir le dashboard GHOSTEYE
3. Le panel "Streams" doit être actif
4. Clique "TEST" → statut doit changer

## 🆘 Troubleshooting

### ffmpeg not found
```bash
# Vérifier
which ffmpeg

# Install
sudo apt install ffmpeg  # Debian/Ubuntu
brew install ffmpeg      # macOS
```

### Port 8082 already in use
```bash
# Voir qui utilise
sudo lsof -i :8082
# OU
sudo netstat -tulpn | grep 8082

# Tuer
sudo kill PID

# Ou changer port
python3 ghosteye_proxy.py 9090
```

### aiohttp not found
```bash
pip3 install aiohttp
# OU
pip3 install -r requirements.txt
```

### Dashboard ne charge pas
- Vérifie : `curl http://localhost:8082/health`
- Vérifie console navigateur (F12)
- Teste Firefox vs Chrome

### Streams ne s'affichent pas
- Vérifie ffmpeg : `ffmpeg -version`
- Teste RTSP URL : `ffprobe rtsp://IP:554/path`
- Regarde logs : `tail -f ghosteye.log`

## 🔄 Mise à jour

```bash
cd ghosteye
git pull origin main
pip3 install -r requirements.txt --upgrade
```

---

**Prêt ?** → [USAGE.md](USAGE.md) pour le guide d'utilisation.

🏴‍☠️ **ghost1o1** — *"There is no lock."*
