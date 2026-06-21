def markdown_to_blocks(markdown: str) -> list[str]:
    split_markdown = markdown.split("\n\n")
    for i in range(len(split_markdown)):
        if split_markdown[i] == "\n":
            split_markdown.remove(split_markdown[i])
        split_markdown[i] = split_markdown[i].strip()
    return split_markdown
