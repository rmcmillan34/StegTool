import cv2

img = cv2.imread('steg_cv2_test.jpg')

print(f"Image Shape {img.shape}")

# Iterate over pixels using cv2
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        (b,g,r) = img[y][x]
        print(f"B:{b} G:{g} R:{r}")
        #(b,g,r) = (0,0,255)
        #img[y][x] = (b,g,r)

# write to file using cv2
#cv2.imwrite("cv2_test.jpg", img)