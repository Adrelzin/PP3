from database import get_db

class Prova:
    def criar(self, nome, descricao, data_prova, id_disciplina):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO prova (nome, descricao, data_prova, id_disciplina) VALUES (%s, %s, %s, %s)",
            (nome, descricao, data_prova, id_disciplina)
        )
        db.commit()
        return cursor.lastrowid

    def listar_por_usuario(self, id_usuario):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*, d.nome AS nome_disciplina FROM prova p
            JOIN disciplina d ON p.id_disciplina = d.id_disciplina
            WHERE d.id_usuario = %s ORDER BY p.data_prova
        """, (id_usuario,))
        return cursor.fetchall()

    def buscar_por_id(self, id_prova):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prova WHERE id_prova = %s", (id_prova,))
        return cursor.fetchone()

    def atualizar(self, id_prova, nome, descricao, data_prova):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE prova SET nome=%s, descricao=%s, data_prova=%s WHERE id_prova=%s",
            (nome, descricao, data_prova, id_prova)
        )
        db.commit()

    def deletar(self, id_prova):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM prova WHERE id_prova = %s", (id_prova,))
        db.commit()
