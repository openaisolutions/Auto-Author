import yaml
import os

def read_toc(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File '{file_path}' does not exist.")
        return

    # Load the TOC data from the YAML file
    with open(file_path, 'r') as file:
        toc_data = yaml.safe_load(file)

    # Print the overview of the book structure
    print("Overview of the book structure:")
    chapters = toc_data.get('chapters', [])
    for chapter in chapters:
        print(f"Chapter: {chapter.get('title', chapter.get('file'))}")
        sections = chapter.get('sections', [])
        for section in sections:
            print(f"  - Section: {section['title']}")
            subsections = section.get('subsections', [])
            for subsection in subsections:
                print(f"    - Subsection: {subsection['title']}")

if __name__ == '__main__':
    # Specify the path to the TOC file (YAML)
    toc_file_path = '_toc.yaml'
    # Call the read_toc function
    read_toc(toc_file_path)
