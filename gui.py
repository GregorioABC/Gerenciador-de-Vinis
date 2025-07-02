import tkinter as tk
from tkinter import filedialog, messagebox
from excel_handler import salvar_disco, ordenar_planilha, carregar_discos, excluir_disco
from tkinter import ttk 

def iniciar_interface():
    #personalização do tkinter
    janela = tk.Tk()
    janela.title("Gerenciador de Vinis")
    janela.configure(bg="white")
    janela.geometry("500x500")

    titulo = ttk.Label(janela, text="Gerenciador de Vinis", font=("Helvetica", 18))
    titulo.pack(pady=10)

    nome_var = tk.StringVar()
    artista_var = tk.StringVar()
    genero_var = tk.StringVar()
    preco_var = tk.StringVar()
    imagem_var = tk.StringVar()
    disponibilidade_var = tk.BooleanVar(value=True)

    def salvar():
        dados = {
            "nome": nome_var.get(),
            "artista": artista_var.get(),
            "genero": genero_var.get(),
            "preco": preco_var.get(),
            "imagem": imagem_var.get(),
            "disponivel": disponibilidade_var.get()
        }
        print(">> Dados recebidos do formulário:", dados)
        salvar_disco(dados)
        ordenar_planilha()
        messagebox.showinfo("Sucesso", "Disco salvo!")
        limpar_campos()

    def limpar_campos():
        nome_var.set("")
        artista_var.set("")
        genero_var.set("")
        preco_var.set("")
        imagem_var.set("")
        disponibilidade_var.set(True)

    def selecionar_imagem():
        caminho = filedialog.askopenfilename()
        if caminho:
            imagem_var.set(caminho)

    def mostrar_discos():
        nova_janela = tk.Toplevel()
        nova_janela.title("Vinis Salvos")

        df = carregar_discos()

        for idx, row in df.iterrows():
            frame = tk.Frame(nova_janela, pady=2)
            frame.pack(fill="x")

            info = f"{row['Nome']} - {row['Artista']} | {row['Gênero']} | R$ {row['Preço']} | {'Disponível' if row['Disponível'] else 'Indisponível'}"
            tk.Label(frame, text=info, anchor="w").pack(side="left", expand=True, fill="x")

            tk.Button(frame, text="Excluir", command=lambda nome=row['Nome']: excluir_e_atualizar(nome, nova_janela)).pack(side="right")

    def excluir_e_atualizar(nome, janela):
        excluir_disco(nome)
        for widget in janela.winfo_children():
            widget.destroy()
        mostrar_discos()

    # ----- Layout principal -----
    tk.Label(janela, text="Nome do Disco").pack()
    tk.Entry(janela, textvariable=nome_var).pack()

    tk.Label(janela, text="Artista").pack()
    tk.Entry(janela, textvariable=artista_var).pack()

    tk.Label(janela, text="Gênero").pack()
    tk.Entry(janela, textvariable=genero_var).pack()

    tk.Label(janela, text="Preço").pack()
    tk.Entry(janela, textvariable=preco_var).pack()

    tk.Button(janela, text="Selecionar Imagem", command=selecionar_imagem).pack()

    tk.Checkbutton(janela, text="Disponível", variable=disponibilidade_var).pack()

    tk.Button(janela, text="Salvar Disco", command=salvar).pack(pady=10)
    tk.Button(janela, text="Mostrar Vinis", command=mostrar_discos).pack(pady=5)

    janela.mainloop()
