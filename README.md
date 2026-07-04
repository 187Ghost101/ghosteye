# 👁 GHOSTEYE v12.0 — NOCTURNE

> **"There is no lock."** — **ghost1o1**

Plateforme de **pentest caméra IP** : RTSP/HLS streaming + reconnaissance (Shodan, ONVIF, port scan, RTSP brute) + exploitation. 9 panels, proxy Python asyncio, installateur universel.

```
GHOSTEYE v12.0 NOCTURNE
   ╔═══════════════════════════════════════╗
   ║  9 PANELS · 5 RECON ENDPOINTS         ║
   ║  HLS STREAMING · ONVIF · RTSP BRUTE   ║
   ╚═══════════════════════════════════════╝
```

## ⚡ Aperçu

| Spec | Valeur |
|------|--------|
| **Version** | 12.0 "NOCTURNE" |
| **Dashboard** | 58 KB (single-file HTML) |
| **Proxy** | 21 KB Python (asyncio) |
| **Dépendances** | Python 3.10+ · ffmpeg |
| **CDN** | 0 (HLS natif browser) |
| **Télémétrie** | 0 |
| **Compatibilité** | Kali / Debian / Ubuntu / macOS / Termux |

## 🎯 9 panels

1. **Streams** — HLS live viewer multi-caméras
2. **Shodan** — recherche internet-exposed
3. **ONVIF** — WS-Discovery multicast + GetDeviceInformation
4. **PortScan** — scanner async (tous ports)
5. **RTSP Brute** — 55 paths courants
6. **Discovery** — résultats agrégés
7. **Credentials** — creds crackées
8. **Exploitation** — vecteurs + shells
9. **Persistence** + **Payloads** + **Console** + **Report**

## 🔌 5 endpoints proxy

| Method | Endpoint | Rôle |
|--------|----------|------|
| `GET`  | `/` | Dashboard HTML |
| `GET`  | `/health` | Status JSON |
| `POST` | `/add` | Ajouter stream RTSP |
| `GET`  | `/streams` | Liste streams |
| `DELETE` | `/stream/{id}` | Stop stream |
| `GET`  | `/{id}/stream.m3u8` | HLS playlist |
| `GET`  | `/{id}/seg_XXX.ts` | HLS segments |
| `POST` | `/onvif/discover` | WS-Discovery multicast |
| `POST` | `/onvif/probe` | GetDeviceInformation SOAP |
| `POST` | `/scan/ports` | Scanner `{ip, ports}` |
| `POST` | `/rtsp/brute` | 55 paths `{ip}` |
| `POST` | `/shodan/search` | Shodan query |

## 🎨 Design

Norme **GHOST1O1 Nocturne** v1.1 :
- Aurora mesh violet/cyan/magenta
- Glassmorphism + 3D tilt
- Watermark 5-layer + corner stamp

## 📦 Installation

Voir [INSTALL.md](INSTALL.md).

Quick start :
```bash
git clone https://github.com/187Ghost101/ghosteye.git
cd ghosteye
sudo apt install ffmpeg python3-pip  # ou brew install ffmpeg
chmod +x install.sh ghosteye_proxy.py
./install.sh
python3 ghosteye_proxy.py
# Ouvre http://localhost:8082
```

## 📖 Utilisation

Voir [USAGE.md](USAGE.md).

Workflow mission :
1. **Recon** : Shodan → ONVIF → PortScan → RTSP Brute
2. **Creds** : Brute force dictionnaire
3. **Exploit** : CVE-2021-36260 / RPC2 bypass
4. **Shell** : reverse shell
5. **Persist** : cron + init.d
6. **Report** : export JSON

## 🔒 Usage autorisé uniquement

⚠️ GHOSTEYE est destiné aux **pentests autorisés** et **red team**. Obtiens une **autorisation écrite** avant tout scan.

## 📂 Structure

```
ghosteye/
├── index.html              # 58 KB — dashboard v12.0
├── ghosteye_proxy.py       # 21 KB — proxy asyncio
├── install.sh              # installateur universel
├── ghost1o1.css            # design system
├── ghost1o1.js             # JS shared
├── README.md
├── INSTALL.md
├── USAGE.md
└── GHOST1O1_BRAND.md
```

---

**© 2026 ghost1o1 · GHOST1O1 Nocturne v1.1**
