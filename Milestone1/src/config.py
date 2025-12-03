import os

# Base Paths
# Assuming the user puts the dataset in a folder named 'dataset' in the root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_ROOT = os.path.join(BASE_DIR, 'dataset', 'PCB_DATASET')

# Input Paths
IMAGES_DIR = os.path.join(DATASET_ROOT, 'images')
TEMPLATE_DIR = os.path.join(DATASET_ROOT, 'PCB_USED')
ANNOTATIONS_DIR = os.path.join(DATASET_ROOT, 'Annotations')

# Output Paths
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
VISUAL_ASSETS_DIR = os.path.join(OUTPUT_DIR, 'Visual_Report_Assets')
LABELED_DATA_DIR = os.path.join(OUTPUT_DIR, 'Labeled_Training_Data')

# Ensure output directories exist
os.makedirs(VISUAL_ASSETS_DIR, exist_ok=True)
os.makedirs(LABELED_DATA_DIR, exist_ok=True)