#!/usr/bin/env python3
"""
GHOSTEYE Proxy v12.0 — NOCTURNE
RTSP → HLS streaming + Recon endpoints (Shodan/ONVIF/PortScan/RTSP Brute)
ghost1o1 · "There is no lock."
"""
import asyncio
import subprocess
import sys
import json
import struct
import os
import hashlib
import base64
import shutil
import socket
import ipaddress
import urllib.request
import urllib.parse
import time
import re
from concurrent.futures import ThreadPoolExecutor

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8082
HOST = "0.0.0.0"

streams = {}
executor = ThreadPoolExecutor(max_workers=8)

RTSP_PATHS = [
    "/Streaming/Channels/101", "/Streaming/Channels/102",
    "/Streaming/Channels/201", "/Streaming/Channels/202",
    "/h264/ch1/main/av_stream", "/h264/ch1/sub/av_stream",
    "/cam/realmonitor?channel=1&subtype=0", "/cam/realmonitor?channel=1&subtype=1",
    "/live", "/live/main", "/live/sub", "/live/0", "/live/1",
    "/11", "/12", "/13", "/14", "/15",
    "/mpeg4", "/mpeg4cif", "/h264", "/h264if",
    "/onvif/streaming/channels/101", "/onvif/streaming/channels/102",
    "/trackID=1", "/trackID=2",
    "/av0_0", "/av0_1", "/av0_2",
    "/video1", "/video2", "/videoinput_1", "/videoinput_2",
    "/MediaInput/h264", "/MediaInput/mpeg4",
    "/ch01.264", "/ch02.264", "/ch01.sdp", "/ch02.sdp",
    "/PSIA/Streaming/channels/101", "/PSIA/Streaming/channels/102",
    "/stream1", "/stream2",
    "/1/h264/main", "/1/h264/sub",
    "/0/usrnm:pwd/0", "/0/usrnm:pwd/1",
    "/cam0_0", "/cam0_1",
    "/h264/ch0/main/av_stream", "/h264/ch0/sub/av_stream",
    "/img/video.sav", "/img/main.sav",
    "/bystream/averrtsp.stream", "/bystream/averrtsp-1.stream",
    "/live/ch00_0", "/live/ch01_0",
    "/ch0_0", "/ch0_1",
]

CAMERA_PORTS = [21, 22, 23, 25, 53, 80, 81, 88, 110, 111, 135, 139, 143, 161, 389, 443,
                445, 554, 587, 631, 873, 902, 989, 990, 993, 995, 1080, 1194, 1433, 1521,
                1723, 1883, 1900, 2000, 2049, 2082, 2083, 2086, 2087, 2095, 2096,
                2222, 2375, 2376, 3000, 3306, 3389, 3690, 4000, 4444, 4567, 4842,
                5000, 5060, 5222, 5432, 5672, 5900, 5984, 6379, 6443, 7000, 7474,
                8000, 8001, 8008, 8009, 8080, 8081, 8082, 8083, 8086, 8088, 8089,
                8090, 8091, 8443, 8500, 8883, 8888, 9000, 9001, 9042, 9092, 9100,
                9200, 9300, 9443, 11211, 15672, 26379, 27017, 27018, 27019, 28017, 50000]

DAHUA_PORTS = [37777, 37778, 37779, 34567, 34599, 34568]
HIKVISION_PORTS = [8899, 8000, 9527, 10510, 10000]

# ─────────────────────────────────────────────────────────────────
# RTSP/HLS STREAMING
# ─────────────────────────────────────────────────────────────────
async def stream_websocket(reader, writer, path):
    stream_id = path.strip("/")
    rtsp_url = streams.get("urls", {}).get(stream_id)
    if not rtsp_url:
        writer.close()
        return
    if not shutil.which("ffmpeg"):
        writer.close()
        return
    if stream_id not in streams:
        proc = subprocess.Popen(
            ["ffmpeg", "-loglevel", "quiet", "-rtsp_transport", "tcp",
             "-i", rtsp_url, "-f", "hls", "-hls_time", "2",
             "-hls_list_size", "3", "-hls_flags", "delete_segments",
             "-hls_segment_filename", f"/tmp/ghosteye_{stream_id}_%03d.ts",
             f"/tmp/ghosteye_{stream_id}.m3u8"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        streams[stream_id] = {"url": rtsp_url, "proc": proc, "clients": []}
    streams[stream_id]["clients"].append(writer)
    print(f"[+] WS client → {stream_id} ({rtsp_url}) [{len(streams[stream_id]['clients'])} clients]")


async def handle_client(reader, writer):
    data = await reader.read(8192)
    headers_text = data.decode(errors="ignore")
    lines = headers_text.split("\r\n")
    first_line = lines[0] if lines else ""

    if "Upgrade: websocket" in headers_text.lower():
        try:
            key = next((l.split(":", 1)[1].strip() for l in lines if l.lower().startswith("sec-websocket-key:")), None)
            if not key:
                writer.close()
                return
            accept = base64.b64encode(hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()).decode()
            writer.write(f"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: {accept}\r\n\r\n".encode())
            await writer.drain()
            get_line = next((l for l in lines if l.startswith("GET")), "")
            path = get_line.split()[1].strip("/") if get_line else ""
            await stream_websocket(reader, writer, path)
        except Exception as e:
            print(f"[-] WS error: {e}")
            writer.close()
        return

    if first_line.startswith("OPTIONS"):
        writer.write(b"HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\n"
                     b"Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS\r\n"
                     b"Access-Control-Allow-Headers: Content-Type\r\n\r\n")
        await writer.drain()
        writer.close()
        return

    if first_line.startswith("GET /streams"):
        urls = streams.get("urls", {})
        body = json.dumps(urls).encode()
        writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                     b"Content-Length: " + str(len(body)).encode() +
                     b"\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + body)
        await writer.drain()
        writer.close()
        return

    if first_line.startswith("GET /health"):
        body = json.dumps({
            "status": "ok", "version": "12.0", "name": "GHOSTEYE — Nocturne",
            "streams": len(streams.get("urls", {})),
            "uptime": time.time()
        }).encode()
        writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                     b"Content-Length: " + str(len(body)).encode() +
                     b"\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + body)
        await writer.drain()
        writer.close()
        return

    if first_line.startswith("GET /"):
        # Serve ghosteye.html from same dir as proxy
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
        if not os.path.exists(html_path):
            html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ghosteye.html")
        if os.path.exists(html_path):
            with open(html_path, "rb") as f:
                content = f.read()
            writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n"
                         b"Content-Length: " + str(len(content)).encode() +
                         b"\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + content)
        else:
            err = b"<h1>GHOSTEYE - index.html not found</h1>"
            writer.write(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n" + err)
        await writer.drain()
        writer.close()
        return

    if first_line.startswith("POST /add"):
        await handle_post_add(reader, writer, data)
        return

    if first_line.startswith("DELETE /stream/"):
        sid = first_line.split("/stream/")[1].split(" ")[0].strip()
        if sid in streams:
            streams[sid]["proc"].kill()
            del streams[sid]
        body = json.dumps({"status": "removed", "id": sid}).encode()
        writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                     b"Content-Length: " + str(len(body)).encode() +
                     b"\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + body)
        await writer.drain()
        writer.close()
        return

    if first_line.startswith("POST /onvif/discover"):
        await handle_onvif_discover(reader, writer, data)
        return

    if first_line.startswith("POST /onvif/probe"):
        await handle_onvif_probe(reader, writer, data)
        return

    if first_line.startswith("POST /scan/ports"):
        await handle_scan_ports(reader, writer, data)
        return

    if first_line.startswith("POST /rtsp/brute"):
        await handle_rtsp_brute(reader, writer, data)
        return

    if first_line.startswith("POST /shodan/search"):
        await handle_shodan(reader, writer, data)
        return

    # Catch-all HLS files
    if ".m3u8" in first_line or ".ts" in first_line:
        m = re.search(r"GET /(\S+)", first_line)
        if m:
            file_path = f"/tmp/{m.group(1).split('?')[0]}"
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
                ctype = b"application/vnd.apple.mpegurl" if file_path.endswith(".m3u8") else b"video/mp2t"
                writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: " + ctype +
                             b"\r\nContent-Length: " + str(len(content)).encode() + b"\r\n\r\n" + content)
                await writer.drain()
        else:
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
        writer.close()
        return

    writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n")
    await writer.drain()
    writer.close()


async def handle_post_add(reader, writer, data):
    body_start = data.find(b"\r\n\r\n") + 4
    try:
        payload = json.loads(data[body_start:].decode())
        sid = payload.get("id", f"stream_{len(streams.get('urls', {}))}")
        if "urls" not in streams:
            streams["urls"] = {}
        streams["urls"][sid] = payload["url"]
        print(f"[+] Stream added: {sid} → {payload['url']}")
        body = json.dumps({"status": "ok", "id": sid}).encode()
    except Exception as e:
        body = json.dumps({"status": "err", "error": str(e)}).encode()
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                 b"Content-Length: " + str(len(body)).encode() +
                 b"\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + body)
    await writer.drain()
    writer.close()


# ─────────────────────────────────────────────────────────────────
# RECON ENDPOINTS
# ─────────────────────────────────────────────────────────────────
async def handle_onvif_discover(reader, writer, data):
    body_start = data.find(b"\r\n\r\n") + 4
    try:
        payload = json.loads(data[body_start:].decode())
        subnet = payload.get("subnet", "10.0.0.0/24")
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, _onvif_discover_sync, subnet)
        body = json.dumps(result).encode()
    except Exception as e:
        body = json.dumps({"error": str(e), "devices": []}).encode()
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                 b"Content-Length: " + str(len(body)).encode() +
                 b"\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + body)
    await writer.drain()
    writer.close()


def _onvif_discover_sync(subnet):
    """WS-Discovery probe on each IP in subnet (limited for speed)."""
    devices = []
    try:
        network = ipaddress.ip_network(subnet, strict=False)
    except ValueError:
        return {"devices": [], "error": "Invalid subnet"}
    # Limit to first 64 hosts for speed
    targets = list(network.hosts())[:64]
    # Try ONVIF SOAP probe
    probe_body = """<?xml version="1.0" encoding="utf-8"?>
<Envelope xmlns:dn="http://www.onvif.org/ver10/network/wsdl" xmlns="http://www.w3.org/2003/05/soap-envelope">
<Header><wsa:MessageID xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">uuid:ghosteye</wsa:MessageID>
<wsa:To xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">urn:schemas-xmlsoap-org:ws:2005:04:discovery</wsa:To>
<wsa:Action xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing">http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</wsa:Action></Header>
<Body><Probe xmlns="http://schemas.xmlsoap.org/ws/2005/04/discovery">
<Types>dn:NetworkVideoTransmitter</Types></Probe></Body></Envelope>"""
    for ip in targets:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((str(ip), 80)) == 0:
                s.close()
                try:
                    req = urllib.request.Request(f"http://{ip}:80/onvif/device_service",
                                                 data=probe_body.encode(),
                                                 headers={"Content-Type": "application/soap+xml"})
                    with urllib.request.urlopen(req, timeout=1.5) as r:
                        body = r.read().decode(errors="ignore")
                        if "NetworkVideoTransmitter" in body or "onvif" in body.lower():
                            m = re.search(r"<dd:Scopes[^>]*>(.*?)</dd:Scopes>", body, re.DOTALL)
                            scopes = m.group(1) if m else ""
                            devices.append({"ip": str(ip), "port": 80, "scopes": scopes[:200]})
                except Exception:
                    pass
        except Exception:
            pass
    return {"devices": devices, "count": len(devices), "subnet": subnet}


async def handle_onvif_probe(reader, writer, data):
    body_start = data.find(b"\r\n\r\n") + 4
    try:
        payload = json.loads(data[body_start:].decode())
        ip, port = payload.get("ip"), payload.get("port", 80)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, _onvif_probe_sync, ip, port)
        body = json.dumps(result).encode()
    except Exception as e:
        body = json.dumps({"error": str(e)}).encode()
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                 b"Content-Length: " + str(len(body)).encode() +
                 b"\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + body)
    await writer.drain()
    writer.close()


def _onvif_probe_sync(ip, port):
    soap = """<?xml version="1.0" encoding="utf-8"?>
<Envelope xmlns="http://www.w3.org/2003/05/soap-envelope" xmlns:tds="http://www.onvif.org/ver10/device/wsdl">
<Body><tds:GetDeviceInformation/></Body></Envelope>"""
    try:
        req = urllib.request.Request(f"http://{ip}:{port}/onvif/device_service",
                                     data=soap.encode(),
                                     headers={"Content-Type": "application/soap+xml"})
        with urllib.request.urlopen(req, timeout=3) as r:
            body = r.read().decode(errors="ignore")
            info = {}
            for tag in ("Manufacturer", "Model", "FirmwareVersion", "SerialNumber", "HardwareId"):
                m = re.search(f"<tds:{tag}>(.*?)</tds:{tag}>", body)
                if m: info[tag] = m.group(1)
            return {"status": "ok", "info": info, "raw": body[:500]}
    except Exception as e:
        return {"status": "err", "error": str(e)}


async def handle_scan_ports(reader, writer, data):
    body_start = data.find(b"\r\n\r\n") + 4
    try:
        payload = json.loads(data[body_start:].decode())
        ip, ports = payload.get("ip"), payload.get("ports", CAMERA_PORTS)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, _scan_ports_sync, ip, ports)
        body = json.dumps(result).encode()
    except Exception as e:
        body = json.dumps({"error": str(e), "results": []}).encode()
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                 b"Content-Length: " + str(len(body)).encode() +
                 b"\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + body)
    await writer.drain()
    writer.close()


def _scan_ports_sync(ip, ports):
    def check(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.6)
            r = s.connect_ex((ip, port))
            s.close()
            return (port, "open" if r == 0 else "closed")
        except Exception:
            return (port, "filtered")
    with ThreadPoolExecutor(max_workers=40) as ex:
        results = list(ex.map(check, ports))
    return {"ip": ip, "results": [{"port": p, "state": s} for p, s in results],
            "open": [p for p, s in results if s == "open"],
            "scanned": len(ports)}


async def handle_rtsp_brute(reader, writer, data):
    body_start = data.find(b"\r\n\r\n") + 4
    try:
        payload = json.loads(data[body_start:].decode())
        ip, port, timeout = payload.get("ip"), int(payload.get("port", 554)), float(payload.get("timeout", 3))
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, _rtsp_brute_sync, ip, port, timeout)
        body = json.dumps(result).encode()
    except Exception as e:
        body = json.dumps({"error": str(e), "valid": []}).encode()
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                 b"Content-Length: " + str(len(body)).encode() +
                 b"\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + body)
    await writer.drain()
    writer.close()


def _rtsp_brute_sync(ip, port, timeout):
    def check(path):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((ip, port))
            req = f"OPTIONS rtsp://{ip}:{port}{path} RTSP/1.0\r\nCSeq: 1\r\nUser-Agent: GHOSTEYE/12.0\r\n\r\n"
            s.send(req.encode())
            resp = s.recv(2048).decode(errors="ignore")
            s.close()
            if "RTSP/1.0 200" in resp or "RTSP/1.0 401" in resp:
                return {"path": path, "status": "valid", "code": 200 if "200" in resp else 401}
            return None
        except Exception:
            return None
    with ThreadPoolExecutor(max_workers=10) as ex:
        results = [r for r in ex.map(check, RTSP_PATHS) if r]
    return {"ip": ip, "port": port, "valid": results, "tested": len(RTSP_PATHS)}


async def handle_shodan(reader, writer, data):
    body_start = data.find(b"\r\n\r\n") + 4
    try:
        payload = json.loads(data[body_start:].decode())
        q, key = payload.get("q"), payload.get("key", "")
        if not key:
            body = json.dumps({"error": "Missing Shodan API key", "matches": []}).encode()
        else:
            url = f"https://api.shodan.io/shodan/host/search?key={key}&query={urllib.parse.quote(q)}"
            with urllib.request.urlopen(url, timeout=10) as r:
                data = json.loads(r.read())
            body = json.dumps(data).encode()
    except Exception as e:
        body = json.dumps({"error": str(e), "matches": []}).encode()
    writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                 b"Content-Length: " + str(len(body)).encode() +
                 b"\r\nAccess-Control-Allow-Origin: *\r\n\r\n" + body)
    await writer.drain()
    writer.close()


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║  GHOSTEYE Proxy v12.0 — NOCTURNE                            ║
║  ghost1o1 · "There is no lock."                              ║
╠═══════════════════════════════════════════════════════════════╣
║  Dashboard: http://0.0.0.0:{PORT}                              ║
║  Health:    http://0.0.0.0:{PORT}/health                       ║
╠═══════════════════════════════════════════════════════════════╣
║  Streaming  /add · /streams · DELETE /stream/<id>            ║
║  Recon      /onvif/discover · /onvif/probe                    ║
║             /scan/ports · /rtsp/brute · /shodan/search       ║
╠═══════════════════════════════════════════════════════════════╣
║  Pre-req:   ffmpeg (apt install ffmpeg)                      ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    if not shutil.which("ffmpeg"):
        print("[!] WARNING: ffmpeg not found. Install: apt install ffmpeg")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[-] GHOSTEYE shut down. ghost1o1.")
