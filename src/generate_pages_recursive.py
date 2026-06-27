import os
from block_to_html import markdown_to_html_node
from extract_title import extract_title

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    current_dir: list[str] = os.listdir(dir_path_content)
    for i in range(len(current_dir)):
        print(f"INFO: Parsing \"./{dir_path_content}\"...")
        if os.path.isfile(dir_path_content + "/" + current_dir[i]):
            # If file, generate a new html file for it and place it in the current dest dir
            print(f"INFO: Generating HTML for \"./{dir_path_content}/{current_dir[i]}\"")
            with open(dir_path_content + "/" + current_dir[i], "r") as f:
                file_content: str = f.read()
                title: str = extract_title(file_content)
                file_content_to_html: str = markdown_to_html_node(file_content).to_html()
            with open(template_path, "r") as f:
                template: str = f.read()
            filled_template: str = template.replace("{{ Title }}", title).replace("{{ Content }}", file_content_to_html)
            file_name: str = current_dir[i].replace(".md", ".html")
            with open(dest_dir_path + "/" + file_name, "w") as f:
                _: int = f.write(filled_template)
            print(f"{GREEN}SUCCESS{RESET}: \"{file_name}\" placed into \"{dest_dir_path}/\"")
            continue
        # If not a file, must be a dir, create that same dir in dest, and recursive call going into that sub dir with a
        # target of dest_dir + sub_dir
        print(f"INFO: Making directory \"{current_dir[i]}\" in \"./{dest_dir_path}\"")
        os.mkdir(dest_dir_path + "/" + current_dir[i])
        generate_pages_recursive(
            dir_path_content + "/" + current_dir[i],
            template_path,
            dest_dir_path + "/" + current_dir[i]
        )
