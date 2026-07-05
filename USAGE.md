# 📖 GHOSTEYE — Guide d'Usage

> *Trois commandes. Mémorise-les.*

---

## Premier lancement

```bash
cd ghosteye
python3 ghosteye_proxy.py 8082
```

Output attendu :
```
   ▄█████ █  ██  ▄█████ ▄█████▄  ██   ██ ▄█████ █    ██  ██ ██    ██
  ██      ██▄██  ██     ██   ██  ██▄▄▄██ ██     ██    ██  ██ ██    ██
  ██  ███ ██▀██  █████  ██████   ██   ██ █████  ██    ██  ██ ██    ██
  ██   ██ ██  ██ ██     ██   ██  ██   ██ ██      ██  ▄██  ██  ██  ██
   ▀████▀ ██  ██ ▀█████ ██   ██  ██   ██ ▀█████   ▀███▀██▄██  ▀███▀

  GHOSTEYE v3.0 — RTSP/HLS Camera Pentest Platform
  ghost1o1 / L'ÉVEIL NOCTURNE — There is no lock.

  Dashboard: http://0.0.0.0:8082
  Health:    http://0.0.0.0:8082/health
```

→ Ouvre Firefox sur `http://localhost:8082`

---

## Scénario 1 — Découverte réseau d'une caméra

**Objectif :** identifier toutes les caméras IP sur le LAN

**Phase 1 du protocole GHOST1O1 : OBSERVER**

```bash
# 1. Scan réseau basique
curl -X POST http://localhost:8082/scan/ports \
  -H 'Content-Type: application/json' \
  -d '{"target":"192.168.1.0/24","ports":[80,554,8899,37777,8080]}'

# 2. ONVIF WS-Discovery
curl -X POST http://localhost:8082/onvif/discover \
  -H 'Content-Type: application/json' -d '{}'

# 3. Pour chaque IP trouvée, probe ONVIF
curl -X POST http://localhost:8082/onvif/probe \
  -H 'Content-Type: application/json' \
  -d '{"ip":"192.168.1.77"}'
```

**Output type :**
```json
{
  "ip": "192.168.1.77",
  "manufacturer": "Hikvision",
  "model": "DS-2CD2142FWD-I",
  "firmware": "V5.5.0 build 210628",
  "serial": "DS-2CD2142FWD-I20210628",
  "hardwareId": "0x9c01"
}
```

→ Tu as maintenant le **modèle exact + firmware**. Tu peux chercher les CVEs sur `https://nvd.nist.gov/vuln/search/results?form_type=Basic&query=DS-2CD2142FWD-I`

---

## Scénario 2 — Bruteforce des paths RTSP

**Objectif :** trouver l'URL exacte du stream sur une caméra identifiée

**Phase 2 du protocole GHOST1O1 : CARTOGRAPHIER**

```bash
curl -X POST http://localhost:8082/rtsp/brute \
  -H 'Content-Type: application/json' \
  -d '{"ip":"192.168.1.77"}'
```

**Output :**
```json
{
  "results": [
    {"path": "/Streaming/Channels/101", "status": "OK", "method": "Hikvision"},
    {"path": "/h264/ch1/main/av_stream", "status": "OK", "method": "Hikvision-Alt"},
    {"path": "/Streaming/Channels/102", "status": "OK", "method": "Hikvision-Sub"}
  ]
}
```

→ Tu as les **URLs qui fonctionnent**. Tu peux maintenant ajouter le stream.

---

## Scénario 3 — Ajout et lecture d'un stream

**Objectif :** visualiser le flux live dans le dashboard

**Phase 3 du protocole GHOST1O1 : INSTRUMENTER**

### Méthode A — Via l'API

```bash
curl -X POST http://localhost:8082/add \
  -H 'Content-Type: application/json' \
  -d '{
    "id":"cam_hik_main",
    "url":"rtsp://192.168.1.77:554/Streaming/Channels/101"
  }'
```

### Méthode B — Via le dashboard

1. Click **+ ADD STREAM** (header)
2. Entrer ID : `cam_hik_main`
3. Entrer URL : `rtsp://192.168.1.77:554/Streaming/Channels/101`
4. Click **ADD TO PROXY**

→ Le stream apparaît dans la grille avec status **LOADING** puis **LIVE**.

### Méthode C — Via presets

Click **📹 LOAD DISCOVERED STREAMS** → ajoute automatiquement Hikvision/Dahua/OEM.

---

## Scénario 4 — Snapshot & rapport

**Objectif :** capturer la preuve d'accès (phase 4 du protocole GHOST1O1)

### Snapshot instantané

Click sur **📸** sur la card du stream → télécharge un PNG horodaté.

### Rapport JSON complet

Click **📥 EXPORT** dans le header → télécharge un JSON avec :
- Timestamp
- Tous les devices découverts
- Tous les credentials testés
- Tous les paths RTSP trouvés
- Tous les streams actifs

```json
{
  "timestamp": "2026-07-05T02:30:00Z",
  "operator": "ghost1o1",
  "tool": "GHOSTEYE v3.0",
  "mission": {
    "subnet": "192.168.1.0/24",
    "devices": [...],
    "creds": [...],
    "rtsp": [...],
    "exploited": [...]
  }
}
```

---

## Scénario 5 — Accès cell depuis n'importe où

**Objectif :** piloter l'audit depuis un cell en 4G

### Tunnel bore.pub (gratuit, instant)

```bash
# Sur la machine qui héberge le proxy
curl -sL https://github.com/ekzhang/bore/releases/download/v0.5.2/bore-v0.5.2-x86_64-unknown-linux-musl.tar.gz | tar xz -C /tmp/
sudo mv /tmp/bore /usr/local/bin/
bore local 8082 --to bore.pub
```

Output : `listening at bore.pub:45623`

→ Sur le cell : `http://bore.pub:45623` (Chrome/Safari/Firefox mobile)

### Tunnel ngrok (URL fixe)

```bash
ngrok config add-authtoken TON_TOKEN
ngrok http 8082
```

Output : `https://abc123.ngrok-free.app`

---

## ⚙️ Options avancées

### Changer le port

```bash
python3 ghosteye_proxy.py 9999
```

### Démarrer en background (Linux)

```bash
nohup python3 ghosteye_proxy.py 8082 > ghosteye.log 2>&1 &
```

### Démarrer en daemon avec systemd

Créer `/etc/systemd/system/ghosteye.service` :
```ini
[Unit]
Description=GHOSTEYE RTSP/HLS Proxy
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ghosteye
ExecStart=/usr/bin/python3 /opt/ghosteye/ghosteye_proxy.py 8082
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now ghosteye
sudo systemctl status ghosteye
```

### Logs

```bash
tail -f ghosteye.log
# ou si systemd
journalctl -u ghosteye -f
```

---

## ⌨️ Raccourcis clavier (dashboard)

| Touche | Action |
|--------|--------|
| `1-9` | Switch panel (Streams/Discovery/...) |
| `L` | Load preset streams |
| `R` | Refresh all streams |
| `A` | Add stream prompt |
| `E` | Export rapport JSON |
| `?` | Afficher aide |

---

## 🔗 Intégration avec les autres outils GHOST1O1

| Depuis GHOSTEYE → Vers | Comment |
|------------------------|---------|
| `ycc365-ghost` | Export JSON → analyse firmware du modèle trouvé |
| `phishcloner-ultimate` | Si tu trouves un portail web sur la caméra, monte un clone pédagogique |
| `quebec-ultimate` | OSINT sur l'IP caméra → pivote vers ASN, registrar, mails admin |
| `biobypass` | Si la caméra a un système d'auth biométrique |
| `ghost1o1-design` | Customise le dashboard avec ton branding |

---

## 📋 Cheatsheet — Référence rapide

```bash
# Démarrer
python3 ghosteye_proxy.py 8082

# Health check
curl -s http://localhost:8082/health

# Discover
curl -X POST http://localhost:8082/onvif/discover -H 'Content-Type: application/json' -d '{}'

# Probe
curl -X POST http://localhost:8082/onvif/probe -H 'Content-Type: application/json' -d '{"ip":"X"}'

# Port scan
curl -X POST http://localhost:8082/scan/ports -H 'Content-Type: application/json' -d '{"target":"X","ports":[80,554]}'

# RTSP brute
curl -X POST http://localhost:8082/rtsp/brute -H 'Content-Type: application/json' -d '{"ip":"X"}'

# Add stream
curl -X POST http://localhost:8082/add -H 'Content-Type: application/json' -d '{"id":"X","url":"rtsp://X"}'

# List streams
curl -s http://localhost:8082/streams

# Delete stream
curl -X DELETE http://localhost:8082/stream/X

# Stop
pkill -f ghosteye_proxy

# Tunnel
bore local 8082 --to bore.pub
# ou
ngrok http 8082
```

---

## 🎯 Cas pédagogiques recommandés

1. **Ton propre lab** : installe une caméra IP bon marché (ou un softcam comme `vlc` ou un serveur RTSP test) et teste toutes les phases du protocole.
2. **HackTheBox / TryHackMe** : des boxes dédiées caméras (Sherlock, challenges réseau).
3. **RTSP test server public** : `rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4` pour tester sans cible réelle.
4. **DVWA / OWASP WebGoat** : si tu testes la partie web d'une caméra (port 80).

---

<div align="center">

**L'ÉVEIL NOCTURNE** · [ghost1o1](https://github.com/187Ghost101) — 2026

*Là où l'ignorance dort, nous allumons.*

</div>
