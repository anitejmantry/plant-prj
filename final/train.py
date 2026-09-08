import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# Dataset location
dataset_path = "dataset"

# Image settings
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 15


# Check dataset
if not os.path.exists(dataset_path):
    print("Dataset folder not found!")
    exit()


# Load training data
train_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)


# Load validation data
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)


# Get class names
class_names = train_dataset.class_names

print()
print("Classes found:")
for name in class_names:
    print("-", name)

print()


# Improve loading performance
AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(
    buffer_size=AUTOTUNE
)

validation_dataset = validation_dataset.prefetch(
    buffer_size=AUTOTUNE
)


# Data augmentation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])


# Load MobileNetV2
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)


# Freeze pretrained layers
base_model.trainable = False


# Create model
model = models.Sequential([

    data_augmentation,

    layers.Rescaling(
        1.0 / 127.5,
        offset=-1
    ),

    base_model,

    layers.GlobalAveragePooling2D(),

    layers.Dropout(0.3),

    layers.Dense(
        len(class_names),
        activation="softmax"
    )
])


# Compile model
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# Display model
model.summary()


# Train
history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS
)


# Create model folder
os.makedirs(
    "model",
    exist_ok=True
)


# Save model
model.save(
    "model/tulsi_leaf_model.keras"
)


# Save class names
with open(
    "model/classes.txt",
    "w"
) as file:

    for class_name in class_names:
        file.write(
            class_name + "\n"
        )


print()
print("Training completed.")
print()
print(
    "Model saved to:"
)
print(
    "model/tulsi_leaf_model.keras"
)


# Plot accuracy
plt.figure(figsize=(8, 5))

plt.plot(
    history.history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    history.history["val_accuracy"],
    label="Validation Accuracy"
)

plt.title(
    "Tulsi Leaf Disease Model Accuracy"
)

plt.xlabel("Epoch")
plt.ylabel("Accuracy")

plt.legend()

plt.tight_layout()

plt.show()


# Plot loss
plt.figure(figsize=(8, 5))

plt.plot(
    history.history["loss"],
    label="Training Loss"
)

plt.plot(
    history.history["val_loss"],
    label="Validation Loss"
)

plt.title(
    "Tulsi Leaf Disease Model Loss"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.legend()

plt.tight_layout()

plt.show()