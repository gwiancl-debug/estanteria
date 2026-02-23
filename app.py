from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('estanteria.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  titulo TEXT,
                  tipo TEXT,
                  rating INTEGER,
                  nota TEXT,
                  portada TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('estanteria.db')
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/agregar', methods=['POST'])
def agregar():
    titulo = request.form['titulo']
    tipo = request.form['tipo']
    rating = request.form['rating']
    nota = request.form['nota']
    portada = request.form['portada']
    conn = sqlite3.connect('estanteria.db')
    c = conn.cursor()
    c.execute('INSERT INTO items (titulo, tipo, rating, nota, portada) VALUES (?,?,?,?,?)',
              (titulo, tipo, rating, nota, portada))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/editar', methods=['POST'])
def editar():
    data = request.get_json()
    conn = sqlite3.connect('estanteria.db')
    c = conn.cursor()
    c.execute('UPDATE items SET rating=?, nota=?, portada=? WHERE id=?',
              (data['rating'], data['nota'], data['portada'], data['id']))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/eliminar', methods=['POST'])
def eliminar():
    data = request.get_json()
    conn = sqlite3.connect('estanteria.db')
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id=?', (data['id'],))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)