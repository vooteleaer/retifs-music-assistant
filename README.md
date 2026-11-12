# retifs for Music Assistant

A [Music Assistant](https://music-assistant.io) music provider for [retifs](https://github.com/vooteleaer/retifs): your music in a retifs library, encrypted and kept on your own devices and nodes, played on any of Music Assistant's players.

> A demo app of [retifs](https://github.com/vooteleaer/retifs), part of its test release. To try retifs, start with [getting started](https://github.com/vooteleaer/retifs/blob/main/docs/getting-started.md).

## What it does

- **Lists the library without fetching audio.** Every audio record is a track; artists and albums come from the attributes retifs' extractor reads from the files (`audio.title`, `audio.artist`, `audio.album`, `audio.track`, `audio.year`, `audio.genre`, `duration`). Where those are missing, from the folders: `Artist/Album (Year)/NN - Title.ext`, discs as `1-01` or `CD1/`.
- **Plays from wherever the pieces are.** A track is read in pieces from retifsd; pieces not on this node yet are fetched from the library's other nodes as it plays. A lazy library plays without being copied whole.
- **Follows changes.** A live query: a track added on any device appears in Music Assistant.
- **Favourites are retifs' own** (`favorite = true` on the record, as in every retifs app), so they're the same on every device.
- **Covers live in retifs.** An album's cover is the image in its folder (`cover.jpg`, `folder.jpg`, `front.*`). A cover Music Assistant finds for an album without one is written into the library there (`source = music-assistant`), so every device and every retifs app has it, without the internet.

## Install

Music Assistant loads every folder in its `providers/` with a `manifest.json`: mount `provider/retifs` there, and give the container retifsd's app socket.

1. retifsd with a second app socket in a folder of its own, so the container sees nothing else of the store:
   `retifsd --app-socket /srv/retifs-apps/apps.sock` (or `app_socket` under `[node]` in `retifs.toml`).
2. A token for Music Assistant, allowed only the music library (write: favourites and covers):
   `retifs app add music-assistant --ns music --write`
3. Mounts for the Music Assistant container:
   - `/srv/retifs-apps` → `/retifs`
   - `provider/retifs` → `/app/venv/lib/python3.14/site-packages/music_assistant/providers/retifs` (read-only)
4. In Music Assistant: Settings → Providers → Add → retifs: the socket (`/retifs/apps.sock`), the token, the library.

Built and tested against Music Assistant 2.10.9.

## Develop

`dev/` runs it all in Docker, shaped like a NAS setup: Reticulum (Python `rnsd`, offline), retifsd and Music Assistant 2.10.9.

```sh
sh dev/build.sh                                   # retifsd etc. from ../retifs into dev/retifs/bin (Linux/WSL)
docker compose -f dev/compose.yaml up -d --build
docker compose -f dev/compose.yaml exec retifs sh /work/make-test-music.sh
docker compose -f dev/compose.yaml exec retifs sh -c 'retifs app add music-assistant --ns music --write'
python dev/ma-setup.py TOKEN                      # first user, then the provider
python dev/ma-check.py                            # library, covers, a preview stream
```

## License

MIT, as retifs.
