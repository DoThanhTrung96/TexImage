import os
import sys
import cv2
from image_processor import load_image, preprocess_image, detect_geometry_roi
from recognizer import analyze_geometry_with_llm
import json

def main():
    # Define the input path for the original image
    base_dir = "C:\\Data\\TexImage-1\\image"
    original_image_path = os.path.join(base_dir, "image.png")

    if not os.path.exists(original_image_path):
        print(f"Error: Original image not found at {original_image_path}")
        sys.exit(1)

    print(f"Loading original image: {original_image_path}")
    original_image = load_image(original_image_path)
    
    # --- 1. Detect and save the Region of Interest ---
    print("Detecting geometry ROI...")
    _, binary_image, _ = preprocess_image(original_image)
    cropped_image, _ = detect_geometry_roi(binary_image, original_image)
    
    cropped_image_path = os.path.join(base_dir, "cropped_image.png")
    cv2.imwrite(cropped_image_path, cropped_image)
    print(f"Cropped ROI image saved to {cropped_image_path}")

    # --- 2. Analyze the ROI with Ollama ---
    print("Analyzing geometry with Ollama...")
    geometry_data = analyze_geometry_with_llm(cropped_image_path)

    # --- 3. Print the structured output ---
    if geometry_data:
        print("\n--- LLM Analysis Result ---")
        print(json.dumps(geometry_data, indent=2))
    else:
        print("\n--- LLM Analysis Failed ---")

if __name__ == '__main__':
    main()
