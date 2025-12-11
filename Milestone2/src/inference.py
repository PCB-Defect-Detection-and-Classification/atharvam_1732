import os
import cv2
import numpy as np
import tensorflow as tf
import glob

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, '../dataset/PCB_DATASET/images')
MODEL_PATH = os.path.join(BASE_DIR, 'output/pcb_defect_model.keras')
OUTPUT_IMG_DIR = os.path.join(BASE_DIR, 'output/Annotated_Test_Images')
IMG_SIZE = (128, 128)

def run_inference():
    print("Starting Visual Inference...")
    os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)
    
    # 1. Load Model
    model = tf.keras.models.load_model(MODEL_PATH)
    
    # 2. Grab Sample Images (1 from each class)
    class_folders = [f for f in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, f))]
    
    for class_name in class_folders:
        folder_path = os.path.join(DATA_DIR, class_name)
        images = glob.glob(os.path.join(folder_path, '*.jpg')) + glob.glob(os.path.join(folder_path, '*.png'))
        
        if not images: continue
        
        # Test on the first image of each class
        img_path = images[0]
        filename = os.path.basename(img_path)
        
        # Preprocess
        img_orig = cv2.imread(img_path)
        img_resized = cv2.resize(img_orig, IMG_SIZE)
        img_batch = np.expand_dims(img_resized, axis=0)
        
        # Predict
        preds = model.predict(img_batch, verbose=0)
        score = np.max(preds) * 100
        pred_idx = np.argmax(preds)
        pred_label = class_folders[pred_idx] # Assuming folder order matches training order
        
        # Annotate
        color = (0, 255, 0) if pred_label == class_name else (0, 0, 255)
        text = f"True: {class_name} | Pred: {pred_label} ({score:.1f}%)"
        
        cv2.putText(img_orig, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Save
        save_path = os.path.join(OUTPUT_IMG_DIR, f"Pred_{class_name}_{filename}")
        cv2.imwrite(save_path, img_orig)
        print(f"   Saved inference for {class_name}")

    print(f"Visual proofs saved to {OUTPUT_IMG_DIR}")

if __name__ == "__main__":
    run_inference()