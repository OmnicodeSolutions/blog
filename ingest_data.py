from langchain_community.document_loaders import UnstructuredMarkdownLoader
import dotenv
import os
import chromadb

dotenv.load_dotenv()

def create_collection(folder_path, en_files):
    client = chromadb.Client()
    if client.count_collections() > 0:
        client.delete_collection("en_posts")
    collection = client.create_collection("en_posts")
    documents = []
    metadatas = []
    ids = []

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

    with open("blog_posts.pkl", "w") as f:
        f.write(str(collection.get()))
