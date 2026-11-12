"""Gives an album in the dev Music Assistant a cover of Music Assistant's own (a
generated PNG as a data URI), as its metadata providers would from the
internet: the provider should then copy it into retifs.

    python dev/ma-give-cover.py "Shoreline" [http://localhost:8095]
"""

import base64
import io
import json
import sys
import urllib.request

from PIL import Image

NAME = sys.argv[1]
BASE = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8095"


def post(path, body, auth=None):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **({"Authorization": f"Bearer {auth}"} if auth else {})})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read() or b"null")


def api(command, args, auth):
    return post("/api", {"message_id": "1", "command": command, "args": args}, auth)


auth = post("/auth/login", {"credentials": {"username": "dev", "password": "retifs-dev-password"}}).get("token")
albums = api("music/albums/library_items", {"limit": 50}, auth)
albums = albums.get("items", albums) if isinstance(albums, dict) else albums
album = next(a for a in albums if a["name"] == NAME)
buf = io.BytesIO()
Image.new("RGB", (300, 300), (200, 80, 40)).save(buf, "PNG")
uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
album.setdefault("metadata", {})["images"] = [{"type": "thumb", "path": uri, "provider": "builtin", "remotely_accessible": False}]
r = api("music/albums/update", {"item_id": album["item_id"], "update": album, "overwrite": False}, auth)
print("updated:", r.get("name"), [i["provider"] for i in (r.get("metadata") or {}).get("images") or []])
