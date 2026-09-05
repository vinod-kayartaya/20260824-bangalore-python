from flask import Flask, render_template, request, redirect, url_for
import sqlite3

dbfilename = 'books.sqlite'
app = Flask('My book manager webapp')

sql_cmd = '''
CREATE TABLE BOOKS(
ID INTEGER PRIMARY KEY AUTOINCREMENT,
TITLE VARCHAR(100) NOT NULL,
AUTHOR VARCHAR(100) NOT NULL,
PRICE DOUBLE NOT NULL)
'''


def init_db():
    try:
        with sqlite3.connect(dbfilename) as conn:
            conn.execute(sql_cmd)
    except:
        # table may already exist; just ignore
        pass
        


@app.route('/view-all')
def view_all_books():

    with sqlite3.connect(dbfilename) as conn:
        cur = conn.cursor()
        cur.execute('SELECT ID,TITLE,AUTHOR,PRICE FROM BOOKS')
        data = cur.fetchall() # list of tuple

        data = [
            dict(id=d[0], title=d[1], author=d[2], price=d[3])
            for d in data
        ]
     
    return render_template('view-all-books.html', books=data)


@app.route('/add-new')
def add_a_book():
    return render_template('add-book.html')


@app.route('/add-new-book', methods=['POST'])
def add_new_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    price = request.form.get("price", "").strip()
    try:
        price = float(price)
    except:
        price = 0

    insert_cmd = 'INSERT INTO BOOKS(TITLE, AUTHOR, PRICE) VALUES (?, ?, ?)'
    with sqlite3.connect(dbfilename) as conn:
        cur = conn.cursor()
        cur.execute(insert_cmd, (title, author, price))
        conn.commit()

    # this is wrong!
    # each POST request should be IDEMPOTENT
    # return render_template('add-book.html')

    # correct method: ask the browser to visit a different url
    return redirect(url_for('add_a_book'))


@app.route('/delete-book')
def delete_book():
    book_id = int(request.args.get('id'))
    delete_cmd = 'DELETE FROM BOOKS WHERE ID=?'
    with sqlite3.connect(dbfilename) as conn:
        cur = conn.cursor()
        cur.execute(delete_cmd, (book_id, ))
        conn.commit()

    return redirect(url_for('view_all_books'))

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    init_db()
    app.run(port=5000, host='0.0.0.0', debug=True)
