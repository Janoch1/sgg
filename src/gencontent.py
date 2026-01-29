from markdown_blocks import markdown_to_html_node
import os
from pathlib import Path

def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath):

    for entry_name in os.listdir(dir_path_content):

        full_source_path = os.path.join(dir_path_content, entry_name)
        full_dest_path = os.path.join(dest_dir_path, entry_name)
        if os.path.isfile(full_source_path):
            dest_html_path =  Path(full_dest_path).with_suffix(".html")
            generate_page(full_source_path, template_path, dest_html_path, basepath)
        else:
            generate_pages_recursively(full_source_path, template_path, full_dest_path, basepath)
        



        