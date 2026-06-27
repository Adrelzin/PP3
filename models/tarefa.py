from database import get_db

class Tarefa:
    def criar(self, titulo, descricao, data_entrega, prioridade, id_disciplina, status='Pendente'):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO tarefa (titulo, descricao, data_entrega, status, prioridade, id_disciplina) VALUES (%s, %s, %s, %s, %s, %s)",
            (titulo, descricao, data_entrega, status, prioridade, id_disciplina)
        )
        db.commit()
        return cursor.lastrowid

    def listar_por_usuario(self, id_usuario):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.*, d.nome AS nome_disciplina FROM tarefa t
            JOIN disciplina d ON t.id_disciplina = d.id_disciplina
            WHERE d.id_usuario = %s ORDER BY t.data_entrega
        """, (id_usuario,))
        return cursor.fetchall()

    def buscar_por_id(self, id_tarefa):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tarefa WHERE id_tarefa = %s", (id_tarefa,))
        return cursor.fetchone()

    def atualizar_status(self, id_tarefa, status):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE tarefa SET status=%s WHERE id_tarefa=%s", (status, id_tarefa))
        db.commit()

    def atualizar(self, id_tarefa, titulo, descricao, data_entrega, prioridade, status):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE tarefa SET titulo=%s, descricao=%s, data_entrega=%s, prioridade=%s, status=%s WHERE id_tarefa=%s",
            (titulo, descricao, data_entrega, prioridade, status, id_tarefa)
        )
        db.commit()

    def deletar(self, id_tarefa):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM tarefa WHERE id_tarefa = %s", (id_tarefa,))
        db.commit()
