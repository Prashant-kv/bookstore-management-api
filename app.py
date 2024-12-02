
from flask import Flask , request, jsonify
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn        

@app.route('/books', methods=['GET', 'POST'])
def hello_world():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM book")
        books=[
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']  
        new_title = request.form['title']
        cursor = cursor.execute("INSERT INTO book (author, language, title) VALUES (?, ?, ?)", (new_author, new_lang, new_title))
        conn.commit()
        return f"Book with id: {cursor.lastrowid} created successfully"


@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id =?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
            if book is not None:
                return jsonify(book), 200
            else:
                return "Something went wrong", 404

    if request.method == 'PUT':
    
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        update_book={
                    'id': id,
                    'author': author,
                    'language': language,
                    'title': title
                }
        cursor.execute("UPDATE book SET author=?, language=?, title=? WHERE id = ?", (author, language, title, id))
        conn.commit()
        return jsonify(update_book)

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM book WHERE id = ?", (id,))
        conn.commit()
        return "The book with id: {} has been deleted".format(id), 200


if __name__ == '__main__':
    app.run(debug=True)