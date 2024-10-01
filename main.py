import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Conectar ao banco de dados de cursos
conn_cursos = sqlite3.connect('cursos.db')
cursor_cursos = conn_cursos.cursor()

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Cadastro de Cursos")

        self.nome_var = tk.StringVar()
        self.duracao_var = tk.IntVar()

        self.create_widgets()
        self.carregar_cursos()

    def create_widgets(self):
        # Campos de entrada
        tk.Label(self.master, text="Nome do Curso").grid(row=0, column=0)
        tk.Entry(self.master, textvariable=self.nome_var).grid(row=0, column=1)

        tk.Label(self.master, text="Duração (horas)").grid(row=1, column=0)
        tk.Entry(self.master, textvariable=self.duracao_var).grid(row=1, column=1)

        # Botões
        tk.Button(self.master, text="Incluir", command=self.incluir_curso).grid(row=2, column=0)
        tk.Button(self.master, text="Alterar", command=self.alterar_curso).grid(row=2, column=1)
        tk.Button(self.master, text="Excluir", command=self.excluir_curso).grid(row=2, column=2)

        # TreeView
        self.tree = ttk.Treeview(self.master, columns=('Nome', 'Duração'), show='headings')
        self.tree.heading('Nome', text='Nome do Curso')
        self.tree.heading('Duração', text='Duração (horas)')
        self.tree.grid(row=3, column=0, columnspan=3)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def carregar_cursos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor_cursos.execute("SELECT * FROM Cursos")
        for row in cursor_cursos.fetchall():
            self.tree.insert('', 'end', values=(row[1], row[2]), tags=(row[0],))

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            self.nome_var.set(item['values'][0])
            self.duracao_var.set(item['values'][1])

    def incluir_curso(self):
        nome = self.nome_var.get()
        duracao = self.duracao_var.get()
        if nome and duracao:
            cursor_cursos.execute("INSERT INTO Cursos (nome, duracao) VALUES (?, ?)", (nome, duracao))
            conn_cursos.commit()
            self.carregar_cursos()
            self.limpar_campos()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos")

    def alterar_curso(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_curso = self.tree.item(selected_item, 'tags')[0]
            nome = self.nome_var.get()
            duracao = self.duracao_var.get()
            cursor_cursos.execute("UPDATE Cursos SET nome=?, duracao=? WHERE id=?", (nome, duracao, id_curso))
            conn_cursos.commit()
            self.carregar_cursos()
            self.limpar_campos()
        else:
            messagebox.showwarning("Aviso", "Selecione um curso para alterar")

    def excluir_curso(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_curso = self.tree.item(selected_item, 'tags')[0]
            cursor_cursos.execute("DELETE FROM Cursos WHERE id=?", (id_curso,))
            conn_cursos.commit()
            self.carregar_cursos()
            self.limpar_campos()
        else:
            messagebox.showwarning("Aviso", "Selecione um curso para excluir")

    def limpar_campos(self):
        self.nome_var.set("")
        self.duracao_var.set(0)

# Inicializar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

    # Fechar a conexão ao sair
    conn_cursos.close()
