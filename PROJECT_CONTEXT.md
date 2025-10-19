# TexImage: 3D Geometric Drawing to LaTeX

A tool to convert 2D images of projected 3D geometric figures into `TikZ` code for use in LaTeX documents.

## Project Scope & Plan

The tool will analyze an image of a 3D geometric figure (like a pyramid or cube) and generate the corresponding `TikZ` code to reproduce it, including perspective and hidden lines.

### Workflow

1.  **Image Input & ROI Detection**: 
    *   The user provides an image file (PNG, JPG).
    *   The image is preprocessed (grayscale, binary inversion, dilation) to find the largest contour, which is assumed to be the geometric figure.
    *   The image is then cropped to the bounding box of this contour (Region of Interest) for all further analysis.

2.  **Primitive Detection (on ROI)**:
    *   **Line Segments**: The Hough Line Transform is used on a Canny edge detection of the ROI to find all line segments.
    *   **Line Style**: Each line is classified as `solid` or `dashed` by analyzing the pixel intensity patterns on the binary version of the ROI.
    *   **Vertices**: Endpoints from all detected lines are collected and clustered based on proximity to identify unique vertices.

3.  **Label Recognition (on OCR-optimized image)**:
    *   **Line Removal**: To isolate text, a copy of the ROI is created, and all detected lines are programmatically erased.
    *   **Image Enhancement**: This "text-only" image is upscaled and sharpened to improve OCR accuracy.
    *   **Tesseract OCR**: The enhanced, text-only image is passed to Tesseract with a specific configuration (PSM 6, character whitelist) to recognize labels.

4.  **3D Structural Reconstruction**: A 3D data model of the geometry is inferred from the 2D primitives. This involves estimating 3D coordinates and building a graph of the figure's structure.

5.  **TikZ Code Generation**: The final `TikZ` code is generated from the 3D model, using libraries like `tikz-3dplot` to handle perspective. Dashed styles are applied to hidden lines.

### Technology Stack

*   **Language**: Python 3
*   **Core Libraries**:
    *   `opencv-python`: For all core computer vision tasks.
    *   `pytesseract`: For Optical Character Recognition (OCR) of labels.
    *   `numpy`: For geometric calculations and coordinate transformations.
    *   `networkx`: For modeling the figure's structure as a graph.
