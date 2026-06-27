from flask import Flask, request, redirect, send_from_directory
from database import close_db
import webbrowser
import threading
import os

from controllers.auth_controller import auth_bp
from controllers.disciplina_controller import disciplina_bp
from controllers.tarefa_controller import tarefa_bp
from controllers.prova_controller import prova_bp
from controllers.meta_controller import meta_bp
from controllers.horario_controller import horario_bp
from controllers.notificacao_controller import notificacao_bp
from controllers.documento_controller import documento_bp

app = Flask(__name__)
app.secret_key = 'pp3_chave_secreta_trocar_depois'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

PASTA_UPLOADS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    return response

@app.route('/api/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    return '', 200

@app.route('/')
def home():
    return redirect('/static/painel_teste.html')

@app.route('/uploads/<path:caminho>')
def servir_upload(caminho):
    return send_from_directory(PASTA_UPLOADS, caminho)

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(disciplina_bp, url_prefix='/api')
app.register_blueprint(tarefa_bp, url_prefix='/api')
app.register_blueprint(prova_bp, url_prefix='/api')
app.register_blueprint(meta_bp, url_prefix='/api')
app.register_blueprint(horario_bp, url_prefix='/api')
app.register_blueprint(notificacao_bp, url_prefix='/api')
app.register_blueprint(documento_bp, url_prefix='/api')

app.teardown_appcontext(close_db)

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        threading.Timer(1.0, lambda: webbrowser.open('http://localhost:5000/')).start()
    app.run(debug=True)