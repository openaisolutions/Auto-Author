import yaml

def generate_toc():
    # Prompt the user for information about the book
    topic = input("Enter the topic of the book: ")
    audience = input("Enter the target audience for the book: ")
    purpose = input("Enter the purpose of the book: ")
    num_chapters = int(input("Enter the number of chapters you want in the book: "))

    # Create an empty list to store the chapters
    chapters = []

    # Prompt the user for chapter titles and add them to the list
    for i in range(1, num_chapters + 1):
        chapter_title = input(f"Enter the title for Chapter {i}: ")
        chapters.append({'file': f'chapter_{i}', 'title': chapter_title})

    # Create the TOC structure
    toc = {
        'topic': topic,
        'audience': audience,
        'purpose': purpose,
        'chapters': chapters
    }

    # Save the TOC to a YAML file
    with open('toc.yaml', 'w') as f:
        yaml.dump(toc, f, default_flow_style=False)

    print("TOC has been successfully generated and saved to toc.yaml")

if __name__ == '__main__':
    generate_toc()
