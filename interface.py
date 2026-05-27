import tkinter as tk
from tkinter import ttk, messagebox

from crud import (
    conectar,
    criar_tabela,
    cadastrar_aluno,
    listar_alunos,
    atualizar_aluno,
    excluir_aluno
)

# === BANCO ===

conn = conectar()
criar_tabela(conn)

# === FUNÇÕES DA INTERFACE ===

def cadastrar():
    nome = entry_nome.get()
    data = entry_data.get()
    curso = entry_curso.get()
    periodo = entry_periodo.get()

    if not nome or not data or not curso or not periodo:
        messagebox.showwarning(
            "Aviso",
            "Preencha todos os campos."
        )
        return

    cadastrar_aluno(
        conn,
        nome,
        data,
        curso,
        int(periodo)
    )

    limpar_campos()
    carregar_tabela()

    messagebox.showinfo(
        "Sucesso",
        "Aluno cadastrado!"
    )

def carregar_tabela():
    for item in tabela.get_children():
        tabela.delete(item)

    alunos = listar_alunos(conn)

    for aluno in alunos:
        tabela.insert("", tk.END, values=aluno)

def selecionar_aluno(event):
    item = tabela.selection()

    if item:
        valores = tabela.item(item, "values")

        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_id.insert(0, valores[0])
        entry_id.config(state="readonly")

        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, valores[1])

        entry_data.delete(0, tk.END)
        entry_data.insert(0, valores[2])

        entry_curso.delete(0, tk.END)
        entry_curso.insert(0, valores[3])

        entry_periodo.delete(0, tk.END)
        entry_periodo.insert(0, valores[4])

def atualizar():
    id_aluno = entry_id.get()

    if not id_aluno:
        messagebox.showwarning(
            "Aviso",
            "Selecione um aluno."
        )
        return

    atualizar_aluno(
        conn,
        id_aluno,
        entry_nome.get(),
        entry_data.get(),
        entry_curso.get(),
        int(entry_periodo.get())
    )

    carregar_tabela()
    limpar_campos()

    messagebox.showinfo(
        "Sucesso",
        "Aluno atualizado!"
    )

def excluir():
    id_aluno = entry_id.get()

    if id_aluno == "":
        messagebox.showwarning(
            "Aviso",
            "Selecione um aluno."
        )
        return

    resposta = messagebox.askyesno(
        "Confirmar",
        "Deseja excluir este aluno?"
    )

    if resposta:
        excluir_aluno(conn, int(id_aluno))

        carregar_tabela()
        limpar_campos()

        messagebox.showinfo(
            "Sucesso",
            "Aluno excluído!"
        )

def limpar_campos():
    entry_id.config(state="normal")
    entry_id.delete(0, tk.END)
    entry_id.config(state="readonly")

    entry_nome.delete(0, tk.END)
    entry_data.delete(0, tk.END)
    entry_curso.delete(0, tk.END)
    entry_periodo.delete(0, tk.END)

# === JANELA ===

janela = tk.Tk()
janela.title("Sistema de Gestão Acadêmica")
janela.geometry("1080x720")
janela.configure(bg="#001F3F")

# === ESTILO ===

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="#222",
    rowheight=30,
    fieldbackground="white",
    font=("Bahnschrift", 16)
)

style.configure(
    "Treeview.Heading",
    background="#1f2937",
    foreground="white",
    font=("Bahnschrift", 16, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#2563eb")]
)

# === TITULO ===

titulo = tk.Label(
    janela,
    text="Sistema de Gestão Acadêmica",
    font=("Bahnschrift", 32, "bold"),
    bg="#001F3F",
    fg="white"
)

titulo.pack(pady=20)

# === CONTAINER PRINCIPAL ===

container = tk.Frame(
    janela,
    bg="white",
    bd=0
)

container.pack(
    fill="both",
    expand=True,
    padx=24,
    pady=12
)

# === FORMULÁRIO===

frame_form = tk.Frame(
    container,
    bg="white"
)

frame_form.pack(
    fill="x",
    padx=24,
    pady=24
)

# Labels

label_style = {
    "bg": "white",
    "fg": "#374151",
    "font": ("Bahnschrift", 16, "bold")
}

entry_style = {
    "font": ("Bahnschrift", 16),
    "bd": 1,
    "relief": "solid"
}

# ID

tk.Label(
    frame_form,
    text="ID",
    **label_style
).grid(row=0, column=0, sticky="w", pady=4)

entry_id = tk.Entry(
    frame_form,
    state="readonly",
    width=4,
    **entry_style
)

entry_id.grid(row=1, column=0, padx=4)

# Nome

tk.Label(
    frame_form,
    text="Nome",
    **label_style
).grid(row=0, column=1, sticky="w", pady=4)

entry_nome = tk.Entry(
    frame_form,
    width=24,
    **entry_style
)

entry_nome.grid(row=1, column=1, padx=4)

# Nascimento

tk.Label(
    frame_form,
    text="Nascimento (Ano/Mês/Dia)",
    **label_style
).grid(row=0, column=2, sticky="w", pady=4)

entry_data = tk.Entry(
    frame_form,
    width=24,
    **entry_style
)

entry_data.grid(row=1, column=2, padx=4)

# Curso

tk.Label(
    frame_form,
    text="Curso",
    **label_style
).grid(row=0, column=3, sticky="w", pady=4)

entry_curso = tk.Entry(
    frame_form,
    width=16,
    **entry_style
)

entry_curso.grid(row=1, column=3, padx=4)

# Período

tk.Label(
    frame_form,
    text="Período",
    **label_style
).grid(row=0, column=4, sticky="w", pady=4)

entry_periodo = tk.Entry(
    frame_form,
    width=8,
    **entry_style
)

entry_periodo.grid(row=1, column=4, padx=4)

# === BOTÕES ===

frame_botoes = tk.Frame(
    container,
    bg="white"
)

frame_botoes.pack(pady=12)

botao_style = {
    "font": ("Bahnschrift", 16, "bold"),
    "bd": 0,
    "cursor": "hand2",
    "width": 15,
    "height": 2
}

btn_cadastrar = tk.Button(
    frame_botoes,
    text="Cadastrar",
    bg="#001F3F",
    fg="white",
    command=cadastrar,
    **botao_style
)

btn_cadastrar.grid(row=0, column=0, padx=4)

btn_atualizar = tk.Button(
    frame_botoes,
    text="Atualizar",
    bg="#083358",
    fg="white",
    command=atualizar,
    **botao_style
)

btn_atualizar.grid(row=0, column=1, padx=4)

btn_excluir = tk.Button(
    frame_botoes,
    text="Excluir",
    bg="#0D63A5",
    fg="white",
    command=excluir,
    **botao_style
)

btn_excluir.grid(row=0, column=2, padx=4)

btn_limpar = tk.Button(
    frame_botoes,
    text="Limpar Campos",
    bg="#FFD717",
    fg="white",
    command=limpar_campos,
    **botao_style
)

btn_limpar.grid(row=0, column=3, padx=4)

# === TABELA ===

frame_tabela = tk.Frame(
    container,
    bg="white"
)

frame_tabela.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

colunas = (
    "ID",
    "Nome",
    "Nascimento",
    "Curso",
    "Período"
)

tabela = ttk.Treeview(
    frame_tabela,
    columns=colunas,
    show="headings"
)

# Cabeçalhos

for coluna in colunas:
    tabela.heading(coluna, text=coluna)

# Larguras

tabela.column("ID", width=60, anchor="center")
tabela.column("Nome", width=250)
tabela.column("Nascimento", width=140, anchor="center")
tabela.column("Curso", width=220)
tabela.column("Período", width=100, anchor="center")

# Scrollbar

scroll = ttk.Scrollbar(
    frame_tabela,
    orient="vertical",
    command=tabela.yview
)

tabela.configure(yscrollcommand=scroll.set)

scroll.pack(side="right", fill="y")

tabela.pack(
    fill="both",
    expand=True
)

tabela.bind(
    "<<TreeviewSelect>>",
    selecionar_aluno
)

# === INICIAR ===

carregar_tabela()

janela.mainloop()