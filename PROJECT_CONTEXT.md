# TexImage: 3D Geometric Drawing to LaTeX

A tool to convert 2D images of projected 3D geometric figures into `TikZ` code for use in LaTeX documents.

## Project Scope & Plan

The tool will analyze an image of a 3D geometric figure (like a pyramid or cube) and generate the corresponding `TikZ` code to reproduce it, including perspective and hidden lines.

### Workflow

Our development has led to two distinct workflows: a fully automated (but currently experimental) pipeline and a semi-automated pipeline that guarantees a perfect output from a verified data source.

**Workflow A: Automated Analysis via LLM (Experimental)**

1.  **Image Input & ROI Detection**: The user provides an image, and the script automatically detects and crops the main geometric figure (Region of Interest).
2.  **LLM-based Recognition**: The cropped image is sent to a multimodal LLM (Ollama/LLaVA) with a detailed "few-shot" prompt. The model is instructed to return a structured JSON object describing the vertices, edges (with styles), and labels.
    *   *Status: This method is promising but currently produces an incomplete/inaccurate analysis. It requires further prompt engineering for reliability.*

**Workflow B: Manual Analysis for TikZ Generation (Verified & Successful)**

1.  **Manual Data Creation**: A `manual_analysis.json` file is created, containing the precise coordinates, vertices, edges, and styles based on a human analysis of the image. This serves as the "source of truth".
2.  **Direct TikZ Generation**: The script reads this perfect JSON file and passes it to the TikZ generator.
    *   *Status: This workflow is 100% reliable. It has successfully validated that our `tikz_generator.py` script can produce a perfect, compilable `.tex` file from a correct geometric description.*

**Current Project Status (80% Complete)**

We have successfully achieved the core goal of converting a structured description of a geometric figure into a perfect TikZ drawing. The `tikz_generator.py` script is complete and robust. The primary remaining challenge is to improve the automated analysis (Workflow A) to match the accuracy of the manual analysis (Workflow B).

### Technology Stack

*   **Language**: Python 3
*   **Core Libraries**:
    *   `opencv-python`: For all core computer vision tasks.
    *   `pytesseract`: For Optical Character Recognition (OCR) of labels.
    *   `numpy`: For geometric calculations and coordinate transformations.
    *   `networkx`: For modeling the figure's structure as a graph.
