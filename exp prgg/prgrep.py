import os
import cv2
import pandas as pd
import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Configuration & paths
FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")

results = []


def detect_color(r, g, b):
    r, g, b = int(r), int(g), int(b)

    # Simple RGB heuristics
    if r < 40 and g < 40 and b < 40:
        return "Black"
    if r > 220 and g > 220 and b > 220:
        return "White"
    if r > 200 and g < 80 and b < 80:
        return "Red"
    if r > 80 and r > g * 1.5 and r > b * 1.5 and g < 100 and b < 100:
        return "Maroon"
    if r > 200 and 80 <= g <= 180 and b < 100:
        return "Orange"
    if r > 180 and 130 <= g <= 200 and b < 100:
        return "Gold"
    if r > 180 and g > 180 and b < 100:
        return "Yellow"
    if r > 100 and g > 180 and b < 100:
        return "Lime"
    if g > 160 and r < 100 and b < 120:
        return "Green"
    if r > 100 and g > 100 and b < 100 and abs(r - g) < 70:
        return "Olive"
    if g > 100 and b > 100 and r < 100 and abs(g - b) < 80:
        return "Teal"
    if g > 160 and b > 160 and r < 100:
        return "Cyan"
    if 80 < b < 180 and r < 80 and g < 100:
        return "Navy"
    if b > 160 and r < 100 and g < 150:
        return "Blue"
    if r > 160 and b > 160 and g < 100:
        return "Magenta"
    if r > 130 and b > 160 and g < 130:
        return "Violet"
    if r > 100 and b > 130 and g < 120:
        return "Purple"
    if r > 180 and b > 130 and 70 <= g < 170:
        return "Pink"
    if r > 100 and 50 <= g <= 140 and b < 100 and r > g:
        return "Brown"
    if r > 180 and g > 160 and 110 < b < 200:
        return "Beige"
    if r > 180 and g > 180 and b > 180 and abs(r - g) < 20 and abs(g - b) < 20:
        return "Light Gray"
    if r > 100 and g > 100 and b > 100 and abs(r - g) < 20 and abs(g - b) < 20:
        return "Gray"
    if r > 40 and g > 40 and b > 40 and abs(r - g) < 20 and abs(g - b) < 20:
        return "Dark Gray"

    return "Mixed"


image_files = sorted([immg for immg in os.listdir(immg) if immg.lower().endswith(IMAGE_EXTENSIONS)])

if not image_files:
    print(f"Error: No valid images found in {FOLDER_PATH}")
    exit()

print(f"Found {len(image_files)} images in directory. Processing pixel data...")

for idx, immg in enumerate(image_files, 1):
    img_path = os.path.join(FOLDER_PATH, immg)
    img = cv2.imread(img_path)

    if img is None:
        print(f"[{idx}/{len(image_files)}] Failed to load {immg}")
        continue

    img = cv2.resize(img, (250, 250))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    rows, cols, _ = img.shape
    for i in range(rows):
        for j in range(cols):
            r, g, b = img[i, j]
            color_label = detect_color(r, g, b)
            results.append([immg, i, j, int(r), int(g), int(b), color_label])

# Save output
df = pd.DataFrame(results, columns=["Image Name", "Row", "Column", "R", "G", "B", "Color"])
csv_path = os.path.join(FOLDER_PATH, "Detected_Colors.csv")
df.to_csv(csv_path, index=False)
print(f"Saved {len(results):,} pixel records to {csv_path}")

# Dashboard state & helper
current_idx = 0


def load_img(index):
    immg = image_files[index]
    path = os.path.join(FOLDER_PATH, immg)
    img = cv2.imread(path)
    img = cv2.resize(img, (250, 250))
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


curr_img = load_img(current_idx)
rows, cols, _ = curr_img.shape

# UI Setup
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.08, right=0.92, top=0.88, bottom=0.25)

img_display = ax.imshow(curr_img)
ax.axis("off")
ax.set_title(f"Image 1 / {len(image_files)}\n{image_files[current_idx]}", fontsize=12, pad=10)

info_text = fig.text(0.5, 0.14, "Hover cursor over image...", ha="center", va="center", fontsize=11)
nav_text = fig.text(0.5, 0.095, f"Image 1 of {len(image_files)}", ha="center", va="center", fontsize=10)

btn_prev_ax = plt.axes([0.28, 0.025, 0.18, 0.055])
btn_next_ax = plt.axes([0.54, 0.025, 0.18, 0.055])

btn_prev = Button(btn_prev_ax, "Previous")
btn_next = Button(btn_next_ax, "Next")


def update_dashboard():
    global curr_img, rows, cols

    curr_img = load_img(current_idx)
    rows, cols, _ = curr_img.shape

    img_display.set_data(curr_img)
    ax.set_title(f"Image {current_idx + 1} / {len(image_files)}\n{image_files[current_idx]}", fontsize=12, pad=10)
    nav_text.set_text(f"Image {current_idx + 1} of {len(image_files)}")
    info_text.set_text("Hover cursor over image...")

    btn_prev.ax.set_visible(current_idx > 0)
    btn_next.ax.set_visible(current_idx < len(image_files) - 1)

    fig.canvas.draw_idle()


def on_next(event):
    global current_idx
    if current_idx < len(image_files) - 1:
        current_idx += 1
        update_dashboard()


def on_prev(event):
    global current_idx
    if current_idx > 0:
        current_idx -= 1
        update_dashboard()


btn_next.on_clicked(on_next)
btn_prev.on_clicked(on_prev)


def on_hover(event):
    if event.inaxes == ax and event.xdata is not None and event.ydata is not None:
        x = min(max(int(event.xdata), 0), cols - 1)
        y = min(max(int(event.ydata), 0), rows - 1)

        r, g, b = curr_img[y, x]
        color = detect_color(r, g, b)
        info_text.set_text(f"Pixel: ({y}, {x})  |  RGB: ({int(r)}, {int(g)}, {int(b)})  |  Color: {color}")
        fig.canvas.draw_idle()


fig.canvas.mpl_connect("motion_notify_event", on_hover)

btn_prev.ax.set_visible(False)
if len(image_files) <= 1:
    btn_next.ax.set_visible(False)

plt.show()