import cv2
import os
import glob
import xml.etree.ElementTree as ET
from src import config

def run_labeled_extraction():
    """
    Module 2: Parses XML annotations to extract Ground Truth ROIs.
    Prepares the 'Clean' dataset for Milestone 2 training.
    """
    print(f"\n[Module 2] Starting XML ROI Extraction...")

    if not os.path.exists(config.ANNOTATIONS_DIR):
        print("Error: Annotations folder not found.")
        return

    xml_files = glob.glob(os.path.join(config.ANNOTATIONS_DIR, '**/*.xml'), recursive=True)
    print(f"   Found {len(xml_files)} XML files. Processing...")

    total_crops = 0
    stats = {}

    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            filename_node = root.find('filename')
            if filename_node is None: continue
            
            img_filename = filename_node.text
            
            # Find the image recursively
            image_matches = glob.glob(os.path.join(config.IMAGES_DIR, '**', img_filename), recursive=True)
            if not image_matches: continue
            
            img_path = image_matches[0]
            img = cv2.imread(img_path)
            
            if img is None: continue
            h_img, w_img, _ = img.shape

            for obj in root.findall('object'):
                label = obj.find('name').text
                bndbox = obj.find('bndbox')
                
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)

                # Safety bounds
                xmin, ymin = max(0, xmin), max(0, ymin)
                xmax, ymax = min(w_img, xmax), min(h_img, ymax)

                roi = img[ymin:ymax, xmin:xmax]

                if roi.size > 0:
                    save_dir = os.path.join(config.LABELED_DATA_DIR, label)
                    os.makedirs(save_dir, exist_ok=True)
                    
                    save_name = f"{label}_{total_crops}.jpg"
                    cv2.imwrite(os.path.join(save_dir, save_name), roi)
                    
                    total_crops += 1
                    stats[label] = stats.get(label, 0) + 1

        except Exception as e:
            continue

    print(f"   Extraction Complete.")
    print(f"   Total Samples: {total_crops}")
    print(f"   Breakdown: {stats}")