from pathlib import Path
import get_file_metadata
import requests


def get_lyrics(artist, title, album, duration):
    lrc_lib = 'https://lrclib.net/api/get'

    try:
        # Try fetching lrc-lib with regular title
        res = requests.get(lrc_lib, params={'artist_name': artist,
                                            'track_name': title,
                                            'album_name': album,
                                            'duration': duration})
        res.raise_for_status()
        return res.json()["syncedLyrics"]
    except requests.exceptions.HTTPError:
        try:
            # If failed, try reaching with explicit title
            res = requests.get(lrc_lib, params={'artist_name': artist,
                                                'track_name': title + " (Explicit)",
                                                'album_name': album,
                                                'duration': duration})
            res.raise_for_status()
            return res.json()["syncedLyrics"]
        except requests.exceptions.HTTPError:
            # If everything fails, return None
            return None


def main():
    # Initialize arguments
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument("-i", "--input", help="Input folder", required=True)
    parser.add_argument("-o", "--output", help="Output folder", required=False)
    parser.add_argument("-r", "--replace", help="Replace existing LRC files", required=False, action="store_true")
    args = parser.parse_args()

    replace = args.replace
    input_folder = args.input
    output_folder = args.output
    # Finished initializing arguments

    files_iterdir = Path(input_folder).iterdir()
    files_list = list()
    lrc_list = list()

    for file in files_iterdir:  # Scans the input folder for files and adds them to a list depending on the file type
        if file.is_file() and file.suffix != ".lrc":
            files_list.append(file)
        elif file.is_file() and file.suffix == ".lrc":
            lrc_list.append(file.stem)

    for file in files_list:
        if file.stem in lrc_list and not replace:
            # If file already has a lyrics file and replace is False, skip
            print("Lyrics already exist for: {}, skipping".format(file))
        else:
            # If file doesn't have a lyrics file or replace is True, get lyrics
            metadata = get_file_metadata.try_get_metadata(file)
            if metadata is not None:
                lyrics = get_lyrics(metadata["artist"], metadata["title"], metadata["album"], metadata["duration"])
                if lyrics is not None:
                    print("Lyrics for: {}, were found, saving to file".format(file.name))

                    if output_folder:
                        lrc_file = Path(output_folder) / (file.stem + ".lrc")
                        with open(lrc_file, "w", encoding="utf-8") as text_file:
                            print(lyrics, file=text_file)

                    else:
                        lrc_file = str(file).replace(file.suffix, ".lrc")
                        with open(lrc_file, "w", encoding="utf-8") as text_file:
                            print(lyrics, file=text_file)
                else:
                    print("No lyrics found for: {}".format(file.name))

    print("Done :)")


if __name__ == "__main__":
    exit(main())
