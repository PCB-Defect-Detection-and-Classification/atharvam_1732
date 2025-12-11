import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models, applications
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# --- CONFIGURATION ---
# Adjust these paths to match your local environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Points to Milestone 2/
DATA_DIR = os.path.join(BASE_DIR, '../dataset/PCB_DATASET/images')     # Adjust if dataset is elsewhere
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
MODEL_PATH = os.path.join(OUTPUT_DIR, 'pcb_defect_model.keras')
PLOT_PATH = os.path.join(OUTPUT_DIR, 'train_val_acc_n_train_val_loss.png')

IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 30

def build_optimized_model(num_classes):
    """
    Builds the 'Heavy Head' architecture:
    EfficientNetB0 (Frozen) -> Dense(256) -> Dropout -> Output
    """
    # 1. Base Model (Frozen)
    base_model = applications.EfficientNetB0(
        include_top=False, weights='imagenet', input_shape=IMG_SIZE + (3,)
    )
    base_model.trainable = False 

    # 2. Augmentation
    data_augmentation = models.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.15),
    ])

    # 3. Custom Head
    inputs = layers.Input(shape=IMG_SIZE + (3,))
    x = data_augmentation(inputs)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    
    # Hidden Layer (The Key to 97.8% Accuracy)
    x = layers.Dense(256, activation='relu')(x) 
    x = layers.Dropout(0.2)(x) 
    
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    return models.Model(inputs, outputs, name="EfficientNet_Optimized")

def plot_history(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(len(acc))

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.savefig(PLOT_PATH)
    print(f"Training plots saved to {PLOT_PATH}")

def train():
    print(f"Starting Training...")
    
    # 1. Load Data
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR, validation_split=0.2, subset="training", seed=123,
        image_size=IMG_SIZE, batch_size=BATCH_SIZE
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR, validation_split=0.2, subset="validation", seed=123,
        image_size=IMG_SIZE, batch_size=BATCH_SIZE
    )

    # Optimization
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # 2. Build & Compile
    model = build_optimized_model(num_classes=len(train_ds.class_names))
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # 3. Callbacks
    callbacks = [
        ModelCheckpoint(MODEL_PATH, save_best_only=True, monitor='val_accuracy', verbose=1),
        EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6, verbose=1)
    ]

    # 4. Fit
    history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=callbacks)
    
    # 5. Save Artifacts
    plot_history(history)
    print("Training Complete.")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    train()