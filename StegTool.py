# StegTool is a steganographic tool written in python as a personal challenge project
# for UNSW Principles of /Security Engineering Hexamester 2 2023 by Ryan McMillan.

import argparse
import cv2
import os
import sys


FILETYPES = ['.jpg','.jpeg','.bmp','.png']


def encode(image: cv2, secret_message: str, filename: str, verbose: bool):
    '''
    encode function takes a file reference and secret message. secret message is
    embedded within the file using Least Significant Bit (LSB) steganography.
    '''

    # Convert secret_message to binary
    if verbose: print("Converting secret message to binary...")
    binary_secret_message = ''.join(format(ord(char), '08b') for char in secret_message)
    if verbose: print(f"SECRET MESSAGE: {binary_secret_message}")

    # Validate secret will fit within carrier image file
    # Calculate max bits available in image in three channels
    max_bits = image.shape[0] * image.shape[1] * image.shape[2]
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
    if verbose: print("Beginning LSB Encoding...")
    msg_idx = 0
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if msg_idx < len(binary_secret_message):
                # extract RGB values
                (b,g,r) = image[y][x]

                # Convert values to binary
                r_binary = format(r,'08b')
                g_binary = format(g,'08b')
                b_binary = format(b,'08b')

                # Sanity and debugging
                #print(f"R: {r_binary}, G: {g_binary}, B: {b_binary}")

                # Replace Least Significant Bit of each colour channel with message bit
                r_binary = r_binary[:-1] + binary_secret_message[msg_idx]
                g_binary = g_binary[:-1] + binary_secret_message[msg_idx + 1]
                b_binary = b_binary[:-1] + binary_secret_message[msg_idx + 2]

                # Sanity and debugging comparison
                #print(f"[{y}][{x}]: NR:{r_binary}, NG:{g_binary}, NB:{b_binary}")

                # Increment message bit index by 3
                msg_idx += 3

                # Convert back to integers
                r_int = int(r_binary, 2)
                g_int = int(g_binary, 2)
                b_int = int(b_binary, 2)

                # Store new binary values in image
                image[y][x] = b_int,g_int,r_int
                #print(image[y][x])
            else:
                break

    if verbose: print("LSB encoding complete!")
    return image



def save_image(image: cv2, filename: str, verbose: bool):
    '''
    Save image file with steganographic encoded message
    '''
    # Save image with embedded message as new image
    if verbose: print("Saving image...")
    filename = filename.split('.')
    cv2.imwrite("./encoded/steg_" + filename[0] + '.png', image)
    if verbose: print('Image saved.')

    return



def decode(image: cv2, verbose: bool) -> str:
    '''
    decode function takes a carrier file image and decodes the image using
    Least Signifocamt Bit steganography and returns the secret message as a string.
    '''
    valid_tokens = ['<!>','<?>']
    # Check that the image contains a valid token
    if verbose: print("Checking for encoded image..")
    if valid_encoding(image, valid_tokens[0]):
        if verbose: print("Image is encoded, beginning decode.")
        message = extract(image, verbose)
    else:
        print("\nERROR: Not a valid carrier file. Exiting.")
        sys.exit()

    return message



def valid_encoding(image: cv2, token: str) -> bool:
    '''
    Check carrier file for valid start_token prior to proceeding with decoding
    returns boolean
    '''
    # Create an empty string to build start_token
    extracted_token = ''

    # Exctract the first three bytes (24bits) from 8 pixels containing 3 channels taking LSB
    for x in range(8):
        # Get RGB values for current pixel
        (b,g,r) = image[0][x]

        # Convert values to binary
        r_binary = format(r,'08b')
        g_binary = format(g,'08b')
        b_binary = format(b,'08b')

        # Append LSB of r,g,b pixels to the token string
        extracted_token = extracted_token + r_binary[-1] + g_binary [-1] + b_binary[-1]

    # Split 24 bit binary into three 8-bit characters
    character_list = [extracted_token[0:8],extracted_token[8:16],extracted_token[16:24]]

    # Convert extracted 8-bit binary to bytes ensure byteorder big endian to fix reveresed character bug
    bytes_char_list = [int(x, 2).to_bytes(2, byteorder='big', signed=False) for x in character_list]

    # Generate string from list elements
    ascii_token = ''.join([chr(int.from_bytes(x, 'big', signed="False")) for x in bytes_char_list])

    # Check if extracted bits are the same as the token
    if ascii_token != token:
        return False
    else:
        return True



def extract(image: cv2, verbose: bool) -> str:
    '''
    Extract the secret message of a known encoded file. returns string containing
    secret message
    '''
    if verbose: print("Extracting message from carrier file...")
    stop_token = ''.join(format(ord(char), '08b') for char in '<?>')
    message = ''
    stop = False
    while not stop:
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                # Get RGB values for current pixel
                (b,g,r) = image[y][x]

                # Convert values to binary
                r_binary = format(r,'08b')
                g_binary = format(g,'08b')
                b_binary = format(b,'08b')

                # Check if extracted bits are the same as the token
                if message[-24:] != stop_token:
                    message = message + r_binary[-1]
                if message[-24:] != stop_token:
                    message = message + g_binary[-1]
                if message[-24:] != stop_token:
                    message = message + b_binary[-1]
                if message[-24:] != stop_token:
                    continue
                else:
                    stop = True
                    break

    # Strip the start and stop tokens
    message = message[24:-24]
    #create a list of 8 bit strings
    character_list = [message[x:x+8] for x in range(0,len(message),8)]
    # Convert extracted 8-bit binary to bytes ensure byteorder big endian to fix reveresed character bug
    bytes_char_list = [int(x, 2).to_bytes(2, byteorder='big', signed=False) for x in character_list]
    # Generate string from list elements
    output = ''.join([chr(int.from_bytes(x, 'big', signed="False")) for x in bytes_char_list])

    if verbose: print('Message extraction complete.')
    return output



def open_file(filename: str, verbose: bool) -> cv2:
    '''
    open the carrier file and return the opencv image object
    '''
    if verbose: print(f"Opening: {filename}")
    image = cv2.imread(filename)
    return image



def main():
    print()
    # Check CLI arguments are valid.
    parser = argparse.ArgumentParser(
                        prog='StegTool',
                        description='A comand line tool to encode a secret message within an image file.')
    parser.add_argument('filename',
                        type=str,
                        help='name of file to perform steganographic function on')
    parser.add_argument('-e', '--encode',
                        help='Performs steganographic encode function',
                        action='store_true')
    parser.add_argument('-d','--decode',
                        help='Performs steganographic decode function',
                        action='store_true')
    parser.add_argument('message',
                        type=str,
                        help='Text string of message to be encoded')
    parser.add_argument('-v', '--verbose',
                        help='Enables a verbose output. Program will output what it is doing.',
                        action='store_true',
                        required=False)

    args = parser.parse_args()


    # Quit program if both or neither flag is set
    if args.encode and args.decode:
        print("Only use the --encode or --decode flag, not both")
        sys.exit()
    elif not args.encode and not args.decode:
        print('Must use one of the --encode or --decode flags')
        sys.exit()

    # Check carrier file exists.
    if not os.path.isfile(args.filename):
       print("No such file exists.")
       sys.exit()

    # Check carrier filetype is valid
    if not (args.filename[-4:] in FILETYPES or args.filename[-5:] in FILETYPES):
        print("Unsupported filetype.")
        sys.exit()

    # Open carrier image with Opencv
    carrier = open_file(args.filename, args.verbose)

    # From provided arguments perform encode or decode functionality.
    if args.encode:
        encoded_carrier = encode(carrier, args.message, args.filename, args.verbose)
        save_image(encoded_carrier, args.filename, args.verbose)
    elif args.decode:
        print(f"Secret Message: {decode(carrier, args.verbose)}")

    else:
        print("ERROR: Incorrect encode/decode flag provided. Exiting.")
        sys.exit()



if __name__ == '__main__':
    main()