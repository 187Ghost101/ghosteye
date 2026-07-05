# 🔧 GHOSTEYE — Guide d'installation multi-OS

> *Trois OS supportés nativement, deux via Docker, un via Replit. Tout est dans ce guide.*

---

## Table des matières

1. [Prérequis communs](#prérequis-communs)
2. [🐧 Kali / Debian / Ubuntu](#-kali--debian--ubuntu)
3. [🏔️ Arch / Manjaro](#-arch--manjaro)
4. [🍎 macOS](#-macos)
5. [🪟 Windows (WSL2)](#-windows-wsl2)
6. [📱 Termux (Android)](#-termux-android)
7. [🐳 Docker](#-docker)
8. [☁️ Replit / GitHub Codespaces](#-replit--github-codespaces)
9. [☁️ bore.pub / ngrok (tunnel)](#-borepub--ngrok-tunnel)
10. [Vérification post-install](#vérification-post-install)
11. [Troubleshooting](#troubleshooting)

---

## Prérequis communs

| Composant | Version | Rôle |
|-----------|---------|------|
| Python | 3.10+ | Runtime proxy |
| ffmpeg | 4.0+ | HLS transcoding |
| Git | 2.0+ | Clone repo |
| Navigateur moderne | Firefox 90+ / Chrome 90+ | Dashboard |

**Connaissances :**
- Savoir ouvrir un terminal
- Savoir taper `cd`, `ls`, `python3 fichier.py`
- C'est tout. Le reste est dans le tuto.

---

## 🐧 Kali / Debian / Ubuntu

**C'est la méthode native, la plus testée.**

### Étape 1 — Installation des dépendances système
```bash
sudo apt update && sudo apt install -y python3 python3-pip ffmpeg git
```

### Étape 2 — Clone du repo
```bash
cd ~
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
```

### Étape 3 — Lancement
```bash
python3 ghosteye_proxy.py 8082
```

### Étape 4 — Test
```bash
# Dans un autre terminal
curl -s http://localhost:8082/health
# → {"status":"ok","version":"3.0","streams":0,"uptime":N}
```

### Étape 5 — Ouvrir le dashboard
```bash
firefox http://localhost:8082
```

### Méthode express (script auto-install)
```bash
curl -sL https://raw.githubusercontent.com/187Ghost101/ghosteye/main/install.sh | bash
```

---

## 🏔️ Arch / Manjaro

```bash
sudo pacman -Syu python ffmpeg git
cd ~
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
firefox http://localhost:8082
```

---

## 🍎 macOS

### Avec Homebrew (recommandé)
```bash
# 1. Installer Homebrew si pas déjà fait
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Dépendances
brew install python3 ffmpeg git

# 3. Clone + run
cd ~
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
open http://localhost:8082
```

### Sans Homebrew
- Installe Python 3 depuis [python.org](https://www.python.org/downloads/)
- Installe ffmpeg via MacPorts : `sudo port install ffmpeg`
- Le reste est identique

---

## 🪟 Windows (WSL2)

### Étape 1 — Installer WSL2
```powershell
# PowerShell admin
wsl --install -d Ubuntu
```

### Étape 2 — Dans Ubuntu WSL
```bash
sudo apt update && sudo apt install -y python3 python3-pip ffmpeg git
cd ~
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
```

### Étape 3 — Depuis le browser Windows
```
http://localhost:8082
```
(WSL2 partage localhost avec Windows, c'est automatique.)

---

## 📱 Termux (Android)

### Méthode native (Termux + Python)
```bash
pkg update && pkg upgrade
pkg install python ffmpeg git
cd ~
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
```

### Méthode proot-distro (Debian complet)
```bash
pkg install proot-distro
proot-distro install debian
proot-distro login debian
# → dans Debian proot
apt update && apt install -y python3 ffmpeg git
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
```

### Accès depuis le browser du cell
```bash
# Sur le même cell, dans Chrome
http://localhost:8082
```

### Accès depuis un autre cell/PC sur le même WiFi
```bash
# Trouve l'IP Termux
ip addr show wlan0 | grep inet
# → 192.168.X.X

# Sur l'autre device
http://192.168.X.X:8082
```

---

## 🐳 Docker

### Image officielle
```bash
docker run -d -p 8082:8082 --name ghosteye --restart unless-stopped 187ghost101/ghosteye
firefox http://localhost:8082
```

### Build local
```bash
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
docker build -t ghosteye .
docker run -d -p 8082:8082 --name ghosteye ghosteye
```

### Docker Compose
```bash
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
docker compose up -d
```

### Avec tunnel bore.pub automatique
```bash
docker run -d -p 8082:8082 --name ghosteye 187ghost101/ghosteye
docker exec -d ghosteye sh -c "curl -sL https://github.com/ekzhang/bore/releases/download/v0.5.2/bore-v0.5.2-x86_64-unknown-linux-musl.tar.gz | tar xz -C /tmp/ && /tmp/bore local 8082 --to bore.pub"
```

---

## ☁️ Replit / GitHub Codespaces

### Replit (one-click)
1. Va sur [replit.com/github/187Ghost101/ghosteye](https://replit.com/github/187Ghost101/ghosteye)
2. Clique **"Import from GitHub"**
3. Replit build et lance automatiquement
4. URL publique générée : `https://ghosteye-USERNAME.repl.co`

### GitHub Codespaces
1. Va sur [github.com/187Ghost101/ghosteye](https://github.com/187Ghost101/ghosteye)
2. Clique **Code** → **Codespaces** → **Create codespace on main**
3. Terminal : `python3 ghosteye_proxy.py 8082`
4. Onglet **Ports** : clic droit sur 8082 → **Port visibility: Public**

---

## ☁️ bore.pub / ngrok (tunnel)

### bore.pub (gratuit, instant, zéro signup)
```bash
curl -sL https://github.com/ekzhang/bore/releases/download/v0.5.2/bore-v0.5.2-x86_64-unknown-linux-musl.tar.gz | tar xz -C /tmp/ && sudo mv /tmp/bore /usr/local/bin/
bore local 8082 --to bore.pub
# → listening at bore.pub:XXXXX
```

### ngrok (token persistant)
```bash
# Une seule fois
ngrok config add-authtoken TON_TOKEN

# À chaque session
ngrok http 8082
# → https://xxxx.ngrok-free.app
```

### SSH tunnel
```bash
# Sur Kali
sudo systemctl start ssh
# Ton IP locale
ip addr show wlan0 | grep inet

# Sur ton cell (via Termux ou JuiceSSH)
ssh -L 8082:localhost:8082 kali@KALI_IP
# Puis dans le browser du cell
http://localhost:8082
```

---

## ✅ Vérification post-install

```bash
# 1. Python OK
python3 --version
# → Python 3.10+ (idéalement 3.12+)

# 2. ffmpeg OK
ffmpeg -version | head -1
# → ffmpeg version 4.0+ (idéalement 6.0+)

# 3. Repo cloné
ls ~/ghosteye/
# → ghosteye.html ghosteye_proxy.py install.sh ...

# 4. Proxy démarre
cd ~/ghosteye && python3 ghosteye_proxy.py 8082 &
sleep 2
curl -s http://localhost:8082/health
# → {"status":"ok",...}

# 5. Dashboard accessible
firefox http://localhost:8082
# → Page GHOSTEYE avec 9 panels
```

**Si les 5 passent : t'es opérationnel.**

---

## 🩹 Troubleshooting

### ❌ "Address already in use"
```bash
# Un proxy tourne déjà
pkill -f ghosteye_proxy
python3 ghosteye_proxy.py 8082
```

### ❌ "ffmpeg: command not found"
```bash
sudo apt install -y ffmpeg   # Debian/Ubuntu
brew install ffmpeg            # macOS
pkg install ffmpeg             # Termux
```

### ❌ "ModuleNotFoundError: No module named 'aiohttp'"
GHOSTEYE utilise **uniquement la stdlib Python** (asyncio, urllib, json). Si tu vois cette erreur, t'as probablement un vieux fork. Re-clone :
```bash
rm -rf ~/ghosteye
git clone https://github.com/187Ghost101/ghosteye.git
```

### ❌ "Permission denied" sur Termux
```bash
termux-setup-storage
chmod +x ~/ghosteye/ghosteye_proxy.py
```

### ❌ "No HLS playback" dans le browser
- Vérifie que ffmpeg est installé : `ffmpeg -version`
- Ouvre F12 → onglet Console → copie les erreurs rouges
- Test direct : `curl -X POST http://localhost:8082/add -d '{"id":"test","url":"rtsp://..."}' -H 'Content-Type: application/json'`

### ❌ Stream reste "LOADING" indéfiniment
- L'URL RTSP est incorrecte ou la caméra n'est pas accessible
- Test avec VLC : `vlc rtsp://10.0.0.77:554/Streaming/Channels/101`
- Si VLC marche pas → caméra inaccessible, pas un problème ghosteye

### ❌ "python3: command not found" (macOS)
```bash
brew install python3
# OU utilise python au lieu de python3
python ghosteye_proxy.py 8082
```

### ❌ Port 8082 bloqué par firewall (Kali)
```bash
sudo ufw allow 8082/tcp
# OU change de port
python3 ghosteye_proxy.py 9090
```

### ❌ Windows WSL2 n'accède pas au localhost
- Vérifie que WSL2 est bien la version par défaut : `wsl -l -v`
- Mets à jour : `wsl --update`
- Le port est partagé automatiquement, mais parfois il faut redémarrer WSL : `wsl --shutdown` puis relancer

---

## 📚 Ressources

- **README principal** : [README.md](README.md)
- **Usage avancé** : [USAGE.md](USAGE.md)
- **Tutoriels GHOST1O1** : [TUTORIALS/](https://github.com/187Ghost101/ghost1o1/tree/main/tutorials)
- **Issues GitHub** : [github.com/187Ghost101/ghosteye/issues](https://github.com/187Ghost101/ghosteye/issues)

---

*"There is no lock." — ghost1o1*
