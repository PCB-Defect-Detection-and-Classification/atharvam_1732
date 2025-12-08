import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

# CONFIG
MODEL_PATH = '../output/pcb_defect_model.keras'
DATA_DIR = '../dataset/Labeled_Training_Data'
OUTPUT_DIR = '../output/Annotated_Test_Images'

def run_inference_demo():
    if not os.path.exists(MODEL_PATH):
        print("Model not found.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    model = tf.keras.models.load_model(MODEL_PATH)

    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATA_DIR, validation_split=0.2, subset="validation", seed=123,
        image_size=(128, 128), batch_size=32, shuffle=True
    )
    class_names = val_ds.class_names
    
    # Get one batch
    images, labels = next(iter(val_ds))

    print(f"Generating Annotated Images in {OUTPUT_DIR}...")
    
    plt.figure(figsize=(15, 10))
    for i in range(12):
        img = images[i].numpy().astype("uint8")
        true_label = class_names[labels[i]]
        
        # Predict
        img_batch = tf.expand_dims(img, 0)
        predictions = model.predict(img_batch, verbose=0)
        
        # Calculate Confidence
        score = predictions[0] 
        pred_index = np.argmax(score)
        pred_label = class_names[pred_index]
        confidence = 100 * np.max(score)
        
        # Color Logic
        color = (0, 255, 0) if true_label == pred_label else (255, 0, 0)
        
        # Save Individual Image
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        text = f"{pred_label} ({confidence:.1f}%)"
        cv2.putText(img_bgr, text, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        cv2.imwrite(os.path.join(OUTPUT_DIR, f"Test_{i}_{pred_label}.jpg"), img_bgr)

        # Plot for Grid
        ax = plt.subplot(3, 4, i + 1)
        plt.imshow(img)
        plt.title(f"True: {true_label}\nPred: {pred_label} ({confidence:.1f}%)", 
                  color='green' if true_label == pred_label else 'red', fontsize=10)
        plt.axis("off")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'Inference_Grid.png'))
    print("Inference Demo Complete.")

if __name__ == "__main__":
    run_inference_demo()