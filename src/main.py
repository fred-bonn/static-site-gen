from static_copy import static_copy
from page_generation import generate_page

static_path = "./static"
public_path = "./public"

def main():
    static_copy(static_path, public_path)
    generate_page("./content/index.md", "./template.html", "./public/index.html")

main()