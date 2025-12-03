from src import processing, extraction
import os

def main():
    print("============================================")
    print("   PCB DEFECT DETECTION - MILESTONE 1       ")
    print("============================================")
    
    # 1. Run Subtraction (Visual Proofs)
    processing.run_subtraction_pipeline()
    
    # 2. Run ROI Extraction (Training Data)
    extraction.run_labeled_extraction()
    
    print("\n============================================")
    print("   PROCESSING COMPLETE")
    print(f"   Outputs saved to: {os.path.abspath('output')}")
    print("============================================")

if __name__ == "__main__":
    main()