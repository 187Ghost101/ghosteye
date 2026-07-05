<div align="center">

```
   ▄█████ █  ██  ▄█████ ▄█████▄  ██   ██ ▄█████ █    ██  ██ ██    ██
  ██      ██▄██  ██     ██   ██  ██▄▄▄██ ██     ██    ██  ██ ██    ██
  ██  ███ ██▀██  █████  ██████   ██   ██ █████  ██    ██  ██ ██    ██
  ██   ██ ██  ██ ██     ██   ██  ██   ██ ██      ██  ▄██  ██  ██  ██
   ▀████▀ ██  ██ ▀█████ ██   ██  ██   ██ ▀█████   ▀███▀██▄██  ▀███▀
```

![GHOST1O1](https://img.shields.io/badge/GHOST1O1-L'EVEIL_NOCTURNE-e63946?style=for-the-badge&logo=ghost&logoColor=white)
![Version](https://img.shields.io/badge/VERSION-12.0-00d4ff?style=for-the-badge)
![Status](https://img.shields.io/badge/STATUS-OPERATIONAL-2ecc71?style=for-the-badge)
![Platforms](https://img.shields.io/badge/OS-LINUX%20%7C%20MAC%20%7C%20WIN%20%7C%20TERMUX-9b59b6?style=for-the-badge)

# 🎯 GHOSTEYE
## *RTSP/HLS Camera Pentest Platform*

**Audit caméras IoT en 60 secondes. Dashboard live, 9 panels, zero install complexe.**

[Demo Live](https://187ghost101.github.io/ghosteye/) · [Replit](https://replit.com/github/187Ghost101/ghosteye) · [Docker](https://hub.docker.com/r/187ghost101/ghosteye) · [Tutorial](https://github.com/187Ghost101/ghost1o1/blob/main/tutorials/TUTORIAL_01_OBSERVER.md)

> *Là où l'ignorance dort, nous allumons.*
> *There is no lock.*

</div>

---

## 🔥 C'est quoi ?

GHOSTEYE est la **plateforme de pentest caméras IoT** la plus directe du marché. Pas de framework lourd, pas de GUI à installer — un **proxy Python** + un **dashboard HTML** qui transforme n'importe quel browser en console de pilotage RTSP.

**Tu lances le proxy, tu ouvres Firefox, tu cliques. Tu vois les streams. Tu testes. Tu documentes.**

Conçu pour le **Protocole GHOST1O1** — phase 1 (Observer) et phase 2 (Cartographier) sur cible caméras IP, NVR, DVR.

---

## ✨ Features

- **9 panels intégrés** : Streams, Discovery, Shodan, ONVIF, PortScan, RTSP Brute, Credentials, Exploit, Shells, Persistence
- **Proxy HLS natif** : RTSP → HLS dans le browser, zéro plugin, zéro flash
- **Recon en un clic** : 55 paths RTSP pré-chargés, ONVIF WS-Discovery, port scan async
- **Dashboard responsive** : fonctionne sur cell/tablette/4K
- **Mode DEMO sans proxy** : ouvre `index.html` direct dans le browser, 5 devices mockés
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

Ouvre `index.html` directement dans le browser. Le dashboard charge en mode démo avec 5 devices mockés visibles. **Aucune dépendance, aucun proxy, aucun réseau.**

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

# 2. Probe ONVIF
curl -X POST http://localhost:8082/onvif/probe -H 'Content-Type: application/json' \
  -d '{"ip":"10.0.0.77"}'

# 3. RTSP brute (55 paths)
curl -X POST http://localhost:8082/rtsp/brute -H 'Content-Type: application/json' \
  -d '{"ip":"10.0.0.77"}'

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
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Firefox/Chrome)                  │
│  ┌────────────────────────────────────────────────────┐    │
│  │  index.html — Dashboard v12.0                       │    │
│  │  • 9 panels + DEMO_MODE sans proxy                  │    │
│  │  • HLS.js pour la lecture vidéo                     │    │
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
| POST | `/scan/ports` | `{target, ports}` | Async port scan |
| POST | `/rtsp/brute` | `{ip}` | 55 paths RTSP brute |
| GET | `/api/streams/discovered` | — | Streams auto-découverts |

---

## 🔐 Légalité & Éthique

GHOSTEYE est un outil **éducatif et de recherche**. Utilisation autorisée uniquement sur :
- Tes propres équipements (lab perso)
- Cibles avec **autorisation écrite** explicite
- Environnements de CTF / HackTheBox / TryHackMe
- Audits de sécurité contractuels

**Pas d'utilisation sur des caméras de tiers sans permission.** La méthodologie GHOST1O1 impose la **preuve**, pas la destruction.

📜 **[SECURITY.md](SECURITY.md)** — politique complète

---

## 🛣️ Roadmap

- [x] Proxy HLS multi-stream
- [x] ONVIF WS-Discovery + Probe
- [x] RTSP brute 55 paths
- [x] Dashboard 9 panels
- [x] DEMO_MODE standalone
- [x] Cross-platform (Linux/Mac/Win/Termux/Docker)
- [ ] ONVIF PTZ control
- [ ] Audio RTSP support
- [ ] Multi-cam grid view
- [ ] AI detection (motion, faces, plates)
- [ ] Mobile app native

---

## 🤝 Contribution

L'ÉVEIL NOCTURNE vit grâce à ses contributeurs. Avant de proposer un PR :
1. Lis le code, chaque ligne est une décision
2. Teste sur 2 OS minimum
3. Signe ton travail
4. Pas de drama, pas d'ego, pas de gatekeeping

📜 **[CONTRIBUTING.md](CONTRIBUTING.md)**

---

## 📜 Licence

**MIT License** — Tu peux forker, modifier, redistribuer, commercialiser. Garde la signature `ghost1o1`, ne gates pas l'accès.

---

<div align="center">

### **L'ÉVEIL NOCTURNE** · Forged in the dark by [ghost1o1](https://github.com/187Ghost101) — 2026

*There is no lock. Du silence naît la lumière.*

</div>
