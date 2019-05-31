import cv2 # OpenCV 2
import os


def to_bit_generator(msg):
    """Converts a message into a generator which returns 1 bit of the message
    each time."""
    for c in (msg):
        o = ord(c)
        for i in range(8):
            yield (o & (1 << i)) >> i

def main():
    # Create a generator for the hidden message
    hidden_message = to_bit_generator(open("README.md", "r").read())

    cwd = os.getcwd()
    msg = open("README.md", "r").read()
    print(type(msg))
    print(len(msg))
    print(cwd + '/original.png')
    # Read the original image
    img = cv2.imread(cwd + '/original.png', cv2.IMREAD_GRAYSCALE)
    try:
        for h in range(len(img)):
            for w in range(len(img[0])):
                # Write the hidden message into the least significant bit
                img[h][w] = (img[h][w] & ~1) | next(hidden_message)
    except Exception as e:
        print(e)
    # Write out the image with hidden message
    cv2.imwrite("output.png", img)

if __name__ == "__main__":
    main()