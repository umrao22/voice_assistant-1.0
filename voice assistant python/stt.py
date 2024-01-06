import gc
import threading
import speech_recognition as sr 
from queue import Queue
from time import sleep
import pyaudio

q=Queue()

class STTEngine:
    

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1
        self.microphone = sr.Microphone()
        self.recognizer.dynamic_energy_threshold=True

    @staticmethod
    def _recognize_speech_from_mic(recognizer ,  audio):
        def wakeword_detection(audio):
            try :
                print(recognizer.recognize_sphinx(audio, keyword_entries=[("genius",0.9), ("xenius", 1.0)]))
                return True
            except sr.UnknownValueError:
                return False
    
        if wakeword_detection(audio) :
            try:
                txt = recognizer.recognize_google(audio).lower()
                print(txt)
                q.put(txt)
            except sr.UnknownValueError:
                print("unknown error")
            
            except sr.RequestError:
                print('error getting response from api')
            
        
    def adjust_for_noise(self) :
        self.recognizer.adjust_for_ambient_noise(self.microphone)
        self.recognizer.dynamic_energy_threshold=True
        print("cleqqr")
        gc.collect()
        threading.Timer(100.0, self.adjust_for_noise).start()

    def get_query(self) :
        return q.get()

    def recognize_input(self):
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
          
        self.recognizer.listen_in_background(self.microphone , self._recognize_speech_from_mic )
        print("strt")

        sleep(8)    
        print("------------cleaner func---------------")
        self.adjust_for_noise()
      

