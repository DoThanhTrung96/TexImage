# TexImage: 3D Geometric Drawing to LaTeX

A tool to convert 2D images of projected 3D geometric figures into `TikZ` code for use in LaTeX documents.

## Project Scope & Plan

The tool will analyze an image of a 3D geometric figure (like a pyramid or cube) and generate the corresponding `TikZ` code to reproduce it, including perspective and hidden lines.

### Workflow

1.  **Image Input**: User provides an image file (PNG, JPG) of a geometric drawing.
2.  **Preprocessing**: The image is converted to grayscale and edges are detected.
3.  **Primitive Detection**:
    *   **Line Segments**: All line segments and their endpoints are detected.
    *   **Line Style**: Each line is classified as `solid` or `dashed`.
    *   **Vertices**: The 2D coordinates of all vertices are identified.
4.  **Label Recognition**: Tesseract OCR is used to identify text labels for vertices (A, B), edges (a), and angles (45°).
5.  **3D Structural Reconstruction**: A 3D data model of the geometry is inferred from the 2D primitives. This involves estimating 3D coordinates and building a graph of the figure's structure.
6.  **TikZ Code Generation**: The final `TikZ` code is generated from the 3D model, using libraries like `tikz-3dplot` to handle perspective. Dashed styles are applied to hidden lines.

### Technology Stack

*   **Language**: Python 3
*   **Core Libraries**:
    *   `opencv-python`: For all core computer vision tasks.
    *   `pytesseract`: For Optical Character Recognition (OCR) of labels.
    *   `numpy`: For geometric calculations and coordinate transformations.
    *   `Pillow`: For image manipulation.
    *   `networkx`: (Recommended) For modeling the figure's structure as a graph.
