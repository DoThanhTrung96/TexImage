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
    Analyze the provided image of a geometric figure with extreme care. Your task is to produce a single, clean JSON object describing the figure.

    Here is an example of a perfect analysis for a simple pyramid:
    ---
    EXAMPLE INPUT IMAGE: [A simple pyramid with top vertex 'O' and base vertices 'A' and 'B'. Edge AB is dashed and labeled 'x'.]
    EXAMPLE OUTPUT JSON:
    {
      "vertices": [
        {"label": "O", "coordinates": [50, 10]},
        {"label": "A", "coordinates": [10, 80]},
        {"label": "B", "coordinates": [90, 80]}
      ],
      "edges": [
        {"start": "O", "end": "A", "style": "solid", "label": null},
        {"start": "O", "end": "B", "style": "solid", "label": null},
        {"start": "A", "end": "B", "style": "dashed", "label": "x"}
      ],
      "angles": []
    }
    ---

    Now, analyze the new image provided. Follow these steps precisely:

    1.  **Find all Vertices:** Scan the entire image and identify every single capital letter (e.g., S, A, B, C, D, I, H). These are the vertices. For each vertex, provide its label and estimated 2D coordinates as percentages of the image width and height (top-left is origin).

    2.  **Find all Edges and their Styles:** Identify every line connecting two vertices. For each and every edge, you MUST classify its style as either 'solid' or 'dashed'.

    3.  **Find all Edge Labels:** Scan for lowercase letters near the midpoint of an edge (e.g., 'a'). Associate it with the correct edge. If an edge has no label, the value for "label" should be null.

    4.  **Final Review (Crucial):** Before generating the JSON, review your findings against the image.
        *   Have you found all vertices, including 'S'?
        *   Have you found all edges and correctly identified their 'solid' or 'dashed' style?
        *   Have you found the edge label 'a'?
        *   Is your output ONLY a single JSON object, just like the example?

    Construct a single JSON object. Do not include any other text or explanations.
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
