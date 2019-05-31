import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import cryptography.hazmat.primitives.kdf
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa
import base64


def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))


def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')


def encode(msg, key=None):

	if key is None:
		key = Fernet.generate_key()

	print ('Key: ' + str(key))

	f = Fernet(key)
	if msg is None:
		return 'Please provide the text to be encrypted!'

	encrypted_msg = f.encrypt(str.encode(msg))
	print ('Encrypted msg: ' + str(encrypted_msg))

	return encrypted_msg, key


def decode(encrypted_msg, key):
	f = Fernet(key)
	if encrypted_msg is None:
		return 'Please provide the text to be decrypted!'

	decrypted_msg = f.decrypt(encrypted_msg)

	print('Decrypted text: ' + str(decrypted_msg))

	return decrypted_msg, key


def encode_with_password(msg, key):

	f = Fernet(key)
	encrypted_msg = f.encrypt(msg)
	return encrypted_msg


def decode_with_password(encrypted_msg, key):
	try:
		f = Fernet(key)
		decrypted_msg = f.decrypt(encrypted_msg.encode())
	except Exception as e:
		print('The stored keys are not for this account!')
		return encrypted_msg
		#exit()

	return decrypted_msg


def gen_asym_keys():
	private_key = rsa.generate_private_key(
    	public_exponent=65537,
    	key_size=2048,
    	backend=default_backend()
	)

	public_key = private_key.public_key()

	return private_key, public_key


def save_asym_keys_to_file(private_key, public_key):
	pem = private_key.private_bytes(
    	encoding=serialization.Encoding.PEM,
    	format=serialization.PrivateFormat.PKCS8,
    	encryption_algorithm=serialization.NoEncryption()
	)

	with open('private_key.pem', 'wb') as f:
		f.write(pem)

	pem = public_key.public_bytes(
    	encoding=serialization.Encoding.PEM,
    	format=serialization.PublicFormat.SubjectPublicKeyInfo
	)

	with open('public_key.pem', 'wb') as f:
		f.write(pem)


def get_asym_keys_from_file():
	with open("private_key.pem", "rb") as key_file:
		private_key = serialization.load_pem_private_key(
        	key_file.read(),
        	password=None,
        	backend=default_backend()
    	)

	with open("public_key.pem", "rb") as key_file:
		public_key = serialization.load_pem_public_key(
        	key_file.read(),
        	backend=default_backend()
    	)

	return private_key, public_key


def encode_asym(msg, public_key):

	encrypted_msg = public_key.encrypt(
    	msg,
    	padding.OAEP(
        	mgf=padding.MGF1(algorithm=hashes.SHA256()),
        	algorithm=hashes.SHA256(),
        	label=None
    	)
	)

	return encrypted_msg


def decode_asym(msg, private_key):

	decrypted_message = private_key.decrypt(
    	encrypted,
    	padding.OAEP(
        	mgf=padding.MGF1(algorithm=hashes.SHA256()),
        	algorithm=hashes.SHA256(),
        	label=None
    	)
	)

	return decrypted_message


def gen_sym_key():
	key = Fernet.generate_key()
	return key


def gen_sym_key_from_password(password):
	salt = os.urandom(16)
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)
	kdf_password = kdf.derive(str.encode(password))
	key = base64.urlsafe_b64encode(kdf_password)
	return key


def key_to_fernet_obj(key):
	f = Fernet(key)
	return f

"""
if __name__ == "__main__":
    encrypted_msg, key = encode("Hey")
    decrypted_msg, key = decode(encrypted_msg, key)
    print (decrypted_msg)
    password = 'password'
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=100000,
		backend=default_backend()
	)
    kdf_password = kdf.derive(str.encode(password))
    encrypted_msg = encode_with_password("Hello", kdf_password)
    decrypted_msg = decode_with_password(encrypted_msg,kdf_password)
    print (decrypted_msg)
  """