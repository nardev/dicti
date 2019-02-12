import os, sys
import pandas
from gtts import gTTS
import requests
import urllib
import json
import base64
import sox
import re
import subprocess

################################################################################
## file paths and config
################################################################################

audio = "word-by-word-combined/"
audio_temp = "word-by-word-uncombined/"
wordslist = "3001.csv"

## read number from file last
last = open("last", "r")
latest = int(last.read())
print "==="
print "starting at: " + str(latest)
print "==="
last.close()

################################################################################
## get text to speach croatian website cookies
################################################################################
session = requests.Session()
# response = session.get('https://alfanum.co.rs/index.php/sr/demonstracija/demonstracija-tts')
# # print(session.cookies.get_dict())
cookies = session.cookies.get_dict()

################################################################################
## get english, serbian and/or croatian audio function
################################################################################

# pretty straight foward how to get mp3 but it looks like those mp3 files lack some characteristics, important for merging
def getEnglishAudio(word,tempname):
    tts = gTTS(word)
    tts.save(audio_temp+tempname+"_en.mp3")
    return audio_temp+tempname+"_en.mp3"


# this website doesn't have request's monitoring so i was able to hit the script constantly
def getCroatianAudio(word,tempname):
    response = requests.post("https://www.hsm360.com/wp-content/plugins/hsm-screen-reader/lib/tts_req.php",data={
    		'input_text': word,
    		'rate':'0.995',
    		'pitch':'0.65',
    		})
    data = response.json()
    fileurl = data["file_url"]
    urllib.urlretrieve (fileurl, audio_temp+tempname+"_ba.mp3")
    return audio_temp+tempname+"_ba.mp3"


# this website has controls requests
def getSerbianAudio(word,tempname):
    response = requests.post("https://www.alfanum.co.rs/tts_req.php",data={
    		'input_text': word,
    		'outlang': 'sr',
    		'speaker':'AlfaNum Ivana',
    		'rate':'0.9995',
    		'pitch':'0.875',
    		'port':'5040',
    		'enc':'1',
    		'address': 'tts4.alfanum.co.rs',
    		'server_id': '0' },cookies=cookies)
    data = response.json()
    fileurl = "https://tts4.alfanum.co.rs:5050/ttsnovi/"+data["file"]
    urllib.urlretrieve (fileurl, audio_temp+tempname+"_ba.mp3")
    return audio_temp+tempname+"_ba.mp3"


################################################################################
## generate combined audio with pause
################################################################################
cbn = sox.Combiner()
def generateCombinedAudio(file1,file2,name):
    print "------------------------"
    print file1 + " & " + file2 + " => " + name +'.mp3'
    print "------------------------"
    command = 'ffmpeg -i '+file1+' -i '+file2+'  -filter_complex "[0:a:0][1:a:0]concat=n=2:v=0:a=1[outa]" -map "[outa]" '+audio+finalname+'.mp3'
    output = subprocess.check_output(['bash','-c', command])

################################################################################
## loop the list of words in csv
################################################################################

wordslistfile = pandas.read_csv(wordslist,skipinitialspace = True, quotechar = '"')

for index, row in wordslistfile.iterrows():
    if index > latest:
    # if index == 58:
        file1 = getEnglishAudio(row['english'].strip(), str(index))
        file2 = getCroatianAudio(row['bosnian'], str(index))
        finalname = row['english'].split(',')[0].strip().replace(" ", "_").replace("'", "")+'-'+ row['bosnian'].split(',')[0].strip().replace(" ", "_")
        generateCombinedAudio(file1,file2,finalname)
        last = open("last", "w")
        last.write(str(index))
        last.close()

print " < vedran alajbegovic - vedran@nardev.org > 2019 SARAJEVO, BOSNA I HERCEGOVINA"

