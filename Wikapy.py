# -*- coding: utf-8 -*-
import win32api
import win32con
import urllib as u
import urllib2
from BeautifulSoup import BeautifulSoup
from google import search
import re

class Wikapy():
    def __init__(self):
        self.query = ""
        
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
        try:
            r = sr.Recognizer()
            m = sr.Microphone()
        except:
            pass
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
        cleanr =re.compile('<.*?>')
        cleantext = re.sub(cleanr,'', raw_html) #omitting tags
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
                for url in search(self.query ,stop=1):
                    urls.append(url)
                mainurl = urls[0]
                print "##############"
                print mainurl
                saved = u.urlretrieve(mainurl,'googled.html')
                saveds = "file:///"+path + "/googled.html"
                page = urllib2.urlopen(saveds)
                soup = BeautifulSoup(page)
                x = soup.body.find('p')
                print "################################"
                print self.cleanhtml(str(x))
                self.speak(self.cleanhtml(str(x)))
            except:
                pass
while True:
        w = Wikapy()
        w.init()


