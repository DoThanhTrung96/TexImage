def generate_tikz_code(geometry_data, image_width, image_height):
    """Generates TikZ code from a structured JSON geometry description."""
    
    if not geometry_data or "vertices" not in geometry_data or "edges" not in geometry_data:
        return "\\documentclass{standalone}\n\\usepackage{tikz}\n\n\\begin{document}\n\\begin{tikzpicture}\n% No geometry data found\n\\end{tikzpicture}\n\\end{document}"

    # Start the TikZ code
    tikz_code = [
        "\\documentclass[border=2mm]{standalone}",
        "\\usepackage{tikz}",
        "\\usepackage{tkz-euclide}",
        "\\usetikzlibrary{quotes,angles}",
        "",
        "\\begin{document}",
        "\\begin{tikzpicture}",
    ]

    # The JSON now provides direct pixel coordinates.
    # We scale them down for a reasonably sized TikZ drawing (e.g., dividing by 50)
    # and flip the y-axis.
    scale_factor = 50
    for vertex in geometry_data["vertices"]:
        label = vertex["label"]
        x, y = vertex["coordinates"]
        x_coord = x / scale_factor
        y_coord = -y / scale_factor
        tikz_code.append(f"\\coordinate ({label}) at ({x_coord:.2f}, {y_coord:.2f});")

    # Draw the edges
    for edge in geometry_data["edges"]:
        start = edge["start"]
        end = edge["end"]
        style = edge.get("style", "solid")
        label = edge.get("label") # Can be null
        
        if label:
            # Use the 'to' syntax with the quotes library for labels
            draw_command = f"\\draw[{style}] ({start}) to[\"${label}$\"] ({end});"
        else:
            # Use the standard '--' syntax for edges without labels
            draw_command = f"\\draw[{style}] ({start}) -- ({end});"
            
        tikz_code.append(draw_command)
        
    # Draw the angles (if any)
    if "angles" in geometry_data and geometry_data["angles"]:
        for angle in geometry_data["angles"]:
            angle_label = angle["label"]
            points = angle["vertices"]
            if len(points) == 3:
                # Add degree symbol if the label is numeric
                if angle_label.isnumeric():
                    angle_label = f"{angle_label}^\\circ"
                tikz_code.append(f"\\tkzMarkAngle[size=0.8, mark=none]({points[2]},{points[1]},{points[0]})")
                tikz_code.append(f"\\tkzLabelAngle[pos=1.2]({points[2]},{points[1]},{points[0]}){{${angle_label}$}}")

    # Add labels to the vertices
    for vertex in geometry_data["vertices"]:
        label = vertex["label"]
        tikz_code.append(f"\\node[above right=1pt of {label}] {{${label}$}};")

    # End the TikZ code
    tikz_code.extend([
        "\\end{tikzpicture}",
        "\\end{document}"
    ])
    
    return "\n".join(tikz_code)
