import os
import sys
import argparse
import cv2
import numpy as np
from image_processor import load_image, preprocess_image, detect_lines, classify_line_style
from recognizer import recognize_labels

def main():
    # Define the input path for the enhanced image
    base_dir = "C:\\Data\\TexImage-1\\image"
    enhanced_image_path = os.path.join(base_dir, "enhanced_image.bmp")

    if not os.path.exists(enhanced_image_path):
        print(f"Error: Enhanced image not found at {enhanced_image_path}")
        print("Please run the full script once to generate the enhanced_image.bmp first.")
        sys.exit(1)

    print(f"Loading enhanced image: {enhanced_image_path}")
    enhanced_image = load_image(enhanced_image_path)
    
    # --- 1. Process and save the Lines Image ---
    print("Processing lines...")
    _, binary_image, edge_image = preprocess_image(enhanced_image)
    lines = detect_lines(edge_image)
    
    # Create a new blank (white) image for the lines output
    lines_output_image = np.full_like(enhanced_image, (255, 255, 255))

    if len(lines) > 0:
        for x1, y1, x2, y2 in lines:
            style = classify_line_style(binary_image, (x1, y1, x2, y2))
            color = (0, 255, 0) if style == 'solid' else (255, 0, 0) # Green for solid, Blue for dashed
            cv2.line(lines_output_image, (x1, y1), (x2, y2), color, 2)
    
    lines_output_path = os.path.join(base_dir, "lines_output.bmp")
    cv2.imwrite(lines_output_path, lines_output_image)
    print(f"Lines image saved to {lines_output_path}")

    # --- 2. Process and save the Labels Image ---
    print("Processing labels...")
    labels = recognize_labels(enhanced_image)
    
    # Create a new blank (white) image for the labels output
    labels_output_image = np.full_like(enhanced_image, (255, 255, 255))

    if len(labels) > 0:
        for label in labels:
            x, y, w, h = label['bbox']
            text = label['text']
            # Draw bounding box and text on the labels image
            cv2.rectangle(labels_output_image, (x, y), (x + w, y + h), (0, 0, 255), 2) # Red box
            cv2.putText(labels_output_image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2) # Black text

    labels_output_path = os.path.join(base_dir, "labels_output.bmp")
    cv2.imwrite(labels_output_path, labels_output_image)
    print(f"Labels image saved to {labels_output_path}")

    print("Processing complete.")

if __name__ == '__main__':
    main()
