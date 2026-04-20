from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'bu-flower-secret-key-2026'

DATABASE = os.path.join(os.getcwd(), 'flowers_store.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    flowers = db.execute('SELECT f.*, c.name as category_name FROM Flowers f JOIN Categories c ON f.category_id = c.id WHERE f.is_available = 1').fetchall()
    return render_template('index.html', flowers=flowers, page='home')

@app.route('/categories')
def categories():
    db = get_db()
    categories = db.execute('SELECT * FROM Categories').fetchall()
    return render_template('index.html', categories=categories, page='categories')

@app.route('/flowers')
def flowers():
    db = get_db()
    flowers = db.execute('SELECT f.*, c.name as category_name FROM Flowers f JOIN Categories c ON f.category_id = c.id').fetchall()
    return render_template('index.html', flowers=flowers, page='flowers')

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db = get_db()
        db.execute('INSERT INTO Categories (name, description) VALUES (?, ?)', (name, description))
        db.commit()
        flash('เพิ่มหมวดหมู่เรียบร้อยแล้ว')
        return redirect(url_for('categories'))
    return render_template('index.html', page='add_category')

@app.route('/add_flower', methods=['GET', 'POST'])
def add_flower():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        category_id = int(request.form['category_id'])
        is_available = 1 if request.form.get('is_available') else 0
        created_at = '2026-04-20'
        db = get_db()
        db.execute('INSERT INTO Flowers (name, price, quantity, category_id, is_available, created_at) VALUES (?, ?, ?, ?, ?, ?)', (name, price, quantity, category_id, is_available, created_at))
        db.commit()
        flash('เพิ่มสินค้าเรียบร้อยแล้ว')
        return redirect(url_for('flowers'))
    db = get_db()
    categories = db.execute('SELECT * FROM Categories').fetchall()
    return render_template('index.html', categories=categories, page='add_flower')

@app.route('/edit_category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        db.execute('UPDATE Categories SET name = ?, description = ? WHERE id = ?', (name, description, id))
        db.commit()
        flash('แก้ไขหมวดหมู่เรียบร้อยแล้ว')
        return redirect(url_for('categories'))
    category = db.execute('SELECT * FROM Categories WHERE id = ?', (id,)).fetchone()
    return render_template('index.html', category=category, page='edit_category')

@app.route('/edit_flower/<int:id>', methods=['GET', 'POST'])
def edit_flower(id):
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        category_id = int(request.form['category_id'])
        is_available = 1 if request.form.get('is_available') else 0
        db.execute('UPDATE Flowers SET name = ?, price = ?, quantity = ?, category_id = ?, is_available = ? WHERE id = ?', (name, price, quantity, category_id, is_available, id))
        db.commit()
        flash('แก้ไขสินค้าเรียบร้อยแล้ว')
        return redirect(url_for('flowers'))
    flower = db.execute('SELECT * FROM Flowers WHERE id = ?', (id,)).fetchone()
    categories = db.execute('SELECT * FROM Categories').fetchall()
    return render_template('index.html', flower=flower, categories=categories, page='edit_flower')

@app.route('/delete_category/<int:id>')
def delete_category(id):
    db = get_db()
    db.execute('DELETE FROM Categories WHERE id = ?', (id,))
    db.commit()
    flash('ลบหมวดหมู่เรียบร้อยแล้ว')
    return redirect(url_for('categories'))

@app.route('/delete_flower/<int:id>')
def delete_flower(id):
    db = get_db()
    db.execute('DELETE FROM Flowers WHERE id = ?', (id,))
    db.commit()
    flash('ลบสินค้าเรียบร้อยแล้ว')
    return redirect(url_for('flowers'))

if __name__ == '__main__':
    app.run(debug=True)