import cv2
import matplotlib.pyplot as plt

# Read image
image = cv2.imread("pic11.jpg")

if image is None:
    print("Image not found!")
    exit()

# Resize for easy testing
image = cv2.resize(image, (25, 25))

# Convert BGR to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

rows, cols, _ = image.shape

print("Detected Colors:\n")

for i in range(rows):
    for j in range(cols):

        r, g, b = image[i, j]

        # Simple color detection
        # Simple color detection

        if r > 200 and 80 <= g <= 180 and b < 100:
            color = "Orange"

        elif r > 150 and 50 <= g <= 120 and b < 80:
            color = "Brown"

        elif r > 200 and g < 100 and b < 100:
            color = "Red"

        elif g > 180 and r < 100 and b < 100:
            color = "Green"

        elif b > 180 and r < 100 and g < 100:
            color = "Blue"

        elif r > 200 and g > 180 and b < 100:
            color = "Yellow"

        elif r > 200 and g > 200 and b > 200:
            color = "White"

        elif r < 50 and g < 50 and b < 50:
            color = "Black"

        else:
            color = "Mixed Color"

        print(f"Pixel ({i},{j}) -> RGB({r},{g},{b}) : {color}")

# Show image
plt.imshow(image)
plt.title("Test Image")
plt.axis("off")
plt.show()