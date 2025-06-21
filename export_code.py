import os

# Set the environment variable with your OpenAI API key. Replace the empty
# string with your actual key if you want this script to set it for you.
os.environ['OPENAI_API_KEY'] = ""

# Retrieve the value of the environment variable
api_key = os.environ['OPENAI_API_KEY']

# Print the value to verify
print(api_key)
