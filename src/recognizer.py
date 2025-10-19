import cv2
import pytesseract

def recognize_labels(image):
    """Recognizes text labels in the image using Tesseract OCR."""
    # Convert the image to a format suitable for Tesseract
    # Tesseract works best with preprocessed images (e.g., grayscale, binarized)
    # For now, we'll assume the input image is already preprocessed (e.g., edges or binary)
    
    # You might need to install Tesseract OCR engine separately on your system
    # and configure its path if it's not in your system's PATH.
    # Example for Windows: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    labels = []
    n_boxes = len(text_data['level'])
    for i in range(n_boxes):
        if int(text_data['conf'][i]) > 60: # Filter out low confidence detections
            x, y, w, h = text_data['left'][i], text_data['top'][i], text_data['width'][i], text_data['height'][i]
            text = text_data['text'][i]
            if text.strip(): # Only add non-empty text
                labels.append({'text': text, 'bbox': (x, y, w, h)})
    return labels
