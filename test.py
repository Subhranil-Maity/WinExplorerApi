import requests

Base = 'http://127.0.0.1:5000/'

responce = requests.get(Base + "get")
print(responce.json())