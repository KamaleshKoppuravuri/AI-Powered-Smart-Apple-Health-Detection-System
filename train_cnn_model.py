
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os

# Set your paths
train_data_path = r"D:\8th sem\Iot Domain Analyst\project\pro\apple_recovery_project\dataset\Train"
val_data_path = r"D:\8th sem\Iot Domain Analyst\project\pro\apple_recovery_project\dataset"
model_save_path = r"D:\8th sem\Iot Domain Analyst\project\pro\apple_recovery_project\models\apple_cnn_model.h5"

# Data Augmentation
train_datagen = ImageDataGenerator(rescale=1.0/255.0, rotation_range=20, horizontal_flip=True)
val_datagen = ImageDataGenerator(rescale=1.0/255.0)

train_generator = train_datagen.flow_from_directory(
    train_data_path, target_size=(64, 64), batch_size=32, class_mode='categorical')

val_generator = val_datagen.flow_from_directory(
    val_data_path, target_size=(64, 64), batch_size=32, class_mode='categorical')

#  Model Architecture
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D(2, 2),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(train_generator.num_classes, activation='softmax')  # Dynamically setting output neurons
])

# Compile Model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train Model
model.fit(train_generator, validation_data=val_generator, epochs=10)

# Save Model
model.save(model_save_path)
print(f" Model saved at {model_save_path}")
