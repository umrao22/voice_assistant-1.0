from threading import Thread
from stt import STTEngine  
from api_calling import get_ans

s=STTEngine()
s.recognize_input()
a=get_ans()

while True :
    z=Thread(target=a.action  , args=(s.get_query(),) )
    z.start()