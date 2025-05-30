import tkinter as tk
from tkinter import messagebox
import main_setting as dt

def nova_janela():
    conn, cursor = dt.conectar_db()  # faz conexão com banco de dados que está em outro arquivo
    def enviar_formulario():
        if conn and cursor:
            nome = entry_nome.get()
            curso_selecionado = var_curso.get()

            dt.inserirAluno(conn, cursor, nome, curso_selecionado)
            messagebox.showinfo("Sucesso", "Dados enviados com sucesso! Verifique o console.")

            entry_nome.delete(0, tk.END)
            nova.destroy()
            dt.fechar_conexao(conn)
        else:
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados.")

    nova = tk.Toplevel()
    nova.title("Formulário de Cadastro de Aluno")
    nova.geometry("500x450")
    nova.resizable(False, False)
    nova.configure(bg="#F0F0F0")

    form_frame = tk.Frame(nova, bg="white", padx=20, pady=20, relief="groove", bd=2)
    form_frame.pack(pady=30, padx=30, expand=True)

    label_titulo = tk.Label(form_frame, text="Cadastro de Aluno", font=("Arial", 16, "bold"), bg="white", fg="#333333")
    label_titulo.grid(row=0, column=0, columnspan=2, pady=15)

    label_nome = tk.Label(form_frame, text="Nome Completo:", font=("Arial", 10), bg="white", fg="#555555")
    label_nome.grid(row=1, column=0, sticky="w", pady=5)
    entry_nome = tk.Entry(form_frame, width=40, font=("Arial", 10), bd=1, relief="solid")
    entry_nome.grid(row=1, column=1, sticky="we", pady=5, padx=5)


    label_curso = tk.Label(form_frame, text="Curso:", font=("Arial", 10), bg="white", fg="#555555")
    label_curso.grid(row=5, column=0, sticky="w", pady=5)

    # Verifica se a conexão foi bem-sucedida antes de consultar o DB
    if conn and cursor:
        cursos_db = dt.consultarMinicursos(cursor)
    else:
        messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados para carregar cursos.")
        cursos_db = []  # Garante que a lista não seja None em caso de erro

    lista_de_cursos = ["Selecione um curso"]  # Adiciona uma opção padrão
    for row in cursos_db:
        lista_de_cursos.append(row[1])  # row[1] é o título do minicurso/oficina

    var_curso = tk.StringVar(nova)
    var_curso.set(lista_de_cursos[0])  # Define o valor inicial

    option_menu_curso = tk.OptionMenu(form_frame, var_curso, *lista_de_cursos)
    option_menu_curso.grid(row=5, column=1, sticky="we", pady=5, padx=5)
    option_menu_curso.config(width=38)

    button_enviar = tk.Button(form_frame, text="Enviar Cadastro", command=enviar_formulario,
                              bg="#fa8c05", fg="black", font=("Arial", 12, "bold"),
                              padx=10, pady=5, relief="raised", bd=2)
    button_enviar.grid(row=6, column=0, columnspan=2, pady=20)


    nova.mainloop()
if __name__ == "__main__":
    nova_janela()