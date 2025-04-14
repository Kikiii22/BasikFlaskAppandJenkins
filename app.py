from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row  # To work with results as dictionaries
    return conn

# Home page showing all books
@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)


# Add a new book
@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    publication_year = request.form['publication_year']

    conn = get_db_connection()
    conn.execute('INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)',
                 (title, author, publication_year))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


# Edit an existing book
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    conn = get_db_connection()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']

        conn.execute('UPDATE books SET title = ?, author = ?, publication_year = ? WHERE id = ?',
                     (title, author, publication_year, book_id))
        conn.commit()
        return redirect(url_for('index'))

    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    return render_template('edit.html', book=book)


# Delete a book
@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':

    app.run(debug=True)
