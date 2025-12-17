import os

# Config for the Final App
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'pcb_defect_model.keras')
IMG_SIZE = (128, 128)