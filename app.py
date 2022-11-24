from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import pandas as pd
import numpy as np
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678'

#Configuração de conexão PostgreSQL
engine = create_engine("postgresql://gnggejexlutedp:f3417af94cbd82be2a689b33e4104c5466509659ccf1dbf359ca59164594fba6@ec2-54-160-200-167.compute-1.amazonaws.com:5432/dc24uh2ha4lenk")
db = scoped_session(sessionmaker(bind=engine))
app.secret_key = '123456789'
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"



#Página inicial
@app.route('/')
def index():
    geo = db.execute('select json_build_array(geo_lat::numeric,geo_long::numeric,id,contato,data) from posts_geo').fetchall()
    db.close()
    return render_template('index.html', Geo_pontos=geo)


#Página de informação do grupo#
@app.route('/sobre')
def sobreNos():
    return render_template('sobre.html')


#Página de aprofundamento do tema
@app.route('/aprofundando')
def aprofundando():
    return render_template('aprofundando.html')


#Criação de postagens
@app.route('/create', methods=('GET', 'POST'))
def create():
    erro = None
    if request.method == 'POST':
        contato = request.form.get('contato')
        geo = request.form.get('geo')
        data = request.form.get('data')
        if contato == ''or geo =='None':
            #return render_template('create.html')
            erro = 'Erro no preenchimento ou validação da sua localização.'

        else:
            db.execute("INSERT INTO posts (contato,geo) VALUES (:contato, :geo)" , {"contato": contato, "geo": geo})
            db.commit()
            return redirect(url_for('index'))
    return render_template('create.html',erro=erro)

#Report page
@app.route('/report')
def report():
    getData = db.execute('select geo_lat, geo_long, contato, data from posts_geo').fetchall()
    getData = [{'Latitude':col1, 'Longitude': col2, 'Descrição': col3, 'Data': col4} for (col1, col2, col3, col4) in getData]
    getData = pd.DataFrame(getData);
    chartData = getData['Descrição'];
    chartData = chartData.value_counts();
    chartDataValue = chartData.values.tolist();
    chartDataValuePerc = (chartData.values/chartData.values.sum())*100;
    chartDataValuePerc = chartDataValuePerc.round(1);
    chartDataValuePerc = chartDataValuePerc.tolist();
    chartDataDesc = chartData.index.tolist();
    return render_template('report.html', table=getData.to_html(index=False, classes="table table-striped table-bordered ", table_id="sortTable" ), chartDataValue=chartDataValue, chartDataValuePerc=chartDataValuePerc, chartDataDesc=chartDataDesc, titles='Relatório dos pontos submetidos:')
