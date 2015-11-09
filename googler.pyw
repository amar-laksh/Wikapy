# -*- coding: utf-8 -*-
import win32api
import win32con
import urllib as u
import urllib2
from BeautifulSoup import BeautifulSoup
from google import search
import re

def speak(sent,rate = 150):
    import pyttsx
    engine = pyttsx.init()
    engine.setProperty('rate',rate)
    voiceid = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0'
    engine.setProperty('voice', voiceid)
    engine.say(sent)
    engine.runAndWait()
    engine.stop()

def STT():
    global query
    query1 = ""
    import speech_recognition as sr

    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(r.energy_threshold))
        print '\a',"Say something!"
        speak("Ask me a query")
        audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            print("You said " + r.recognize(audio))
            query1 = r.recognize(audio)
            query = "Wikipedia " + query1
        except LookupError:
            print("Oops! Didn't catch that")
            speak("Oops! Didn't catch that")
            query=""
   
def cleanhtml(raw_html):
    cleanr =re.compile('<.*?>')
    cleantext = re.sub(cleanr,'', raw_html) #omitting tags
    cleantext =re.sub(r'\([^)]*\)', '',cleantext) #omitting (a-Z)
    cleantext = re.sub(r'\[[^\]]*\]', '', cleantext) #omitting [0-9]
    cleantext = re.sub(r'/.*?/', '', cleantext) #omitting [/-- abstract chrs --/]
    return cleantext

def main():
        urls = []
        import os
        path = os.getcwd()
        path = path.replace("\\","/")
        STT()
        """
        query = raw_input("Please enter a word: ")
        query = "Wikipedia"+query
        """
        try:
            
            for url in search(query ,stop=1):
                urls.append(url)
            print "##############"
            mainurl = urls[0]
            print "##############"
            print mainurl
            saved = u.urlretrieve(mainurl,'googled.html')
            saveds = "file:///"+path + "/googled.html"
            page = urllib2.urlopen(saveds)
            soup = BeautifulSoup(page)
            x = soup.body.find('p')
            import sys
            y = re.findall(r'<p.*?>(.*?)</p>',str(x))
            print "################################"
            print cleanhtml(str(x))
            speak(cleanhtml(str(x)))
        except:
            pass
while True:
        main()


