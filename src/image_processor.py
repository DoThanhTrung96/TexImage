import cv2
import numpy as np

def load_image(image_path):
    """Loads an image from the specified path."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    return image

def preprocess_image(image):
    """Converts image to grayscale, binarizes, and performs edge detection.
    Returns the grayscale, binary, and edge-detected images.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    edges = cv2.Canny(binary, 50, 150)
    return gray, binary, edges

def detect_lines(edges):
    """Detects line segments in an edge-detected image using Hough Line Transform."""
    detected_lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)
    if detected_lines is not None:
        return detected_lines.reshape(-1, 4)  # Reshape to N x 4 array (x1, y1, x2, y2)
    return np.array([])

def classify_line_style(binary_image, line_segment):
    """Classifies a line segment as solid or dashed based on pixel intensity patterns.
    Takes the binary image to analyze pixel patterns along the line.
    """
    x1, y1, x2, y2 = map(int, line_segment)

    # Create a mask for the line segment on the binary image
    mask = np.zeros_like(binary_image, dtype=np.uint8)
    cv2.line(mask, (x1, y1), (x2, y2), 255, 1)  # Draw a thin white line on a black mask

    # Get pixel values along the line segment from the binary image
    line_pixels = binary_image[mask == 255]

    if len(line_pixels) < 10:  # Not enough pixels to reliably classify
        return "solid"

    # Count transitions between foreground (255) and background (0) pixels
    # A dashed line will have more transitions than a solid line
    transitions = np.sum(np.abs(np.diff(line_pixels.astype(int))) > 0)

    # Heuristic threshold for dashed lines (can be tuned)
    # This threshold needs to be carefully chosen based on expected dash patterns
    if transitions > len(line_pixels) / 10: # Adjusted threshold for more sensitivity
        return "dashed"
    else:
        return "solid"

def detect_geometry_roi(binary_image, original_image):
    """Detects the region of interest containing the main geometric figure.
    Uses the binary image for contour detection and the original image for cropping.
    """
    # Apply dilation to connect fragmented contours in the binary image
    kernel = np.ones((5, 5), np.uint8)
    dilated_binary = cv2.dilate(binary_image, kernel, iterations=1)

    contours, _ = cv2.findContours(dilated_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return original_image, (0, 0)  # Return original if no contours found

    # Find the largest contour, assuming it's the main geometric figure
    largest_contour = max(contours, key=cv2.contourArea)

    # Get the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Add some padding to the bounding box to ensure labels are included
    padding = 10
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(original_image.shape[1] - x, w + 2 * padding)
    h = min(original_image.shape[0] - y, h + 2 * padding)

    # Crop the original image using the adjusted bounding box
    cropped_image = original_image[y:y+h, x:x+w]

    return cropped_image, (x, y)

def detect_vertices(lines):
    """Detects vertices (endpoints and intersections) from detected lines. (Placeholder)"""
    # This will involve finding intersections of lines and unique endpoints.
    return np.array([])