import smtplib
import sys
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(from_addr, to_addr, key):
    subject = ''
    content = ''

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    body = MIMEText(content, 'plain')
    msg.attach(body)

    # filename = 'test.txt'#
    #with open(filename, 'r') as f:
    part = MIMEApplication(key, Name = basename('key'))
    part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.login(from_addr, 'password')
    server.send_message(msg, from_addr = from_addr, to_addrs = [to_addr])

if __name__ == "__main__":
    send_email(sys.argv[0], sys.argv[1], sys.argv[2])