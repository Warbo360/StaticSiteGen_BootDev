import re

def extract_markdown_images(text: str) -> list[tuple[str, str]]:

    # regex to pull inline images from markdown text, regex reads as staring with an exlamantion point, left bracket,
    # then capture group which can be anything but brackets, forward slashes zero to multiple times, then after that
    # capture group left bracket, right parens, 2nd capture group which excludes parens, brackets, and whitespace.
    # Should re-work for filepaths (which would allow whitespace) if needed. That group atleast 1 of more times then
    # ending in a right parens
    # Example pattern to be matched: ![alt-text](https:www.somelinktoanimage.png)
    # will return matches as a list of tuples each tuple being (alt-text, url) matches found in the passed text

    return re.findall(r"!\[([^\[\]\\]*?)\]\(([^\(\)\[\]\s]+?)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:

    # Same as above but uses a behind lookaround for an "!" to be sure it is not an inline image, and is just a link in
    # markdown, also returns as a list of tuples in the same format as above

    return re.findall(r"(?<!!)\[([^\[\]]+)\]??\(([^()]+)\)", text)



