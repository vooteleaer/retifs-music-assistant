#!/bin/sh
# retifsd with a second app socket in /apps (shared with Music Assistant,
# which sees nothing else of the store), and the extractor for $EXTRACT_NS.
set -e
mkdir -p "$RETIFS_STORE" /apps
retifsd --store "$RETIFS_STORE" --no-mounts --app-socket /apps/apps.sock &
pid=$!
i=0
until retifs ping >/dev/null 2>&1; do
    i=$((i + 1)); [ $i -gt 120 ] && { echo "retifsd didn't come up"; exit 1; }
    sleep 1
done
echo "retifsd is up: $(retifs ping 2>&1 | head -1)"
if [ -n "$EXTRACT_NS" ]; then
    T="$RETIFS_STORE/extract.token"
    if [ ! -s "$T" ]; then
        for ns in $(echo "$EXTRACT_NS" | tr ',' ' '); do retifs ns info "$ns" >/dev/null 2>&1 || retifs ns address "$ns" >/dev/null; done
        retifs app add extract --ns "$EXTRACT_NS" --write \
            --keys "mime,width,height,taken,camera,geo,duration,exif.*,audio.*,doc.*,block:*,@content,type,extracted" > "$T"
    fi
    retifs-extractd --token-file "$T" &
fi
wait $pid
