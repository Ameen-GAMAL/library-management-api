from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
import json
import os

app = Flask(__name__)


# Path to data storage
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

# Load data from JSON file or create empty list if doesn't exist
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        books = json.load(f)
else:
    books = []

@app.route('/swagger/swagger.yaml')
def swagger_spec():
    return send_from_directory(os.path.join(app.root_path, 'swagger'), 'swagger.yaml')

SWAGGER_URL = '/api-docs'
API_URL = '/swagger/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Library Management API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


### Helper Functions ###
def save_data():
    """Save the current 'books' list to the data.json file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(books, f, indent=2)

def find_book_by_isbn(isbn):
    """Find a book in the 'books' list by its ISBN."""
    for book in books:
        if book['isbn'] == isbn:
            return book
    return None


### Routes ###


@app.route('/')
def home():
    return "Welcome to the Library Management API!"


@app.route('/books', methods=['GET'])
def list_books():
    """
    List all books.
    Returns a JSON array of all book objects.
    """
    return jsonify(books)

@app.route('/addbooks', methods=['POST'])
def add_book():
    """
    Add a new book.
    Expects JSON body with title, author, published_year, isbn, and optional genre.
    """
    data = request.get_json()
    required_fields = ['title', 'author', 'published_year', 'isbn']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Check if ISBN already exists
    if find_book_by_isbn(data['isbn']):
        return jsonify({"error": "ISBN already exists"}), 400

    new_book = {
        "title": data['title'],
        "author": data['author'],
        "published_year": data['published_year'],
        "isbn": data['isbn'],
        "genre": data.get('genre', "")
    }
    books.append(new_book)
    save_data()
    return jsonify(new_book), 201

@app.route('/books/search', methods=['GET'])
def search_books():
    """
    Search books by author, published_year, or genre.
    Query parameters:
    - author=<string>
    - published_year=<int>
    - genre=<string>
    """
    author = request.args.get('author')
    published_year = request.args.get('published_year')
    genre = request.args.get('genre')

    filtered = books
    if author:
        filtered = [b for b in filtered if b['author'].lower() == author.lower()]
    if published_year:
        filtered = [b for b in filtered if str(b['published_year']) == published_year]
    if genre:
        filtered = [b for b in filtered if b['genre'].lower() == genre.lower()]

    return jsonify(filtered), 200

@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    """
    Delete a book by ISBN.
    """
    global books
    book = find_book_by_isbn(isbn)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    # Rebuild the book list without the deleted book
    books = [b for b in books if b['isbn'] != isbn]
    save_data()
    return jsonify({"message": "Book deleted successfully"}), 200

@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    """
    Update a book by ISBN.
    Request body can include any subset of fields: title, author, published_year, genre.
    """
    book = find_book_by_isbn(isbn)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()

    # Update only provided fields
    if 'title' in data: book['title'] = data['title']
    if 'author' in data: book['author'] = data['author']
    if 'published_year' in data: book['published_year'] = data['published_year']
    if 'genre' in data: book['genre'] = data['genre']

    save_data()
    return jsonify(book), 200


if __name__ == "__main__":
    # Running locally for testing
    app.run(host='0.0.0.0', port=5000, debug=True)
