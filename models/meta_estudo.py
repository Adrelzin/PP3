from database import get_db

class MetaEstudo:
    def criar(self, descricao, prazo, id_usuario, progresso=0):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO meta_estudo (descricao, prazo, progresso, id_usuario) VALUES (%s, %s, %s, %s)",
            (descricao, prazo, progresso, id_usuario)
        )
        db.commit()
        return cursor.lastrowid

    def listar_por_usuario(self, id_usuario):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM meta_estudo WHERE id_usuario = %s ORDER BY prazo", (id_usuario,))
        return cursor.fetchall()

    def buscar_por_id(self, id_meta):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM meta_estudo WHERE id_meta = %s", (id_meta,))
        return cursor.fetchone()

    def atualizar_progresso(self, id_meta, progresso):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE meta_estudo SET progresso=%s WHERE id_meta=%s", (progresso, id_meta))
        db.commit()

    def atualizar(self, id_meta, descricao, prazo, progresso):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE meta_estudo SET descricao=%s, prazo=%s, progresso=%s WHERE id_meta=%s",
            (descricao, prazo, progresso, id_meta)
        )
        db.commit()

    def deletar(self, id_meta):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM meta_estudo WHERE id_meta = %s", (id_meta,))
        db.commit()
