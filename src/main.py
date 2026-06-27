from generate_pages_recursive import generate_pages_recursive
from textnode import *
from static_to_public import static_to_public
import sys

def main():

    basepath: str = ""
    if len(sys.argv) < 2:
        basepath = "/"
    elif len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        sys.exit(f"USAGE: python3 main.py <arg1>")
    print(basepath)

    static_to_public("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()
