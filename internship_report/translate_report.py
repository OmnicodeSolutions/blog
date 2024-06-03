import sys

from openai import OpenAI
from dotenv import load_dotenv

def translate_report():  
    with open('report.md') as file:
    
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
            "content": file.read()
            }
        ],
        temperature=0.7,
        max_tokens=3000,
        top_p=1
        )
        
        translated_text = response.choices[0].message.content
        
        pt_file = open('report.pt.md', 'w')
        pt_file.write(translated_text)
        pt_file.close()
        
        file.close()