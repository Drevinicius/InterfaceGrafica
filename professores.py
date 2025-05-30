import tkinter as tk
from tkinter import ttk
import main_setting as bk

conn, cursor = bk.conectar_db()
professores = bk.consultarProfessores(cursor)


def professor():
    def carregar_e_exibir_professores_local():
        if professores:
            lista_professores_str = "Professores Cadastrados:\n\n"
            for prof in professores:
                lista_professores_str += f"{prof[0]} - Nome: {prof[1]}\nEmail: {prof[2]}\n\n"
            label_professores_display.config(text=lista_professores_str)
        else:
            label_professores_display.config(text="Nenhum professor na lista local.")

    tela = tk.Tk()
    tela.title("Professores ministrantes")
    tela.geometry("800x600")
    tela.configure(bg="#c4c0c0")
    tela.resizable(False, False)

    main_frame = tk.Frame(tela, bg="#c4c0c0")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    top_frame = tk.Frame(main_frame, bg="#c4c0c0", pady=10)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    form_frame = tk.LabelFrame(main_frame, text="Exemplo de Formulário", bg="#c4c0c0", padx=15, pady=15)
    form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10, expand=False)

    display_area_frame = tk.Frame(main_frame, bg="#c4c0c0", padx=10, pady=10)
    display_area_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)

    professores_frame = tk.LabelFrame(display_area_frame, text="Professores Cadastrados", bg="#c4c0c0", padx=10,
                                      pady=10)
    professores_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

    label_professores_display = tk.Label(professores_frame, text="Carregando professores...",
                                         bg="white", fg="#333", justify=tk.LEFT, anchor="nw",
                                         relief="sunken", bd=1, padx=5, pady=5,
                                         wraplength=350,
                                         font=("Arial", 10))
    label_professores_display.pack(fill=tk.BOTH, expand=True)

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10))
    style.configure("TEntry", font=("Arial", 11))
    style.configure("TLabel", background="#c4c0c0", foreground="#333")
    style.configure("TFrame", background="#c4c0c0")
    style.configure("TMenubutton", font=("Arial", 11), padding=[10, 5, 10, 5])

    carregar_e_exibir_professores_local()

    tela.mainloop()
    bk.fechar_conexao(conn)


if __name__ == "__main__":  # Teste manual
    professor()