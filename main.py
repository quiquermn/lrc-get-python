# iterate all files in folder and print file name
from os import listdir
import os
from time import sleep

mypath = input("Enter path: ")
onlyfiles = [f for f in listdir(mypath)]
ffmpegPATH = input("Enter ffmpeg path: ")
vbr = input("Enter VBR: ")
os.chdir(ffmpegPATH)

for x in onlyfiles:
    if x.find("flac") == -1:
        continue

    # print(os.path.basename(x))
    file = mypath + "\\" + os.path.basename(x)

    flacFile = '"' + file + '"'
    finalFile = '"' + file.replace(".flac", ".m4a") + '"'

    # ffmpeg -i input.mp3 -c:a aac -q 4 output.m4a

    ffmpegCommand = "ffmpeg -i " + flacFile + \
        " -c:a libfdk_aac -vbr " + vbr + " -map a " + finalFile
    # print(ffmpegCommand)
    os.system(ffmpegCommand)
    sleep(1)
