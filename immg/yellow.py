import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog


def select_image():

    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")
        ]
    )

    root.destroy()

    return file_path


# Select image
image_path = select_image()

if not image_path:
    print("No image selected.")
    exit()


# Read image
image = cv2.imread(image_path)

if image is None:
    print("Could not read image.")
    exit()


# Convert BGR to RGB
rgb_image = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2RGB
)


# Convert RGB to HSV
hsv_image = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2HSV
)


# Yellow color range

lower_yellow = np.array([
    20,
    80,
    80
])

upper_yellow = np.array([
    40,
    255,
    255
])


# Create yellow mask
yellow_mask = cv2.inRange(
    hsv_image,
    lower_yellow,
    upper_yellow
)


# Show only yellow
yellow_only = cv2.bitwise_and(
    rgb_image,
    rgb_image,
    mask=yellow_mask
)


# Hide yellow
non_yellow_mask = cv2.bitwise_not(
    yellow_mask
)

yellow_hidden = cv2.bitwise_and(
    rgb_image,
    rgb_image,
    mask=non_yellow_mask
)


# Calculate yellow percentage
total_pixels = yellow_mask.shape[0] * yellow_mask.shape[1]

yellow_pixels = np.count_nonzero(
    yellow_mask
)

yellow_percentage = (
    yellow_pixels / total_pixels
) * 100


print()
print("------------------------------")
print("YELLOW COLOR ANALYSIS")
print("------------------------------")
print(
    f"Yellow pixels: {yellow_pixels}"
)
print(
    f"Total pixels: {total_pixels}"
)
print(
    f"Yellow percentage: "
    f"{yellow_percentage:.2f}%"
)
print("------------------------------")


# Display results
plt.figure(figsize=(15, 5))


plt.subplot(1, 3, 1)

plt.imshow(rgb_image)

plt.title("Original Image")

plt.axis("off")


plt.subplot(1, 3, 2)

plt.imshow(yellow_only)

plt.title(
    f"Yellow Only\n"
    f"{yellow_percentage:.2f}%"
)

plt.axis("off")


plt.subplot(1, 3, 3)

plt.imshow(yellow_hidden)

plt.title("Yellow Hidden")

plt.axis("off")


plt.tight_layout()

plt.show()