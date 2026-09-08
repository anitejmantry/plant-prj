import math
from collections import Counter

import cv2
import matplotlib.pyplot as plt

# -----------------------------
# Basic RGB Colors
# -----------------------------
colors = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Gray": (128, 128, 128)
}

# -----------------------------
# Function to detect nearest color
# -----------------------------
def detect_color(r, g, b):
    min_distance = float("inf")
    detected = ""

    for color_name, (cr, cg, cb) in colors.items():

        distance = math.sqrt(
            (r - cr) ** 2 +
            (g - cg) ** 2 +
            (b - cb) ** 2
        )

        if distance < min_distance:
            min_distance = distance
            detected = color_name

    return detected


# -----------------------------
# Read Image
# -----------------------------
image = cv2.imread("pic11.jpg")

if image is None:
    print("Image not found!")
    exit()

# Convert BGR to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

rows, cols, _ = image.shape

color_counter = Counter()

print("\nDetected Colors:\n")

# -----------------------------
# Detect color of every pixel
# -----------------------------
for i in range(rows):
    for j in range(cols):

        r, g, b = image[i, j]

        color = detect_color(r, g, b)

        color_counter[color] += 1

        print(f"Pixel ({i},{j}) -> RGB({r},{g},{b}) = {color}")

# -----------------------------
# Print Summary
# -----------------------------
print("\n-------------------------")
print("Color Summary")
print("-------------------------")

total_pixels = rows * cols

for color, count in color_counter.items():

    percentage = (count / total_pixels) * 100

    print(f"{color:10} : {count} pixels ({percentage:.2f}%)")

dominant = color_counter.most_common(1)[0]

print("\nDominant Color :", dominant[0])

# -----------------------------
# Display Image
# -----------------------------
plt.figure(figsize=(6,6))
plt.imshow(image)
plt.title(f"Dominant Color : {dominant[0]}")
plt.axis("off")
plt.show()