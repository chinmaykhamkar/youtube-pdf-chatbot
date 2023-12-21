from langchain.llms import OpenAI
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

# print(os.getenv("OPENAI_API_KEY"))

embedding = OpenAIEmbeddings()
url = "https://youtu.be/DcWqzZ3I2cY?si=yaCCqDsAj-OOznTu"
def yt_url_to_vectordb(url):
    loader = YoutubeLoader.from_youtube_url(url)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    docs = text_splitter.split_documents(docs)
    db = FAISS.from_documents(docs, embedding)
    return docs

def get_query_response(db, query, k=4):
    docs = db.similarity_search(query, k=k)
    merged_docs = " ".join([doc.page_content for doc in docs])
    
    llm = OpenAI(model = "text-davinci-003")
    prompt = PromptTemplate(
        input_variables=["question", "docs"],
        template=""" you are a helpful yoututbe assistant whos job is to
                     answer questions based on the video transcript provided.
                     Answer the following question: {question}
                     by serching through the following transcript: {docs}
                     only use factual informtion from the transcript. 
                     if you feel you don't have sufficient information
                     to answer the question, say "i don't know" your answer
                     should be verbose and detailed.""",
    )
    
    chain = LLMChain(
        llm=llm,
        prompt=prompt
    )
    
    response = chain.run(question=query, docs=merged_docs)
    response = response.replace("\n", " ")
    return response


test = yt_url_to_vectordb(url)
print(get_query_response(test, "what are jezz bezos thoughts on disagree and commit"))