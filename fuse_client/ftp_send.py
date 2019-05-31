import ftplib


def send_ftp(server, username, password, msg):
	bmsg = io.BytesIO(str.encode(msg))
	session = ftplib.FTP(server, username, password)
	session.storbinary('key', bmsg)
	file.close()
	session.quit()


if __name__ == "__main__":
	send_ftp('tst_server', 'username', 'password', 'msg')