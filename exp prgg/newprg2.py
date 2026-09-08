import os
import cv2
import pandas as pd
import matplotlib

# Use interactive backend (important for PyCharm)
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# ---------------- Folder Path ----------------
folder_path = "immg"      # Folder containing all images
results = []

# ---------------- Color Detection ----------------
def detect_color(r, g, b):

    if r > 220 and g > 220 and b > 220:
        return "White"

    elif r < 40 and g < 40 and b < 40:
        return "Black"

    elif r > 200 and g < 80 and b < 80:
        return "Red"

    elif r > 200 and 100 <= g <= 190 and b < 80:
        return "Orange"

    elif r > 180 and g > 180 and b < 80:
        return "Yellow"

    elif r > 120 and 60 <= g <= 120 and b < 70:
        return "Brown"

    elif g > 180 and r < 120 and b < 120:
        return "Green"

    elif b > 180 and r < 120 and g < 120:
        return "Blue"

    elif r > 180 and b > 180:
        return "Pink"

    elif r > 120 and g > 120 and b > 120:
        return "Gray"

    else:
        return "Mixed"

# ---------------- Process All Images ----------------
image_extensions = (".jpg", ".jpeg", ".png", ".bmp")

image_files = [
    f for f in os.listdir(folder_path)
    if f.lower().endswith(image_extensions)
]

print(f"Total Images Found: {len(image_files)}")

for image_name in image_files:

    image_path = os.path.join(folder_path, image_name)

    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not read {image_name}")
        continue

    image = cv2.resize(image, (250, 250))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    rows, cols, _ = image.shape

    print(f"Processing {image_name}...")

    for i in range(rows):
        for j in range(cols):

            r, g, b = image[i, j]

            color = detect_color(r, g, b)

            results.append([
                image_name,
                i,
                j,
                int(r),
                int(g),
                int(b),
                color
            ])

print("All Images Processed.")

# ---------------- Save Results ----------------
df = pd.DataFrame(
    results,
    columns=[
        "Image Name",
        "Row",
        "Column",
        "R",
        "G",
        "B",
        "Color"
    ]
)

df.to_csv("Detected_Colors.csv", index=False)

print("Results Saved as Detected_Colors.csv")

# ---------------- Display First Image ----------------
if len(image_files) > 0:

    first_image = cv2.imread(os.path.join(folder_path, image_files[0]))
    first_image = cv2.resize(first_image, (250, 250))
    first_image = cv2.cvtColor(first_image, cv2.COLOR_BGR2RGB)

    rows, cols, _ = first_image.shape

    fig, ax = plt.subplots(figsize=(6,6))
    plt.subplots_adjust(bottom=0.18)

    ax.imshow(first_image)
    ax.set_title("Color Detection Dashboard")
    ax.axis("off")

    text = fig.text(
        0.02,
        0.02,
        "Move cursor over image",
        fontsize=11,
        color="blue"
    )

    def hover(event):

        if event.inaxes == ax and event.xdata is not None and event.ydata is not None:

            x = min(max(int(event.xdata),0),cols-1)
            y = min(max(int(event.ydata),0),rows-1)

            r,g,b = first_image[y,x]

            color = detect_color(r,g,b)

            text.set_text(
                f"Pixel ({y},{x}) RGB=({r},{g},{b}) Color={color}"
            )

            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    plt.show()