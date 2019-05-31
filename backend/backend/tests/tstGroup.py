import requests
import json


### LOGIN
url = 'http://127.0.0.1:8000/v1/login'

data = {'username' : 'admin', 'password' : 'admin'}
r = requests.post(url, json=data)
print(r.content)
obj = json.loads(r.content)
print(obj["token"])


### CREATE GROUP
url = 'http://127.0.0.1:8000/v1/createGroup'
values = {'name': 'cool_Group'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, headers=header, data=values)
print(r.content)


### ADD USER TO GROUP
url = 'http://127.0.0.1:8000/v1/joinGroup'
values = {'name': 'cool_Group', 'user': 'testUser'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, headers=header, data=values)
print(r.content)


### LIST USERS IN GROUP

url = 'http://127.0.0.1:8000/v1/listUsersInGroup'
values = {'name': 'cool_Group'}
header = {'Authorization' : 'Token ' + obj["token"]}
r = requests.get(url, headers=header, data=values)
print(r.content)

### LOGOUT
url = 'http://127.0.0.1:8000/v1/logout'
header = {'Authorization' : 'Token ' + obj["token"]}
r = requests.post(url, headers=header)
print(r.content)