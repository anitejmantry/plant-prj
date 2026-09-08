import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, messagebox



# Select image


def select_image(title):
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title=title,
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp")
        ]
    )

    root.destroy()

    return file_path

# Load and prepare image

def prepare_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return None

    # Resize both images to the same size
    image = cv2.resize(
        image,
        (5000, 5000)
    )

    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    return rgb_image

# Compare two images

def compare_images(reference, input_image):

    # Convert RGB to grayscale
    reference_gray = cv2.cvtColor(
        reference,
        cv2.COLOR_RGB2GRAY
    )

    input_gray = cv2.cvtColor(
        input_image,
        cv2.COLOR_RGB2GRAY
    )


    # Calculate absolute difference
    difference = cv2.absdiff(
        reference_gray,
        input_gray
    )


    # Remove small image noise
    difference = cv2.GaussianBlur(
        difference,
        (5, 5),
        0
    )


    # Threshold the difference
    _, difference_mask = cv2.threshold(
        difference,
        30,
        255,
        cv2.THRESH_BINARY
    )


    # Remove small noise
    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    difference_mask = cv2.morphologyEx(
        difference_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    difference_mask = cv2.morphologyEx(
        difference_mask,
        cv2.MORPH_CLOSE,
        kernel
    )


    # Calculate percentage of changed pixels

    total_pixels = (
        difference_mask.shape[0]
        * difference_mask.shape[1]
    )

    changed_pixels = np.count_nonzero(
        difference_mask
    )

    difference_percentage = (
        changed_pixels
        / total_pixels
    ) * 100


    return difference, difference_mask, difference_percentage

# Main program


print()
print("==============================================")
print("       TULSI PLANT INFECTION DETECTION")
print("==============================================")
print()


# Select reference image

print("Select the reference Tulsi plant image.")

reference_path = select_image(
    "Select Reference Tulsi Plant Image"
)


if not reference_path:

    messagebox.showerror(
        "Error",
        "Reference image was not selected."
    )

    exit()

# Select new image


print("Select the Tulsi plant image to test.")

input_path = select_image(
    "Select Tulsi Plant Image to Test"
)


if not input_path:

    messagebox.showerror(
        "Error",
        "Test image was not selected."
    )

    exit()


print()
print("Reference image:")
print(reference_path)

print()
print("Test image:")
print(input_path)

print()

# Prepare images


reference_image = prepare_image(
    reference_path
)

input_image = prepare_image(
    input_path
)


if reference_image is None:

    messagebox.showerror(
        "Error",
        "Could not read the reference image."
    )

    exit()


if input_image is None:

    messagebox.showerror(
        "Error",
        "Could not read the test image."
    )

    exit()

# Compare


difference, difference_mask, difference_percentage = (
    compare_images(
        reference_image,
        input_image
    )
)


print(
    f"Difference detected: "
    f"{difference_percentage:.2f}%"
)

# Infection threshold

# This value can be changed after testing
# with your actual Tulsi images.

THRESHOLD = 8.0


if difference_percentage >= THRESHOLD:

    result = "INFECTED"

    result_message = (
        "Difference detected between the images.\n\n"
        "Result: POSSIBLY INFECTED"
    )

else:

    result = "NOT INFECTED"

    result_message = (
        "No significant difference detected.\n\n"
        "Result: NOT INFECTED"
    )


print()
print("==============================================")
print("RESULT")
print("==============================================")
print()

print(
    f"Difference: "
    f"{difference_percentage:.2f}%"
)

print(
    f"Threshold: "
    f"{THRESHOLD:.2f}%"
)

print(
    f"Status: {result}"
)

print()

# Create highlighted difference image


highlighted = input_image.copy()


# Red highlight where difference exists
highlighted[difference_mask > 0] = [
    255,
    0,
    0
]


# Blend original and highlighted image

highlighted = cv2.addWeighted(
    input_image,
    0.7,
    highlighted,
    0.3,
    0
)

# Display results

plt.figure(
    figsize=(15, 5)
)


# Reference image

plt.subplot(
    1,
    3,
    1
)

plt.imshow(
    reference_image
)

plt.title(
    "Reference Tulsi Image"
)

plt.axis("off")


# Test image

plt.subplot(
    1,
    3,
    2
)

plt.imshow(
    input_image
)

plt.title(
    "Test Tulsi Image"
)

plt.axis("off")


# Difference

plt.subplot(
    1,
    3,
    3
)

plt.imshow(
    highlighted
)

plt.title(
    f"Difference: "
    f"{difference_percentage:.2f}%"
)

plt.axis("off")


plt.tight_layout()

plt.show()

# Final message

root = Tk()
root.withdraw()

messagebox.showinfo(
    "Tulsi Plant Result",
    f"Difference detected: "
    f"{difference_percentage:.2f}%\n\n"
    f"Result: {result}"
)

root.destroy()