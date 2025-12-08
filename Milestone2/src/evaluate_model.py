import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import os

# CONFIG
MODEL_PATH = '../output/pcb_defect_model.keras'
DATA_DIR = '../dataset/Labeled_Training_Data'
OUTPUT_DIR = '../output'

def evaluate_performance():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        return

    print("Loading Model and Validation Data...")
    model = tf.keras.models.load_model(MODEL_PATH)
    
    # Shuffle=True ensures we see all classes in the validation set
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR, validation_split=0.2, subset="validation", seed=123,
        image_size=(128, 128), batch_size=32, shuffle=True
    )
    class_names = val_ds.class_names

    y_true, y_pred = [], []
    print("Generating Predictions...")
    for img, label in val_ds:
        pred = model.predict(img, verbose=0)
        y_true.extend(label.numpy())
        y_pred.extend(np.argmax(pred, axis=1))

    # Metrics
    report = classification_report(y_true, y_pred, target_names=class_names)
    print("\nClassification Report:\n")
    print(report)
    
    # Save Report
    with open(os.path.join(OUTPUT_DIR, 'evaluation_report.txt'), 'w') as f:
        f.write(report)

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10,8))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=class_names, yticklabels=class_names, cmap='Blues')
    plt.title("Confusion Matrix")
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'confusion_matrix.png'))
    print(f"Evaluation Complete. Results saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    evaluate_performance()