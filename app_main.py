import tkinter as tk
from tkinter import ttk
import main_setting as dt
from janela import nova_janela
from cursos import cursos_fornecidos
from professores import professor

conn, cursor = dt.conectar_db()

def realizar_pesquisa_por_selecao(selected_item):
    text_resultados.delete(1.0, tk.END)
    oficinas_com_alunos = dt.consultarMinicursos(cursor)
    if selected_item == "Todos os cursos":
        text_resultados.insert(tk.END, "Exibindo todos os itens:\n\n")
        for item in db_itens_pesquisa[1:]:
            text_resultados.insert(tk.END, f"- {item}\n")

    else:
        oficinas_com_alunos = dt.consultarInscricoes(cursor)
        # A lógica de pesquisa para um item específico já selecionado
        encontrados = []
        for item in oficinas_com_alunos:
            if selected_item == item[2]:  # Compara diretamente o item selecionado
                encontrados.append(item[1])

        if encontrados:
            text_resultados.insert(tk.END, f"Alunos cadastrados em '{selected_item}':\n\n")
            for item in encontrados:
                text_resultados.insert(tk.END, f"- {item}\n")
        else:
            text_resultados.insert(tk.END, f"{selected_item} sem aluno cadastrado.\n")

tela = tk.Tk()
tela.title("ENCOSIS 2025")
tela.resizable(False, False)
tela.configure(bg="#c4c0c0")

# Frame superior para os botões e o OptionMenu de pesquisa
top_frame = tk.Frame(tela, bg="#c4c0c0", pady=10)
top_frame.pack(side=tk.TOP, fill=tk.X)

# Frame para os resultados da pesquisa
bottom_frame = tk.Frame(tela, bg="#fa8c05", padx=20, pady=20)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Botões de navegação
btn_esquerdo = ttk.Button(top_frame, text="Novo cadastro", command=nova_janela)
btn_esquerdo.pack(side=tk.LEFT, padx=20, pady=10)

btn_direito = ttk.Button(top_frame, text="Professores", command=professor)
btn_direito.pack(side=tk.LEFT, padx=20, pady=10)

btn_cursos = ttk.Button(top_frame, text="Minicursos", command=cursos_fornecidos)
btn_cursos.pack(side=tk.LEFT, padx=20, pady=10)

search_group_frame = tk.Frame(top_frame, bg="#c4c0c0")
search_group_frame.pack(side=tk.RIGHT, padx=20, pady=10)

label_pesquisar_text = tk.Label(search_group_frame, text="Selecionar Item:", font=("Arial", 9, "bold"), bg="#c4c0c0",
                                fg="#333")
label_pesquisar_text.pack(side=tk.TOP, anchor="e", padx=5)

aux = dt.consultarMinicursos(cursor)
db_itens_pesquisa = []
for i in aux:
    db_itens_pesquisa.append(i[1])

var_selecao_pesquisa = tk.StringVar(tela)
var_selecao_pesquisa.set(db_itens_pesquisa[0])

option_menu_pesquisa = ttk.OptionMenu(
    search_group_frame,
    var_selecao_pesquisa,
    var_selecao_pesquisa.get(),
    *db_itens_pesquisa,
    command=realizar_pesquisa_por_selecao
)
option_menu_pesquisa.pack(side=tk.LEFT, padx=5)
option_menu_pesquisa.config(width=25)

label_resultados = tk.Label(bottom_frame, text="Resultados da Seleção:", font=("Arial", 12, "bold"), bg="#fa8c05",
                            fg="#333")
label_resultados.pack(side=tk.TOP, anchor="w", pady=10)

text_resultados_frame = tk.Frame(bottom_frame)
text_resultados_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

scrollbar_y = ttk.Scrollbar(text_resultados_frame, orient=tk.VERTICAL)
text_resultados = tk.Text(text_resultados_frame, wrap=tk.WORD, yscrollcommand=scrollbar_y.set,
                          font=("Arial", 11), bg="white", fg="#222", relief="sunken", bd=1, padx=10, pady=10)
scrollbar_y.config(command=text_resultados.yview)

text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

style = ttk.Style()
style.configure("TButton", font=("Arial", 10))
style.configure("TEntry", font=("Arial", 11))
style.configure("TLabel", background="#fa8c05", foreground="#333")
style.configure("TFrame", background="#c4c0c0")
style.configure("TMenubutton", font=("Arial", 12), padding=[10, 5, 10, 5])

realizar_pesquisa_por_selecao(var_selecao_pesquisa.get())

tela.mainloop()
dt.fechar_conexao(conn)