import re

# !\[.+?\]\(.+?\) is the regex pattern for finding pairs of inline images in markdown (excluding empty formatters), can
# then split at the the "]" character to insert, acutally not complete it will pattern match with partially filled in
# inline images or sometimes even empty still in the right context

# !\[([^\[\]]+)\]??\(([^()]+)\) is the best combination of regex that seems to only get properly filled out patterns for
# inline images with capture groups for the alt text and the url

def extract_markdown_images(text):
    pass
