import yaml
import openai
import nbformat
from nbformat.v4 import new_markdown_cell, new_code_cell, new_notebook

def generate_content(yaml_content):
    # Load the YAML content
    toc = yaml.load(yaml_content, Loader=yaml.SafeLoader)
    # Define the API key
    api_key = 

    # Set the API key for the OpenAI library
    openai.api_key = api_key

    # Loop through parts
    for part in toc['parts']:
        part_description = part.get('caption', '')
        # Loop through chapters
        for chapter in part['chapters']:
            chapter_description = chapter.get('title', '')
            # Create a new notebook
            nb = new_notebook()

            # Loop through sections
            for section in chapter['sections']:
                section_description = section.get('title', '')
                # Use descriptions to prompt GPT-3 for content generation
                messages = [
                    {"role": "system", "content": "You are a helpful content writing assistant."},
                    {"role": "user", "content": f"Generate content for this section:\n{part_description}\n{chapter_description}\n{section_description}"}
                ]
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                generated_content = completion.choices[0].message['content'].strip()
                # Add generated content to notebook cells
                nb.cells.append(new_markdown_cell(generated_content))

            # Save the notebook to the specified filename
            with open(f"{chapter['file']}.ipynb", 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
            print("Generated content for", chapter['file'])

# Load the YAML content from the file
with open('_toc.yaml', 'r') as toc_file:
    yaml_content = toc_file.read()

# Call the function to generate content
generate_content(yaml_content)
