import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, '../dataset/PCB_DATASET/images')
MODEL_PATH = os.path.join(BASE_DIR, 'output/pcb_defect_model.keras')
CM_PATH = os.path.join(BASE_DIR, 'output/confusion_matrix.png')
IMG_SIZE = (128, 128)
BATCH_SIZE = 32

def evaluate():
    print("Starting Evaluation...")
    
    # 1. Load Validation Data
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR, validation_split=0.2, subset="validation", seed=123,
        image_size=IMG_SIZE, batch_size=BATCH_SIZE, shuffle=False
    )
    class_names = val_ds.class_names

    # 2. Load Model
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Run training first.")
        return
    
    model = tf.keras.models.load_model(MODEL_PATH)
    
    # 3. Predict
    y_true = []
    y_pred = []
    
    print("   Running predictions...")
    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(labels.numpy())
        y_pred.extend(np.argmax(preds, axis=1))

    # 4. Metrics
    print("\n" + "="*50)
    print("   CLASSIFICATION REPORT")
    print("="*50)
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    # 5. Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', 
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix (EfficientNetB0 Optimized)')
    plt.savefig(CM_PATH)
    print(f"Confusion Matrix saved to {CM_PATH}")

if __name__ == "__main__":
    evaluate()