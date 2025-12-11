import os

# 1. Get the absolute path of the 'src' directory
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Get the Project Root (Go up one level from 'src' to 'Milestone 3')
PROJECT_ROOT = os.path.dirname(SRC_DIR)

# 3. Define the Model Path
# Structure: Milestone 3/models/pcb_defect_model.keras
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'pcb_defect_model.keras')

# 4. Global Configuration
IMG_SIZE = (128, 128)      # Must match the training input size
BATCH_SIZE = 32            # Used if processing batches (optional for inference)