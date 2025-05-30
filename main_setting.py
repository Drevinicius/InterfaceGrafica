import sqlite3
import os
from tkinter import messagebox

banco_dados = 'DATABASE.db'


def conectar_db():
    try:
        conn = sqlite3.connect(banco_dados)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        print(f"Conectado ao banco de dados: {banco_dados}")
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None, None

def criar_tabelas(cursor):
    try:
        # Professores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Professores (
                id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')

        # Minicursos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Minicursos (
                id_minicurso INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL UNIQUE,
                sala TEXT NOT NULL,
                ID_professor INTEGER,
                FOREIGN KEY (id_professor) REFERENCES Professores (id_professor) ON DELETE CASCADE
            )
        ''')

        # Alunos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Alunos (
                id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
            )
        ''')


        # Inscricoes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Inscricoes (
                id_inscricao INTEGER PRIMARY KEY AUTOINCREMENT,
                id_aluno INTEGER,
                id_minicurso INTEGER,
                FOREIGN KEY (id_aluno) REFERENCES Alunos (id_aluno) ON DELETE CASCADE,
                FOREIGN KEY (id_minicurso) REFERENCES Minicursos (id_minicurso) ON DELETE CASCADE
            )
        ''')
    except sqlite3.Error as e:
        print(f"Erro ao criar tabelas: {e}")


# Funçoes CRUD do banco de dados
# Função upatade - Todos ok (inserirProfessor, inserirMinicurso, inserirAluno, inscreverAluno)
# Funções de Read - Todos Ok (consultarProfessor, consultarProfessores, consultarAlunos, consultarInscricoes)
def consultarMinicursos(cursor, termo_pesquisa=None):
    """Consulta minicursos, pode filtrar e mostra nome do professor."""
    try:
        if termo_pesquisa:
            termo_pesquisa = f'%{termo_pesquisa}%'
            cursor.execute('''
                SELECT mc.id_minicurso, mc.titulo, mc.sala, p.nome
                FROM minicursos mc
                LEFT JOIN professores p ON mc.ID_professor = p.id_professor
                WHERE mc.titulo LIKE ? OR p.nome LIKE ?
            ''', (termo_pesquisa, termo_pesquisa))
        else:
            cursor.execute('''
                SELECT mc.id_minicurso, mc.titulo, mc.sala, p.nome
                FROM minicursos mc
                LEFT JOIN professores p ON mc.ID_professor = p.id_professor
            ''')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar minicursos: {e}")
        return []

def inserirProfessor(conn, cursor, nome, email): # Função que insere os professores
    """Insere um novo professor."""
    try:
        cursor.execute('INSERT INTO Professores (nome, email) VALUES (?, ?)', (nome, email))
        conn.commit()
        #messagebox.showinfo("Sucesso",f"Professor '{nome}' inserido com sucesso")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        messagebox.showerror("Email já cadastrado", f"Já há cadastro de professor com o email:\n{email}\nCadastro não efetuado")
    except sqlite3.Error as e:
        messagebox.showerror(f"Erro ao inserir professor: {e}","Erro ao inserir o professor\nTente mais tarde")
        return None

def inserirMinicurso(conn, cursor, titulo, sala, id_professor):
    """Insere um novo minicurso."""
    try:
        cursor.execute('''
            INSERT INTO Minicursos (titulo, sala, id_professor)
            VALUES (?, ?, ?)
        ''', (titulo, sala, id_professor))
        conn.commit()
        print(f"Minicurso '{titulo}' inserido com sucesso. ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Erro: Minicurso com título '{titulo}' já existe.")
        return None
    except sqlite3.Error as e:
        print(f"Erro ao inserir minicurso: {e}")
        return None

def inscreverAluno(conn, cursor, id_aluno, id_minicurso):
    """
    Inscreve um aluno em um minicurso.
    Retorna True se a inscrição foi bem-sucedida, False caso contrário.
    """
    try:
        cursor.execute('''
            INSERT INTO Inscricoes (id_aluno, id_minicurso)
            VALUES (?, ?)
        ''', (id_aluno, id_minicurso))
        conn.commit()
        print(f"Aluno ID {id_aluno} inscrito no Minicurso ID {id_minicurso} com sucesso.")
        return True
    except sqlite3.IntegrityError as e:
        # Captura erro se o aluno já estiver inscrito no minicurso
        print(
            f"Erro: Aluno ID {id_aluno} já está inscrito no Minicurso ID {id_minicurso} ou IDs inválidos. Detalhes: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Erro ao inscrever aluno no minicurso: {e}")
        return False

def inserirAluno(conn, cursor, nome, curso_selecionado='Não selecionado'):
    try:
        id_minicurso = consultarMinicursos(cursor, curso_selecionado)[0][0]
        cursor.execute('''
            INSERT INTO alunos (nome)
            VALUES (?)
        ''', (nome,))
        conn.commit()
        id_aluno_add = cursor.lastrowid
        inscreverAluno(conn, cursor, id_aluno_add, id_minicurso)
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao inserir aluno: {e}")
        messagebox.showerror("Erro de cadastro", "CPF ou Matricula já registrado")
        return None

def consultarProfessores(cursor):
    """Consulta todos os professores."""
    cursor.execute('SELECT id_professor, nome, email FROM Professores')
    return cursor.fetchall()

def consultarProfessor(cursor, id):
    """Consulta o professor por nome."""
    cursor.execute('''SELECT id_professor, nome, email FROM Professores WHERE id_professor LIKE ?''', (id,))
    return cursor.fetchall()

def consultarAluno(cursor, id_aluno):
    """Consulta alunos na tabela."""
    try:
        if id_aluno:
            cursor.execute('''
                SELECT id_aluno, nome FROM Alunos WHERE id_aluno LIKE ?''', (id_aluno,))
        else:
            cursor.execute('SELECT id, nome FROM Alunos')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar alunos: {e}")
        return []

def consultarAlunos(cursor):
    cursor.execute('''SELECT * FROM Alunos''')
    return cursor.fetchall()

def consultarInscricoes(cursor, id_aluno=None):
    """Consulta inscrições de alunos em minicursos."""
    try:
        if id_aluno:
            cursor.execute('''
                SELECT ins.id_inscricao, a.nome, mc.titulo
                FROM Inscricoes ins
                JOIN Alunos a ON ins.id_aluno = a.id_aluno
                JOIN Minicursos mc ON ins.id_minicurso = mc.id_minicurso
                WHERE a.id_aluno = ?
            ''', (id_aluno,))
        else:
            cursor.execute('''
                SELECT Inscricoes.id_inscricao, a.nome, mc.titulo
                FROM Inscricoes
                JOIN Alunos a ON Inscricoes.id_aluno = a.id_aluno
                JOIN Minicursos mc ON Inscricoes.id_minicurso = mc.id_minicurso
            ''')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao consultar inscrições em minicursos: {e}")
        return []

def fechar_conexao(conn):
    """Fecha a conexão com o banco de dados."""
    if conn:
        conn.close()
        print("Conexão com o banco de dados fechada.")


if __name__ == "__main__":
    messagebox.showwarning("Teste Manual", "Foi dado inicio ao teste manual")
    if os.path.exists(banco_dados):
        os.remove(banco_dados)
    conn, cursor = conectar_db()
    if conn and cursor:
        criar_tabelas(cursor)

        inserirProfessor(conn, cursor,"João Pedro", "joao.pedroo@gmail.com")
        inserirProfessor(conn, cursor, "Ana Clara", "ana.clara@gmail.com")
        inserirProfessor(conn, cursor, "Mariana Costa", "mariana.costa@gmail.com")
        inserirProfessor(conn, cursor, "Rafael Almeida", "rafael.almeida@gmail.com")
        inserirProfessor(conn, cursor, "Fernanda Lima", "fernada.lima@gmail.com")

        inserirMinicurso(conn, cursor, "Introdução ao Tricô e Crochê", "A-12", 1)
        inserirMinicurso(conn, cursor, "Libras: Conversação básica", "A-13", 2)
        inserirMinicurso(conn, cursor, "Criação de conteúdo para as redes sociais", "A-14", 3)
        inserirMinicurso(conn, cursor, "Programação com python para iniciantes", "A-15", 4)
        inserirMinicurso(conn, cursor, "Finanças pessoais descomplicadas", "A-16", 5)

        inserirAluno(conn, cursor, "Lucas Pereira", "Programação com python para iniciantes")
        inserirAluno(conn, cursor, "Beatriz Santos", "Libras: Conversação básica")
        inserirAluno(conn, cursor, "Gabriel Rodrigues", "Finanças pessoais descomplicadas")
        inserirAluno(conn, cursor, "Isabela Fernandes", "Programação com python para iniciantes")
        inserirAluno(conn, cursor, "Matheus Souza", "Criação de conteúdo para as redes sociais")
        inserirAluno(conn, cursor, "Laura Martins", "Programação com python para iniciantes")
        inserirAluno(conn, cursor, "Pedro Herique", "Introdução ao Tricô e Crochê")
        inserirAluno(conn, cursor, "Juliana Gomes", "Libras: Conversação básica")
        inserirAluno(conn, cursor, "Daniel Ribeiro", "Programação com python para iniciantes")
        inserirAluno(conn, cursor, "Sofia Carvalho", "Finanças pessoais descomplicadas")

        fechar_conexao(conn)
    else:
        print("Não foi possível estabelecer conexão com o banco de dados.")

    print(f"\nArquivo gerado {banco_dados}")
