# StegTool is a steganographic tool written in python as a personal challenge project
# for UNSW Principles of /Security Engineering Hexamester 2 2023 by Ryan McMillan.

import os
import argparse
import sys
from PIL import Image

FILETYPES = ['.jpg','.jpeg','.bmp']


def encode(image: Image, secret_message: str) -> Image:
    '''
    encode function takes a file reference and secret message. secret message is
    embedded within the file using Least Significant Bit (LSB) steganography.
    '''

    # Convert secret_message to binary
    binary_secret_message = ''.join(format(ord(char), '08b') for char in secret_message)

    # Validate secret will fit within carrier image file
    # Calculate max bits available in image in three channels
    max_bits = image.width * image.width * 3
    # Check max_bits > length of message - 6 for start and stop message token
    if len(binary_secret_message) > max_bits - 6:
        raise ValueError("Secret message too large for carrier file")

    # Encode start message token into first three pixels '<!>'
    start_token = ''.join(format(ord(char), '08b') for char in '<!>')
    # Encode stop message token into final three pixels '<?>'
    stop_token = ''.join(format(ord(char), '08b') for char in '<?>')

    # Append start_token and stop_token to message
    binary_secret_message = start_token + binary_secret_message + stop_token

    # Ensure secret message is divisible by three by padding the message with 1 or 2 zeros
    binary_secret_message = binary_secret_message + ('0'* (3 - (len(binary_secret_message) % 3)))

    # Iterate over each pixel in image
    # msg_idx keeps track of the bits of secret message that have been encoded.
    msg_idx = 0
    for x in range(image.width):
        for y in range(image.height):
            if msg_idx < len(binary_secret_message):
                # extract RGB values
                r,g,b = image.getpixel((x,y))

                # Convert values to binary
                r_binary = format(r,'08b')
                g_binary = format(g,'08b')
                b_binary = format(b,'08b')

                # Sanity and debugging
                print(f"R: {r_binary}, G: {g_binary}, B: {b_binary}")

                # Replace Least Significant Bit of each colour channel with message bit
                r_binary = r_binary[:-1] + binary_secret_message[msg_idx]
                g_binary = g_binary[:-1] + binary_secret_message[msg_idx + 1]
                b_binary = b_binary[:-1] + binary_secret_message[msg_idx + 2]

                # Sanity and debugging comparison
                print(f"NR:{r_binary}, NG:{g_binary}, NB:{b_binary}")

                # Increment message bit index by 3
                msg_idx += 3

                # Convert back to integers
                r_int = int(r_binary, 2)
                g_int = int(g_binary, 2)
                b_int = int(b_binary, 2)

                # Store new binary values in image
                image.putpixel((x,y), (r_int,g_int,b_int))

    return image



def save_image(image:Image, filename:str):
    '''
    Save image file with steganographic encoded message
    '''
    # Save image with embedded message as new image
    image.save("steg_" + filename)



def decode(image: Image) -> str:
    '''
    decode function takes a carrier file image and decodes the image using
    Least Signifocamt Bit steganography and returns the secret message as a string.
    '''
    print("IN DECODING FUNCTION")



def open_file(filename: str) -> Image:
    '''
    open the carrier file and return the bytestring of the image
    '''
    image = Image.open(filename)
    return image



def main():
    # Check CLI arguments are valid.
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str,
                        help='name of file to perform steganographic function on')
    parser.add_argument('--encode', help='Performs steganographic encode function',
                        action='store_true')
    parser.add_argument('--decode', help='Performs steganographic decode function',
                        action='store_true')
    parser.add_argument('message', type=str,
                        help='Text string of message to be encoded')

    args = parser.parse_args()

    # Quit program if both or neither flag is set
    if args.encode and args.decode:
        print("Only use the --encode or --decode flag, not both")
        sys.exit()
    elif not args.encode and not args.decode:
        print('use one of the --encode or --decode flags')
        sys.exit()

    # Check carrier file exists.
    if not os.path.isfile(args.filename):
       print("no such file")
       sys.exit()

    # Check carrier filetype is valid
    if not (args.filename[-4:] in FILETYPES or args.filename[-5:] in FILETYPES):
        sys.exit()

    # Open carrier image with Python Image Library(PIL)
    carrier = open_file(args.filename)

    if args.encode:
        carrier = encode(carrier, args.message)
        save_image(carrier, args.filename)
    elif args.decode:
        decode()
    else:
        print("Unsupported filetype")
        sys.exit()


if __name__ == '__main__':
    main()