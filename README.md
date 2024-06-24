# mit_ai_class_bot
Code to build a simple chatbot with ability to ustilize transcripts of class videos


Instructions:
1) CREATE ENV FILE: create a file called ".env" with
    OPENAI_API_KEY='<your-key>'

2) DATA SETUP:
    A) PDFS: add pdfs of the transcript to the data folder
    B) CREATE DB: in a python shell, run the following commands
            python
            >>> from utils import retriever
            >>> retriever.create_db()
    C) REBUILDING DB: if you need to rebuild the database, run the following commands
            python
            >>> from utils import retriever
            >>> retriever.rebuild_db()

3) RUN: 
    A) run "python app.py"
    B) go to a browser and navigate to "http://localhost:8888/"

4) enjoy