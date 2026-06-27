from flask import Blueprint, request, jsonify, session
from models.horario import Horario
from models.disciplina import Disciplina
from validacoes import dia_semana_valido, hora_fim_apos_inicio, DIAS_SEMANA_VALIDOS

horario_bp = Blueprint('horario', __name__)
horario_model = Horario()
disciplina_model = Disciplina()

def requer_login():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Nao autenticado'}), 401
    return None

def horario_pertence_ao_usuario(id_horario, id_usuario):
    horario = horario_model.buscar_por_id(id_horario)
    if not horario:
        return None
    if horario['id_usuario'] != id_usuario:
        return False
    return horario

@horario_bp.route('/horarios', methods=['GET'])
def listar():
    erro = requer_login()
    if erro: return erro
    return jsonify(horario_model.listar_por_usuario(session['id_usuario']))

@horario_bp.route('/horarios', methods=['POST'])
def criar():
    erro = requer_login()
    if erro: return erro
    dados = request.json
    for campo in ['dia_semana', 'hora_inicio', 'hora_fim', 'id_disciplina']:
        if not dados.get(campo):
            return jsonify({'erro': f'Campo {campo} obrigatorio'}), 400

    disciplina = disciplina_model.buscar_por_id(dados['id_disciplina'])
    if not disciplina or disciplina['id_usuario'] != session['id_usuario']:
        return jsonify({'erro': 'Disciplina invalida'}), 403

    if not dia_semana_valido(dados['dia_semana']):
        return jsonify({'erro': f'Dia da semana deve ser um de: {DIAS_SEMANA_VALIDOS}'}), 400

    if not hora_fim_apos_inicio(dados['hora_inicio'], dados['hora_fim']):
        return jsonify({'erro': 'Hora de fim deve ser apos a hora de inicio, use HH:MM'}), 400

    id_h = horario_model.criar(dados['dia_semana'], dados['hora_inicio'], dados['hora_fim'], dados['id_disciplina'], session['id_usuario'])
    return jsonify({'mensagem': 'Horario criado', 'id_horario': id_h}), 201

@horario_bp.route('/horarios/<int:id_horario>', methods=['PUT'])
def atualizar(id_horario):
    erro = requer_login()
    if erro: return erro
    horario = horario_pertence_ao_usuario(id_horario, session['id_usuario'])
    if horario is None:
        return jsonify({'erro': 'Horario nao encontrado'}), 404
    if horario is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    dados = request.json
    for campo in ['dia_semana', 'hora_inicio', 'hora_fim', 'id_disciplina']:
        if not dados.get(campo):
            return jsonify({'erro': f'Campo {campo} obrigatorio'}), 400

    disciplina = disciplina_model.buscar_por_id(dados['id_disciplina'])
    if not disciplina or disciplina['id_usuario'] != session['id_usuario']:
        return jsonify({'erro': 'Disciplina invalida'}), 403

    if not dia_semana_valido(dados['dia_semana']):
        return jsonify({'erro': f'Dia da semana deve ser um de: {DIAS_SEMANA_VALIDOS}'}), 400

    if not hora_fim_apos_inicio(dados['hora_inicio'], dados['hora_fim']):
        return jsonify({'erro': 'Hora de fim deve ser apos a hora de inicio, use HH:MM'}), 400

    horario_model.atualizar(id_horario, dados['dia_semana'], dados['hora_inicio'], dados['hora_fim'], dados['id_disciplina'])
    return jsonify({'mensagem': 'Horario atualizado'})

@horario_bp.route('/horarios/<int:id_horario>', methods=['DELETE'])
def deletar(id_horario):
    erro = requer_login()
    if erro: return erro
    horario = horario_pertence_ao_usuario(id_horario, session['id_usuario'])
    if horario is None:
        return jsonify({'erro': 'Horario nao encontrado'}), 404
    if horario is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    horario_model.deletar(id_horario)
    return jsonify({'mensagem': 'Horario removido'})