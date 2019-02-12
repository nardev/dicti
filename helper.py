# Vedran Alajbegovic - Feb.2019

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


# TODO - Za neku narednu verziju, trebalo bi dodati sledece:
# funkcija: spoji sve fajlove po slovima
# funkcija: spoji sve u jedan veliki fajl
# funkcija: randomiziraj po custom listi

# Do tada, gore pomenuto se moze napraviti sa aplikacijom sox za bash
# naprimjer, za slovo a: sox word-by-word-combined/[aA]*.mp3 combined-by-first-letter/a.mp3
# naprimjer sve u jedan: sox combined-by-first-letter/*.mp3 all-in-one.mp3
