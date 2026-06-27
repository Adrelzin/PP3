from flask import Blueprint, request, jsonify, session
from models.meta_estudo import MetaEstudo
from validacoes import data_valida, progresso_valido

meta_bp = Blueprint('meta', __name__)
meta_model = MetaEstudo()

def requer_login():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Nao autenticado'}), 401
    return None

def meta_pertence_ao_usuario(id_meta, id_usuario):
    meta = meta_model.buscar_por_id(id_meta)
    if not meta:
        return None
    if meta['id_usuario'] != id_usuario:
        return False
    return meta

@meta_bp.route('/metas', methods=['GET'])
def listar():
    erro = requer_login()
    if erro: return erro
    return jsonify(meta_model.listar_por_usuario(session['id_usuario']))

@meta_bp.route('/metas', methods=['POST'])
def criar():
    erro = requer_login()
    if erro: return erro
    dados = request.json
    for campo in ['descricao', 'prazo']:
        if not dados.get(campo):
            return jsonify({'erro': f'Campo {campo} obrigatorio'}), 400

    if not data_valida(dados['prazo']):
        return jsonify({'erro': 'Prazo invalido, use AAAA-MM-DD'}), 400

    progresso = dados.get('progresso', 0)
    if not progresso_valido(progresso):
        return jsonify({'erro': 'Progresso deve ser um numero entre 0 e 100'}), 400

    id_m = meta_model.criar(dados['descricao'], dados['prazo'], session['id_usuario'], progresso)
    return jsonify({'mensagem': 'Meta criada', 'id_meta': id_m}), 201

@meta_bp.route('/metas/<int:id_meta>', methods=['PUT'])
def atualizar(id_meta):
    erro = requer_login()
    if erro: return erro
    meta = meta_pertence_ao_usuario(id_meta, session['id_usuario'])
    if meta is None:
        return jsonify({'erro': 'Meta nao encontrada'}), 404
    if meta is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    dados = request.json
    for campo in ['descricao', 'prazo']:
        if not dados.get(campo):
            return jsonify({'erro': f'Campo {campo} obrigatorio'}), 400

    if not data_valida(dados['prazo']):
        return jsonify({'erro': 'Prazo invalido, use AAAA-MM-DD'}), 400

    progresso = dados.get('progresso', 0)
    if not progresso_valido(progresso):
        return jsonify({'erro': 'Progresso deve ser um numero entre 0 e 100'}), 400

    meta_model.atualizar(id_meta, dados['descricao'], dados['prazo'], progresso)
    return jsonify({'mensagem': 'Meta atualizada'})

@meta_bp.route('/metas/<int:id_meta>/progresso', methods=['PATCH'])
def atualizar_progresso(id_meta):
    erro = requer_login()
    if erro: return erro
    meta = meta_pertence_ao_usuario(id_meta, session['id_usuario'])
    if meta is None:
        return jsonify({'erro': 'Meta nao encontrada'}), 404
    if meta is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    dados = request.json
    if 'progresso' not in dados:
        return jsonify({'erro': 'Campo progresso obrigatorio'}), 400
    if not progresso_valido(dados['progresso']):
        return jsonify({'erro': 'Progresso deve ser um numero entre 0 e 100'}), 400

    meta_model.atualizar_progresso(id_meta, dados['progresso'])
    return jsonify({'mensagem': 'Progresso atualizado'})

@meta_bp.route('/metas/<int:id_meta>', methods=['DELETE'])
def deletar(id_meta):
    erro = requer_login()
    if erro: return erro
    meta = meta_pertence_ao_usuario(id_meta, session['id_usuario'])
    if meta is None:
        return jsonify({'erro': 'Meta nao encontrada'}), 404
    if meta is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    meta_model.deletar(id_meta)
    return jsonify({'mensagem': 'Meta removida'})
