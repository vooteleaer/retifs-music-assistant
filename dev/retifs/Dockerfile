# retifsd for the dev setup, from binaries built for Linux x86_64 (copied
# into bin/ by dev/build.sh). Joins the rns container's shared instance: the
# compose file puts both in one network namespace.
FROM debian:trixie-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates ffmpeg && rm -rf /var/lib/apt/lists/*
COPY bin/ /usr/local/bin/
COPY entry.sh /entry.sh
ENV RETIFS_STORE=/data/store
CMD ["sh", "/entry.sh"]
