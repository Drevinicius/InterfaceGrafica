import tkinter as tk
from tkinter import ttk
import main_setting as dt

def cursos_fornecidos():
    def exibirCursos(minicurso):
        text_cursos_display.delete(1.0, tk.END)
        i = 1
        if minicurso:
            lista_minicursos_str = "Minicursos:\n\n"
            for mini in minicurso:
                lista_minicursos_str += f"{mini[0]} - {mini[1]}\nProfessor: {mini[3]}, sala: {mini[2]}\n\n"
                i+=1
            text_cursos_display.insert(tk.END, lista_minicursos_str)

    tela = tk.Tk()
    tela.title("Minicursos")
    tela.geometry("800x600")
    tela.configure(bg="#c4c0c0")
    tela.resizable(False, False)

    main_frame = tk.Frame(tela, bg="#c4c0c0")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    cursos_display_frame = tk.LabelFrame(main_frame, text="Minicursos Disponíveis", bg="#c4c0c0", padx=10, pady=10)
    cursos_display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)

    text_scroll_frame = tk.Frame(cursos_display_frame)
    text_scroll_frame.pack(fill=tk.BOTH, expand=True)

    text_cursos_display = tk.Text(text_scroll_frame,
                                  wrap=tk.WORD,
                                  bg="white", fg="#333",
                                  relief="sunken", bd=1, padx=5, pady=5,
                                  font=("Arial", 10))

    scrollbar_y = ttk.Scrollbar(text_scroll_frame, orient=tk.VERTICAL, command=text_cursos_display.yview)
    text_cursos_display.config(yscrollcommand=scrollbar_y.set)

    text_cursos_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 10))
    style.configure("TEntry", font=("Arial", 11))
    style.configure("TLabel", background="#c4c0c0", foreground="#333")
    style.configure("TFrame", background="#c4c0c0")
    style.configure("TMenubutton", font=("Arial", 11), padding=[10, 5, 10, 5])

    conn, cursor = dt.conectar_db()
    minicurso_oficinas = dt.consultarMinicursos(cursor)

    exibirCursos(minicurso_oficinas)

    tela.mainloop()
    dt.fechar_conexao(conn)

if __name__ == "__main__":
    cursos_fornecidos()