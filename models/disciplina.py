from database import get_db

class Disciplina:
    def criar(self, nome, descricao, id_usuario):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO disciplina (nome, descricao, id_usuario) VALUES (%s, %s, %s)",
            (nome, descricao, id_usuario)
        )
        db.commit()
        return cursor.lastrowid

    def listar_por_usuario(self, id_usuario):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM disciplina WHERE id_usuario = %s", (id_usuario,))
        return cursor.fetchall()

    def buscar_por_id(self, id_disciplina):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM disciplina WHERE id_disciplina = %s", (id_disciplina,))
        return cursor.fetchone()

    def atualizar(self, id_disciplina, nome, descricao):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE disciplina SET nome=%s, descricao=%s WHERE id_disciplina=%s",
            (nome, descricao, id_disciplina)
        )
        db.commit()

    def deletar(self, id_disciplina):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM disciplina WHERE id_disciplina = %s", (id_disciplina,))
        db.commit()
