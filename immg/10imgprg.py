import os
import cv2
import pandas as pd
import matplotlib

# ============================================================
# MATPLOTLIB BACKEND
# ============================================================

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.widgets import Button


# ============================================================
# IMAGE FOLDER
# ============================================================


folder_path = os.path.dirname(os.path.abspath(__file__))

# Store all pixel results
results = []


# ============================================================
# COLOR DETECTION
# ============================================================

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

    elif (
        r > 80
        and r > g * 1.5
        and r > b * 1.5
        and g < 100
        and b < 100
    ):
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

    elif (
        r > 100
        and g > 100
        and b < 100
        and abs(r - g) < 70
    ):
        return "Olive"

    elif (
        g > 100
        and b > 100
        and r < 100
        and abs(g - b) < 80
    ):
        return "Teal"

    elif g > 160 and b > 160 and r < 100:
        return "Cyan"

    elif (
        b > 80
        and b < 180
        and r < 80
        and g < 100
    ):
        return "Navy"

    elif b > 160 and r < 100 and g < 150:
        return "Blue"

    elif r > 160 and b > 160 and g < 100:
        return "Magenta"

    elif r > 130 and b > 160 and g < 130:
        return "Violet"

    elif r > 100 and b > 130 and g < 120:
        return "Purple"


    elif (
        r > 180
        and b > 130
        and 70 <= g < 170
    ):
        return "Pink"


    elif (
        r > 100
        and 50 <= g <= 140
        and b < 100
        and r > g
    ):
        return "Brown"

    elif (
        r > 180
        and g > 160
        and 110 < b < 200
    ):
        return "Beige"


    elif (
        r > 180
        and g > 180
        and b > 180
        and abs(r - g) < 20
        and abs(g - b) < 20
    ):
        return "Light Gray"


    elif (
        r > 100
        and g > 100
        and b > 100
        and abs(r - g) < 20
        and abs(g - b) < 20
    ):
        return "Gray"


    elif (
        r > 40
        and g > 40
        and b > 40
        and abs(r - g) < 20
        and abs(g - b) < 20
    ):
        return "Dark Gray"


    else:
        return "Mixed"


# ============================================================
# IMAGE EXTENSIONS
# ============================================================

image_extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp"
)


# ============================================================
# FIND ALL IMAGES
# ============================================================

image_files = []

for file_name in os.listdir(folder_path):

    if file_name.lower().endswith(image_extensions):

        image_files.append(file_name)


image_files.sort()


print()
print("=============================================")
print("       RGB COLOR DETECTION SYSTEM")
print("=============================================")

print()
print("Image Folder:")
print(folder_path)

print()
print(f"Total Images Found: {len(image_files)}")

print()
print("=============================================")



if len(image_files) == 0:

    print()
    print("ERROR: No images found!")

    print()
    print("Put your images in:")

    print(folder_path)

    input("Press Enter to exit...")

    exit()


# ============================================================
# PROCESS ALL IMAGES
# ============================================================

for image_number, image_name in enumerate(
    image_files,
    start=1
):

    image_path = os.path.join(
        folder_path,
        image_name
    )

    # Read image
    image = cv2.imread(image_path)

    if image is None:

        print(
            f"[{image_number}/{len(image_files)}] "
            f"Could not read: {image_name}"
        )

        continue


    # Resize
    image = cv2.resize(
        image,
        (250, 250)
    )


    # Convert BGR → RGB
    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )


    rows, cols, channels = image.shape


    # Display progress
    print(
        f"[{image_number}/{len(image_files)}] "
        f"Processing: {image_name}"
    )


    # --------------------------------------------------------
    # PROCESS EVERY PIXEL
    # --------------------------------------------------------

    for i in range(rows):

        for j in range(cols):

            r, g, b = image[i, j]

            color = detect_color(
                r,
                g,
                b
            )


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
print("=============================================")
print("       ALL IMAGES PROCESSED")
print("=============================================")

print()
print(
    f"Total Pixel Records: {len(results):,}"
)


# ============================================================
# CREATE DATAFRAME
# ============================================================

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
    folder_path,
    "Detected_Colors.csv"
)


df.to_csv(
    output_file,
    index=False
)


print()
print("=============================================")
print("       RESULTS SAVED SUCCESSFULLY")
print("=============================================")

print()
print("Output file:")
print(output_file)

print()
print("=============================================")


current_index = 0


# ============================================================
# LOAD IMAGE FUNCTION
# ============================================================

def load_image(index):

    image_name = image_files[index]

    image_path = os.path.join(
        folder_path,
        image_name
    )

    image = cv2.imread(
        image_path
    )

    image = cv2.resize(
        image,
        (250, 250)
    )

    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    return image


# ============================================================
# LOAD FIRST IMAGE
# ============================================================

current_image = load_image(
    current_index
)


rows, cols, _ = current_image.shape



fig, ax = plt.subplots(
    figsize=(8, 8)
)



plt.subplots_adjust(
    left=0.08,
    right=0.92,
    top=0.88,
    bottom=0.25
)


# ============================================================
# DISPLAY IMAGE
# ============================================================

image_display = ax.imshow(
    current_image
)



ax.set_title(
    f"Image 1 / {len(image_files)}\n"
    f"{image_files[current_index]}",
    fontsize=14,
    pad=12
)


# Hide axes
ax.axis("off")


# ============================================================
# RGB INFORMATION AREA
# ============================================================

info_text = fig.text(
    0.5,
    0.14,
    "Move cursor over the image",
    ha="center",
    va="center",
    fontsize=12
)


# ============================================================
# NAVIGATION INFORMATION
# ============================================================

navigation_text = fig.text(
    0.5,
    0.095,
    f"Image 1 of {len(image_files)}",
    ha="center",
    va="center",
    fontsize=11
)


previous_ax = plt.axes(
    [0.28, 0.025, 0.18, 0.055]
)


previous_button = Button(
    previous_ax,
    "← Previous"
)



next_ax = plt.axes(
    [0.54, 0.025, 0.18, 0.055]
)


next_button = Button(
    next_ax,
    "Next →"
)



def update_image():

    global current_image
    global rows
    global cols


    # Load image
    current_image = load_image(
        current_index
    )


    # Get dimensions
    rows, cols, _ = current_image.shape


    # Update image
    image_display.set_data(
        current_image
    )


    # Update title
    ax.set_title(
        f"Image {current_index + 1} / "
        f"{len(image_files)}\n"
        f"{image_files[current_index]}",
        fontsize=14,
        pad=12
    )


    # Update navigation text
    navigation_text.set_text(
        f"Image {current_index + 1} "
        f"of {len(image_files)}"
    )


    # Reset RGB information
    info_text.set_text(
        "Move cursor over the image"
    )


    # Enable / disable buttons
    previous_button.ax.set_visible(
        current_index > 0
    )

    next_button.ax.set_visible(
        current_index < len(image_files) - 1
    )


    # Refresh
    fig.canvas.draw_idle()


def next_image(event):

    global current_index


    if current_index < len(image_files) - 1:

        current_index += 1

        update_image()


# Connect Next button
next_button.on_clicked(
    next_image
)



def previous_image(event):

    global current_index


    if current_index > 0:

        current_index -= 1

        update_image()


# Connect Previous button
previous_button.on_clicked(
    previous_image
)


# ============================================================
# MOUSE HOVER
# ============================================================

def hover(event):

    if (
        event.inaxes == ax
        and event.xdata is not None
        and event.ydata is not None
    ):


        # X coordinate
        x = min(
            max(
                int(event.xdata),
                0
            ),
            cols - 1
        )


        # Y coordinate
        y = min(
            max(
                int(event.ydata),
                0
            ),
            rows - 1
        )


        # RGB values
        r, g, b = current_image[y, x]


        # Detect color
        color = detect_color(
            r,
            g,
            b
        )


        # ----------------------------------------------------
        # UPDATE RGB INFORMATION
        # ----------------------------------------------------

        info_text.set_text(
            f"Pixel: ({y}, {x})     "
            f"RGB: ({int(r)}, {int(g)}, {int(b)})     "
            f"Color: {color}"
        )


        # Refresh
        fig.canvas.draw_idle()


# Connect hover
fig.canvas.mpl_connect(
    "motion_notify_event",
    hover
)


previous_button.ax.set_visible(False)

if len(image_files) <= 1:
    next_button.ax.set_visible(False)



plt.show()