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
values = {'name': 'folderTest/'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, headers=header, data=values)
print(r.content)


### FILE UPLOAD
url = 'http://127.0.0.1:8000/v1/fileupload'
files = {'upload_file': open('tst.py','rb')}
values = {'name': 'folderTest/tst1.py'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, files=files, headers=header, data=values)
print(r.content)


### SHARE FOLDER
url = 'http://127.0.0.1:8000/v1/shareFolder'
values = {'name': 'folderTest/', 'user': 'testUser'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, files=files, headers=header, data=values)
print(r.content)


### LOGOUT
url = 'http://127.0.0.1:8000/v1/logout'
header = {'Authorization' : 'Token ' + obj["token"]}
r = requests.post(url, headers=header)
print(r.content)