import os
import sys
import json
import cv2
from tikz_generator import generate_tikz_code

def main():
    # Define paths
    base_dir = "C:\\Data\\TexImage-1\\image"
    json_path = os.path.join(base_dir, "manual_analysis.json")
    image_path = os.path.join(base_dir, "cropped_image.png") # Needed for dimensions
    output_tex_path = os.path.join(base_dir, "output.tex")

    if not os.path.exists(json_path):
        print(f"Error: Manual analysis JSON not found at {json_path}")
        sys.exit(1)
        
    if not os.path.exists(image_path):
        print(f"Error: Cropped image not found at {image_path}")
        sys.exit(1)

    print(f"Loading manual analysis from: {json_path}")
    with open(json_path, "r") as f:
        geometry_data = json.load(f)
        
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # --- Generate and save the TikZ code ---
    print("\n--- Generating TikZ Code from Manual Analysis ---")
    tikz_code = generate_tikz_code(geometry_data, width, height)
    
    with open(output_tex_path, "w") as f:
        f.write(tikz_code)
    print(f"TikZ code saved to {output_tex_path}")

if __name__ == '__main__':
    main()
