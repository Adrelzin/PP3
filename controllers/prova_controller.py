from flask import Blueprint, request, jsonify, session
from models.prova import Prova
from models.disciplina import Disciplina
from validacoes import data_valida

prova_bp = Blueprint('prova', __name__)
prova_model = Prova()
disciplina_model = Disciplina()

def requer_login():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Nao autenticado'}), 401
    return None

def prova_pertence_ao_usuario(id_prova, id_usuario):
    prova = prova_model.buscar_por_id(id_prova)
    if not prova:
        return None
    disciplina = disciplina_model.buscar_por_id(prova['id_disciplina'])
    if not disciplina or disciplina['id_usuario'] != id_usuario:
        return False
    return prova

@prova_bp.route('/provas', methods=['GET'])
def listar():
    erro = requer_login()
    if erro: return erro
    return jsonify(prova_model.listar_por_usuario(session['id_usuario']))

@prova_bp.route('/provas', methods=['POST'])
def criar():
    erro = requer_login()
    if erro: return erro
    dados = request.json
    for campo in ['nome', 'data_prova', 'id_disciplina']:
        if not dados.get(campo):
            return jsonify({'erro': f'Campo {campo} obrigatorio'}), 400

    disciplina = disciplina_model.buscar_por_id(dados['id_disciplina'])
    if not disciplina or disciplina['id_usuario'] != session['id_usuario']:
        return jsonify({'erro': 'Disciplina invalida'}), 403

    if not data_valida(dados['data_prova']):
        return jsonify({'erro': 'Data da prova invalida, use AAAA-MM-DD'}), 400

    id_p = prova_model.criar(dados['nome'], dados.get('descricao'), dados['data_prova'], dados['id_disciplina'])
    return jsonify({'mensagem': 'Prova criada', 'id_prova': id_p}), 201

@prova_bp.route('/provas/<int:id_prova>', methods=['PUT'])
def atualizar(id_prova):
    erro = requer_login()
    if erro: return erro
    prova = prova_pertence_ao_usuario(id_prova, session['id_usuario'])
    if prova is None:
        return jsonify({'erro': 'Prova nao encontrada'}), 404
    if prova is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    dados = request.json
    for campo in ['nome', 'data_prova']:
        if not dados.get(campo):
            return jsonify({'erro': f'Campo {campo} obrigatorio'}), 400

    if not data_valida(dados['data_prova']):
        return jsonify({'erro': 'Data da prova invalida, use AAAA-MM-DD'}), 400

    prova_model.atualizar(id_prova, dados['nome'], dados.get('descricao'), dados['data_prova'])
    return jsonify({'mensagem': 'Prova atualizada'})

@prova_bp.route('/provas/<int:id_prova>', methods=['DELETE'])
def deletar(id_prova):
    erro = requer_login()
    if erro: return erro
    prova = prova_pertence_ao_usuario(id_prova, session['id_usuario'])
    if prova is None:
        return jsonify({'erro': 'Prova nao encontrada'}), 404
    if prova is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    prova_model.deletar(id_prova)
    return jsonify({'mensagem': 'Prova removida'})
