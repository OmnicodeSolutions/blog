import sys

from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

if len(sys.argv) > 1:
  en_path = f'content/posts/{sys.argv[1]}.md'
  pt_path = f'content/posts/{sys.argv[1]}.pt.md'
else:
  date = datetime.today().strftime('%Y-%m-%d')
  en_path = f'content/posts/{date}.md'
  pt_path = f'content/posts/{date}.pt.md'

en_file = open(en_path, 'r+')

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {
      "role": "system",
      "content": "You will be provided with a markdown text in English, and your task is to translate the content to Brazilian Portuguese."
    },
    {
      "role": "user",
      "content": en_file.read()
    }
  ],
  temperature=0.7,
  max_tokens=3000,
  top_p=1
)

translated_text = response.choices[0].message.content

pt_file = open(pt_path, 'w')
pt_file.write(translated_text)
pt_file.close()

en_file.close()