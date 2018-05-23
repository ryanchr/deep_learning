#!/usr/bin/env python3

import urllib2
import speech_recognition as sr
import subprocess
import os

mp4file = 'common_qa_in_english'

cmdline = ['avconv',
	   '-i',
	   mp4file + '.mp4',
	   '-vn',
	   '-f',
	   'wav',
  	   mp4file + '.wav']

##subprocess.call(cmdline)

r = sr.Recognizer()

with sr.AudioFile(mp4file + '.wav') as source:
    audio = r.record(source)
    print("finished reading the audio file")
    try:
        command = r.recognize_google(audio, language = "en-US")
	print command
    except sr.UnknownValueError:
	print("Google speech recognition could not understand audio")		
    except sr.RequestError as e:
	print("Can not request results from Google Speech service; {0}".format(e))

