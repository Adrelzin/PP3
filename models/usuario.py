from database import get_db

class Usuario:
    def criar(self, nome, email, senha, tipo_usuario, foto_perfil=None):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha, tipo_usuario, foto_perfil) VALUES (%s, %s, %s, %s, %s)",
            (nome, email, senha, tipo_usuario, foto_perfil)
        )
        db.commit()
        return cursor.lastrowid

    def buscar_por_email(self, email):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        return cursor.fetchone()

    def buscar_por_id(self, id_usuario):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
        return cursor.fetchone()

    def listar(self):
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nome, email, tipo_usuario, foto_perfil FROM usuario")
        return cursor.fetchall()

    def atualizar(self, id_usuario, nome, email, foto_perfil=None):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE usuario SET nome=%s, email=%s, foto_perfil=%s WHERE id_usuario=%s",
            (nome, email, foto_perfil, id_usuario)
        )
        db.commit()

    def deletar(self, id_usuario):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
        db.commit()
