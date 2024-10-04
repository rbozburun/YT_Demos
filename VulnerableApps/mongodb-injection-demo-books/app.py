from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps  # Import dumps from bson.json_util
import json

app = Flask(__name__)

# Connect to MongoDB (assumes MongoDB is running in a Docker container with default settings)
client = MongoClient('mongodb://mongo:27017/')
db = client['testdb']
books_collection = db['books']
# Added for gitleaks
base64_secret = 'KanalaAboneOlun-Secret!'

@app.route('/')
def index():
    return render_template('index.html')


## ATTACK:
""" {"category":{"$ne":""}} """
@app.route('/books', methods=['POST'])
def books():
    data = request.get_json()
    print(f"Query:  {data}")

    # Perform the query
    try:
        books_cursor = books_collection.find(data)
    except Exception as e:
        # Log and return an error if the query fails
        print(f"Error querying MongoDB: {e}")
        return jsonify({'error': 'Invalid query'}), 400

    # Convert the cursor to a list of dictionaries and serialize to JSON
    books_list = list(books_cursor)
    for book in books_list:
        book['_id'] = str(book['_id'])  # Convert ObjectId to string

    return jsonify(books_list)

@app.route('/populate', methods=['POST'])
def populate():
    # Sample data to insert
    books = [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "classic"},
        {"title": "1984", "author": "George Orwell", "category": "dystopian"},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "classic"},
        {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "classic"},
        {"title": "This is fiction", "author": "J.D. Salinger", "category": "fiction"},
        {"title": "Brave New World", "author": "Aldous Huxley", "category": "dystopian"}
    ]
    books_collection.insert_many(books)
    return jsonify({"message": "Books inserted successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
