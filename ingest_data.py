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

folder_path = "content/posts/"
files = os.listdir(folder_path)
en_files = [file for file in files if ('.pt' not in file) and ('_index' not in file) and ('2023' or '2024-01' or '2024-02' or '2024-03-01' in file)]

for file in en_files:
    markdown_path = f"{folder_path}{file}"
    loader = UnstructuredMarkdownLoader(markdown_path)

    raw_documents = loader.load()
    content = raw_documents[0].page_content

    documents.append(content)
    metadatas.append({"source": folder_path + file})
    ids.append(file)

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids,
)

with open("vectorstore.pkl", "w") as f:
	f.write(str(collection.get()))