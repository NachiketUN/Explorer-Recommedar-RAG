from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        print(query)
        print(latitude)
        print(longitude)
        return retrieval_info(query,latitude,longitude)   
    return render_template('search.html')

@app.route('/search/', methods=['GET', 'POST'])
def get_restaurant_info(restaurant_id):
    if request.method == 'POST':
        return recommender_info(restaurant_id)  
    return render_template('restaurant.html')
    
if __name__ == '__main__':
    app.run(debug=True)