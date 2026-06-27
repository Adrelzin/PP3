from flask import Blueprint, request, jsonify, session
from models.documento import Documento
from models.tarefa import Tarefa
from models.disciplina import Disciplina
from werkzeug.utils import secure_filename
import os

documento_bp = Blueprint('documento', __name__)
documento_model = Documento()
tarefa_model = Tarefa()
disciplina_model = Disciplina()

TIPOS_ARQUIVO_VALIDOS = ['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg', 'txt']
PASTA_UPLOADS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads')

def requer_login():
    if 'id_usuario' not in session:
        return jsonify({'erro': 'Nao autenticado'}), 401
    return None

def tarefa_pertence_ao_usuario(id_tarefa, id_usuario):
    tarefa = tarefa_model.buscar_por_id(id_tarefa)
    if not tarefa:
        return False
    disciplina = disciplina_model.buscar_por_id(tarefa['id_disciplina'])
    return bool(disciplina and disciplina['id_usuario'] == id_usuario)

def documento_pertence_ao_usuario(id_documento, id_usuario):
    documento = documento_model.buscar_por_id(id_documento)
    if not documento:
        return None
    if not tarefa_pertence_ao_usuario(documento['id_tarefa'], id_usuario):
        return False
    return documento

def extensao_do_arquivo(nome_arquivo):
    if '.' not in nome_arquivo:
        return ''
    return nome_arquivo.rsplit('.', 1)[1].lower()

@documento_bp.route('/documentos/tarefa/<int:id_tarefa>', methods=['GET'])
def listar(id_tarefa):
    erro = requer_login()
    if erro: return erro
    if not tarefa_pertence_ao_usuario(id_tarefa, session['id_usuario']):
        return jsonify({'erro': 'Acesso negado'}), 403
    return jsonify(documento_model.listar_por_tarefa(id_tarefa))

@documento_bp.route('/documentos', methods=['POST'])
def criar():
    erro = requer_login()
    if erro: return erro

    if 'arquivo' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400

    arquivo = request.files['arquivo']
    if arquivo.filename == '':
        return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400

    id_tarefa_raw = request.form.get('id_tarefa')
    if not id_tarefa_raw:
        return jsonify({'erro': 'Campo id_tarefa obrigatorio'}), 400
    try:
        id_tarefa = int(id_tarefa_raw)
    except (ValueError, TypeError):
        return jsonify({'erro': 'id_tarefa deve ser um numero'}), 400

    if not tarefa_pertence_ao_usuario(id_tarefa, session['id_usuario']):
        return jsonify({'erro': 'Tarefa invalida'}), 403

    extensao = extensao_do_arquivo(arquivo.filename)
    if extensao not in TIPOS_ARQUIVO_VALIDOS:
        return jsonify({'erro': f'Tipo de arquivo deve ser um de: {TIPOS_ARQUIVO_VALIDOS}'}), 400

    nome_seguro = secure_filename(arquivo.filename)
    pasta_tarefa = os.path.join(PASTA_UPLOADS, f'tarefa_{id_tarefa}')
    os.makedirs(pasta_tarefa, exist_ok=True)

    caminho_completo = os.path.join(pasta_tarefa, nome_seguro)
    arquivo.save(caminho_completo)
    caminho_relativo = f'/uploads/tarefa_{id_tarefa}/{nome_seguro}'

    id_d = documento_model.criar(nome_seguro, extensao, caminho_relativo, id_tarefa)
    return jsonify({'mensagem': 'Documento anexado a tarefa', 'id_documento': id_d, 'caminho': caminho_relativo}), 201

@documento_bp.route('/documentos/<int:id_documento>', methods=['DELETE'])
def deletar(id_documento):
    erro = requer_login()
    if erro: return erro
    documento = documento_pertence_ao_usuario(id_documento, session['id_usuario'])
    if documento is None:
        return jsonify({'erro': 'Documento nao encontrado'}), 404
    if documento is False:
        return jsonify({'erro': 'Acesso negado'}), 403

    caminho_fisico = os.path.join(
        os.path.dirname(PASTA_UPLOADS),
        documento['caminho_arquivo'].lstrip('/')
    )
    if os.path.exists(caminho_fisico):
        os.remove(caminho_fisico)

    documento_model.deletar(id_documento)
    return jsonify({'mensagem': 'Documento removido'})