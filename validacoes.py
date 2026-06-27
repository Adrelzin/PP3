import re
from datetime import datetime

PRIORIDADES_VALIDAS = ['Baixa', 'Media', 'Alta']
STATUS_TAREFA_VALIDOS = ['Pendente', 'Concluida']
TIPOS_USUARIO_VALIDOS = ['Administrador', 'Professor', 'Aluno']

def email_valido(email):
    return re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email) is not None

def senha_valida(senha):
    return isinstance(senha, str) and len(senha) >= 6

def data_valida(data_str):
    try:
        datetime.strptime(data_str, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False

def data_nao_passada(data_str):
    if not data_valida(data_str):
        return False
    return datetime.strptime(data_str, '%Y-%m-%d').date() >= datetime.now().date()

def prioridade_valida(prioridade):
    return prioridade in PRIORIDADES_VALIDAS

def status_tarefa_valido(status):
    return status in STATUS_TAREFA_VALIDOS

def progresso_valido(progresso):
    return isinstance(progresso, (int, float)) and 0 <= progresso <= 100

def hora_valida(hora_str):
    try:
        datetime.strptime(hora_str, '%H:%M')
        return True
    except (ValueError, TypeError):
        return False

def hora_fim_apos_inicio(hora_inicio, hora_fim):
    if not (hora_valida(hora_inicio) and hora_valida(hora_fim)):
        return False
    return datetime.strptime(hora_fim, '%H:%M') > datetime.strptime(hora_inicio, '%H:%M')

DIAS_SEMANA_VALIDOS = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']

def dia_semana_valido(dia):
    return dia in DIAS_SEMANA_VALIDOS