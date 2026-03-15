import os

from md_to_htmlnode import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown content.")

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()
    
    content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    html_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", content)
    html_content = html_content.replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')

    dest_dir_path = os.path.dirname(dest_path)
    os.makedirs(dest_dir_path, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(html_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for file in os.listdir(dir_path_content):
        src_file = os.path.join(dir_path_content, file)
        dest_file = os.path.join(dest_dir_path, file)

        if os.path.isdir(src_file):
            generate_pages_recursive(src_file, template_path, dest_file, base_path)
        elif src_file.endswith(".md"):
            dest_file = dest_file[:-3] + ".html"
            generate_page(src_file, template_path, dest_file, base_path)