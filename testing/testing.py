from PIL import Image
import PIL

image = Image.open("test.jpg")
for y in range(image.height):
    for x in range(image.width):
        r,g,b = image.getpixel((x,y))

        # Convert values to binary
        r_binary = format(r,'08b')
        g_binary = format(g,'08b')
        b_binary = format(b,'08b')

        r_binary = r_binary[:-1] + "0"
        g_binary = g_binary[:-1] + "0"
        b_binary = b_binary[:-1] + "0"

        # Convert back to integers
        r_int = int(r_binary, 2)
        g_int = int(g_binary, 2)
        b_int = int(b_binary, 2)

        print(r_int)

        image.putpixel((x,y), (r_int, g_int, b_int))


image.save("test_test.jpg")
image.close()

image_2 = Image.open("test_test.jpg")
bits = []

for y in range(image_2.height):
    for x in range(image_2.width):
        r,g,b = image_2.getpixel((x,y))

        # Convert values to binary
        r_binary = format(r,'08b')
        g_binary = format(g,'08b')
        b_binary = format(b,'08b')

        r_int = int(r_binary, 2)
        #print(r_binary + ' ' + str(r_int))

        bits.append(r_binary[-1])
        bits.append(g_binary[-1])
        bits.append(b_binary[-1])

image_2.close()
#print(''.join(bits))