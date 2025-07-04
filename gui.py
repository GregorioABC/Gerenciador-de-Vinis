import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
import os
from excel_handler import salvar_disco, carregar_discos, excluir_disco, inicializar_planilha, ordenar_planilha

def iniciar_interface():
    inicializar_planilha()

    janela = tk.Tk()
    janela.title("Gerenciador de Vinis")
    janela.geometry("800x600")
    janela.configure(bg="#f4f4f4")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Segoe UI", 10), padding=6, relief="flat", background="#2d89ef", foreground="white")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)
    style.configure("TLabel", background="#f4f4f4")

    frame = ttk.Frame(janela, padding=20)
    frame.pack(fill="both", expand=True)

    nome = tk.StringVar()
    artista = tk.StringVar()
    preco = tk.StringVar()
    disponibilidade = tk.BooleanVar()
    imagem_path = tk.StringVar()

    ttk.Label(frame, text="Nome do Vinil:").grid(row=0, column=0, sticky="w")
    ttk.Entry(frame, textvariable=nome, width=40).grid(row=0, column=1, pady=5, columnspan=2)

    ttk.Label(frame, text="Nome do Artista:").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame, textvariable=artista, width=40).grid(row=1, column=1, pady=5, columnspan=2)

    ttk.Label(frame, text="Preço:").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame, textvariable=preco, width=20).grid(row=2, column=1, pady=5)

    ttk.Checkbutton(frame, text="Disponível", variable=disponibilidade).grid(row=3, column=0, pady=5, sticky="w")

    def escolher_imagem():
        caminho = filedialog.askopenfilename(title="Escolher imagem", filetypes=[("Imagens", "*.jpg *.png *.jpeg")])
        if caminho:
            imagem_path.set(caminho)

    ttk.Button(frame, text="Selecionar Imagem", command=escolher_imagem).grid(row=3, column=1, pady=5)

    def salvar():
        if not nome.get() or not preco.get():
            messagebox.showerror("Erro", "Nome e preço são obrigatórios.")
            return
        disco = {
            "Nome": nome.get(),
            "Artista":artista.get(),
            "Preço": preco.get(),
            "Disponibilidade": "Sim" if disponibilidade.get() else "Não",
            "Imagem": imagem_path.get()
        }
        salvar_disco(disco)
        ordenar_planilha()
        messagebox.showinfo("Salvo", "Disco salvo com sucesso!")
        nome.set("")
        artista.set("")
        preco.set("")
        disponibilidade.set(False)
        imagem_path.set("")
        atualizar_tabela()

    ttk.Button(frame, text="Salvar Disco", command=salvar).grid(row=4, column=1, pady=10)

    # Tabela
    tabela = ttk.Treeview(frame, columns=("Nome","Artista", "Preço", "Disponibilidade", "Imagem"), show="headings")
    for col in ("Nome","Artista", "Preço", "Disponibilidade", "Imagem"):
        tabela.heading(col, text=col)
        tabela.column(col, minwidth=50, width=120)
    tabela.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=10)

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=5, column=3, sticky="ns")

    def atualizar_tabela():
        for i in tabela.get_children():
            tabela.delete(i)
        df = carregar_discos()
        for i, row in df.iterrows():
            tabela.insert("", "end", iid=i, values=list(row))

    def deletar_disco():
        selecionado = tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para excluir.")
            return
        indice = int(selecionado[0])
        excluir_disco(indice)
        atualizar_tabela()
        messagebox.showinfo("Excluído", "Disco excluído com sucesso.")

    ttk.Button(frame, text="Excluir Selecionado", command=deletar_disco).grid(row=6, column=0, columnspan=2)
    
    def mostrar_imagem(event):
        selecionado = tabela.selection()
        if selecionado:
            indice = int(selecionado[0])
            df = carregar_discos()
            caminho_imagem = df.loc[indice, "Imagem"]
            if caminho_imagem and os.path.exists(caminho_imagem):
                img = Image.open(caminho_imagem)
                img.thumbnail((200, 200))
                img_tk = ImageTk.PhotoImage(img)
                label_imagem.configure(image=img_tk)
                label_imagem.image = img_tk  
            else:
                label_imagem.configure(image="")
                label_imagem.image = None

    tabela.bind("<<TreeviewSelect>>", mostrar_imagem)
    label_imagem = ttk.Label(frame)
    label_imagem.grid(row=0, column=4, rowspan=6, padx=10)

    atualizar_tabela()
    janela.mainloop()
