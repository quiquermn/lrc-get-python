# import lrc_get_rewritten
from ffmpeg import probe as ffprobe


def to_lower_keys_in_dict(_dict):
    lower_dict = dict()
    for x in _dict:
        key = x.lower()
        value = _dict[x]
        if key in ["artist", "title", "album"]:
            lower_dict[key] = value
    return lower_dict


def get_metadata(file):
    f_format = ffprobe(file)["format"]
    tags = to_lower_keys_in_dict(f_format["tags"])
    duration = round(float(f_format["duration"]))
    tags["duration"] = duration

    return tags


def try_get_metadata(file):
    try:  # Try to get metadata
        metadata = get_metadata(file)
    except (Exception,):
        return None
    else:
        return metadata


if __name__ == "__main__":
    exit(print(try_get_metadata(input("Enter file path: "))))
