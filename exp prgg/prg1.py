import cv2
image = cv2.imread("pic11.jpg")

# Resize to 5x5
image = cv2.resize(image, (5, 5))

# OpenCV stores image as BGR, convert to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

rows, cols, _ = image.shape

for i in range(rows):
    for j in range(cols):
        r, g, b = image[i, j]
        print(f"Pixel ({i},{j}) -> R={r}, G={g}, B={b}")