from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['testdb']
books_collection = db['books']

# Sample data to insert
books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classic"},
    {"title": "1984", "author": "George Orwell", "category": "Dystopian"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Classic"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "Classic"},
    {"title": "Brave New World", "author": "Aldous Huxley", "category": "Dystopian"}
]

# Insert data into the collection
books_collection.insert_many(books)

print("Books inserted successfully.")
