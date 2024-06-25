import dotenv
import os, shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()

def get_embedding():
    return OpenAIEmbeddings()

def get_db_path():
    return "db"

def get_pdf_documents():
    DATA_FOLDER = "data"
    print('getting pdfs from {}'.format(DATA_FOLDER))
    loader = PyPDFDirectoryLoader(DATA_FOLDER)
    docs = loader.load()
    print('docs loaded')
    return docs

def split_text(documents):
    print('splitting text')
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len
    )
    splits = text_splitter.split_documents(documents)
    print('done splitting text')
    return splits

def create_Chroma_db(text_splits):
    print('creating db and saving here: {}'.format(get_db_path()))
    db = Chroma.from_documents(
        documents=text_splits,
        embedding=get_embedding(),
        persist_directory=get_db_path()
    )
    print('done creating db')
    return db

def create_db():
    pdfs = get_pdf_documents()
    text = split_text(pdfs)
    vector_db = create_Chroma_db(text)
    return vector_db

def rebuild_db():
    print('rebuilding db')
    print('deleting db')
    try:
        folder_path = get_db_path()
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        print(f"All contents of the folder '{folder_path}' have been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return create_db()