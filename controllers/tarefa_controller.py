from flask import Blueprint, request, jsonify, session
from models.tarefa import Tarefa
from models.disciplina import Disciplina
from validacoes import data_valida, prioridade_valida, status_tarefa_valido, STATUS_TAREFA_VALIDOS, PRIORIDADES_VALIDAS

tarefa_bp = Blueprint('tarefa', __name__)
tarefa_model = Tarefa()
disciplina_model = Disciplina()

def requer_login():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Nao autenticado'}), 401
    return None

def tarefa_pertence_ao_usuario(id_tarefa, id_usuario):
    tarefa = tarefa_model.buscar_por_id(id_tarefa)
    if not tarefa:
        return None
    disciplina = disciplina_model.buscar_por_id(tarefa['id_disciplina'])
    if not disciplina or disciplina['id_usuario'] != id_usuario:
        return False
    return tarefa

@tarefa_bp.route('/tarefas', methods=['GET'])
def listar():
    erro = requer_login()
    if erro: return erro
    tarefas = tarefa_model.listar_por_usuario(session['id_usuario'])
    return jsonify(tarefas)

@tarefa_bp.route('/tarefas', methods=['POST'])
def criar():
    erro = requer_login()
    if erro: return erro
    dados = request.json
    campos = ['titulo', 'data_entrega', 'prioridade', 'id_disciplina']
    for campo in campos:
        if not dados.get(campo):
            return jsonify({'erro': f'Campo {campo} obrigatorio'}), 400

    disciplina = disciplina_model.buscar_por_id(dados['id_disciplina'])
    if not disciplina or disciplina['id_usuario'] != session['id_usuario']:
        return jsonify({'erro': 'Disciplina invalida'}), 403

    if not data_valida(dados['data_entrega']):
        return jsonify({'erro': 'Data de entrega invalida, use AAAA-MM-DD'}), 400

    if not prioridade_valida(dados['prioridade']):
        return jsonify({'erro': f'Prioridade deve ser uma de: {PRIORIDADES_VALIDAS}'}), 400

    id_t = tarefa_model.criar(
        dados['titulo'], dados.get('descricao'),
        dados['data_entrega'], dados['prioridade'], dados['id_disciplina']
    )
    return jsonify({'mensagem': 'Tarefa criada', 'id_tarefa': id_t}), 201

@tarefa_bp.route('/tarefas/<int:id_tarefa>', methods=['GET'])
def buscar(id_tarefa):
    erro = requer_login()
    if erro: return erro
    tarefa = tarefa_pertence_ao_usuario(id_tarefa, session['id_usuario'])
    if tarefa is None:
        return jsonify({'erro': 'Tarefa nao encontrada'}), 404
    if tarefa is False:
        return jsonify({'erro': 'Acesso negado'}), 403
    return jsonify(tarefa)

@tarefa_bp.route('/tarefas/<int:id_tarefa>', methods=['PUT'])
def atualizar(id_tarefa):
    erro = requer_login()
    if erro: return erro
    tarefa = tarefa_pertence_ao_usuario(id_tarefa, session['id_usuario'])
    if tarefa is None:
        return jsonify({'erro': 'Tarefa nao encontrada'}), 404
    if tarefa is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    dados = request.json
    campos = ['titulo', 'data_entrega', 'prioridade', 'status']
    for campo in campos:
        if not dados.get(campo):
            return jsonify({'erro': f'Campo {campo} obrigatorio'}), 400

    if not data_valida(dados['data_entrega']):
        return jsonify({'erro': 'Data de entrega invalida, use AAAA-MM-DD'}), 400

    if not prioridade_valida(dados['prioridade']):
        return jsonify({'erro': f'Prioridade deve ser uma de: {PRIORIDADES_VALIDAS}'}), 400

    if not status_tarefa_valido(dados['status']):
        return jsonify({'erro': f'Status deve ser um de: {STATUS_TAREFA_VALIDOS}'}), 400

    tarefa_model.atualizar(
        id_tarefa, dados['titulo'], dados.get('descricao'),
        dados['data_entrega'], dados['prioridade'], dados['status']
    )
    return jsonify({'mensagem': 'Tarefa atualizada'})

@tarefa_bp.route('/tarefas/<int:id_tarefa>/status', methods=['PATCH'])
def atualizar_status(id_tarefa):
    erro = requer_login()
    if erro: return erro
    tarefa = tarefa_pertence_ao_usuario(id_tarefa, session['id_usuario'])
    if tarefa is None:
        return jsonify({'erro': 'Tarefa nao encontrada'}), 404
    if tarefa is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    dados = request.json
    if not dados.get('status'):
        return jsonify({'erro': 'Campo status obrigatorio'}), 400
    if not status_tarefa_valido(dados['status']):
        return jsonify({'erro': f'Status deve ser um de: {STATUS_TAREFA_VALIDOS}'}), 400

    tarefa_model.atualizar_status(id_tarefa, dados['status'])
    return jsonify({'mensagem': 'Status atualizado'})

@tarefa_bp.route('/tarefas/<int:id_tarefa>', methods=['DELETE'])
def deletar(id_tarefa):
    erro = requer_login()
    if erro: return erro
    tarefa = tarefa_pertence_ao_usuario(id_tarefa, session['id_usuario'])
    if tarefa is None:
        return jsonify({'erro': 'Tarefa nao encontrada'}), 404
    if tarefa is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    tarefa_model.deletar(id_tarefa)
    return jsonify({'mensagem': 'Tarefa removida'})
