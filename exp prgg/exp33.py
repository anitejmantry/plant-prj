# Using a pre-trained model like MobileNet or a Food101 model
import tensorflow as tf
from PIL import Image
import numpy as np

# Load a model fine-tuned on food datasets (Food101, etc.)
model = tf.keras.models.load_model('food_model.h5')
food_classes = ['apple', 'banana', 'pizza', 'burger', ...]  # Your food classes

# Calorie database
calorie_db = {
    'apple': 95,
    'banana': 105,
    'pizza_slice': 285,
    'burger': 354,
    # ...
}


def estimate_calories(image_path):
    img = Image.open(image_path).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    food_class = food_classes[np.argmax(predictions)]
    calories = calorie_db.get(food_class, "Unknown")

    return food_class, calories