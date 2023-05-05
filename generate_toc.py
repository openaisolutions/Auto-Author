import os
import openai
import re
import requests

# Define the API key
api_key = 

# Set the API key for the OpenAI library
openai.api_key = api_key

def extract_yaml(response_text):
    # Define a regular expression pattern to match the YAML content
    pattern = re.compile(r'```(.*?)```', re.DOTALL)

    # Use the regular expression to search for the YAML content
    match = pattern.search(response_text)

    # If a match is found, extract and return the YAML content
    if match:
        yaml_content = match.group(1).strip()
        return yaml_content

    # If no match is found, return the original response_text
    return response_text

def generate_toc():
    # Get user input
    topic = input("Enter the topic of the book: ")
    audience = input("Enter the target audience for the book: ")
    purpose = input("Enter the purpose of the book: ")

    # Define the prompt for ChatGPT
    prompt = (f"Generate a table of contents in Jupyter-Book YAML format for a book on the topic '{topic}'. "
            f"Please create chapters, sections, and subsections with filename, title, and content. Follow these guidelines:\n"
            f"for every line, please add at least one comment using the pound sign (#). \n"
            f"the comment should be a short description of the line below it. use mulitple comments for each line if necessary.\n"
            f"- do not preface with YAML. Use proper YAML formatting and indentation as per Jupyter-book YAML guidance with this example:\n"
            f"    format: jb-book\n"
            f"    root: intro\n"
            f"    parts:\n"
            f"    - caption: Tutorials\n"
            f"      chapters:\n"
            f"      - file: start/your-first-book\n"
            f"        sections:\n"
            f"        - file: start/overview\n"
            f"- follow YAML rules for indentation. use 4 spaces for indentation.  \n"
            f"- do NOT use colons (:) in titles or text. \n"
            f"- do NOT use double quotes (\") in titles or text. \n"
            f"- do NOT use backticks (`) in titles or text. .\n"
            f"- do NOT use square brackets ([]) in titles or text.\n"
            f"- do NOT use a period (.) in titles or text. .\n"
            f"- do NOT use a comma (,) in titles or text. .\n"
            f"- Ensure that subsections are correctly nested under their respective sections.\n"
            f"The book is targeted at the audience '{audience}', with the purpose '{purpose}':")


    # Define the conversation messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    # Set the API endpoint and headers
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {'model': 'gpt-3.5-turbo', 'messages': messages}

    # Make the API call using the requests library
    response = requests.post(url, headers=headers, json=data).json()

    # Extract the generated TOC from the response
    generated_toc = response['choices'][0]['message']['content'].strip()

    # Extract the YAML content from the generated TOC
    yaml_content = extract_yaml(generated_toc)

    # Save the TOC to a YAML file
    with open('_toc.yaml', 'w') as f:
        f.write(yaml_content)

    print("TOC has been successfully generated and saved to _toc")

if __name__ == '__main__':
    generate_toc()
