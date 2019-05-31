import requests
import json


### LOGIN
url = 'http://127.0.0.1:8000/v1/login'

data = {'username' : 'admin', 'password' : 'admin'}
r = requests.post(url, json=data)
print(r.content)
obj = json.loads(r.content)
print(obj["token"])


### FOLDER UPLOAD
url = 'http://127.0.0.1:8000/v1/uploadFolder'
values = {'name': 'this is a foler'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, headers=header, data=values)
print(r.content)


### FOLDER RENAME
url = 'http://127.0.0.1:8000/v1/renameFolder'
values = {'name': 'this is a new folder', 'old_name': 'this is a foler'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, headers=header, data=values)
print(r.content)


### FOLDER DELETE
url = 'http://127.0.0.1:8000/v1/deleteFolder'
values = {'name': 'this is a new folder'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, headers=header, data=values)
print(r.content)


### LOGOUT
url = 'http://127.0.0.1:8000/v1/logout'
header = {'Authorization' : 'Token ' + obj["token"]}
r = requests.post(url, headers=header)
print(r.content)

