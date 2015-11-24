# -*- coding: utf-8 -*-
import win32api
import win32con
import urllib as u
import urllib2 as ur
from BeautifulSoup import BeautifulSoup
from google import search
import re

class Wikapy():
    def __init__(self):
        self.query = ""
        self.code = 0

    def OnKeyboardEvent(self,event):
     key = (event.Ascii)
     if key == 126 and self.code == 0:     # ~ symbol
         self.code = 1
         print "You pressed ~ once with c=",self.code
         
     elif(key == 126 and self.code == 1):
         self.code = 0
         print "You pressed ~ once with c=",self.code
     if key == 63 and self.code == 1:      # ? symbol
         c = 0
         while c != 1:
             try:
                 import speech_recognition as sr
                 r = sr.Recognizer()
                 m = sr.Microphone()
                 c = 1
             except:
                 pass
         self.init()
     return True

    def dae(self):
        import pyHook, pythoncom, sys
        hooks_manager = pyHook.HookManager ( )
        hooks_manager.KeyDown = self.OnKeyboardEvent
        hooks_manager.HookKeyboard ( )
        pythoncom.PumpMessages () #pythoncom module is used to capture the key messages.

            
    def speak(self,sent):
        import pyttsx
        engine = pyttsx.init()
        engine.setProperty('rate',150)
        voiceid = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0'
        engine.setProperty('voice', voiceid)
        engine.say(sent)
        engine.runAndWait()
        engine.stop()
        

    def STT(self):
        import speech_recognition as sr
        r = sr.Recognizer()
        m = sr.Microphone()
        with m as source:
            r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
            print '\a',"Say something!"
            self.speak("Ask me a query")
            audio = r.listen(source)
            print("Got it! Now to recognize it...")
            try:
                print("You said " + r.recognize(audio))
                self.query = r.recognize(audio)
                self.query = "Wikipedia " + self.query
            except LookupError:
                print("Oops! Didn't catch that")
                self.speak("Oops! Didn't catch that")
                self.query=""

       
    def cleanhtml(self,raw_html):
        cleantext = re.sub(r'<.*?>','', raw_html) #omitting tags
        cleantext =re.sub(r'\([^)]*\)', '',cleantext) #omitting (a-Z)
        cleantext = re.sub(r'\[[^\]]*\]', '', cleantext) #omitting [0-9]
        cleantext = re.sub(r'/.*?/', '', cleantext) #omitting [/-- abstract chrs --/]
        return cleantext

    def init(self):
            urls = []
            import os
            path = os.getcwd()
            path = path.replace("\\","/")
            try:
                self.STT()
                mainurl = [urls.append(url) for url in search(self.query ,stop=1)]
                sav = ur.urlopen(mainurl[0])
                page = sav.read()
                soup = BeautifulSoup(page)
                x = soup.body.find('p')
                self.speak(self.cleanhtml(str(x)))
                saveds = "./googled.html"
                f = open(saveds,'w')
                f.write(page)
                f.close()
            except:
                pass
while True:
        w = Wikapy()
        w.dae()


