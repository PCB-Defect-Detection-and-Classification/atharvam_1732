import cv2
import numpy as np
import os
import glob
from src import config

def run_subtraction_pipeline():
    """
    Module 1: Performs image alignment, subtraction, and thresholding.
    Generates visual assets for the report.
    """
    print(f"\n[Module 1] Starting Subtraction Pipeline...")
    
    if not os.path.exists(config.IMAGES_DIR):
        print(f"Error: Dataset not found at {config.IMAGES_DIR}")
        return

    # Get categories based on folder names
    categories = [d for d in os.listdir(config.IMAGES_DIR) 
                  if os.path.isdir(os.path.join(config.IMAGES_DIR, d))]

    for category in categories:
        cat_path = os.path.join(config.IMAGES_DIR, category)
        images = glob.glob(os.path.join(cat_path, '*.jpg'))
        
        if not images:
            continue

        # Process only the first image of each category for the report
        img_path = images[0]
        filename = os.path.basename(img_path)
        
        # Find matching template
        temp_id = filename.split('_')[0]
        template_candidates = glob.glob(os.path.join(config.TEMPLATE_DIR, f"{temp_id}.*"))
        
        if not template_candidates:
            print(f"Warning: Template not found for {filename}")
            continue
            
        template_path = template_candidates[0]

        # Logic
        img_test = cv2.imread(img_path)
        img_temp = cv2.imread(template_path)

        if img_test is None or img_temp is None:
            continue

        # Resize for alignment
        img_test = cv2.resize(img_test, (img_temp.shape[1], img_temp.shape[0]))

        # Subtraction
        diff = cv2.absdiff(img_temp, img_test)
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Thresholding (Otsu)
        _, thresh = cv2.threshold(gray_diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Morphological Cleaning
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        # Visualization of result
        result_viz = img_test.copy()
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w * h > 100:
                cv2.rectangle(result_viz, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Save Assets
        prefix = f"{category}_Demo"
        cv2.imwrite(os.path.join(config.VISUAL_ASSETS_DIR, f"{prefix}_1_Template.jpg"), img_temp)
        cv2.imwrite(os.path.join(config.VISUAL_ASSETS_DIR, f"{prefix}_2_Test.jpg"), img_test)
        cv2.imwrite(os.path.join(config.VISUAL_ASSETS_DIR, f"{prefix}_3_Diff.jpg"), gray_diff)
        cv2.imwrite(os.path.join(config.VISUAL_ASSETS_DIR, f"{prefix}_4_Mask.jpg"), mask)
        cv2.imwrite(os.path.join(config.VISUAL_ASSETS_DIR, f"{prefix}_5_Result.jpg"), result_viz)

        print(f"   Saved report assets for category: {category}")