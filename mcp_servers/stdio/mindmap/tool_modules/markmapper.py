from typing import Optional

# You can embed the template directly, or load from a file. Here it’s embedded for clarity.
html_template = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <style>
      svg.markmap {{
        width: 100%;
        height: 100vh;
      }}
      
    </style>
    <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.18"></script>
  </head>
  <body>
    <div class="markmap">
      <script type="text/template">
        ---
        markmap:
          maxWidth: 300
          initialExpandLevel: -1
          spacingHorizontal: 80
          spacingVertical: 5
          duration: 1000
          colorFreezeLevel: 3
        ---
{script_content}
      </script>
    </div>
  </body>
</html>"""

def convert_markdown_to_html(markdown_content: str, title: str, output_filename: Optional[str] = None) -> dict:
    """
    Converts a markdown string into an interactive HTML mindmap using markmap.js.
    
    Args:
        markdown_content (str): The markdown text to visualize. Use headers (#) and bullets (-) for hierarchy.
        title (str): The title of the generated HTML page.
        output_filename (str): Optional. The filename to save the HTML to (e.g., 'my_mindmap.html').
                               If not provided, defaults to '{title}.html'.
    
    Returns:
        dict: A status dictionary like {"done": "good"}.
    """
    def validate_markdown_content(md: str) -> str:
        valid_markdown_characters = ("#", "-", "*", ">", "`", "=")
        output_lines = []
        for line in md.splitlines():
            if not line.strip():
                output_lines.append("")
            elif line.lstrip() != line:
                # Leave indented (nested) lines alone
                output_lines.append(line)
            elif line.startswith(valid_markdown_characters):
                output_lines.append(line)
            else:
                output_lines.append(f"- {line}")
        return "\n".join(output_lines)

    validated_content = validate_markdown_content(markdown_content)
    # Indent the markdown block for pretty output
    indented_content = "\n".join("        " + line if line.strip() else "" for line in validated_content.splitlines())
    html_output = html_template.format(title=title, script_content=indented_content)

    if output_filename is None:
        output_filename = f"{title}.html"

    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_output)
        return {"status": "success", "file_path": output_filename}
    except IOError as e:
        raise RuntimeError(f"Error writing to file {output_filename}: {e}")

if __name__ == "__main__":
    sample_markdown = """
# Sample Markmap
This is a sample mind map.
- Node 1
  - Subnode 1.1
    - Deeper Node
  - Subnode 1.2
Another line without a bullet
* Another bullet
    - A nested item
- Node 2
  - Another Subnode
"""
    output_filename = "test_markmap_corrected.html"
    print("Converting sample markdown to HTML with corrected logic...")
    convert_markdown_to_html(sample_markdown, title="Test_Markmap", output_filename=output_filename)
    print(f"Successfully saved Markmap to '{output_filename}'")
    print("Open the file in a browser to see that nested items are now rendered correctly.")
