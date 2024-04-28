from flask import Flask, request, jsonify, render_template
from main import *
from llm_functions import summary
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

#Restaurant document data
data = pd.read_pickle('restaurent_docs_1.pickle')
recommender_data = pd.read_pickle('recommendation_1.pickle')
#comverting the docs into lists for BM25 
documents = data['doc_information'].to_list()
tokenized_docs = [doc.split(" ") for doc in documents]
bm25 = BM25Okapi(tokenized_docs)
global api_key 
api_key = os.environ["OPENAI_API_KEY"]
llm = ChatOpenAI(openai_api_key=api_key, temperature=0, model_name="gpt-3.5-turbo-1106")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.json["query"]
        zipcode = request.json["zipcode"]
        return jsonify(retrieval_info(data, bm25, query,zipcode))

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
    
    
if __name__ == '__main__':
    app.run(debug=True)