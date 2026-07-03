# GHOSTEYE v12.0 — NOCTURNE

> **"There is no lock."** — *ghost1o1*

The avant-garde camera & IoT pentest dashboard. HLS live streaming · ONVIF · PortScan · RTSP Brute · Shodan · Exploit tracking · Shell console · Persistence generator.

![version](https://img.shields.io/badge/version-v12.0-e3063e?style=for-the-badge)
![license](https://img.shields.io/badge/license-educational-a855f7?style=for-the-badge)
![deps](https://img.shields.io/badge/dependencies-0-00f3ff?style=for-the-badge)
![design](https://img.shields.io/badge/design-GHOST1O1%20Nocturne-ec4899?style=for-the-badge)

## 9 panels

- **Streams** — HLS live camera feeds (4-grid)
- **Shodan** — internet-wide device search
- **ONVIF** — WS-Discovery + SOAP probe
- **PortScan** — Nmap-style async scanner (camera presets)
- **RTSP Brute** — 55 common RTSP paths
- **Discovery** — device summary + scan results
- **Credentials** — cracked/default fingerprint DB
- **Exploitation** — CVE library + auto-pivot
- **Shells** — WebSocket + reverse TCP console
- **Persistence** — payload generator (persist/cleaner/recon/privesc)
- **Payloads Library** — 12 ready-to-deploy scripts
- **Console** — live event log
- **Report** — JSON/HTML export

## Design — Nocturne Cipher

Aurora mesh · glassmorphism · 3D tilt · particles · cursor glow · **GHOST1O1 signature anchored 5 layers deep**.

| Layer | Where | Visibility |
|-------|-------|-----------|
| 1. Watermark bg | Repeating | Atmosphere |
| 2. Brand mark "G1" | Nav, sidebar | Visible |
| 3. Sig block | About, splash | Hero |
| 4. Sig inline | Topbar, footer, cards | Always |
| 5. Sig glow | Hero, dramatic | Animated |

## Install

```bash
# One command (from this repo)
git clone https://github.com/ghost1o1/ghosteye.git
cd ghosteye
bash install.sh
bash ~/ghosteye/launch.sh
```

Then open: **http://localhost:8082**

## Pre-req

```bash
sudo apt install ffmpeg python3
```

## Diagnostic history

- v6.1 (2026-07-02): button handlers not triggering → **FIXED in v12.0** by using `DOMContentLoaded` listener + checking `document.readyState` + removing all external CDN dependencies.

## Stack

- HTML5 · CSS3 · vanilla JS (no React/Vue/jQuery)
- Python 3.12 · asyncio stdlib
- ffmpeg for HLS transcoding
- 0 CDN · 0 telemetry · 100% local

## License

Educational use only. © 2026 ghost1o1.
