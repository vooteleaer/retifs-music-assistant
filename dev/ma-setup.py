"""Sets up the dev Music Assistant over its API: the first user (if none), then
a retifs provider instance with the given token. Prints what it did.

    python dev/ma-setup.py TOKEN [http://localhost:8095]
"""

import json
import sys
import urllib.error
import urllib.request

TOKEN = sys.argv[1]
BASE = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8095"
USER, PASSWORD = "dev", "retifs-dev-password"


def post(path, body, auth=None):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **({"Authorization": f"Bearer {auth}"} if auth else {})})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        return {"http_error": e.code, "body": e.read().decode(errors="replace")[:500]}


def api(command, args, auth):
    return post("/api", {"message_id": "1", "command": command, "args": args}, auth)


r = post("/setup", {"username": USER, "password": PASSWORD, "display_name": "dev"})
if "http_error" in r:
    r = post("/auth/login", {"credentials": {"username": USER, "password": PASSWORD}})
auth = r.get("token") or r.get("access_token")
print("auth:", "ok" if auth else r)
step = api("config/providers/setup", {"provider_domain": "retifs"}, auth)
print("setup step:", json.dumps(step)[:400])
flow = step.get("flow_id")
done = api("config/flows/submit", {"flow_id": flow, "values": {"socket": "/retifs/apps.sock", "token": TOKEN, "library": "music", "save_artwork": True}}, auth)
print("submitted:", json.dumps(done)[:600])
