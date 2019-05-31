import requests
import json


### LOGIN
url = 'http://127.0.0.1:8000/v1/login'

data = {'username' : 'admin', 'password' : 'admin'}
r = requests.post(url, json=data)
print(r.content)
obj = json.loads(r.content)
print(obj["token"])


### Upload key

url = 'http://127.0.0.1:8000/v1/setKey'
values = {'key': 'THIS IS A KEY', 'meant_for': '*'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, headers=header, data=values)
print(r.content)
o = json.loads(r.content)
print(o["key"])


### Link key

url = 'http://127.0.0.1:8000/v1/downloadKey/' + o['key']
header = {'Authorization' : 'Token ' + obj["token"]}
print(url)
r = requests.get(url, headers=header)
print(r.content)

### LOGOUT
url = 'http://127.0.0.1:8000/v1/logout'
header = {'Authorization' : 'Token ' + obj["token"]}
r = requests.post(url, headers=header)
print(r.content)