""""
Based on https://github.com/tranxuanthang/lrcget.git

This script will take an audio file path, search for synced lyrics on lrclib.net and save them to a lrc file.

"""

# -*- coding: utf-8 -*-
import requests
import os
import ffmpeg
import argparse
from time import sleep as wait

# Initialize parser
parser = argparse.ArgumentParser(
    prog="lrc-get",
    description="Fetches lyrics from lrc-lib.net and saves them to a lrc file.",

)

# Adding optional argument
parser.add_argument("-i", "--input", help="Input folder", required=True)
parser.add_argument("-o", "--output", help="Output folder", required=False)
parser.add_argument(
    "-r", "--replace", help="replace existing LRC files", required=False, action="store_true")

# Read arguments from command line
args = parser.parse_args()


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
    # Help I don't even understand python
    try:
        res = requests.get(lrcLib, params=params)
        res.raise_for_status()

    except requests.exceptions.HTTPError as err:
        try:
            # Try with explicit
            res = requests.get(lrcLib, params=paramsExplicit)
            print(
                "Using explicit fallback for: {} - {}, by {}".format(title, album, artist))
        except requests.exceptions.HTTPError as err:
            print(err)  # In case of error the error will be printed
            return

    finally:
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
# Main code starts here


print("Scanning: " + args.input)
if args.replace:
    print("Replacing existing lrc files")
else:
    print("Skipping existing lrc files")

wait(2)

filesWithLRC = list()


def checkLRC(file):
    # check for existing lrc file and replace the file if it exists and the user wants to replace
    if (os.path.splitext(file)[1] == ".lrc" or (os.path.splitext(file)[0] in filesWithLRC)):

        filesWithLRC.append(os.path.splitext(file)[0])  # Append file to list

        if args.replace:  # Check if user wants to replace existing lrc
            return False
        else:
            return True
    else:
        return False


os.chdir(args.input)

filesFolder = [f for f in os.listdir(os.curdir)]

for x in filesFolder:
    # replace scanning of lrc files
    if checkLRC(x):
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
        except:  # If no metadata found, replace the file
            continue

    # Search for lyrics using the data read before
    syncedLyrics = fetch_lyrics(artist, title, album, duration)

    # Replace file extension with .lrc

    if args.output:
        fileName = args.output + "\\" + \
            x.replace(os.path.splitext(x)[1], ".lrc")
    else:
        fileName = x.replace(os.path.splitext(x)[1], ".lrc")

    # Save lyrics to a file
    if syncedLyrics is not None:  # Check if lyrics were found
        with open(fileName, "w", encoding="utf-8") as text_file:
            text_file.write(syncedLyrics)
            text_file.close()
