import re

def extract_title(md: str) -> str:
    header: re.Match[str] | None = re.search(r"# (.+)", md, re.M)
    if not header:
        raise Exception(f"ERROR: \"{md}\" does not contain a \"h1\" header")
    return header.group(1)
