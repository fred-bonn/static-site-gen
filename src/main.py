from textnode import TextNode, TextType

def main():
    node = TextNode("Hello, World!", TextType.PLAIN, "www.example.come")
    print(node)

main()