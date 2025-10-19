import os
import sys
import argparse
import cv2
from image_processor import load_image, preprocess_image, detect_lines, classify_line_style, detect_vertices, detect_geometry_roi
from recognizer import recognize_labels

def main():
    parser = argparse.ArgumentParser(description="Process a geometric image and generate TikZ code.")
    parser.add_argument("image_path", type=str, help="Path to the input image file.")
    args = parser.parse_args()

    if not os.path.exists(args.image_path):
        print(f"Error: Image file not found at {args.image_path}")
        sys.exit(1)

    print(f"Loading image: {args.image_path}")
    original_image = load_image(args.image_path)
    gray_image, binary_image, edge_image = preprocess_image(original_image)

    print("Detecting geometry region of interest...")
    cropped_image, offset = detect_geometry_roi(binary_image, original_image)
    print(f"Geometry ROI detected. Cropped image size: {cropped_image.shape[:2]}, Offset: {offset}")

    # Now all subsequent operations use the cropped_image
    _, cropped_binary_image, cropped_edge_image = preprocess_image(cropped_image) # Preprocess cropped image for line detection and style classification
    lines = detect_lines(cropped_edge_image)
    print(f"Detected {len(lines)} lines in ROI.")

    # Visualize detected lines on the cropped image
    line_image_roi = cropped_image.copy()
    if len(lines) > 0:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image_roi, (x1, y1), (x2, y2), (0, 255, 0), 2) # Green lines
            style = classify_line_style(cropped_binary_image, (x1, y1, x2, y2))
            print(f"Line (ROI): ({x1},{y1}) to ({x2},{y2}), Style: {style})")

    labels = recognize_labels(cropped_image) # Use the cropped image for OCR
    print(f"Detected {len(labels)} labels in ROI.")

    # Visualize detected labels on the cropped image
    label_image_roi = cropped_image.copy()
    for label in labels:
        x, y, w, h = label['bbox']
        text = label['text']
        cv2.rectangle(label_image_roi, (x, y), (x + w, y + h), (255, 0, 0), 2) # Blue rectangle
        cv2.putText(label_image_roi, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow("Detected Lines (ROI)", line_image_roi)
    cv2.imshow("Detected Labels (ROI)", label_image_roi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
