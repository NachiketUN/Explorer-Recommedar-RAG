from flask import Flask, request, jsonify, render_template
from main import *
from llm_functions import summary
from flask_cors import CORS
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

import time


app = Flask(__name__)
CORS(app)
global api_key 
api_key = os.environ["OPENAI_API_KEY"]
#Restaurant document data
data = pd.read_pickle('restaurent_docs_1.pickle')
loader = DataFrameLoader(data, page_content_column="doc_information")
bm25 = BM25Retriever.from_documents(loader.load())
bm25.k = 10
embeddings = OpenAIEmbeddings(openai_api_key=api_key)
vectordb = Chroma(persist_directory='./chroma_db_res2', embedding_function=embeddings)
# vector_retriever = vectordb.as_retriever(search_kwargs={"k": 5},search_type="mmr")

vector_retriever = vectordb.as_retriever(search_kwargs={"k": 10})

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25, vector_retriever], weights=[0.5, 0.5]
)

recommender_data = pd.read_pickle('recommendation_1.pickle')
# documents = data['doc_information'].to_list()
# tokenized_docs = [doc.split(" ") for doc in documents]
# bm25 = BM25Okapi(tokenized_docs)


llm = ChatOpenAI(openai_api_key=api_key, temperature=0, model_name="gpt-3.5-turbo-1106")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.json["query"]
        zipcode = request.json["zipcode"]
        # return jsonify(retrieval_info(data, bm25, query,zipcode))
        return jsonify(ensemble(llm,ensemble_retriever, query,zipcode))

@app.route('/search', methods=['POST'])
def get_restaurant_info():
    if request.method == 'POST':
        print("hello")
        return jsonify(recommender_info(llm, data,recommender_data,request.json["gmap_id"])) 
    
@app.route('/summary', methods=['POST'])
def get_summary():
    if request.method == 'POST':
        text = summary(request.json["gmap_id"],data,api_key)
        print(text)
        return jsonify(text) 

@app.route('/ensemble', methods=['GET', 'POST'])
def get_ensemble():
    if request.method == 'POST':
        query = request.json["query"]
        zipcode = request.json["zipcode"]
        return jsonify(ensemble(llm,ensemble_retriever, query,zipcode))
    
@app.route("/chat-data", methods=['POST'])
def get_chat_data():
    if request.method == 'POST':
        meta = request.json["meta"]
        rag_output = rag(llm,meta['items'], meta['query'])
        # print(rag_output)
        lines = rag_output.split('\n')
        # print(lines)
        
        chat_data = [
            {"text": "Here's more about your results", "type": "bot"}            
        ]
        for line in lines:
            chat_data.append({"text": line, "type": "user"})
        # Return the chat data as JSON
        return jsonify({"messages": chat_data})
    
    
if __name__ == '__main__':
    app.run(debug=True)