from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
import utils
from langchain_text_splitters import RecursiveCharacterTextSplitter


import os
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class CustomDataChatbot:
    def __init__(self):
        self.openai_model = utils.configure_openai()

    def save_file(self, file: UploadFile):
        folder = 'tmp'
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_path = f'./{folder}/{file.filename}'
        with open(file_path, 'wb') as f:
            f.write(file.file.read())
        return file_path

    def setup_qa_chain(self, uploaded_files: List[UploadFile]):
        # Load documents
        docs = []
        for file in uploaded_files:
            file_path = self.save_file(file)
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load())
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        # Create embeddings and store in vectordb
        embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)

        # Define retriever
        retriever = vectordb.as_retriever(
            search_type='mmr',
            search_kwargs={'k':2, 'fetch_k':4}
        )

        # Setup memory for contextual conversation        
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            output_key='answer',
            return_messages=True
        )

        # Setup LLM and QA chain
        llm = ChatOpenAI(model_name=self.openai_model, temperature=0, streaming=True)
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=True
        )
        return qa_chain

    def get_response(self, user_query: str, uploaded_files: List[UploadFile]):
        qa_chain = self.setup_qa_chain(uploaded_files)
        result = qa_chain.invoke({"question": user_query})
        response = result["answer"]
        sources = [
            {"filename": os.path.basename(doc.metadata['source']),
             "page": doc.metadata['page'],
             "content": doc.page_content}
            for doc in result['source_documents']
        ]
        return response, sources

chatbot = CustomDataChatbot()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_files(files: List[UploadFile], user_query: str = Form(...)):
    if not files:
        return JSONResponse(content={"error": "Please upload PDF documents to continue!"}, status_code=400)

    response, sources = chatbot.get_response(user_query, files)
    return JSONResponse(content={"answer": response, "sources": sources})

@app.post("/stream/")
async def stream_files(request: Request):
    # Implement streaming if necessary
    return JSONResponse(content={"message": "Streaming not yet implemented"}, status_code=501)
