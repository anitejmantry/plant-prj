import os
import sys
import cv2
import pandas as pd
import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import messagebox


# Find the folder where the program is running
if getattr(sys, "frozen", False):
    base_folder = os.path.dirname(os.path.abspath(sys.executable))
else:
    base_folder = os.path.dirname(os.path.abspath(__file__))

folder_path = os.path.join(base_folder, "immmg")

results = []


def detect_color(r, g, b):
    r = int(r)
    g = int(g)
    b = int(b)

    if r < 40 and g < 40 and b < 40:
        return "Black"

    elif r > 220 and g > 220 and b > 220:
        return "White"

    elif r > 200 and g < 80 and b < 80:
        return "Red"

    elif r > 80 and r > g * 1.5 and r > b * 1.5 and g < 100 and b < 100:
        return "Maroon"

    elif r > 200 and 80 <= g <= 180 and b < 100:
        return "Orange"

    elif r > 180 and 130 <= g <= 200 and b < 100:
        return "Gold"

    elif r > 180 and g > 180 and b < 100:
        return "Yellow"

    elif r > 100 and g > 180 and b < 100:
        return "Lime"

    elif g > 160 and r < 100 and b < 120:
        return "Green"

    elif r > 100 and g > 100 and b < 100 and abs(r - g) < 70:
        return "Olive"

    elif g > 100 and b > 100 and r < 100 and abs(g - b) < 80:
        return "Teal"

    elif g > 160 and b > 160 and r < 100:
        return "Cyan"

    elif b > 80 and b < 180 and r < 80 and g < 100:
        return "Navy"

    elif b > 160 and r < 100 and g < 150:
        return "Blue"

    elif r > 160 and b > 160 and g < 100:
        return "Magenta"

    elif r > 130 and b > 160 and g < 130:
        return "Violet"

    elif r > 100 and b > 130 and g < 120:
        return "Purple"

    elif r > 180 and b > 130 and 70 <= g < 170:
        return "Pink"

    elif r > 100 and 50 <= g <= 140 and b < 100 and r > g:
        return "Brown"

    elif r > 180 and g > 160 and 110 < b < 200:
        return "Beige"

    elif (
        r > 180 and
        g > 180 and
        b > 180 and
        abs(r - g) < 20 and
        abs(g - b) < 20
    ):
        return "Light Gray"

    elif (
        r > 100 and
        g > 100 and
        b > 100 and
        abs(r - g) < 20 and
        abs(g - b) < 20
    ):
        return "Gray"

    elif (
        r > 40 and
        g > 40 and
        b > 40 and
        abs(r - g) < 20 and
        abs(g - b) < 20
    ):
        return "Dark Gray"

    return "Mixed"


# Supported image formats
extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp"
)


# Check if the image folder exists
if not os.path.exists(folder_path):
    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(
        "Folder Not Found",
        "The 'immg' folder was not found.\n\n"
        "Expected location:\n" + folder_path
    )

    root.destroy()
    sys.exit()


# Get all images from the folder
image_files = [
    file for file in os.listdir(folder_path)
    if file.lower().endswith(extensions)
]

image_files.sort()


if len(image_files) == 0:
    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(
        "No Images",
        "No supported images were found in:\n\n" + folder_path
    )

    root.destroy()
    sys.exit()


print("RGB Color Detection System")
print("--------------------------")
print("Image folder:", folder_path)
print("Images found:", len(image_files))
print()


# Process all images
for number, image_name in enumerate(image_files, 1):

    image_path = os.path.join(folder_path, image_name)

    image = cv2.imread(image_path)

    if image is None:
        print("Could not read:", image_name)
        continue

    image = cv2.resize(image, (250, 250))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    rows, cols, _ = image.shape

    print(
        f"Processing {number}/{len(image_files)}: "
        f"{image_name}"
    )

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


print()
print("Processing completed.")
print("Total pixel records:", len(results))


# Save the results
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

output_file = os.path.join(
    base_folder,
    "Detected_Colors.csv"
)

df.to_csv(output_file, index=False)

print("Results saved to:", output_file)


# Image navigation
current_index = 0


def load_image(index):
    path = os.path.join(
        folder_path,
        image_files[index]
    )

    image = cv2.imread(path)

    if image is None:
        return None

    image = cv2.resize(image, (250, 250))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image


current_image = load_image(current_index)

if current_image is None:
    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(
        "Image Error",
        "The first image could not be loaded."
    )

    root.destroy()
    sys.exit()


rows, cols, _ = current_image.shape


# Create the dashboard
fig, ax = plt.subplots(figsize=(8, 8))

plt.subplots_adjust(
    left=0.08,
    right=0.92,
    top=0.88,
    bottom=0.25
)

image_display = ax.imshow(current_image)

ax.set_title(
    f"Image 1 / {len(image_files)}\n"
    f"{image_files[current_index]}",
    fontsize=14
)

ax.axis("off")


info_text = fig.text(
    0.5,
    0.14,
    "Move the mouse over the image",
    ha="center",
    va="center",
    fontsize=12
)

navigation_text = fig.text(
    0.5,
    0.095,
    f"Image 1 of {len(image_files)}",
    ha="center",
    va="center",
    fontsize=11
)


# Navigation buttons
previous_ax = plt.axes(
    [0.28, 0.025, 0.18, 0.055]
)

previous_button = Button(
    previous_ax,
    "Previous"
)


next_ax = plt.axes(
    [0.54, 0.025, 0.18, 0.055]
)

next_button = Button(
    next_ax,
    "Next"
)


def update_image():

    global current_image
    global rows
    global cols

    current_image = load_image(current_index)

    if current_image is None:
        return

    rows, cols, _ = current_image.shape

    image_display.set_data(current_image)

    ax.set_title(
        f"Image {current_index + 1} / {len(image_files)}\n"
        f"{image_files[current_index]}",
        fontsize=14
    )

    navigation_text.set_text(
        f"Image {current_index + 1} of {len(image_files)}"
    )

    info_text.set_text(
        "Move the mouse over the image"
    )

    previous_button.ax.set_visible(
        current_index > 0
    )

    next_button.ax.set_visible(
        current_index < len(image_files) - 1
    )

    fig.canvas.draw_idle()


def next_image(event):

    global current_index

    if current_index < len(image_files) - 1:
        current_index += 1
        update_image()


def previous_image(event):

    global current_index

    if current_index > 0:
        current_index -= 1
        update_image()


def hover(event):

    if (
        event.inaxes != ax
        or event.xdata is None
        or event.ydata is None
    ):
        return

    x = min(
        max(int(event.xdata), 0),
        cols - 1
    )

    y = min(
        max(int(event.ydata), 0),
        rows - 1
    )

    r, g, b = current_image[y, x]

    color = detect_color(r, g, b)

    info_text.set_text(
        f"Pixel: ({y}, {x})    "
        f"RGB: ({int(r)}, {int(g)}, {int(b)})    "
        f"Color: {color}"
    )

    fig.canvas.draw_idle()


next_button.on_clicked(next_image)
previous_button.on_clicked(previous_image)

fig.canvas.mpl_connect(
    "motion_notify_event",
    hover
)


previous_button.ax.set_visible(False)

if len(image_files) <= 1:
    next_button.ax.set_visible(False)


plt.show()