# GHOSTEYE — Image Docker officielle
# Usage: docker run -d -p 8082:8082 --name ghosteye 187ghost101/ghosteye
FROM python:3.12-slim

LABEL maintainer="ghost1o1"
LABEL description="GHOSTEYE v3.0 — RTSP/HLS camera pentest platform"
LABEL version="3.0"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 ghost && mkdir -p /app && chown -R ghost:ghost /app
WORKDIR /app
USER ghost

# Copy application
COPY --chown=ghost:ghost ghosteye.html ghosteye_proxy.py ./

# Expose port
EXPOSE 8082

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8082/health', timeout=2)" || exit 1

# Default command
CMD ["python3", "ghosteye_proxy.py", "8082"]
