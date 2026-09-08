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

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.drawing.image import Image as ExcelImage


# ------------------------------------------------------------
# Find application folder
# ------------------------------------------------------------

if getattr(sys, "frozen", False):
    base_folder = os.path.dirname(
        os.path.abspath(sys.executable)
    )
else:
    base_folder = os.path.dirname(
        os.path.abspath(__file__)
    )


# Image folder
folder_path = os.path.join(
    base_folder,
    "imgdect"
)


# ------------------------------------------------------------
# Color detection
# ------------------------------------------------------------

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

    elif r > 180 and b > 130 and 70 <= g < 170:
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


# ------------------------------------------------------------
# Check image folder
# ------------------------------------------------------------

if not os.path.exists(folder_path):

    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(
        "Folder Not Found",
        "Image folder was not found.\n\n"
        "Expected location:\n"
        + folder_path
    )

    root.destroy()
    sys.exit()


# ------------------------------------------------------------
# Find images
# ------------------------------------------------------------

extensions = (
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp"
)

image_files = [
    file
    for file in os.listdir(folder_path)
    if file.lower().endswith(extensions)
]

image_files.sort()


if len(image_files) == 0:

    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(
        "No Images",
        "No supported images were found in:\n\n"
        + folder_path
    )

    root.destroy()
    sys.exit()


print("RGB Color Detection")
print("-------------------")
print("Images found:", len(image_files))
print()


# ------------------------------------------------------------
# Store results
# ------------------------------------------------------------

image_results = []


# ------------------------------------------------------------
# Process every image
# ------------------------------------------------------------

for number, image_name in enumerate(
    image_files,
    start=1
):

    image_path = os.path.join(
        folder_path,
        image_name
    )

    image = cv2.imread(image_path)

    if image is None:

        print("Could not read:", image_name)
        continue


    image = cv2.resize(
        image,
        (250, 250)
    )

    image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )


    rows, cols, _ = image.shape

    color_counts = {}


    print(
        f"Processing {number}/{len(image_files)}: "
        f"{image_name}"
    )


    # Process pixels

    for i in range(rows):

        for j in range(cols):

            r, g, b = image[i, j]

            color = detect_color(
                r,
                g,
                b
            )

            if color not in color_counts:
                color_counts[color] = 0

            color_counts[color] += 1


    total_pixels = rows * cols


    # Find dominant color

    if color_counts:

        dominant_color = max(
            color_counts,
            key=color_counts.get
        )

    else:

        dominant_color = "Unknown"


    # Create image ID

    image_id = f"IMG_{number:04d}"


    # Create result

    result = {
        "Image ID": image_id,
        "Image Name": image_name,
        "Image Path": image_path,
        "Dominant Color": dominant_color
    }


    # Add color percentages

    all_colors = [
        "White",
        "Black",
        "Red",
        "Maroon",
        "Orange",
        "Gold",
        "Yellow",
        "Lime",
        "Green",
        "Olive",
        "Teal",
        "Cyan",
        "Navy",
        "Blue",
        "Magenta",
        "Violet",
        "Purple",
        "Pink",
        "Brown",
        "Beige",
        "Light Gray",
        "Gray",
        "Dark Gray",
        "Mixed"
    ]


    for color in all_colors:

        count = color_counts.get(
            color,
            0
        )

        percentage = (
            count / total_pixels
        ) * 100

        result[
            color + " %"
        ] = round(
            percentage,
            2
        )


    image_results.append(result)


print()
print("Image processing completed.")
print()


# ------------------------------------------------------------
# Create Excel workbook
# ------------------------------------------------------------

workbook = Workbook()

index_sheet = workbook.active

index_sheet.title = "Image Index"


# ------------------------------------------------------------
# Main sheet headers
# ------------------------------------------------------------

headers = [
    "Image ID",
    "Image Name",
    "Open Image",
    "Image Path",
    "Dominant Color"
]


for column, header in enumerate(
    headers,
    start=1
):

    cell = index_sheet.cell(
        row=1,
        column=column
    )

    cell.value = header

    cell.font = Font(
        bold=True,
        color="FFFFFF"
    )

    cell.fill = PatternFill(
        "solid",
        fgColor="1F4E78"
    )

    cell.alignment = Alignment(
        horizontal="center"
    )


# ------------------------------------------------------------
# Add image information to index
# ------------------------------------------------------------

for row_number, result in enumerate(
    image_results,
    start=2
):

    image_id = result["Image ID"]

    image_name = result["Image Name"]

    image_path = result["Image Path"]

    dominant_color = result[
        "Dominant Color"
    ]


    index_sheet.cell(
        row=row_number,
        column=1
    ).value = image_id


    index_sheet.cell(
        row=row_number,
        column=2
    ).value = image_name


    # Hyperlink to actual image

    image_link = "file:///" + image_path.replace(
        "\\",
        "/"
    )


    open_image_cell = index_sheet.cell(
        row=row_number,
        column=3
    )

    open_image_cell.value = "Open Image"

    open_image_cell.hyperlink = image_link

    open_image_cell.style = "Hyperlink"


    index_sheet.cell(
        row=row_number,
        column=4
    ).value = image_path


    index_sheet.cell(
        row=row_number,
        column=5
    ).value = dominant_color


# ------------------------------------------------------------
# Create individual sheet for every image
# ------------------------------------------------------------

for result in image_results:

    image_id = result["Image ID"]

    image_name = result["Image Name"]

    image_path = result["Image Path"]


    # Excel sheet names cannot contain some characters
    sheet_name = image_id[:31]


    sheet = workbook.create_sheet(
        title=sheet_name
    )


    # Title

    sheet["A1"] = image_id

    sheet["A1"].font = Font(
        bold=True,
        size=18
    )


    sheet["A2"] = "Image Name"

    sheet["B2"] = image_name


    sheet["A3"] = "Dominant Color"

    sheet["B3"] = result[
        "Dominant Color"
    ]


    # Link back to index

    sheet["A5"] = "Back to Image Index"

    sheet["A5"].hyperlink = (
        "#'Image Index'!A1"
    )

    sheet["A5"].style = "Hyperlink"


    # Insert image into worksheet

    try:

        excel_image = ExcelImage(
            image_path
        )

        excel_image.width = 400
        excel_image.height = 400

        sheet.add_image(
            excel_image,
            "A7"
        )

    except Exception as e:

        sheet["A7"] = (
            "Unable to display image: "
            + str(e)
        )


    # Add color information

    start_row = 29

    sheet.cell(
        row=start_row,
        column=1
    ).value = "Color"

    sheet.cell(
        row=start_row,
        column=2
    ).value = "Percentage"


    sheet.cell(
        row=start_row,
        column=1
    ).font = Font(
        bold=True
    )

    sheet.cell(
        row=start_row,
        column=2
    ).font = Font(
        bold=True
    )


    row = start_row + 1


    for key, value in result.items():

        if key.endswith(" %"):

            sheet.cell(
                row=row,
                column=1
            ).value = key[:-2]

            sheet.cell(
                row=row,
                column=2
            ).value = value

            row += 1


    sheet.column_dimensions[
        "A"
    ].width = 25

    sheet.column_dimensions[
        "B"
    ].width = 25


# ------------------------------------------------------------
# Formatting
# ------------------------------------------------------------

index_sheet.freeze_panes = "A2"

index_sheet.auto_filter.ref = (
    index_sheet.dimensions
)


index_sheet.column_dimensions[
    "A"
].width = 15

index_sheet.column_dimensions[
    "B"
].width = 40

index_sheet.column_dimensions[
    "C"
].width = 20

index_sheet.column_dimensions[
    "D"
].width = 70

index_sheet.column_dimensions[
    "E"
].width = 20


# ------------------------------------------------------------
# Save workbook
# ------------------------------------------------------------

excel_file = os.path.join(
    base_folder,
    "Detected_Colors.xlsx"
)


workbook.save(
    excel_file
)


print(
    "Excel file created:"
)

print(
    excel_file
)


# ------------------------------------------------------------
# Final message
# ------------------------------------------------------------

root = tk.Tk()
root.withdraw()

messagebox.showinfo(
    "Completed",
    "Processing completed.\n\n"
    "Images processed: "
    + str(len(image_results))
    + "\n\n"
    "Excel file:\n"
    + excel_file
)

root.destroy()