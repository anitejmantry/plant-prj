import cv2
import pandas as pd
import matplotlib

# Use interactive backend (important for PyCharm)
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# ---------------- Read Image ----------------
image = cv2.imread("pic12.jpeg")

if image is None:
    print("Image not found!")
    exit()

image = cv2.resize(image, (250, 250))
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

rows, cols, _ = image.shape

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

# ---------------- Store Pixel Data ----------------
for i in range(rows):
    for j in range(cols):

        r, g, b = image[i, j]

        color = detect_color(r, g, b)

        results.append([i, j, r, g, b, color])

# ---------------- Dashboard ----------------
fig, ax = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(bottom=0.18)

ax.imshow(image)
ax.set_title("Color Detection Dashboard")
ax.axis("off")

text = fig.text(
    0.02,
    0.02,
    "Move cursor over image",
    fontsize=11,
    color="blue"
)

# ---------------- Mouse Hover ----------------
def hover(event):

    if event.inaxes == ax and event.xdata is not None and event.ydata is not None:

        x = min(max(int(event.xdata), 0), cols - 1)
        y = min(max(int(event.ydata), 0), rows - 1)

        r, g, b = image[y, x]

        color = detect_color(r, g, b)

        text.set_text(
            f"Pixel ({y}, {x})   RGB=({r}, {g}, {b})   Color={color}"
        )

        fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

# ---------------- Save Button ----------------
button_ax = plt.axes([0.72, 0.04, 0.22, 0.06])
button = Button(button_ax, "Save Results")

def save(event):

    df = pd.DataFrame(
        results,
        columns=["Row", "Column", "R", "G", "B", "Color"]
    )

    df.to_csv("Detected_Colors.csv", index=False)

    print("Results Saved as Detected_Colors.csv")

button.on_clicked(save)

plt.show()