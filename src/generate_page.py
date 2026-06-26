from block_to_html import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from \"{from_path}\" to \"{dest_path}\" using \"{template_path}\"")
    with open(from_path) as from_file:
        from_file_content = from_file.read()
    with open(template_path) as template_file:
        template_file_content = template_file.read()
    html_string = markdown_to_html_node(from_file_content).to_html()
    title = extract_title(from_file_content)
    pass
