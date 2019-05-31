import qrcode
import uuid

def gen_qr(msg):
	qr = qrcode.QRCode(
    	version=1,
    	error_correction=qrcode.constants.ERROR_CORRECT_L,
    	box_size=10,
    	border=4,
	)

	qr.add_data(msg)
	qr.make(fit=True)

	img = qr.make_image(fill_color="black", back_color="white")
	name = uuid.uuid4().__str__().replace("-","")
	img.save(name + ".jpg")

	return name + ".jpg"

if __name__ == "__main__":
	decode()