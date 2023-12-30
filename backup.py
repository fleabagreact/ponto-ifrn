import tkinter as tk
from tkinter import filedialog, messagebox
import pickle
from datetime import datetime

class JanelaBackup:
    def __init__(self, master, cadastrador, atualizar_lista_professores, atualizar_hora_ponto):
        self.master = master
        self.master.title('Backup')
        self.cadastrador = cadastrador
        self.atualizar_lista_professores = atualizar_lista_professores
        self.atualizar_hora_ponto = atualizar_hora_ponto

        self.label_info = tk.Label(master, text='Clique no botão para criar backup.')
        self.label_info.pack(pady=10)

        self.backup_button = tk.Button(master, text='Criar Backup', command=self.criar_backup, width=15, height=2)
        self.backup_button.pack(pady=10)

    def criar_backup(self):
        dados_professores = self.cadastrador.obter_dados_professores()

        dados_backup = {
            'dados_professores': dados_professores,
            'data_criacao': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle Files", "*.pkl")])

        with open(file_path, 'wb') as file:
            pickle.dump(dados_backup, file)

        messagebox.showinfo("Backup criado", "Backup criado com sucesso!")