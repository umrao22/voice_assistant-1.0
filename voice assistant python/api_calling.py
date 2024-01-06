import gc
import requests
import json 
import numpy as np
import pyttsx3

class get_ans():
    
    def __init__(self) :
        super().__init__()
        self.url="http://localhost:7004/qrySrch"
        self.header={
                    'Content-Type': 'application/json'
                    }
        self.speech_stop = True
        self.is_speaking=True
       
    def action(self , text) :
        while self.speech_stop==False :           
            self.is_speaking=False

        self.is_speaking=True
        self.speech_stop=False
        payload = json.dumps({
                     "query": ""+text+""
                            })

        response = requests.request("POST", self.url, headers=self.header, data=payload)

        result=json.loads(response.text)
        txt=result['MESSAGE']
        print(txt)
        self.speak(txt)

    def txt_breaker(self , text) :
        lst=text.split(" ")
        lst_batch=[]
        if(len(lst)<8):
            lst_batch.append(text) 
            return lst_batch

        b=np.array_split(lst,len(lst)/8)
        
        for i in b :
            lst_batch.append(" ".join(i))
        return lst_batch

    def speak(self,text) :
        batches=self.txt_breaker(text)
        tts_engine = pyttsx3.init()
        tts_engine.setProperty("rate", 140)
     
       
        for i in batches : 
            
            if (self.is_speaking==False) :
                print("stop speccchhhhhhh")
                self.speech_stop=True
                print(self.speech_stop)
                print(self.is_speaking)
                
                return 
            tts_engine.say(i)
            print(i)
            tts_engine.runAndWait()

        print("speech stop==true------------------------------------------------------------------------------")
        self.speech_stop=True  
        gc.collect()