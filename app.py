from flask import Flask, request, jsonify, render_template
from main import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#Restaurant document data
data = pd.read_pickle('restaurent_docs.pickle')
#comverting the docs into lists for BM25 
documents = data['doc_information'].to_list()
tokenized_docs = [doc.split(" ") for doc in documents]
bm25 = BM25Okapi(tokenized_docs)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.json["query"]
        zipcode = request.json["zipcode"]
        return jsonify(retrieval_info(data,bm25, query,zipcode))

@app.route('/search', methods=['POST'])
def get_restaurant_info():
    if request.method == 'POST':
        return jsonify(recommender_info(data,request.json["gmap_id"])) 
    
    
if __name__ == '__main__':
    app.run(debug=True)