""""
Based on https://github.com/tranxuanthang/lrcget.git

This script will take an audio file path, search for synced lyrics on lrclib.net and save them to a lrc file.

"""

# -*- coding: utf-8 -*-
import requests
import os
import ffmpeg


def fetch_lyrics(artist, title, album, totalsec):
    lrcLib = 'https://lrclib.net/api/get'

    params = dict(artist_name=artist,
                  track_name=title,
                  album_name=album,
                  duration=totalsec,)

    paramsExplicit = dict(artist_name=artist,
                          track_name=title+" (Explicit)",
                          album_name=album,
                          duration=totalsec,)
    # HTTP request error handling and explicit fallback
    try:
        res = requests.get(lrcLib, params=params)
        res.raise_for_status()

    except requests.exceptions.HTTPError as err:
        try:
            # Try with explicit
            res = requests.get(lrcLib, params=paramsExplicit)
        except requests.exceptions.HTTPError as err:
            print(err)  # In case of error the error will be printed

    # In case of no errors the main code will execute

    else:
        if res.json()["plainLyrics"] == None:
            print("Lyrics not available for: {} - {}, by {}".format(
                title, album, artist))
            return

        syncedLyrics = res.json()["syncedLyrics"]

        if syncedLyrics is None:
            print("Synced lyrics not found for: {} - {}, by {}".format(
                title, album, artist))
        else:
            print("Lyrics found for: {} - {}, by {}".format(title, album, artist))
            return syncedLyrics

# -----------------------------------------------------------------------------------


workingFolder = input("Enter audio folder: ")
os.chdir(workingFolder)


filesFolder = [f for f in os.listdir(os.curdir)]

for x in filesFolder:
    # Skip scanning of lrc files
    if os.path.splitext(x)[1] == ".lrc":
        continue

    # Read metadata from audio file using ffprobe
    try:  # Check for metadata found in m4a files
        audioTags = ffmpeg.probe(x)["format"]["tags"]
        artist = audioTags["artist"]
        title = audioTags["title"]
        album = audioTags["album"]
        duration = str(round(float(ffmpeg.probe(x)["format"]["duration"])))
    except:
        try:  # Check for metadata found in flac files
            artist = audioTags["ARTIST"]
            title = audioTags["TITLE"]
            album = audioTags["ALBUM"]
            duration = str(round(float(ffmpeg.probe(x)["format"]["duration"])))
        except:  # If no metadata found, skip the file
            continue

    # Search for lyrics using the data read before
    syncedLyrics = fetch_lyrics(artist, title, album, duration)

    # Replace file extension with .lrc
    fileName = x.replace(os.path.splitext(x)[1], ".lrc")

    # Save lyrics to a file
    if syncedLyrics is not None:  # Check if lyrics were found
        with open(fileName, "w", encoding="utf-8") as text_file:
            text_file.write(syncedLyrics)
            text_file.close()
