import requests
import json


### LOGIN
url = 'http://127.0.0.1:8000/v1/login'

data = {'username' : 'admin', 'password' : 'admin'}
r = requests.post(url, json=data)
print(r.content)
obj = json.loads(r.content)
print(obj["token"])


### FILE UPLOAD
url = 'http://127.0.0.1:8000/v1/fileupload'
files = {'upload_file': open('tst.py','rb')}
values = {'name': 'tst1.py'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, files=files, headers=header, data=values)
print(r.content)


### FILE RENAME
url = 'http://127.0.0.1:8000/v1/renameFile'
values = {'name': 'Renamed_File_1.py', 'old_name': 'tst1.py'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, headers=header, data=values)
print(r.content)


url = 'http://127.0.0.1:8000/v1/listFiles'
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.get(url, headers=header, data=values)
print(r.content)

url = 'http://127.0.0.1:8000/v1/downloadFile'
values = {'name': 'Renamed_File_1.py'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.get(url, headers=header, data=values)
print(r.content)
exit()

"""
### FILE DELETE
url = 'http://127.0.0.1:8000/v1/deleteFile'
values = {'name': 'Renamed_File.py'}
header = {'Authorization' : 'Token ' + obj["token"]}

r = requests.post(url, headers=header, data=values)
print(r.content)
"""