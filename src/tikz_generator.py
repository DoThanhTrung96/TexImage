def generate_tikz_code(geometry_data, image_size):
    """Generates TikZ code from a structured JSON geometry description."""
    
    if not geometry_data or "vertices" not in geometry_data or "edges" not in geometry_data:
        return "\\documentclass{standalone}\n\\usepackage{tikz}\n\n\\begin{document}\n\\begin{tikzpicture}\n% No geometry data found\n\\end{tikzpicture}\n\\end{document}"

    # Start the TikZ code
    tikz_code = [
        "\\documentclass[tikz, border=10pt]{standalone}",
        "\\usepackage{tikz}",
        "\\usepackage{amsmath}",
        "\\usetikzlibrary{quotes, angles}",
        "",
        "\\begin{document}",
        "\\begin{tikzpicture}[scale=10]", # Scale up the drawing
    ]

    # Define coordinates for each vertex
    # The LLM provides normalized coordinates, so we scale them by the image size
    # And flip the y-axis
    img_h, img_w = image_size
    
    processed_labels = set()
    for vertex in geometry_data.get("vertices", []):
        label = vertex["label"]
        if label in processed_labels:
            continue
        processed_labels.add(label)
        
        x, y = vertex["coordinates"]
        # Apply scaling and flip y-axis
        tikz_code.append(f"\\coordinate ({label}) at ({x:.3f}, {-y:.3f});")

    # Draw the edges
    for edge in geometry_data.get("edges", []):
        start = edge["start"]
        end = edge["end"]
        style = edge.get("style", "solid")
        label = edge.get("label", "")
        
        draw_command = f"\\draw[{style}] ({start}) -- ({end})"
        if label:
            draw_command += f" node[midway, above] {{${label}$}};"
        else:
            draw_command += ";"
        tikz_code.append(draw_command)
        
    # Add labels to the vertices
    for label in processed_labels:
        tikz_code.append(f"\\node[above right, font=\\small] at ({label}) {{${label}$}};")

    # Draw angles
    for angle in geometry_data.get("angles", []):
        label = angle["label"]
        verts = angle["vertices"]
        if len(verts) == 3:
            tikz_code.append(
                f"\\pic [draw, angle radius=0.5cm, \"${label}$\", angle eccentricity=1.5] {{angle = {verts[2]}--{verts[1]}--{verts[0]}}};"
            )

    # End the TikZ code
    tikz_code.extend([
        "\\end{tikzpicture}",
        "\\end{document}"
    ])
    
    return "\n".join(tikz_code)
