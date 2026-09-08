import os
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk, ImageDraw
from ultralytics import YOLO


# ============================================================
# SETTINGS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "best.pt")

# Lower value helps when the model is not very confident.
CONFIDENCE_THRESHOLD = 0.10

# For classification models, these words are treated as infected.
INFECTED_WORDS = [
    "diseased",
    "disease",
    "infected",
    "infection",
    "leaf_spot",
    "leaf spot",
    "spot",
    "blight",
    "mildew",
    "rust",
    "fungal",
    "infected_region"
]

selected_image_path = None
original_image = None
result_image = None
detections = []


# ============================================================
# CHECK MODEL
# ============================================================

if not os.path.exists(MODEL_PATH):
    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(
        "Model Error",
        "Model file not found.\n\n"
        "Expected:\n" + MODEL_PATH
    )

    root.destroy()
    raise SystemExit


print()
print("Loading model:")
print(MODEL_PATH)
print()

model = YOLO(MODEL_PATH)

print("Model task:", getattr(model, "task", "unknown"))
print("Model classes:", model.names)
print()


# ============================================================
# HELPER - IS CLASS INFECTED?
# ============================================================

def is_infected_class(class_name):
    name = str(class_name).lower().strip()

    for word in INFECTED_WORDS:
        if word in name:
            return True

    return False


# ============================================================
# SELECT IMAGE
# ============================================================

def select_image():
    global selected_image_path
    global original_image

    file_path = filedialog.askopenfilename(
        title="Select Tulsi Leaf Image",
        filetypes=[
            (
                "Image Files",
                "*.jpg *.jpeg *.png *.bmp *.webp"
            )
        ]
    )

    if not file_path:
        return

    try:
        selected_image_path = file_path

        original_image = Image.open(
            file_path
        ).convert("RGB")

        clear_result()
        show_original_image()

        status_label.config(
            text="Image selected. Click Detect Disease.",
            fg="darkgreen"
        )

    except Exception as e:
        messagebox.showerror(
            "Image Error",
            str(e)
        )


# ============================================================
# SHOW ORIGINAL
# ============================================================

def show_original_image():
    if original_image is None:
        return

    image = original_image.copy()

    image.thumbnail(
        (520, 520),
        Image.Resampling.LANCZOS
    )

    photo = ImageTk.PhotoImage(image)

    original_label.config(
        image=photo,
        text=""
    )

    original_label.image = photo


# ============================================================
# PIXEL GRID
# ============================================================

def create_pixel_grid(image, x1, y1, x2, y2):
    x1 = max(0, min(int(x1), image.width - 1))
    y1 = max(0, min(int(y1), image.height - 1))
    x2 = max(x1 + 1, min(int(x2), image.width))
    y2 = max(y1 + 1, min(int(y2), image.height))

    crop = image.crop(
        (x1, y1, x2, y2)
    )

    scale = 3

    enlarged = crop.resize(
        (
            crop.width * scale,
            crop.height * scale
        ),
        Image.Resampling.NEAREST
    )

    draw = ImageDraw.Draw(enlarged)

    grid_step = 10 * scale

    for x in range(
        0,
        enlarged.width,
        grid_step
    ):
        draw.line(
            (x, 0, x, enlarged.height),
            fill="white",
            width=1
        )

    for y in range(
        0,
        enlarged.height,
        grid_step
    ):
        draw.line(
            (0, y, enlarged.width, y),
            fill="white",
            width=1
        )

    enlarged.thumbnail(
        (500, 400),
        Image.Resampling.LANCZOS
    )

    return enlarged


# ============================================================
# DRAW BOX
# ============================================================

def draw_detection(draw, x1, y1, x2, y2, label):
    draw.rectangle(
        (x1, y1, x2, y2),
        outline="red",
        width=5
    )

    text_box = draw.textbbox(
        (x1, y1),
        label
    )

    draw.rectangle(
        (
            text_box[0],
            text_box[1],
            text_box[2] + 8,
            text_box[3] + 8
        ),
        fill="red"
    )

    draw.text(
        (
            x1 + 4,
            y1 + 4
        ),
        label,
        fill="white"
    )


# ============================================================
# DETECTION
# ============================================================

def detect_disease():
    global result_image
    global detections

    if original_image is None or selected_image_path is None:
        messagebox.showwarning(
            "No Image",
            "Please select a Tulsi leaf image first."
        )
        return

    status_label.config(
        text="Analyzing image...",
        fg="darkgreen"
    )

    root.update_idletasks()

    try:
        # Run prediction.
        results = model.predict(
            source=selected_image_path,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )

        if not results:
            raise RuntimeError(
                "The YOLO model returned no result."
            )

        result = results[0]

        result_image = original_image.copy()
        draw = ImageDraw.Draw(result_image)

        detections = []

        # ====================================================
        # CASE 1: DETECTION MODEL
        # ====================================================

        if result.boxes is not None and len(result.boxes) > 0:

            boxes = result.boxes

            for i in range(len(boxes)):

                box = boxes.xyxy[i]

                x1 = int(box[0].item())
                y1 = int(box[1].item())
                x2 = int(box[2].item())
                y2 = int(box[3].item())

                confidence = float(
                    boxes.conf[i].item()
                )

                class_id = int(
                    boxes.cls[i].item()
                )

                class_name = result.names[class_id]

                # Only count disease/infection classes.
                if not is_infected_class(class_name):
                    continue

                width = max(0, x2 - x1)
                height = max(0, y2 - y1)
                area = width * height

                detections.append({
                    "class": str(class_name),
                    "confidence": confidence,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "width": width,
                    "height": height,
                    "area": area,
                    "type": "detection"
                })

                label = (
                    f"{class_name} "
                    f"{confidence * 100:.1f}%"
                )

                draw_detection(
                    draw,
                    x1,
                    y1,
                    x2,
                    y2,
                    label
                )

        # ====================================================
        # CASE 2: CLASSIFICATION MODEL
        # ====================================================

        elif result.probs is not None:

            probs = result.probs

            top_index = int(probs.top1)
            confidence = float(
                probs.top1conf.item()
            )

            class_name = str(
                result.names[top_index]
            )

            infected = is_infected_class(
                class_name
            )

            if infected:

                # A classification model does NOT know the
                # exact infected region. We show the full image
                # box only to clearly indicate classification.
                x1 = 0
                y1 = 0
                x2 = original_image.width - 1
                y2 = original_image.height - 1

                detections.append({
                    "class": class_name,
                    "confidence": confidence,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "width": original_image.width,
                    "height": original_image.height,
                    "area": original_image.width * original_image.height,
                    "type": "classification"
                })

                label = (
                    f"{class_name} "
                    f"{confidence * 100:.1f}%"
                )

                draw_detection(
                    draw,
                    x1,
                    y1,
                    x2,
                    y2,
                    label
                )

            else:
                detections = []

        # ====================================================
        # NO SUPPORTED OUTPUT
        # ====================================================

        else:
            raise RuntimeError(
                "The model returned neither detection boxes "
                "nor classification probabilities."
            )

        # ====================================================
        # DISPLAY
        # ====================================================

        show_result_image()
        update_information()

        if len(detections) > 0:

            detection = detections[0]

            if detection["type"] == "detection":

                zoom = create_pixel_grid(
                    original_image,
                    detection["x1"],
                    detection["y1"],
                    detection["x2"],
                    detection["y2"]
                )

                show_zoom(zoom)

                status_label.config(
                    text=(
                        f"STATUS: INFECTED | "
                        f"{len(detections)} region(s) detected"
                    ),
                    fg="red"
                )

            else:

                zoom_label.config(
                    image="",
                    text="Classification model: exact infected region unavailable."
                )

                zoom_label.image = None

                status_label.config(
                    text=(
                        f"STATUS: INFECTED | "
                        f"{detection['class']} "
                        f"{detection['confidence'] * 100:.1f}%"
                    ),
                    fg="red"
                )

        else:

            zoom_label.config(
                image="",
                text="No infected region detected"
            )

            zoom_label.image = None

            status_label.config(
                text="STATUS: NOT INFECTED",
                fg="green"
            )

            messagebox.showinfo(
                "Result",
                "No infected class/region was detected.\n\n"
                "If the leaf is actually diseased, check the "
                "training labels and model accuracy."
            )

    except Exception as e:

        status_label.config(
            text="Detection failed.",
            fg="red"
        )

        messagebox.showerror(
            "Detection Error",
            str(e)
        )


# ============================================================
# SHOW RESULT
# ============================================================

def show_result_image():
    if result_image is None:
        return

    image = result_image.copy()

    image.thumbnail(
        (650, 500),
        Image.Resampling.LANCZOS
    )

    photo = ImageTk.PhotoImage(image)

    result_label.config(
        image=photo,
        text=""
    )

    result_label.image = photo


# ============================================================
# SHOW ZOOM
# ============================================================

def show_zoom(zoom_image):
    zoom_image = zoom_image.copy()

    zoom_image.thumbnail(
        (360, 300),
        Image.Resampling.LANCZOS
    )

    photo = ImageTk.PhotoImage(
        zoom_image
    )

    zoom_label.config(
        image=photo,
        text=""
    )

    zoom_label.image = photo


# ============================================================
# INFORMATION
# ============================================================

def update_information():

    for widget in details_frame.winfo_children():
        widget.destroy()

    if len(detections) == 0:

        tk.Label(
            details_frame,
            text="STATUS: NOT INFECTED",
            font=("Arial", 16, "bold"),
            fg="green"
        ).pack(
            pady=20
        )

        return

    tk.Label(
        details_frame,
        text="STATUS: INFECTED",
        font=("Arial", 18, "bold"),
        fg="red"
    ).pack(
        pady=10
    )

    for number, detection in enumerate(
        detections,
        start=1
    ):

        frame = tk.LabelFrame(
            details_frame,
            text=f"Region {number}",
            font=("Arial", 11, "bold")
        )

        frame.pack(
            fill="x",
            padx=8,
            pady=5
        )

        if detection["type"] == "classification":
            location_text = (
                "Location: Not available "
                "(classification model)"
            )
        else:
            location_text = (
                f"X1: {detection['x1']} pixels\n"
                f"Y1: {detection['y1']} pixels\n"
                f"X2: {detection['x2']} pixels\n"
                f"Y2: {detection['y2']} pixels\n\n"
                f"Width: {detection['width']} pixels\n"
                f"Height: {detection['height']} pixels\n"
                f"Bounding-box area: "
                f"{detection['area']:,} pixels"
            )

        info = (
            f"Disease / Class: {detection['class']}\n"
            f"Confidence: "
            f"{detection['confidence'] * 100:.2f}%\n\n"
            f"{location_text}"
        )

        tk.Label(
            frame,
            text=info,
            justify="left",
            font=("Arial", 10)
        ).pack(
            padx=10,
            pady=8
        )


# ============================================================
# CLEAR
# ============================================================

def clear_result():

    global result_image
    global detections

    result_image = None
    detections = []

    if "result_label" in globals():
        result_label.config(
            image="",
            text="Detection result will appear here"
        )
        result_label.image = None

    if "zoom_label" in globals():
        zoom_label.config(
            image="",
            text="No detected region"
        )
        zoom_label.image = None

    if "details_frame" in globals():
        for widget in details_frame.winfo_children():
            widget.destroy()

    if "status_label" in globals():
        status_label.config(
            text="Ready.",
            fg="darkgreen"
        )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Tulsi Leaf Disease Detection - YOLOv8"
)

root.geometry(
    "1450x900"
)

root.minsize(
    1200,
    750
)


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    root,
    text="Tulsi Leaf Disease Detection",
    font=("Arial", 28, "bold"),
    fg="darkgreen"
)

title.pack(
    pady=(15, 2)
)


subtitle = tk.Label(
    root,
    text="Powered by YOLOv8",
    font=("Arial", 15, "bold"),
    fg="gray"
)

subtitle.pack(
    pady=(0, 15)
)


# ============================================================
# MAIN CONTENT
# ============================================================

main_frame = tk.Frame(root)

main_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


# ============================================================
# ORIGINAL
# ============================================================

original_frame = tk.LabelFrame(
    main_frame,
    text="Original Image",
    font=("Arial", 14, "bold")
)

original_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5
)

original_label = tk.Label(
    original_frame,
    text="No image selected",
    font=("Arial", 12)
)

original_label.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# ============================================================
# RESULT
# ============================================================

result_frame = tk.LabelFrame(
    main_frame,
    text="Detection Result - Infected Region",
    font=("Arial", 14, "bold")
)

result_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=5
)

result_label = tk.Label(
    result_frame,
    text="Detection result will appear here",
    font=("Arial", 12)
)

result_label.pack(
    pady=10
)


zoom_title = tk.Label(
    result_frame,
    text="Zoomed Infected Region",
    font=("Arial", 12, "bold")
)

zoom_title.pack(
    pady=5
)


zoom_label = tk.Label(
    result_frame,
    text="No detected region",
    font=("Arial", 10)
)

zoom_label.pack(
    pady=5
)


# ============================================================
# DETAILS
# ============================================================

details_outer = tk.LabelFrame(
    main_frame,
    text="Prediction Details",
    font=("Arial", 14, "bold")
)

details_outer.pack(
    side="right",
    fill="both",
    expand=True,
    padx=5
)

details_frame = tk.Frame(
    details_outer
)

details_frame.pack(
    fill="both",
    expand=True,
    padx=5,
    pady=5
)


# ============================================================
# BUTTONS
# ============================================================

button_frame = tk.Frame(root)

button_frame.pack(
    pady=15
)


select_button = tk.Button(
    button_frame,
    text="Select Image",
    command=select_image,
    font=("Arial", 13, "bold"),
    width=18,
    height=2
)

select_button.pack(
    side="left",
    padx=10
)


detect_button = tk.Button(
    button_frame,
    text="Detect Disease",
    command=detect_disease,
    font=("Arial", 13, "bold"),
    width=18,
    height=2
)

detect_button.pack(
    side="left",
    padx=10
)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_result,
    font=("Arial", 13, "bold"),
    width=18,
    height=2
)

clear_button.pack(
    side="left",
    padx=10
)


# ============================================================
# STATUS
# ============================================================

status_label = tk.Label(
    root,
    text="Ready. Select a Tulsi leaf image.",
    font=("Arial", 13, "bold"),
    fg="darkgreen"
)

status_label.pack(
    pady=(0, 15)
)


# ============================================================
# START
# ============================================================

root.mainloop()
