from database import get_db

def _formatar_hora(valor):
    if valor is None:
        return None
    total_segundos = int(valor.total_seconds())
    horas, resto = divmod(total_segundos, 3600)
    minutos = resto // 60
    return f"{horas:02d}:{minutos:02d}"

def _formatar_horario(registro):
    if registro is None:
        return None
    registro['hora_inicio'] = _formatar_hora(registro['hora_inicio'])
    registro['hora_fim'] = _formatar_hora(registro['hora_fim'])
    return registro

class Horario:
    def criar(self, dia_semana, hora_inicio, hora_fim, id_disciplina, id_usuario):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO horario (dia_semana, hora_inicio, hora_fim, id_disciplina, id_usuario) VALUES (%s, %s, %s, %s, %s)",
            (dia_semana, hora_inicio, hora_fim, id_disciplina, id_usuario)
        )
        db.commit()
        return cursor.lastrowid

    def listar_por_usuario(self, id_usuario):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT h.*, d.nome AS nome_disciplina FROM horario h
            JOIN disciplina d ON h.id_disciplina = d.id_disciplina
            WHERE h.id_usuario = %s ORDER BY h.hora_inicio
        """, (id_usuario,))
        registros = cursor.fetchall()
        return [_formatar_horario(r) for r in registros]

    def buscar_por_id(self, id_horario):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM horario WHERE id_horario = %s", (id_horario,))
        return _formatar_horario(cursor.fetchone())

    def atualizar(self, id_horario, dia_semana, hora_inicio, hora_fim, id_disciplina):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE horario SET dia_semana=%s, hora_inicio=%s, hora_fim=%s, id_disciplina=%s WHERE id_horario=%s",
            (dia_semana, hora_inicio, hora_fim, id_disciplina, id_horario)
        )
        db.commit()

    def deletar(self, id_horario):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM horario WHERE id_horario = %s", (id_horario,))
        db.commit()