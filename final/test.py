import os
import numpy as np
import tensorflow as tf

from tkinter import Tk, filedialog, messagebox

from tensorflow.keras.preprocessing import image


MODEL_PATH = "model/tulsi_leaf_model.keras"
CLASS_FILE = "model/classes.txt"

IMG_SIZE = 224


# Check model
if not os.path.exists(MODEL_PATH):

    root = Tk()
    root.withdraw()

    messagebox.showerror(
        "Error",
        "Trained model not found."
    )

    root.destroy()

    exit()


# Load model
model = tf.keras.models.load_model(
    MODEL_PATH
)


# Load class names
with open(
    CLASS_FILE,
    "r"
) as file:

    class_names = [
        line.strip()
        for line in file
    ]


# Select leaf
root = Tk()
root.withdraw()

image_path = filedialog.askopenfilename(
    title="Select Tulsi Leaf Image",
    filetypes=[
        (
            "Image Files",
            "*.jpg *.jpeg *.png *.bmp *.webp"
        )
    ]
)

root.destroy()


if not image_path:

    print("No image selected.")
    exit()


# Load image
img = image.load_img(
    image_path,
    target_size=(
        IMG_SIZE,
        IMG_SIZE
    )
)


# Convert to array
img_array = image.img_to_array(
    img
)


# Add batch dimension
img_array = np.expand_dims(
    img_array,
    axis=0
)


# Prediction
prediction = model.predict(
    img_array,
    verbose=0
)


# Find predicted class
predicted_index = np.argmax(
    prediction[0]
)

predicted_class = class_names[
    predicted_index
]


confidence = (
    prediction[0][predicted_index]
    * 100
)


print()
print("==============================")
print("TULSI LEAF ANALYSIS")
print("==============================")

print(
    "Image:",
    os.path.basename(image_path)
)

print(
    "Prediction:",
    predicted_class
)

print(
    f"Confidence: {confidence:.2f}%"
)

print("==============================")
print()


# Show result
root = Tk()
root.withdraw()

messagebox.showinfo(
    "Tulsi Leaf Result",
    f"Prediction: {predicted_class}\n\n"
    f"Confidence: {confidence:.2f}%"
)

root.destroy()