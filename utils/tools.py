import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough
from utils import prompts, retriever

dotenv.load_dotenv()

def get_chat_model():
    chat_model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    return chat_model

def get_db_retriever(rebuild=False):
    if rebuild:
        retriever.rebuild_db()
    db = Chroma(
        persist_directory=retriever.get_db_path(),
        embedding_function=retriever.get_embedding()
    )
    db_retriever = db.as_retriever(k=5)
    return db_retriever

def get_chain():
    chain = (
        {"context": get_db_retriever(), "question": RunnablePassthrough()}
        | prompts.get_template() 
        | get_chat_model() 
        | StrOutputParser()
    )
    return chain


#testing
question = 'list out the 4 steps of AI design. return as a numbered list'
output = get_chain().invoke(question)
print(output)

