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
def cadastrar_aluno(conn):
    cursor = conn.cursor()

    print("\n=== CADASTRAR ALUNO ===")
    nome = input("Nome do aluno: ")
    data_nasc = input("Data de Nascimento (AAAA-MM-DD): ")
    curso = input("Curso: ")
    periodo = int(input("Período (Número inteiro): "))

    cursor.execute('''
        INSERT INTO alunos (nome, data_nascimento, curso, periodo)
        VALUES (?, ?, ?, ?)
    ''', (nome, data_nasc, curso, periodo))

    conn.commit()
    print(f"\nAluno {nome} cadastrado com sucesso!")

# === READ ===
def listar_alunos(conn):
    cursor = conn.cursor()

    print("\n=== LISTA DE ALUNOS ===")
    cursor.execute("SELECT * FROM alunos ORDER BY nome")
    alunos = cursor.fetchall()

    if not alunos:
        print("Nenhum aluno cadastrado.")
        return

    print("\n" + "="*75)
    print(f"{'ID':<4} | {'NOME':<20} | {'NASCIMENTO':<12} | {'CURSO':<15} | {'PERÍODO'}")
    print("-" * 75)

    for aluno in alunos:
        print(f"{aluno[0]:<4} | {aluno[1]:<20} | {aluno[2]:<12} | {aluno[3]:<15} | {aluno[4]}º")

    print("="*75)

# === UPDATE ===
def atualizar_aluno(conn):
    cursor = conn.cursor()

    print("\n=== ATUALIZAR ALUNO ===")
    id_busca = input("Digite o ID do aluno: ")

    cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_busca,))
    aluno = cursor.fetchone()

    if not aluno:
        print("Aluno não encontrado.")
        return

    print(f"\nEditando: {aluno[1]} ({aluno[4]}º período de {aluno[3]})")
    print("Digite 0 para manter o valor atual.\n")

    novo_nome = input(f"Novo nome [{aluno[1]}]: ")
    nova_data = input(f"Nova data [{aluno[2]}]: ")
    novo_curso = input(f"Novo curso [{aluno[3]}]: ")
    novo_periodo = input(f"Novo período [{aluno[4]}]: ")

    # Mantém valores antigos se o usuário digitar "0"
    novo_nome = aluno[1] if novo_nome == "0" else novo_nome
    nova_data = aluno[2] if nova_data == "0" else nova_data
    novo_curso = aluno[3] if novo_curso == "0" else novo_curso

    if novo_periodo == "0":
        novo_periodo = aluno[4]
    else:
        novo_periodo = int(novo_periodo)

    cursor.execute('''
        UPDATE alunos
        SET nome = ?, data_nascimento = ?, curso = ?, periodo = ?
        WHERE id = ?
    ''', (novo_nome, nova_data, novo_curso, novo_periodo, id_busca))

    conn.commit()
    print("Dados atualizados com sucesso!")

# === DELETE ===
def excluir_aluno(conn):
    cursor = conn.cursor()

    print("\n=== EXCLUIR ALUNO ===")
    id_busca = input("Digite o ID do aluno: ")

    cursor.execute("SELECT * FROM alunos WHERE id = ?", (id_busca,))
    aluno = cursor.fetchone()

    if not aluno:
        print("❌ Aluno não encontrado.")
        return

    cursor.execute("DELETE FROM alunos WHERE id = ?", (id_busca,))
    conn.commit()
    print("Aluno removido com sucesso!")


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
            excluir_aluno(conn)
        elif opcao == "5":
            print("Saindo do sistema...")
            conn.close()
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
