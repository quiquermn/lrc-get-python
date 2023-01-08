""""
Based on https://github.com/tranxuanthang/lrcget.git

This script will take an audio file path, search for synced lyrics on lrclib.net and print them to the console.

"""


import requests
import audioread
import audio_metadata

lrcLib = 'https://lrclib.net/api/get'
audio = input("Enter music file path: ")

with audioread.audio_open(audio) as f:

    # totalsec contains the length in float
    totalsec = f.duration

metadata = audio_metadata.load(audio)
tags = metadata["tags"]
artist = tags["artist"][0]
album = tags["album"][0]
title = tags["title"][0]


print("Searching for: " + artist + ", " + album + ", " + title)

params = dict(artist_name=artist,
              track_name=title,
              album_name=album,
              duration=totalsec,)
res = requests.get(lrcLib, params=params)

# print(res.json())

if res.json()["plainLyrics"] == None:
    print("Lyrics not found")
    exit()

syncedLyrics = res.json()["syncedLyrics"]

if syncedLyrics is None:
    print("Synced lyrics not found")

    if input("Press Y to search for lyrics without sync: ") == "Y" or "y":
        print(res.json()["plainLyrics"])
else:
    print(syncedLyrics)
