from flask import Flask, request, render_template
from main import *

app = Flask(__name__)
#Restaurant document data
data = pd.read_pickle('restaurent_docs.pickle')
#comverting the docs into lists for BM25 
documents = data['doc_information'].to_list()
tokenized_docs = [doc.split(" ") for doc in documents]
bm25 = BM25Okapi(tokenized_docs)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        print(query)
        print(latitude)
        print(longitude)
        return retrieval_info(data,bm25, query,float(latitude),float(longitude))  
    return render_template('index.html')

@app.route('/search/', methods=['GET', 'POST'])
def get_restaurant_info(restaurant_id):
    if request.method == 'POST':
        return recommender_info(data, restaurant_id)  
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)