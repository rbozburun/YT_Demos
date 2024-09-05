from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps  # Import dumps from bson.json_util

app = Flask(__name__)

# Connect to MongoDB (assumes MongoDB is running in a Docker container with default settings)
client = MongoClient('mongodb://mongo:27017/')
db = client['testdb']
books_collection = db['books']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books', methods=['POST'])
def books():
    category = request.form.get('category', '')
    # Vulnerable query - MongoDB injection possible
    query = {'category': category}
    books_cursor = books_collection.find(query)

    # Convert the cursor to a list of dictionaries and serialize to JSON
    books_list = list(books_cursor)
    for book in books_list:
        book['_id'] = str(book['_id'])  # Convert ObjectId to string

    return jsonify(books_list)

@app.route('/populate', methods=['POST'])
def populate():
    # Sample data to insert
    books = [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classic"},
        {"title": "1984", "author": "George Orwell", "category": "Dystopian"},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Classic"},
        {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "Classic"},
        {"title": "Brave New World", "author": "Aldous Huxley", "category": "Dystopian"}
    ]
    books_collection.insert_many(books)
    return jsonify({"message": "Books inserted successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
