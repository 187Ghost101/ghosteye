<div align="center">

```
   ▄█████ █  ██  ▄█████ ▄█████▄  ██   ██ ▄█████ █    ██  ██ ██    ██
  ██      ██▄██  ██     ██   ██  ██▄▄▄██ ██     ██    ██  ██ ██    ██
  ██  ███ ██▀██  █████  ██████   ██   ██ █████  ██    ██  ██ ██    ██
  ██   ██ ██  ██ ██     ██   ██  ██   ██ ██      ██  ▄██  ██  ██  ██
   ▀████▀ ██  ██ ▀█████ ██   ██  ██   ██ ▀█████   ▀███▀██▄██  ▀███▀
```

![GHOST1O1](https://img.shields.io/badge/GHOST1O1-NOCTURNE-e63946?style=for-the-badge&logo=ghost&logoColor=white)
![Version](https://img.shields.io/badge/VERSION-12.0-00d4ff?style=for-the-badge)
![Status](https://img.shields.io/badge/STATUS-OPERATIONAL-2ecc71?style=for-the-badge)
![Platforms](https://img.shields.io/badge/OS-LINUX%20%7C%20MAC%20%7C%20WIN%20%7C%20TERMUX-9b59b6?style=for-the-badge)

# 🎯 GHOSTEYE
## *RTSP/HLS Camera Pentest Platform*

**Audit caméras IoT en 60 secondes. Dashboard live, 9 panels, zero install complexe.**

[Demo Live](https://187ghost101.github.io/ghosteye/) · [Replit](https://replit.com/github/187Ghost101/ghosteye) · [Docker](https://hub.docker.com/r/187ghost101/ghosteye) · [Tutorial](https://github.com/187Ghost101/ghost1o1/blob/main/tutorials/TUTORIAL_01_OBSERVER.md)

</div>

---

## 🔥 C'est quoi ?

GHOSTEYE est la **plateforme de pentest caméras IoT** la plus directe du marché. Pas de framework lourd, pas de GUI à installer — un **proxy Python** + un **dashboard HTML** qui transforme n'importe quel browser en console de pilotage RTSP.

**Tu lances le proxy, tu ouvres Firefox, tu cliques. Tu vois les streams. Tu testes. Tu documentes.**

Conçu pour le **Protocole GHOST1O1** — phase 1 (Observer) et phase 2 (Cartographier) sur cible caméras IP, NVR, DVR.

---

## ✨ Features

- **9 panels intégrés** : Streams, Discovery, Shodan, ONVIF, PortScan, RTSP Brute, Credentials, Exploit, Shells, Persistence
- **Proxy HLS natif** : RTSP → HLS dans le browser, zéro plugin, zero flash
- **Recon en un clic** : 55 paths RTSP pré-chargés, ONVIF WS-Discovery, port scan async
- **Dashboard responsive** : fonctionne sur cell/tablette/4K
- **Mode DEMO sans proxy** : ouvre `ghosteye.html` direct dans le browser, 5 devices mockés
- **Tunnel instantané** : bore.pub, ngrok, SSH — accès cell depuis n'importe où
- **Rapport JSON** : export one-click de toute l'opération
- **Multi-OS** : Linux, macOS, Windows WSL2, Termux, Docker, Replit

---

## 🚀 Démarrage 60 secondes

### Méthode 1 — Auto-install (recommandée)

```bash
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
bash install.sh
python3 ghosteye_proxy.py 8082
firefox http://localhost:8082
```

### Méthode 2 — Manuel

```bash
# Prérequis
sudo apt install -y python3 ffmpeg    # Kali/Debian/Ubuntu
# brew install python3 ffmpeg          # macOS
# pacman -S python ffmpeg              # Arch

# Clone + run
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
```

### Méthode 3 — Docker

```bash
docker run -d -p 8082:8082 --name ghosteye 187ghost101/ghosteye
firefox http://localhost:8082
```

### Méthode 4 — Replit (one-click cloud)

[![Run on Replit](https://replit.com/badge/github/187Ghost101/ghosteye)](https://replit.com/github/187Ghost101/ghosteye)

### Méthode 5 — Termux (Android)

```bash
pkg update && pkg install python ffmpeg
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
python3 ghosteye_proxy.py 8082
```

### Méthode 6 — Sans rien installer (DEMO_MODE)

Ouvre `ghosteye.html` directement dans le browser. Le dashboard charge en mode démo avec 5 devices mockés visibles. **Aucune dépendance, aucun proxy, aucun réseau.**

```bash
git clone https://github.com/187Ghost101/ghosteye.git
firefox ghosteye/index.html
```

---

## 📱 Accès cell depuis n'importe où

```bash
# bore.pub (gratuit, instant, zéro signup)
curl -sL https://github.com/ekzhang/bore/releases/download/v0.5.2/bore-v0.5.2-x86_64-unknown-linux-musl.tar.gz | tar xz -C /tmp/ && sudo mv /tmp/bore /usr/local/bin/
bore local 8082 --to bore.pub
# → http://bore.pub:XXXXX → ouvre sur ton cell
```

**Même WiFi :** `http://KALI_IP:8082`  
**4G cellulaire :** `bore.pub:XXXXX`  
**ngrok (token persistant) :** `ngrok http 8082` → `https://xxxx.ngrok-free.app`

---

## 🎯 Usage — 3 scénarios

### Scénario 1 — Audit Hikvision sur LAN

```bash
# 1. Découverte automatique
curl -X POST http://localhost:8082/onvif/discover -H 'Content-Type: application/json' -d '{}'
# → [{"ip":"10.0.0.77","brand":"Hikvision",...}]

# 2. Probe ONVIF
curl -X POST http://localhost:8082/onvif/probe -H 'Content-Type: application/json' \
  -d '{"ip":"10.0.0.77"}'
# → {"manufacturer":"Hikvision","model":"DS-2CD2142FWD-I","firmware":"V5.5.0"}

# 3. RTSP brute (55 paths)
curl -X POST http://localhost:8082/rtsp/brute -H 'Content-Type: application/json' \
  -d '{"ip":"10.0.0.77"}'
# → ["rtsp://10.0.0.77:554/Streaming/Channels/101", ...]

# 4. Ajout stream + visualisation
curl -X POST http://localhost:8082/add -H 'Content-Type: application/json' \
  -d '{"id":"hik_main","url":"rtsp://10.0.0.77:554/Streaming/Channels/101"}'
firefox http://localhost:8082
```

### Scénario 2 — Test credentials par défaut (Dahua, Hikvision, OEM)

```bash
# Panel Credentials dans le dashboard
# → 15 brands pré-chargés avec credentials par défaut
# → Test en un clic
```

### Scénario 3 — Port scan rapide

```bash
curl -X POST http://localhost:8082/scan/ports -H 'Content-Type: application/json' \
  -d '{"target":"192.168.1.0/24","ports":[80,554,8899,37777,8080,9527,34567]}'
# → {"results":[{"ip":"192.168.1.77","open":[80,554,8899]},...]}
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Firefox/Chrome)                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │  ghosteye.html — Dashboard v12.0                   │    │
│  │  • 9 panels (Streams, Discovery, Shodan, ONVIF...) │    │
│  │  • HLS.js pour la lecture vidéo                     │    │
│  │  • Fetch() pour les appels API                     │    │
│  └────────────────┬───────────────────────────────────┘    │
└───────────────────┼─────────────────────────────────────────┘
                    │ HTTP / WebSocket
                    ▼
┌─────────────────────────────────────────────────────────────┐
│              ghosteye_proxy.py (Python 3 stdlib)             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Dashboard│  │ HLSProxy │  │ ONVIF    │  │ PortScan │   │
│  │ GET /    │  │ /{id}/...│  │ discover │  │ /scan    │   │
│  └──────────┘  └────┬─────┘  └──────────┘  └──────────┘   │
│                     │                                        │
│                     ▼                                        │
│              ┌──────────┐                                    │
│              │  ffmpeg  │  (subprocess)                      │
│              └────┬─────┘                                    │
└───────────────────┼──────────────────────────────────────────┘
                    │ RTSP
                    ▼
              ┌──────────┐
              │  Caméra  │
              │  (cible) │
              └──────────┘
```

---

## 📡 API Endpoints

| Method | Path | Body | Description |
|--------|------|------|-------------|
| GET | `/` | — | Dashboard HTML |
| GET | `/health` | — | Status JSON `{status, version, streams, uptime}` |
| POST | `/add` | `{id, url}` | Ajoute un stream RTSP |
| GET | `/streams` | — | Liste des streams actifs |
| DELETE | `/stream/{id}` | — | Stop un stream |
| GET | `/{id}/stream.m3u8` | — | HLS playlist |
| GET | `/{id}/seg_XXX.ts` | — | HLS segments |
| POST | `/onvif/discover` | `{}` | WS-Discovery multicast |
| POST | `/onvif/probe` | `{ip}` | GetDeviceInformation SOAP |
| POST | `/scan/ports` | `{target, ports}` | Port scan async |
| POST | `/rtsp/brute` | `{ip}` | 55 paths RTSP brute |

---

## 🛠️ Stack

- **Python 3.12+** (asyncio stdlib)
- **ffmpeg** (HLS transcoding)
- **HLS.js** (browser, CDN)
- **Vanilla JS** (no framework, no build step)
- **HTML/CSS pur** (single file, 58KB)

---

## 📂 Structure

```
ghosteye/
├── ghosteye.html          # Dashboard v12.0 (58KB, 9 panels)
├── ghosteye_proxy.py      # Proxy v3.0 (HLS + recon)
├── ghosteye_mission.sh    # Launcher
├── install.sh             # Auto-install multi-OS
├── Dockerfile             # Image Docker
├── docker-compose.yml     # Compose
├── .replit                # Replit config
├── README.md              # Ce fichier
├── INSTALL.md             # Guide install détaillé par OS
├── USAGE.md               # Exemples avancés
├── CHANGELOG.md           # Historique versions
├── LICENSE                # MIT
├── SECURITY.md            # Politique disclosure
└── GHOST1O1_BRAND.md      # Brand kit
```

---

## 🗺️ Roadmap

- [x] v3.0 — HLS + recon endpoints (ONVIF/PortScan/RTSP brute)
- [x] v6.1 — Smart dashboard (auto-detect proxyHost)
- [x] v12.0 — 9 panels + Shodan integration
- [ ] v13.0 — Mode record + replay timeline
- [ ] v14.0 — Multi-target concurrent
- [ ] v15.0 — WebRTC P2P (latency < 500ms)

---

## 🤝 Contribution

GHOSTEYE vit grâce à ses contributeurs. PRs bienvenues pour :
- Nouveaux panels (Shodan, Censys, BinaryEdge)
- Nouveaux paths RTSP (marques exotiques)
- Traductions (FR, ES, DE, PT, RU)
- Bugfixes (PR avec test obligatoire)

📜 **[CONTRIBUTING.md](https://github.com/187Ghost101/ghost1o1/blob/main/CONTRIBUTING.md)**

---

## 🔒 Sécurité & Légalité

**GHOSTEYE est un outil éducatif et de pentest autorisé.** Tu es responsable de ce que tu en fais.

- ✅ Lab personnel
- ✅ Tests sur ton propre équipement
- ✅ Audits avec **autorisation écrite**
- ❌ Caméras d'autrui sans permission
- ❌ Exfiltration / diffusion non autorisée

📜 **[SECURITY.md](https://github.com/187Ghost101/ghost1o1/blob/main/SECURITY.md)** — politique complète

---

## 📜 Licence

MIT — voir [LICENSE](https://github.com/187Ghost101/ghosteye/blob/main/LICENSE)

---

## 🔗 Liens

- **Hub GHOST1O1** : [github.com/187Ghost101/ghost1o1](https://github.com/187Ghost101/ghost1o1)
- **Méthodologie** : [PROTOCOL.md](https://github.com/187Ghost101/ghost1o1/blob/main/PROTOCOL.md)
- **Manifeste** : [MANIFESTO.md](https://github.com/187Ghost101/ghost1o1/blob/main/MANIFESTO.md)
- **Tutoriels** : [TUTORIALS/](https://github.com/187Ghost101/ghost1o1/tree/main/tutorials)
- **Auteur** : [@187Ghost101](https://github.com/187Ghost101)

---

<div align="center">

### Forged in the dark by [ghost1o1](https://github.com/187Ghost101) — 2026

*"There is no lock."*

</div>
