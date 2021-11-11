import sqlite3

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort



def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory=sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = '999888777666'


@app.route('/')
def index():
    conn = get_db_connection()
    p = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=p)


@app.route('/db')
def db_process():
    conn = get_db_connection()
    sel_db = conn.execute('SELECT count(*) FROM posts WHERE content.distinct ').fetchall()

    conn.close()


    return render_template('db_process.html', posts = sel_db)


@app.route('/testePI')
def teste():
    return render_template('testePI.html')

@app.route('/sobre')
def sobreNos():
    return render_template('sobre.html')

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            flash('Por favor preencha os campos!')

        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            flash('Por favor preencha os campos para editar!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" foi deletado com sucesso!'.format(post['title']))
    return redirect(url_for('index'))
