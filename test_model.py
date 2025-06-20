import cv2
import tensorflow as tf
import numpy as np
import serial
import time
import os

# Load the CNN model
model_path = r"D:\8th sem\Iot Domain Analyst\project\pro\apple_recovery_project\models\apple_cnn_model.h5"
try:
    model = tf.keras.models.load_model(model_path)
    print(" Model loaded successfully!")
except Exception as e:
    print(f"Failed to load model: {e}")
    exit()

# Class labels
labels = ['Fresh', 'Infected', 'Rotten', 'Bruised', 'Moldy', 'Discolored']

# Sensor Data from Arduino
def get_sensor_data():
    try:
        ser = serial.Serial('COM3', 9600, timeout=2)
        time.sleep(2)
        line = ser.readline().decode('utf-8').strip()
        ser.close()

        if line:
            parts = line.split(",")
            if len(parts) == 3:
                return float(parts[0]), float(parts[1]), float(parts[2])
        
        print("Invalid sensor data received.")
        return 0.0, 0.0, 0.0
    except Exception as e:
        print(f" Error reading sensor: {e}")
        return 0.0, 0.0, 0.0

# Get latest image from the 'captured_images' folder
def get_latest_image():
    folder_path = "captured_images"
    if not os.path.exists(folder_path):
        print(f" Folder '{folder_path}' not found.")
        return None

    images = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]
    if not images:
        print(f" No images found in '{folder_path}'.")
        return None

    latest_image = max(images, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    print(f"Latest image found: {latest_image}")
    return os.path.join(folder_path, latest_image)

# Prediction function
def predict(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(" Error: Could not read image.")
        return

    image = cv2.resize(image, (64, 64))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    confidence_scores = model.predict(image)[0]
    predicted_index = np.argmax(confidence_scores)

    if predicted_index >= len(labels):
        print("Invalid prediction index!")
        return

    predicted_class = labels[predicted_index]
    confidence = confidence_scores[predicted_index]

    # Read sensor data
    temperature, humidity, gas = get_sensor_data()

    print("\nPrediction Result")
    print("---------------------")
    print(f"Condition: {predicted_class}")
    print(f"Confidence: {confidence * 100:.2f}%")
    print(f"Temp: {temperature}°C | umidity: {humidity}% | Gas: {gas}")

    # Apple recovery mapping
    recovery_map = {
        "Fresh": 0,
        "Infected": 60,
        "Rotten": 80,
        "Bruised": 40,
        "Moldy": 90,
        "Discolored": 50
    }

    recovery = recovery_map.get(predicted_class, 0)

    print(f"\n Recovery Required for Apple: {recovery}%")

    if recovery > 0:
        print(" Suggestion: Apply pesticide/fertilizer for apple recovery.")
    else:
        print(" Apple is healthy. No treatment needed.")

    # Additional crop-level recovery suggestion
    crop_recovery = int(recovery * 1.5)
    if crop_recovery > 100:
        crop_recovery = 100

    print(f"\nEstimated Crop Recovery Needed: {crop_recovery}%")
    if crop_recovery > 0:
        print("Suggestion: Treat the crop based on similar apple conditions.")

# Main run
image_path = get_latest_image()
if image_path:
    predict(image_path)
