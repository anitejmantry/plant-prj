import os
import shutil
from ultralytics import YOLO


# -----------------------------
# Project folder
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# -----------------------------
# Settings
# -----------------------------

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset"
)

MODEL_NAME = os.path.join(
    BASE_DIR,
    "yolov8n-cls.pt"
)

IMAGE_SIZE = 224
EPOCHS = 30
BATCH_SIZE = 8


# -----------------------------
# Check dataset
# -----------------------------

if not os.path.exists(DATASET_PATH):

    print("Dataset folder not found!")

    exit()


# -----------------------------
# Find classes
# -----------------------------

classes = []

for folder in os.listdir(DATASET_PATH):

    folder_path = os.path.join(
        DATASET_PATH,
        folder
    )

    if os.path.isdir(folder_path):

        classes.append(folder)


print()
print("==============================")
print("TULSI LEAF YOLOv8 TRAINING")
print("==============================")

print()

print("Dataset:")
print(DATASET_PATH)

print()

print("Classes found:")

for class_name in classes:

    print("-", class_name)

print()


# -----------------------------
# Load YOLOv8 classification model
# -----------------------------

print("Loading YOLOv8 model...")

model = YOLO(MODEL_NAME)


# -----------------------------
# Training output
# -----------------------------

RUNS_FOLDER = os.path.join(
    BASE_DIR,
    "runs"
)


# -----------------------------
# Train
# -----------------------------

print()
print("Starting training...")
print()


results = model.train(

    data=DATASET_PATH,

    epochs=EPOCHS,

    imgsz=IMAGE_SIZE,

    batch=BATCH_SIZE,

    project=RUNS_FOLDER,

    name="tulsi_leaf",

    exist_ok=True

)


# -----------------------------
# Find best model
# -----------------------------

trained_model = os.path.join(

    RUNS_FOLDER,
    "tulsi_leaf",
    "weights",
    "best.pt"

)


# -----------------------------
# Create model folder
# -----------------------------

MODEL_FOLDER = os.path.join(
    BASE_DIR,
    "model"
)

os.makedirs(
    MODEL_FOLDER,
    exist_ok=True
)


# -----------------------------
# Copy best.pt
# -----------------------------

final_model = os.path.join(

    MODEL_FOLDER,
    "best.pt"

)


if os.path.exists(trained_model):

    shutil.copy2(

        trained_model,
        final_model

    )

    print()
    print("==============================")
    print("TRAINING COMPLETED")
    print("==============================")

    print()

    print("Best model saved at:")

    print(final_model)

    print()

else:

    print()
    print("ERROR: best.pt was not found.")
    print()