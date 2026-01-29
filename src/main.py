#!/usr/bin/env python3
import os
import shutil
from markdown_blocks import markdown_to_html_node
from gencontent import generate_pages_recursively
from copystatic import copy_files_recursive
import sys



dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

    



def main():

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursively(dir_path_content, template_path, dir_path_public , basepath)

if __name__ == "__main__":
    main()



