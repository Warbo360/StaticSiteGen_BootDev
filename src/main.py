from generate_pages_recursive import generate_pages_recursive
from textnode import *
from static_to_public import static_to_public

def main():

    static_to_public("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()
