from flask import Blueprint, request, jsonify, session
from models.disciplina import Disciplina

disciplina_bp = Blueprint('disciplina', __name__)
disciplina_model = Disciplina()

def requer_login():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Nao autenticado'}), 401
    return None

def disciplina_pertence_ao_usuario(id_disciplina, id_usuario):
    disciplina = disciplina_model.buscar_por_id(id_disciplina)
    if not disciplina:
        return None
    if disciplina['id_usuario'] != id_usuario:
        return False
    return disciplina

@disciplina_bp.route('/disciplinas', methods=['GET'])
def listar():
    erro = requer_login()
    if erro: return erro
    disciplinas = disciplina_model.listar_por_usuario(session['id_usuario'])
    return jsonify(disciplinas)

@disciplina_bp.route('/disciplinas', methods=['POST'])
def criar():
    erro = requer_login()
    if erro: return erro
    dados = request.json
    if not dados.get('nome'):
        return jsonify({'erro': 'Nome obrigatorio'}), 400
    id_disc = disciplina_model.criar(dados['nome'], dados.get('descricao'), session['id_usuario'])
    return jsonify({'mensagem': 'Disciplina criada', 'id_disciplina': id_disc}), 201

@disciplina_bp.route('/disciplinas/<int:id_disciplina>', methods=['GET'])
def buscar(id_disciplina):
    erro = requer_login()
    if erro: return erro
    disc = disciplina_pertence_ao_usuario(id_disciplina, session['id_usuario'])
    if disc is None:
        return jsonify({'erro': 'Disciplina nao encontrada'}), 404
    if disc is False:
        return jsonify({'erro': 'Acesso negado'}), 403
    return jsonify(disc)

@disciplina_bp.route('/disciplinas/<int:id_disciplina>', methods=['PUT'])
def atualizar(id_disciplina):
    erro = requer_login()
    if erro: return erro
    disc = disciplina_pertence_ao_usuario(id_disciplina, session['id_usuario'])
    if disc is None:
        return jsonify({'erro': 'Disciplina nao encontrada'}), 404
    if disc is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    dados = request.json
    if not dados.get('nome'):
        return jsonify({'erro': 'Nome obrigatorio'}), 400

    disciplina_model.atualizar(id_disciplina, dados['nome'], dados.get('descricao'))
    return jsonify({'mensagem': 'Disciplina atualizada'})

@disciplina_bp.route('/disciplinas/<int:id_disciplina>', methods=['DELETE'])
def deletar(id_disciplina):
    erro = requer_login()
    if erro: return erro
    disc = disciplina_pertence_ao_usuario(id_disciplina, session['id_usuario'])
    if disc is None:
        return jsonify({'erro': 'Disciplina nao encontrada'}), 404
    if disc is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    disciplina_model.deletar(id_disciplina)
    return jsonify({'mensagem': 'Disciplina removida'})
