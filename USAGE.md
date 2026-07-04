# 🎮 GHOSTEYE v12.0 — Guide d'utilisation

> 9 panels · workflow mission · raccourcis clavier.

## 🎯 Premier lancement

```bash
python3 ghosteye_proxy.py 8082
```

Ouvre `http://localhost:8082` dans Firefox/Chrome.

## 🧭 Navigation

### Sidebar (gauche)
9 sections principales :
1. **Streams** (défaut)
2. **Shodan**
3. **ONVIF**
4. **PortScan**
5. **RTSP Brute**
6. **Discovery**
7. **Credentials**
8. **Exploitation**
9. **Shells** + **Persistence** + **Payloads** + **Console** + **Report**

### Raccourcis clavier
| Touche | Action |
|--------|--------|
| `1-9` | Switch panel |
| `L` | Load preset streams |
| `R` | Refresh |
| `A` | Add stream prompt |
| `E` | Export report |
| `?` | Help overlay |
| `Esc` | Close modal |

## 📡 Panel 1 — Streams (HLS Live)

### Ajouter un stream RTSP

```bash
# Via UI
Sidebar → Streams → + ADD STREAM
ID: cam1
URL: rtsp://10.0.0.77:554/Streaming/Channels/101

# Via API
curl -X POST http://localhost:8082/add \
  -H 'Content-Type: application/json' \
  -d '{"id":"cam1","url":"rtsp://10.0.0.77:554/Streaming/Channels/101"}'
```

### Presets inclus
- **hikvision** : `rtsp://HOST:554/Streaming/Channels/101`
- **dahua** : `rtsp://HOST:554/cam/realmonitor?channel=1&subtype=0`
- **oem** : `rtsp://HOST:554/live`
- **hikvision_sub** : `rtsp://HOST:554/h264/ch1/main/av_stream`

### Snapshot
Clic 📸 sur une carte → PNG téléchargé.

## 🔍 Panel 2 — Shodan

Recherche internet-exposed cameras.

```bash
# Via UI
Sidebar → Shodan
Query: "Hikvision" country:CA port:554
Search

# Via API
curl -X POST http://localhost:8082/shodan/search \
  -H 'Content-Type: application/json' \
  -d '{"query":"webcamxp country:CA"}'
```

⚠️ **API key requise.** Ajoute dans `.env` ou variable d'env :
```bash
export SHODAN_API_KEY=YOUR_KEY
```

## 📡 Panel 3 — ONVIF

WS-Discovery multicast.

```bash
# Via UI
Sidebar → ONVIF
Subnet: 10.0.0.0/24
DISCOVER

# Via API
curl -X POST http://localhost:8082/onvif/discover \
  -H 'Content-Type: application/json' \
  -d '{"subnet":"10.0.0.0/24","timeout":5}'
```

Sortie : liste devices avec :
- IP
- XAddrs (endpoints ONVIF)
- Manufacturer
- Model
- Firmware
- Serial

### Probe individuel

```bash
curl -X POST http://localhost:8082/onvif/probe \
  -H 'Content-Type: application/json' \
  -d '{"ip":"10.0.0.77"}'
```

## 🔌 Panel 4 — PortScan

Scanner async.

```bash
# Via UI
Sidebar → PortScan
Target IP: 10.0.0.77
Ports: 80,443,554,8899,37777,8080,9527,34567
SCAN

# Via API
curl -X POST http://localhost:8082/scan/ports \
  -H 'Content-Type: application/json' \
  -d '{"target":"10.0.0.77","ports":[80,443,554,8899,37777,8080,9527,34567]}'
```

Ports caméra courants :
- **554** : RTSP
- **80/443** : HTTP/HTTPS admin
- **8899** : Hikvision SADP
- **37777** : Dahua
- **8080** : OEM/HTTP alt
- **9527** : HiSilicon backdoor
- **34567** : Dahua RTSP alt

## 🎬 Panel 5 — RTSP Brute

55 paths RTSP testés.

```bash
# Via UI
Sidebar → RTSP Brute
Target IP: 10.0.0.77
BRUTE

# Via API
curl -X POST http://localhost:8082/rtsp/brute \
  -H 'Content-Type: application/json' \
  -d '{"ip":"10.0.0.77","port":554,"user":"admin","pass":"12345"}'
```

Paths testés :
- `/Streaming/Channels/101`
- `/Streaming/Channels/1`
- `/cam/realmonitor`
- `/live`
- `/h264/ch1/main/av_stream`
- `/mpeg4/ch1/main/av_stream`
- `/onvif/streaming/channels/101`
- ... (48 autres)

## 🔎 Panel 6 — Discovery

Agrège résultats de tous les recon panels.

Vue : tableau tous devices + statut.

## 🔑 Panel 7 — Credentials

Cracked creds table.

Colonnes : IP · Port · User · Pass · Device · Brand

```bash
# Export
Sidebar → Credentials → EXPORT CSV
```

## 💣 Panel 8 — Exploitation

Vecteurs connus :

| Brand | Vector | CVE |
|-------|--------|-----|
| Hikvision | Web command injection | CVE-2021-36260 |
| Dahua | RPC2_Login bypass | - |
| HiSilicon | Backdoor | - |

```bash
# Lancement via shell (après creds)
curl http://admin:@10.0.0.77/ISAPI/System/Network/interfaces
```

## 🐚 Panel 9 — Shells

Quick command executor (post-exploit).

## ♾️ Persistence + Payload Generator

Crée `persist.sh` et `cleaner.sh`.

## 📋 Console + Report

### Console
Tous les events en live.

### Report
Export JSON avec :
- Timestamp
- Operator
- Targets
- Creds
- Exploited
- Streams
- Persistence

```bash
Sidebar → Report → EXPORT JSON
```

## 🎯 Workflow mission complet

### Étape 1 — Recon passive
```
1. Shodan : query cameras dans scope
2. ONVIF discover : broadcast WS-Discovery
3. Résultat : liste devices
```

### Étape 2 — Recon active
```
1. PortScan sur chaque device
2. RTSP Brute pour trouver streams
3. Identification brand/model/firmware
```

### Étape 3 — Credential access
```
1. Default creds (admin/12345/admin/etc)
2. Dictionary brute (rockyou.txt)
3. CVE-2021-36260 si Hikvision
```

### Étape 4 — Exploitation
```
1. RCE via CVE si applicable
2. Reverse shell
3. Listener port 4444
```

### Étape 5 — Persistence
```
1. Cron job reverse shell
2. init.d / systemd service
3. Watchdog (auto-reconnect)
```

### Étape 6 — Report
```
1. Export JSON toutes les données
2. OPSEC : zero trace cleaner
3. Chiffrement GPG du rapport
```

## 🛠️ Commandes utiles

### Kill zombie
```bash
pkill -f ghosteye_proxy
```

### Voir logs
```bash
tail -f ghosteye.log
```

### Restart
```bash
pkill -f ghosteye_proxy
python3 ghosteye_proxy.py 8082 &
```

### Backup config
```bash
cp -r ghosteye ~/backup/ghosteye-$(date +%F)
```

## 🔒 OPSEC

- ✅ Utilise VPN/Tor avant scan
- ✅ Change LPORT à chaque mission
- ✅ Pas de logs sur cible
- ✅ cleaner.sh après mission
- ✅ Rapports chiffrés GPG

## 🆘 Help

Touche `?` dans l'app → help overlay détaillé.

---

🏴‍☠️ **ghost1o1** — *"There is no lock."*
