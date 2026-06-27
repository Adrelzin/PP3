from database import get_db

class Documento:
    def criar(self, nome_arquivo, tipo_arquivo, caminho_arquivo, id_tarefa):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO documento (nome_arquivo, tipo_arquivo, caminho_arquivo, id_tarefa) VALUES (%s, %s, %s, %s)",
            (nome_arquivo, tipo_arquivo, caminho_arquivo, id_tarefa)
        )
        db.commit()
        return cursor.lastrowid

    def listar_por_tarefa(self, id_tarefa):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM documento WHERE id_tarefa = %s", (id_tarefa,))
        return cursor.fetchall()

    def buscar_por_id(self, id_documento):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM documento WHERE id_documento = %s", (id_documento,))
        return cursor.fetchone()

    def deletar(self, id_documento):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM documento WHERE id_documento = %s", (id_documento,))
        db.commit()
