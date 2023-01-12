# Implementation of lrc-get in python

## How to use
`python .\lrc_get.py -i [INPUT-FOLDER])`

## Examples
- `python .\lrc_get.py -i "C:\music\Lit Killah - SnipeZ "`
- `python .\lrc_get.py -i "C:\music\Lit Killah - SnipeZ " -o "C:\music\lyrics"` (lyrics will be saved to output folder)
- `python .\lrc_get.py -i "C:\music\Lit Killah - SnipeZ " -r` (existing lyrics will be replaced)

## Arguments
- `-i` or `--input`  : Path of audio files  <br>
- `-o` or `--output` : (OPTIONAL) Output folder of lyrics files <br>
- `-r` or `--replace`: (OPTIONAL) If present, replaces existing .lrc files <br>

## Installation
1. Clone this repository
2. Install ffmpeg and add it to PATH
3. Install dependencies
    - `pip install -r requirements.txt`

## TODO:
- [ ] Don't use ffmpeg
- [ ] Add GUI
- [ ] Manual search for lyrics

## Notes
I'm not very good with python and english is not my main language, so I would greatly appreciate your help in my little project

<hr>

#### Based on the work by @tranxuanthang in https://github.com/tranxuanthang/lrcget
