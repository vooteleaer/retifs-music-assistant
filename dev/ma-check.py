"""Checks the dev Music Assistant through its API: what its library holds from
retifs, an album's image, and a track's audio through the preview stream
(which runs the provider's get_audio_stream through ffmpeg).

    python dev/ma-check.py [http://localhost:8095]
"""

import json
import sys
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8095"
USER, PASSWORD = "dev", "retifs-dev-password"


def post(path, body, auth=None):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **({"Authorization": f"Bearer {auth}"} if auth else {})})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read() or b"null")


def api(command, args, auth):
    return post("/api", {"message_id": "1", "command": command, "args": args}, auth)


auth = post("/auth/login", {"credentials": {"username": USER, "password": PASSWORD}}).get("token")
for kind in ("artists", "albums", "tracks"):
    items = api(f"music/{kind}/library_items", {"limit": 50}, auth)
    items = items.get("items", items) if isinstance(items, dict) else items
    print(f"{kind}: {len(items)}")
    for it in items:
        imgs = (it.get("metadata") or {}).get("images") or []
        extra = ""
        if kind == "tracks":
            extra = f" #{it.get('track_number')} {it.get('duration')}s album={((it.get('album') or {}).get('name'))} artists={[a['name'] for a in it.get('artists', [])]}"
        if kind == "albums":
            extra = f" ({it.get('year')}) by {[a['name'] for a in it.get('artists', [])]}"
        print(f"   {it['name']}{extra} images={[(i['provider'][:10], i['path'][:12]) for i in imgs]}")
tracks = api("music/tracks/library_items", {"limit": 50}, auth)
tracks = tracks.get("items", tracks) if isinstance(tracks, dict) else tracks
t = tracks[0]
m = next(m for m in t["provider_mappings"] if m["provider_domain"] == "retifs")
url = api("music/tracks/preview", {"provider_instance_id_or_domain": m["provider_instance"], "item_id": m["item_id"]}, auth)
full = url if url.startswith("http") else BASE + url
with urllib.request.urlopen(full, timeout=120) as r:
    data = r.read()
print(f"preview of {t['name']}: {len(data)} bytes, starts {data[:4]!r} ({r.headers.get('Content-Type')})")
