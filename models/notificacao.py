from database import get_db
from datetime import datetime

class Notificacao:
    def criar(self, mensagem, id_usuario, status='nao_lida'):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO notificacao (mensagem, data_envio, status, id_usuario) VALUES (%s, %s, %s, %s)",
            (mensagem, datetime.now(), status, id_usuario)
        )
        db.commit()
        return cursor.lastrowid

    def listar_por_usuario(self, id_usuario):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM notificacao WHERE id_usuario = %s ORDER BY data_envio DESC",
            (id_usuario,)
        )
        return cursor.fetchall()

    def marcar_como_lida(self, id_notificacao):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE notificacao SET status='lida' WHERE id_notificacao=%s", (id_notificacao,))
        db.commit()

    def deletar(self, id_notificacao):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM notificacao WHERE id_notificacao = %s", (id_notificacao,))
        db.commit()
