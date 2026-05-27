import sqlite3
import os

def conectar():
    return sqlite3.connect('Alunos.db')

def criar_tabela(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nascimento DATE NOT NULL,
            curso TEXT NOT NULL,
            periodo INTEGER NOT NULL
        )
    ''')
    conn.commit()


# === CREATE ===
def cadastrar_aluno(conn, nome, data_nasc, curso, periodo):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alunos (nome, data_nascimento, curso, periodo)
        VALUES (?, ?, ?, ?)
    """, (nome, data_nasc, curso, periodo))

    conn.commit()

# === READ ===
def listar_alunos(conn):
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM alunos ORDER BY nome"
    )

    return cursor.fetchall()

# === UPDATE ===
def atualizar_aluno(conn, id_aluno, nome, data_nasc, curso, periodo):
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE alunos
        SET nome = ?, data_nascimento = ?, curso = ?, periodo = ?
        WHERE id = ?
    """, (
        nome,
        data_nasc,
        curso,
        periodo,
        id_aluno
    ))

    conn.commit()

# === DELETE ===

def excluir_aluno(conn, id_aluno):
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM alunos WHERE id = ?",
        (id_aluno,)
    )

    conn.commit()


# === MENU ===
def menu():
    print("\n=== SISTEMA DE GESTÃO ACADÊMICA ===")
    print("1 - Cadastrar aluno")
    print("2 - Listar alunos")
    print("3 - Atualizar aluno")
    print("4 - Excluir aluno")
    print("5 - Sair")


def main():
    conn = conectar()
    criar_tabela(conn)

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_aluno(conn)
        elif opcao == "2":
            listar_alunos(conn)
        elif opcao == "3":
            atualizar_aluno(conn)
        elif opcao == "4":
            id_aluno = int(input("Digite o ID do aluno a ser excluído: "))
            excluir_aluno(conn, id_aluno)
        elif opcao == "5":
            print("Saindo do sistema...")
            conn.close()
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()