import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('GPT')

completion = openai.ChatCompletion.create(
    model ="gpt-3.5-turbo",
    message=[{"role": "user", "content": "Tell the world about chatgpt api"}]
)

print(completion.choices[0].message)








