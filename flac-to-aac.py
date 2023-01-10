from os import listdir
import os
from time import sleep

mypath = input("Enter path: ")
filesFolder = [f for f in listdir(mypath)]
ffmpegPATH = input("Enter ffmpeg path (type PATH if is in env variables): ")

if ffmpegPATH != "PATH":
    os.chdir(ffmpegPATH)
else:
    print("Using ffmpeg from env variables")

vbr = input("Enter VBR (from 1 to 5 [2 is recommended]): ")
os.system("ffmpeg -version")

for x in filesFolder:
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
