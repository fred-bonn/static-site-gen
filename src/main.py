import sys

from static_copy import static_copy
from page_generation import generate_pages_recursive

static_path = "./static"
public_path = "./public"

def main():
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    static_copy(static_path, public_path)
    generate_pages_recursive("./content", "./template.html", "./docs", base_path)

main()