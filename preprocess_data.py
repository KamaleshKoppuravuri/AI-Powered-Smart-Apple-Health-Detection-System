import pandas as pd
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("dataset/plant_data.csv")

# Features (sensors) & target (image)
X = df[['Temperature', 'Gas_Level', 'Humidity']].values
y = np.array([cv2.imread(img, cv2.IMREAD_GRAYSCALE) for img in df['Image_Path']])

# Normalize images
y = np.array([cv2.resize(img, (64, 64)) for img in y])  # Resize to 64x64
y = y / 255.0  # Scale pixel values

# Standardize sensor values
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save processed data
np.save("dataset/X_train.npy", X_train)
np.save("dataset/X_test.npy", X_test)
np.save("dataset/y_train.npy", y_train)
np.save("dataset/y_test.npy", y_test)

print(" Data preprocessing complete!")
