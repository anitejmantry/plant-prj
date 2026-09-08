import cv2
import numpy as np

# Read image
image = cv2.imread("image.jpg")

# Resize
image = cv2.resize(image, (5,5))

# Convert BGR to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

rows, cols, _ = image.shape

# Create blank image
new_image = np.zeros((rows, cols, 3), dtype=np.uint8)

# Copy pixels
for i in range(rows):
    for j in range(cols):
        r, g, b = image[i, j]
        print(f"Pixel ({i},{j}) -> R={r}, G={g}, B={b}")

        new_image[i, j] = [r, g, b]

# Convert back to BGR for display
new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)

cv2.imshow("Original", cv2.resize(cv2.imread("image.jpg"), (250,250)))
cv2.imshow("Recreated", cv2.resize(new_image, (250,250)))

cv2.waitKey(0)
cv2.destroyAllWindows()