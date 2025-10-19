import ollama
import base64
import json

def analyze_geometry_with_llm(image_path):
    """
    Analyzes a geometric image using a multimodal LLM (Ollama) with a detailed prompt
    and returns a structured JSON description.
    """
    with open(image_path, "rb") as f:
        image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")

    prompt = """
    Analyze the provided image of a geometric figure with extreme care. Your task is to produce a single, clean JSON object describing the figure. Follow these steps precisely:

    1.  **Find all Vertices:** Scan the entire image and identify every single capital letter (e.g., S, A, B, C, D, I, H). These are the vertices. For each vertex, provide its label and estimated 2D coordinates (top-left is origin).

    2.  **Find all Edges and their Styles:** Identify every line connecting two vertices. For each and every edge, you MUST classify its style as either 'solid' or 'dashed'. This is a mandatory field.

    3.  **Find all Edge Labels:** Scan the image for any lowercase letters, typically positioned near the midpoint of an edge (e.g., 'a'). Associate each lowercase letter with the edge it is labeling.

    4.  **Find all Angle Labels:** Locate any angle notations (e.g., '45°') and identify the three vertices that form the angle.

    5.  **Final Review (Crucial):** Before generating the JSON, review your findings.
        *   Have you included the vertex 'S'?
        *   Have you included the edge label 'a'?
        *   Does every single edge in your list have a 'style' attribute?

    Now, construct a single JSON object with the following structure. Do not include any other text, explanations, or markdown formatting outside of the final JSON block.

    {
      "vertices": [
        {"label": "...", "coordinates": [x, y]},
        ...
      ],
      "edges": [
        {"start": "...", "end": "...", "style": "solid|dashed", "label": "a"},
        ...
      ],
      "angles": [
        {"label": "45°", "vertices": ["vertex1", "vertex2", "vertex3"]}
      ]
    }
    """

    try:
        response = ollama.chat(
            model="llava",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [encoded_image],
                }
            ],
        )
        
        json_response = response["message"]["content"]
        
        # Extract only the JSON block from the response
        json_start = json_response.find('{')
        json_end = json_response.rfind('}') + 1
        
        if json_start != -1 and json_end != -1:
            json_string = json_response[json_start:json_end]
            return json.loads(json_string)
        else:
            print("Error: Could not find a JSON block in the Ollama response.")
            return None

    except Exception as e:
        print(f"An error occurred while communicating with Ollama: {e}")
        return None
