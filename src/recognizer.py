import ollama
import base64
import json

def recognize_labels_with_ollama(image_path, model='llava'):
    """
    Recognizes single-character labels in an image using a multimodal LLM via Ollama.
    """
    print(f"Recognizing labels in {image_path} using Ollama model '{model}'...")
    
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    prompt = """
    Analyze the provided image of a geometric drawing.
    Identify all single-character uppercase or lowercase letter labels (A-Z, a-z).
    Return a JSON object containing a single key "labels".
    The value of "labels" should be a list of objects, where each object has:
    1. "label": the single character identified (e.g., "S", "A", "B").
    2. "center": a list of two integers [x, y] representing the center coordinates of the label.
    Do not identify any multi-character text or symbols.
    Example response: {"labels": [{"label": "S", "center": [150, 30]}, {"label": "A", "center": [50, 200]}]}
    """

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                    'images': [image_data]
                }
            ],
            format='json'
        )
        
        # The response content is a JSON string, so we need to parse it
        response_text = response['message']['content']
        print("Ollama response received. Parsing JSON...")
        data = json.loads(response_text)
        
        # Basic validation of the response structure
        if "labels" in data and isinstance(data["labels"], list):
            print(f"Successfully parsed {len(data['labels'])} labels from Ollama response.")
            return data["labels"]
        else:
            print("Warning: Ollama response did not contain a valid 'labels' list.")
            return []

    except Exception as e:
        print(f"An error occurred while communicating with Ollama: {e}")
        print("Please ensure Ollama is running and the specified model is available.")
        return []
