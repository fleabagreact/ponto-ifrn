import tkinter.simpledialog
from tkinter import messagebox
import sqlite3

class CadastradorProfessor:
    def __init__(self, ponto_app=None):
        self.conn = sqlite3.connect('PontoApp.db')
        self.cursor = self.conn.cursor()
        self.ponto_app = ponto_app

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS professores (
                matricula INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                ponto_batido INTEGER NOT NULL,
                entrada TEXT,
                saida TEXT,
                data_ponto TEXT,
                UNIQUE(matricula, data_ponto)
            )
        ''')

    def obter_dados_professores(self):
        self.cursor.execute('SELECT * FROM professores')
        professores = self.cursor.fetchall()

        dados_professores = []
        for professor in professores:
            matricula = professor[0]
            nome = professor[1]
            entrada = professor[3] if professor[3] else None
            saida = professor[4] if professor[4] else None

            dados_professor = {
                'matricula': matricula,
                'nome': nome,
                'entrada': entrada,
                'saida': saida,
            }
            dados_professores.append(dados_professor)

        return dados_professores

    def cadastrar_professor(self, matricula, nome):
        if not (isinstance(matricula, int) and len(str(matricula)) == 8):
            messagebox.showwarning("Cadastro de Professor", 'Matrícula inválida. Insira uma matrícula válida com 8 números.')
            return

        if self.matricula_existe(matricula):
            messagebox.showwarning("Cadastro de Professor", 'Matrícula já cadastrada. Tente novamente.')
            return

        try:
            self.cursor.execute('INSERT INTO professores VALUES (?, ?, ?, NULL, NULL, NULL)', (matricula, nome, 0))
            self.conn.commit()
            messagebox.showinfo("Cadastro de Professor", f'Professor cadastrado: {nome} (Matrícula: {matricula})')
            self.atualizar_lista_professores()
        except sqlite3.IntegrityError:
            messagebox.showwarning("Cadastro de Professor", 'Erro ao cadastrar professor. Tente novamente.')

    def obter_professores(self):
        self.cursor.execute('SELECT * FROM professores')
        return self.cursor.fetchall()

    def cancelar_matricula(self, matricula):
        if not self.matricula_existe(matricula):
            messagebox.showwarning("Cancelar Matrícula", f"Matrícula {matricula} não encontrada. Certifique-se de que a matrícula está cadastrada.")
            return

        confirmar = messagebox.askokcancel("Cancelar Matrícula", f"Tem certeza que deseja cancelar a matrícula {matricula}?")
        
        if confirmar:
            self.cursor.execute('DELETE FROM professores WHERE matricula = ?', (matricula,))
            self.conn.commit()
            messagebox.showinfo("Matrícula Cancelada", f"Matrícula {matricula} foi cancelada com sucesso.")

    def matricula_existe(self, matricula):
        self.cursor.execute('SELECT * FROM professores WHERE matricula = ?', (matricula,))
        return self.cursor.fetchone() is not None

    def atualizar_lista_professores(self):
        dados_professores = self.obter_dados_professores()
        if self.ponto_app:
            self.ponto_app.atualizar_lista_professores(dados_professores)

    def fechar_conexao(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()