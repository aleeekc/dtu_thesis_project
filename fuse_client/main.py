import argparse
import requests
import json
from variables import variables
import fs
import db
import crypt
import send_email
import qr_gen
import ftp_send
import cv2
import os
import io
import signal
import getpass
import shutil


parser = argparse.ArgumentParser()

parser.add_argument("-n", "--new", help="Create new account", action='store_true')
parser.add_argument("-l", "--logout", help="Logout from account", action='store_true')
parser.add_argument("-u", "--username", help="Set account username")
parser.add_argument("-p", "--password", help="Set account password")
parser.add_argument("-t", "--token", help="Set a user token")
parser.add_argument("-m", "--mount", help="Set the mount point")
parser.add_argument("-s", "--share", help="Share a folder with a user; please provide folder path and username", nargs='+')
parser.add_argument("-dl", "--downloadLink", help="Create a dowmload link for a file; please provide the file")
parser.add_argument("-nk", "--new_key", help="Generate a new symmetric key for a folder")
parser.add_argument("-e", "--export", help="Export a key encrypted with a provided public key; please provide the shared folder path and the public key of the recipient", nargs='+')
parser.add_argument("-ep", "--export_public_key", help="Export the accout public key", action='store_true')
parser.add_argument("-i", "--import_key", help="Import a key")
args = parser.parse_args()

username = ''
password = ''
token = ''
mount = ''


import atexit

@atexit.register
def goodbye():
    print ("Exiting!")
    shutil.rmtree("/tmp/.tmp_fuse/")


def login():
	url = variables['server'] + '/v1/login'

	data = {'username': username, 'password': password}
	r = requests.post(url, json=data)

	if r.status_code != 200:
		print(url)
		print(r.content)
		exit()

	print(r.content)
	obj = json.loads(r.content.decode('utf-8'))
	token = obj["token"]
	print(obj["token"])
	return token

if args.username:
    username = args.username
    print("Username:" + username)

if args.password:
    password = args.password
    print('Password:' + password)
else:
	password = getpass.getpass('Password:')

if args.token:
    token = args.token

if args.new:
    url = variables['server'] + '/v1/register'
    data = {'username': username, 'password': password}
    r = requests.post(url, json=data)
    print(r.content)
    obj = json.loads(r.content.decode('utf-8'))
    token = obj["token"]
    print(obj["token"])
else:
	token = login()

if args.share:
	user = args.share[0]
	path = args.share[1]
	url = variables['server'] + '/v1/shareFolder'
	values = {'name': path, 'user': user}
	header = {'Authorization' : 'Token ' + token}

	r = requests.post(url, headers=header, data=values)
	print(r.content)
	exit()

if args.downloadLink:
	path = args.downloadLink
	url = variables['server'] + '/v1/downloadLink'
	values = {'file': path}
	header = {'Authorization' : 'Token ' + token}

	r = requests.post(url, headers=header, data=values)
	print(r.content)
	exit()

if args.new_key:
	path = args.new_key
	dbms = db.db_connect(username, password)
	key = crypt.gen_sym_key_from_password(password)
	r = dbms.insert_key(key,path)
	print(r)
	exit()

if args.export:
	path = args.export[0]
	key = args.export[1] # TODO: Read from a file

	print ("Export options:")
	print ("----------------------------------")
	print ("1. Save to file")
	print ("2. Save to a zip")
	print ("3. Generate a QR Code")
	print ("4. Send an email")
	print ("5. Embed into an image")
	print ("6. Upload to voult")
	print ("7. Upload to an ftp")

	print ("")
	var = input("Choice: ")
	dbms = db.db_connect(username, password)
	skey = dbms.get_key_from_path(path)
	if var == 1:
		encoded_msg = crypt.encode_asym(skey, key)
		f= open("/tmp/export.fuse","w+")
		f.write(encoded_msg)
		f.close()
	elif var == 2:
		import zipfile

		encoded_msg = crypt.encode_asym(skey, key)
		f= open("/tmp/export.fuse","w+")
		f.write(encoded_msg)
		f.close()

		s = io.StringIO()
		with zipfile.ZipFile(s, "w", compression=zipfile.ZIP_DEFLATED) as zf:
			zf.write('/tmp/export.fuse')
	elif var == 3:
		encoded_msg = crypt.encode_asym(skey, key)
		qr_gen.gen_qr(encoded_msg)
	elif var == 4:
		encoded_msg = crypt.encode_asym(skey, key)
		email_from = input("Email from: ")
		email_to = input("Email to: ")
		send_email.send_email(email_from, email_to, encoded_msg)
	elif var == 5:
		encoded_msg = crypt.encode_asym(skey, key)

		def to_bit_generator(msg):
			"""Converts a message into a generator which returns 1 bit of the message
    		each time."""
			for c in (msg):
				o = ord(c)
			for i in range(8):
				yield (o & (1 << i)) >> i

		img = cv2.imread(os.getcwd() + '/original.png', cv2.IMREAD_GRAYSCALE)
		try:
			for h in range(len(img)):
				for w in range(len(img[0])):
					img[h][w] = (img[h][w] & ~1) | next(encoded_msg)
		except Exception as e:
			print(e)

		# Write out the image with hidden message
		cv2.imwrite("/tmp/export.png", img)

	elif var == 6:
		key = input("Enter the key you wish to upload to the key vault: ")

		url = variables['server'] + '/v1/setKey'
		values = {'key': str(key), 'meant_for': '*'}
		header = {'Authorization': 'Token ' + token}

		r = requests.post(url, headers=header, data=values)

		o = json.loads(r.content)
		print(o["key"])
		exit()

	elif var == 7:
		encoded_msg = crypt.encode_asym(skey, key)
		server = input("Enter ftp server:")
		username = input("Enter ftp username:")
		password = input("Enter ftp password:")
		ftp_send.send_ftp(server, username, password, encoded_msg)
		# TODO TEST
		exit()

	exit()

if args.export_public_key:
	dbms = db.db_connect(username, password)
	public = dbms.get_all_pkeys
	print(public)
	exit()

if args.import_key:
	key = args.import_key[0]
	path = args.import_key[1]
	dbms = db.db_connect(username, password)
	r = dbms.insert_key(key,path)
	print(r)
	exit()

if args.logout:
	url = variables['server'] + '/v1/logout'
	header = {'Authorization': 'Token ' + token}
	r = requests.post(url, headers=header)
	print(r.content)
	exit()

if args.mount:
    mount = args.mount
else:
    print('Please provide a mount point!')
    exit()



dbms = db.db_connect(username, password)
if dbms.get_all_tokens() is None:
	print("no tokens present")
	dbms.db_drop_all()
	dbms.create_db_tables()

	private, public = crypt.gen_asym_keys()

	dbms.insert_pkey(public, private)

print (token)
dbms.insert_token(token)

fs.main(mount, username, token)
