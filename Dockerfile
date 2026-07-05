FROM python:3.12-slim

LABEL maintainer="ghost1o1 <ghost1o1@proton.me>"
LABEL description="GHOSTEYE - RTSP/HLS Camera Pentest Platform - L'EVEIL NOCTURNE"
LABEL version="12.0"

ENV PORT=8082
ENV PYTHONUNBUFFERED=1

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy proxy + dashboard
COPY ghosteye_proxy.py .
COPY index.html .

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/health', timeout=3).read()" || exit 1

EXPOSE ${PORT}

# Run as non-root
RUN useradd -m -u 1000 ghost1o1 && chown -R ghost1o1:ghost1o1 /app
USER ghost1o1

CMD ["python3", "ghosteye_proxy.py", "8082"]
