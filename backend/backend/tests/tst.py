import requests
import json

url = 'http://127.0.0.1:8000/v1/register'

data = {'username' : 'as', 'password' : 'as'}
r = requests.post(url, json=data)
print(r.content)
obj = json.loads(r.content)
print(obj["token"])

url = 'http://127.0.0.1:8000/v1/login'

data = {'username' : 'as', 'password' : 'as'}
r = requests.post(url, json=data)
print(r.content)
obj = json.loads(r.content)
print(obj["token"])

url = 'http://127.0.0.1:8000/v1/ping'

#header = {'Authorization' : 'Token ' + obj["token"]}
r = requests.get(url)#, headers=header)
print(r.content)

url = 'http://127.0.0.1:8000/v1/userinfo'

header = {'Authorization' : 'Token ' + obj["token"]}
r = requests.get(url, headers=header)
print(r.content)


url = 'http://127.0.0.1:8000/v1/login_anon'

header = {'username' : 'mario'}
r = requests.post(url, data=header)
print(r.content)


