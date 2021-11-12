import sqlite3

from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def db_process():
    conn = get_db_connection()
    sl_db=conn.execute(POSTS.query.count())
    conn.close()
    return (sl_db)