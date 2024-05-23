from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import UnstructuredMarkdownLoader
import dotenv
import os
import chromadb

dotenv.load_dotenv()

client = chromadb.Client()
collection = client.create_collection("en_posts")
documents = []
metadatas = []
ids = []

folder_path = "content/posts"
files = os.listdir(folder_path)
en_files = [file for file in files if '.pt' not in file and '_index' not in file]

# Define prompt
prompt_template = """Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:"""
prompt = PromptTemplate.from_template(prompt_template)

# Define LLM chain
llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
llm_chain = LLMChain(llm=llm, prompt=prompt)

for file in en_files:
    markdown_path = f"content/posts/{file}"
    loader = UnstructuredMarkdownLoader(markdown_path)

    docs = loader.load()
    content = docs[0].page_content

    documents.append(content)
    metadatas.append({"source": folder_path})
    ids.append(file)

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
)
