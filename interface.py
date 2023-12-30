import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
from cadastro import CadastradorProfessor
from ponto import RegistradorPonto
from backup import JanelaBackup
from datetime import datetime

class PontoApp:
    def __init__(self, master):
        self.master = master
        master.title('Controle de Ponto Eletrônico')

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.ponto_frame = tk.Frame(self.notebook)
        self.cadastros_frame = tk.Frame(self.notebook)
        self.cancelar_matricula_frame = tk.Frame(self.notebook)

        # menu
        self.notebook.add(self.ponto_frame, text='Confirmar presença')
        self.notebook.add(self.cadastros_frame, text='Cadastro de Professores')
        self.notebook.add(self.cancelar_matricula_frame, text='Cancelar Matrícula')

        self.label_data = tk.Label(self.ponto_frame, text=self.obter_data_atual(), font=('Arial', 14))
        self.label_data.pack(pady=5)

        # janela bater ponto
        self.imagem_confirmar_presenca = PhotoImage(file='ifrn-logo.png')
        self.label_imagem_confirmar_presenca = tk.Label(self.ponto_frame, image=self.imagem_confirmar_presenca)
        self.label_imagem_confirmar_presenca.pack(pady=10)

        self.label_matricula_ponto = tk.Label(self.ponto_frame, text='Matrícula:')
        self.label_matricula_ponto.pack(pady=5)

        self.matricula_entry_ponto = tk.Entry(self.ponto_frame)
        self.matricula_entry_ponto.pack(pady=5)

        self.resultado_label_ponto = tk.Label(self.ponto_frame, text='')
        self.resultado_label_ponto.pack(pady=5)

        self.bater_entrada_button = tk.Button(self.ponto_frame, text='Bater Entrada', command=self.bater_entrada)
        self.bater_entrada_button.pack(pady=10)

        self.bater_saida_button = tk.Button(self.ponto_frame, text='Bater Saída', command=self.bater_saida)
        self.bater_saida_button.pack(pady=10)

        self.hora_label = tk.Label(self.ponto_frame, text='')
        self.hora_label.pack(pady=10)

        self.professores_listbox = tk.Listbox(self.ponto_frame)
        self.professores_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.cadastrador = CadastradorProfessor()
        self.registrador_ponto = RegistradorPonto(self.cadastrador)

        # janela cadastrar professor
        self.imagem_cadastro_professores = PhotoImage(file='ifrn-logo.png')
        self.label_imagem_cadastro_professores = tk.Label(self.cadastros_frame, image=self.imagem_cadastro_professores)
        self.label_imagem_cadastro_professores.pack(pady=10)

        self.label_matricula_cadastro = tk.Label(self.cadastros_frame, text='Matrícula:')
        self.label_matricula_cadastro.pack(pady=5)

        self.matricula_entry_cadastro = tk.Entry(self.cadastros_frame)
        self.matricula_entry_cadastro.pack(pady=5)

        self.label_nome_cadastro = tk.Label(self.cadastros_frame, text='Nome:')
        self.label_nome_cadastro.pack(pady=5)

        self.nome_entry_cadastro = tk.Entry(self.cadastros_frame)
        self.nome_entry_cadastro.pack(pady=5)

        self.cadastrar_button = tk.Button(self.cadastros_frame, text='Cadastrar Professor', command=self.cadastrar)
        self.cadastrar_button.pack(pady=10)

        # janela cancelar matricula
        self.imagem_cancelar_matricula = PhotoImage(file='ifrn-logo.png')
        self.label_imagem_cancelar_matricula = tk.Label(self.cancelar_matricula_frame, image=self.imagem_cancelar_matricula)
        self.label_imagem_cancelar_matricula.pack(pady=10)

        self.label_matricula_cancelar = tk.Label(self.cancelar_matricula_frame, text='Matrícula a Cancelar:')
        self.label_matricula_cancelar.pack(pady=5)

        self.matricula_entry_cancelar = tk.Entry(self.cancelar_matricula_frame)
        self.matricula_entry_cancelar.pack(pady=5)

        self.cancelar_matricula_button = tk.Button(self.cancelar_matricula_frame, text='Cancelar Matrícula', command=self.cancelar_matricula)
        self.cancelar_matricula_button.pack(pady=10)

        # backup
        self.backup_button = tk.Button(self.ponto_frame, text='Abrir Backup', command=self.abrir_janela_backup, width=20, height=2)
        self.backup_button.pack(pady=10)

        self.atualizar_hora_ponto()
        self.atualizar_lista_professores()

    def abrir_janela_backup(self):
        janela_backup = tk.Toplevel(self.master)
        JanelaBackup(janela_backup, self.cadastrador, self.atualizar_lista_professores, self.atualizar_hora_ponto)

    def cadastrar(self):
        matricula = int(self.matricula_entry_cadastro.get())
        nome = self.nome_entry_cadastro.get()
        if nome:
            self.cadastrador.cadastrar_professor(matricula, nome)
            self.atualizar_lista_professores()

    def bater_entrada(self):
        matricula_str = self.matricula_entry_ponto.get()

        if not matricula_str:
            messagebox.showwarning("Registro de Entrada", "Por favor, insira uma matrícula.")
            return

        try:
            matricula = int(matricula_str)
        except ValueError:
            messagebox.showwarning("Registro de Entrada", "Matrícula inválida. Insira uma matrícula válida com 8 números.")
            return

        resultado = self.registrador_ponto.registrar_entrada(matricula)
        self.atualizar_lista_professores()
        self.resultado_label_ponto.config(text=resultado)
        self.atualizar_hora_ponto()

    def bater_saida(self):
        matricula = int(self.matricula_entry_ponto.get())
        resultado = self.registrador_ponto.registrar_saida(matricula)
        self.atualizar_lista_professores()
        self.resultado_label_ponto.config(text=resultado)
        self.atualizar_hora_ponto()

    def cancelar_matricula(self):
        matricula = int(self.matricula_entry_cancelar.get())
        confirmar = messagebox.askokcancel("Cancelar Matrícula", f"Tem certeza que deseja cancelar a matrícula {matricula}?")
        
        if confirmar:
            self.cadastrador.cancelar_matricula(matricula)
            self.atualizar_lista_professores()

    def atualizar_lista_professores(self):
        self.professores_listbox.delete(0, tk.END)

        professores = self.cadastrador.obter_professores()

        for professor in professores:
            if professor[2] == 1:
                status = f'Entrada: {professor[3]}'
                if professor[4]:
                    entrada = datetime.strptime(professor[3], '%H:%M:%S')
                    saida = datetime.strptime(professor[4], '%H:%M:%S')
                    horas_trabalhadas = saida - entrada
                    horas_formatadas = "{:02}:{:02}".format(horas_trabalhadas.seconds // 3600, (horas_trabalhadas.seconds % 3600) // 60)
                    status += f' / Saída: {professor[4]} / Horas: {horas_formatadas}'
            else:
                status = ''
            info = f'{professor[1]} (Matrícula: {professor[0]}) - {status}'
            self.professores_listbox.insert(tk.END, info)
            self.cadastrador = CadastradorProfessor()

    def obter_data_atual(self):
        data_atual = datetime.now().strftime('%d/%m/%Y')
        return f'Data: {data_atual}'

    def atualizar_hora_ponto(self):
        hora_atual = datetime.now().strftime('%H:%M:%S')
        self.hora_label.config(text=f'Hora: {hora_atual}')
        self.master.after(1000, self.atualizar_hora_ponto)

if __name__ == '__main__':
    root = tk.Tk()
    app = PontoApp(root)
    root.geometry("600x400")
    root.mainloop()
    app.cadastrador.fechar_conexao()