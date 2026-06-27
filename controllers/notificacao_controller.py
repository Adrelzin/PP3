from flask import Blueprint, request, jsonify, session
from models.notificacao import Notificacao

notificacao_bp = Blueprint('notificacao', __name__)
notificacao_model = Notificacao()

def requer_login():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Nao autenticado'}), 401
    return None

def notificacao_pertence_ao_usuario(id_notificacao, id_usuario):
    db_lista = notificacao_model.listar_por_usuario(id_usuario)
    for n in db_lista:
        if n['id_notificacao'] == id_notificacao:
            return n
    return None

@notificacao_bp.route('/notificacoes', methods=['GET'])
def listar():
    erro = requer_login()
    if erro: return erro
    return jsonify(notificacao_model.listar_por_usuario(session['id_usuario']))

@notificacao_bp.route('/notificacoes/nao-lidas', methods=['GET'])
def listar_nao_lidas():
    erro = requer_login()
    if erro: return erro
    todas = notificacao_model.listar_por_usuario(session['id_usuario'])
    nao_lidas = [n for n in todas if n['status'] == 'nao_lida']
    return jsonify(nao_lidas)

@notificacao_bp.route('/notificacoes/<int:id_notificacao>/lida', methods=['PATCH'])
def marcar_lida(id_notificacao):
    erro = requer_login()
    if erro: return erro
    if not notificacao_pertence_ao_usuario(id_notificacao, session['id_usuario']):
        return jsonify({'erro': 'Notificacao nao encontrada ou acesso negado'}), 404
    notificacao_model.marcar_como_lida(id_notificacao)
    return jsonify({'mensagem': 'Notificacao marcada como lida'})

@notificacao_bp.route('/notificacoes/<int:id_notificacao>', methods=['DELETE'])
def deletar(id_notificacao):
    erro = requer_login()
    if erro: return erro
    if not notificacao_pertence_ao_usuario(id_notificacao, session['id_usuario']):
        return jsonify({'erro': 'Notificacao nao encontrada ou acesso negado'}), 404
    notificacao_model.deletar(id_notificacao)
    return jsonify({'mensagem': 'Notificacao removida'})