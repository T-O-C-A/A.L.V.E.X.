import openai

openai.api_key = 'your-api-key-here'

def process_nlp_input(command):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following command into actions: {command}",
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()
