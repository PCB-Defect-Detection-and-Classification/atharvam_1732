import tensorflow as tf
from tensorflow.keras import layers, models, applications
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import os
import numpy as np

# ==========================================
# CONFIGURATION
# ==========================================
# NOTE: Update these paths if running locally
DATA_DIR = '../dataset/Labeled_Training_Data' 
OUTPUT_DIR = '../output'
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 20

def train_efficientnet():
    # 1. Data Pipeline
    print(f"Loading Data from {DATA_DIR}...")
    try:
        train_ds = tf.keras.utils.image_dataset_from_directory(
            DATA_DIR, validation_split=0.2, subset="training", seed=123,
            image_size=IMG_SIZE, batch_size=BATCH_SIZE
        )
        val_ds = tf.keras.utils.image_dataset_from_directory(
            DATA_DIR, validation_split=0.2, subset="validation", seed=123,
            image_size=IMG_SIZE, batch_size=BATCH_SIZE
        )
    except FileNotFoundError:
        print("Error: Dataset not found. Please check DATA_DIR path.")
        return

    # Augmentation
    data_augmentation = models.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
    ])

    # 2. Model Architecture (EfficientNetB0)
    base_model = applications.EfficientNetB0(
        include_top=False, weights='imagenet', input_shape=(128, 128, 3)
    )
    base_model.trainable = False # Freeze base

    inputs = layers.Input(shape=(128, 128, 3))
    x = data_augmentation(inputs)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(len(train_ds.class_names), activation='softmax')(x)

    model = models.Model(inputs, outputs)

    # 3. Compile
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # 4. Train
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    callbacks = [
        ModelCheckpoint(os.path.join(OUTPUT_DIR, 'pcb_defect_model.keras'), save_best_only=True),
        EarlyStopping(monitor='val_loss', patience=5)
    ]
    
    print("Starting Training...")
    history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=callbacks)
    np.save(os.path.join(OUTPUT_DIR, 'history.npy'), history.history)
    print("Training Complete.")

if __name__ == "__main__":
    train_efficientnet()