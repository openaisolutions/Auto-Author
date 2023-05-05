import os
import openai
openai.api_key = "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"


#List the available models
models = openai.Model.list()

# Print the list of models
for model in models['data']:
    print(model.id)