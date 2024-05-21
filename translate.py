from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

text = open(f'content/posts/2024-04-16.md').read()

response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {
      "role": "system",
      "content": "You will be provided with a markdown text in English, and your task is to translate the content to Brazilian Portuguese."
    },
    {
      "role": "user",
      "content": text
    }
  ],
  temperature=0.7,
  max_tokens=7000,
  top_p=1
)

# print(response.choices[0].message.content)