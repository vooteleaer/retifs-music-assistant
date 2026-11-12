#!/bin/sh
# A few short tagged tracks (sine tones) in library `music` of the dev
# retifsd, laid out as Artist/Album (Year)/NN - Title.ext, plus one album
# with no tags at all (named only by its folders) and one without a cover.
#   docker compose -f dev/compose.yaml exec retifs sh /work/make-test-music.sh
set -e
W=$(mktemp -d)
tone() { # file freq title artist album albumartist track year genre
    ffmpeg -loglevel error -f lavfi -i "sine=frequency=$2:duration=20" -ac 2 \
        -metadata title="$3" -metadata artist="$4" -metadata album="$5" -metadata album_artist="$6" \
        -metadata track="$7" -metadata date="$8" -metadata genre="$9" "$1"
}
add() { retifs rec add music "path=$2" --file "$1" >/dev/null && echo "added $2"; }
tone "$W/a1.flac" 440 "Morning" "Test Artist" "First Light" "Test Artist" 1 2024 Ambient
tone "$W/a2.flac" 494 "Noon" "Test Artist" "First Light" "Test Artist" 2 2024 Ambient
tone "$W/a3.flac" 523 "Evening" "Test Artist feat. Guest" "First Light" "Test Artist" 3 2024 Ambient
tone "$W/b1.mp3" 330 "Low Tide" "Second Band" "Shoreline" "Second Band" 1 2019 Rock
tone "$W/b2.mp3" 392 "High Tide" "Second Band" "Shoreline" "Second Band" 2 2019 Rock
ffmpeg -loglevel error -f lavfi -i "sine=frequency=262:duration=15" -ac 2 "$W/c1.ogg"
ffmpeg -loglevel error -f lavfi -i "color=c=teal:s=600x600:d=1" -frames:v 1 "$W/cover.jpg"
add "$W/a1.flac" "/Test Artist/First Light (2024)/01 - Morning.flac"
add "$W/a2.flac" "/Test Artist/First Light (2024)/02 - Noon.flac"
add "$W/a3.flac" "/Test Artist/First Light (2024)/03 - Evening.flac"
add "$W/cover.jpg" "/Test Artist/First Light (2024)/cover.jpg"
add "$W/b1.mp3" "/Second Band/Shoreline (2019)/01 - Low Tide.mp3"
add "$W/b2.mp3" "/Second Band/Shoreline (2019)/02 - High Tide.mp3"
add "$W/c1.ogg" "/Untagged Folk/Field Recordings (2001)/1-01 Birdsong.ogg"
rm -rf "$W"
