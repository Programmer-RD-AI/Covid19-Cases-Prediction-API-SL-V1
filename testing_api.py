import requests

info = requests.get('http://192.168.1.8:9315/20211221').json()
print(info)
