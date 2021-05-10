import threading
import time
import requests
def send_request():
    requests.get('https://covid19api-sl-programmer-rd-ai.herokuapp.com/20211221')
for _ in range(125):
    print(_)
    threading.Thread(target=send_request).start()
    print(_)
