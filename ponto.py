import sqlite3
from tkinter import messagebox
from datetime import datetime

class RegistradorPonto:
    def __init__(self, cadastrador):
        self.conn = sqlite3.connect('PontoApp.db')
        self.cursor = self.conn.cursor()
        self.cadastrador = cadastrador

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

    def verificar_ponto_no_dia(self, matricula):
        data_atual = datetime.now().strftime('%d/%m/%Y')
        self.cursor.execute('SELECT ponto_batido FROM professores WHERE matricula = ? AND data_ponto = ?', (matricula, data_atual))
        resultado = self.cursor.fetchone()
        return resultado is not None and resultado[0] in [0, 1]

    def verificar_saida_registrada(self, matricula):
        data_atual = datetime.now().strftime('%d/%m/%Y')
        self.cursor.execute('SELECT ponto_batido FROM professores WHERE matricula = ? AND data_ponto = ?', (matricula, data_atual))
        resultado = self.cursor.fetchone()
        return resultado is not None and resultado[0] == 0

    def registrar_entrada(self, matricula):
        if len(str(matricula)) != 8:
            messagebox.showwarning("Registro de Entrada", "Matrícula inválida. Insira uma matrícula válida com 8 números.")
            return "Matrícula inválida. Insira uma matrícula válida com 8 números."

        if not self.cadastrador.matricula_existe(matricula):
            messagebox.showwarning("Registro de Entrada", "Matrícula não encontrada. Certifique-se de que a matrícula está cadastrada.")
            return "Matrícula não encontrada. Certifique-se de que a matrícula está cadastrada."

        if self.verificar_ponto_no_dia(matricula):
            messagebox.showwarning("Registro de Entrada", "Entrada já registrada para este professor hoje.")
            return "Entrada já registrada para este professor hoje."

        hora_atual = datetime.now().strftime('%H:%M:%S')
        data_atual = datetime.now().strftime('%d/%m/%Y')

        self.cursor.execute('UPDATE professores SET ponto_batido = 1, entrada = ?, data_ponto = ?, saida = NULL WHERE matricula = ?', (hora_atual, data_atual, matricula))
        self.conn.commit()

        mensagem = f'Entrada registrada para o professor (Matrícula: {matricula}) às {hora_atual}'
        messagebox.showinfo("Registro de Entrada", mensagem)
        return mensagem

    def registrar_saida(self, matricula):
        if len(str(matricula)) != 8:
            messagebox.showwarning("Registro de Saída", "Matrícula inválida. Insira uma matrícula válida com 8 números.")
            return "Matrícula inválida. Insira uma matrícula válida com 8 números."

        if not self.verificar_ponto_no_dia(matricula):
            messagebox.showwarning("Registro de Saída", "Registre a entrada primeiro para este professor hoje.")
            return "Registre a entrada primeiro para este professor hoje."

        if self.verificar_saida_registrada(matricula):
            messagebox.showwarning("Registro de Saída", "Saída já registrada para este professor hoje.")
            return "Saída já registrada para este professor hoje."

        hora_atual = datetime.now().strftime('%H:%M:%S')
        self.cursor.execute('UPDATE professores SET ponto_batido = 0, saida = ? WHERE matricula = ? AND data_ponto = ?', (hora_atual, matricula, datetime.now().strftime('%d/%m/%Y')))
        self.conn.commit()

        mensagem = f'Saída registrada para o professor (Matrícula: {matricula}) às {hora_atual}'
        messagebox.showinfo("Registro de Saída", mensagem)
        return mensagem

    def __del__(self):
        self.conn.close()