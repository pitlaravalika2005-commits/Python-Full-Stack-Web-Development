from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database table
def init_db():
    conn = sqlite3.connect('database.db')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Home page
@app.route('/', methods=['GET', 'POST'])
def index():

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    # Add user
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']

        conn.execute(
            'INSERT INTO users (name, email) VALUES (?, ?)',
            (name, email)
        )

        conn.commit()

        return redirect('/')

    # Fetch users
    users = conn.execute(
        'SELECT * FROM users'
    ).fetchall()

    conn.close()

    return render_template(
        'index.html',
        users=users
    )

# Run app
if __name__ == '__main__':

    init_db()

    app.run(debug=True)