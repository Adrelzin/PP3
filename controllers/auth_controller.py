from flask import Blueprint, request, jsonify, session
from models.usuario import Usuario
from validacoes import email_valido, senha_valida, TIPOS_USUARIO_VALIDOS
from werkzeug.utils import secure_filename
import hashlib
import os

auth_bp = Blueprint('auth', __name__)
usuario_model = Usuario()

TIPOS_FOTO_VALIDOS = ['png', 'jpg', 'jpeg']
PASTA_UPLOADS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def extensao_do_arquivo(nome_arquivo):
    if '.' not in nome_arquivo:
        return ''
    return nome_arquivo.rsplit('.', 1)[1].lower()

def salvar_foto_perfil(arquivo, id_usuario):
    extensao = extensao_do_arquivo(arquivo.filename)
    if extensao not in TIPOS_FOTO_VALIDOS:
        return None, f'Foto deve ser um dos tipos: {TIPOS_FOTO_VALIDOS}'

    nome_seguro = secure_filename(arquivo.filename)
    pasta_usuario = os.path.join(PASTA_UPLOADS, 'perfil', f'usuario_{id_usuario}')
    os.makedirs(pasta_usuario, exist_ok=True)

    caminho_completo = os.path.join(pasta_usuario, nome_seguro)
    arquivo.save(caminho_completo)
    caminho_relativo = f'/uploads/perfil/usuario_{id_usuario}/{nome_seguro}'
    return caminho_relativo, None

@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    dados = request.form
    campos = ['nome', 'email', 'senha', 'tipo_usuario']
    for campo in campos:
        if not dados.get(campo):
            return jsonify({'erro': f'Campo {campo} obrigatorio'}), 400

    if not email_valido(dados['email']):
        return jsonify({'erro': 'Email invalido'}), 400

    if not senha_valida(dados['senha']):
        return jsonify({'erro': 'Senha deve ter no minimo 6 caracteres'}), 400

    if dados['tipo_usuario'] not in TIPOS_USUARIO_VALIDOS:
        return jsonify({'erro': f'Tipo de usuario deve ser um de: {TIPOS_USUARIO_VALIDOS}'}), 400

    if usuario_model.buscar_por_email(dados['email']):
        return jsonify({'erro': 'Email ja cadastrado'}), 409

    id_usuario = usuario_model.criar(
        dados['nome'],
        dados['email'],
        hash_senha(dados['senha']),
        dados['tipo_usuario'],
        None
    )

    if 'foto_perfil' in request.files and request.files['foto_perfil'].filename != '':
        caminho_foto, erro_foto = salvar_foto_perfil(request.files['foto_perfil'], id_usuario)
        if erro_foto:
            return jsonify({'erro': erro_foto}), 400
        usuario_model.atualizar(id_usuario, dados['nome'], dados['email'], caminho_foto)

    return jsonify({'mensagem': 'Usuario criado com sucesso', 'id_usuario': id_usuario}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    dados = request.json
    if not dados.get('email') or not dados.get('senha'):
        return jsonify({'erro': 'Email e senha obrigatorios'}), 400

    usuario = usuario_model.buscar_por_email(dados['email'])
    if not usuario or usuario['senha'] != hash_senha(dados['senha']):
        return jsonify({'erro': 'Email ou senha incorretos'}), 401

    session['id_usuario'] = usuario['id_usuario']
    session['nome'] = usuario['nome']
    session['tipo_usuario'] = usuario['tipo_usuario']

    return jsonify({
        'mensagem': 'Login realizado com sucesso',
        'usuario': {
            'id_usuario': usuario['id_usuario'],
            'nome': usuario['nome'],
            'email': usuario['email'],
            'tipo_usuario': usuario['tipo_usuario'],
            'foto_perfil': usuario.get('foto_perfil')
        }
    })

@auth_bp.route('/logout', methods=['POST'])
def logout():
    havia_sessao = 'id_usuario' in session
    session.clear()
    if not havia_sessao:
        return jsonify({'mensagem': 'Nenhuma sessao ativa para encerrar'}), 200
    return jsonify({'mensagem': 'Logout realizado'}), 200

@auth_bp.route('/perfil', methods=['GET'])
def perfil():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Nao autenticado'}), 401
    usuario = usuario_model.buscar_por_id(session['id_usuario'])
    usuario.pop('senha', None)
    return jsonify(usuario)

@auth_bp.route('/perfil/foto', methods=['POST'])
def atualizar_foto():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Nao autenticado'}), 401

    if 'foto_perfil' not in request.files or request.files['foto_perfil'].filename == '':
        return jsonify({'erro': 'Nenhuma foto enviada'}), 400

    caminho_foto, erro_foto = salvar_foto_perfil(request.files['foto_perfil'], session['id_usuario'])
    if erro_foto:
        return jsonify({'erro': erro_foto}), 400

    usuario = usuario_model.buscar_por_id(session['id_usuario'])
    usuario_model.atualizar(session['id_usuario'], usuario['nome'], usuario['email'], caminho_foto)
    return jsonify({'mensagem': 'Foto de perfil atualizada', 'foto_perfil': caminho_foto})