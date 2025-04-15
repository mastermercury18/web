import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    characters = conn.execute('SELECT c_id, c_name FROM characters').fetchall()
    conn.close()
    
    return render_template('characters.html', characters=characters)

@app.route('/character/<int:character_id>')
def character(character_id):
    conn = get_db_connection()
    character = conn.execute(
        'SELECT * FROM characters WHERE c_id = ?',
        (character_id,)
    ).fetchone()
    conn.close()
    
    return render_template('character.html', character=character)

@app.route('/character/<int:character_id>/update', methods=['GET', 'POST'])
def update_character(character_id):
    conn = get_db_connection()
    character = conn.execute('SELECT * FROM characters WHERE c_id = ?', (character_id,)).fetchone()

    if request.method == 'POST':
        new_name = request.form['c_name']
        conn.execute('UPDATE characters SET c_name = ? WHERE c_id = ?', (new_name, character_id))
        conn.commit()
        conn.close()
        return redirect(url_for('character', character_id=character_id))

    conn.close()
    return render_template('update_character.html', character=character)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)