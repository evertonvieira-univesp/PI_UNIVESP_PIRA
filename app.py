import os
import psycopg2
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = '999888777666'


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='PIUNIVESP2022',
                            user='admin',
                            password='123')
    return conn


def get_post(post_id):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM "PIUNIVESP2022.public.posts" WHERE post_id = id').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    conn = get_db_connection()
    with conn:
        with conn.cursor() as curs:
            curs.execute('SELECT * FROM "resultados"')
    return render_template('index.html', Resultados=curs)


@app.route('/db')
def db_process():
    conn = get_db_connection()
    sl_db2 = conn.execute('SELECT * FROM "PIUNIVESP2022.public.posts.contato"').fetchall()
    conn.close()
    return render_template('db_process.html', contato=sl_db2)


@app.route('/ftr')
def filter():
    conn = get_db_connection()
    sl_db3 = conn.execute('SELECT * FROM Res_filtro').fetchall()
    conn.close()
    return render_template('filter.html', Res_filtro=sl_db3)


@app.route('/sobre')
def sobreNos():
    return render_template('sobre.html')


@app.route('/aprofundando')
def aprofundando():
    return render_template('aprofundando.html')


@app.route('/<int:id>')
def post(id):
    post = get_post(post_id)
    return render_template('post.html', post=post)
