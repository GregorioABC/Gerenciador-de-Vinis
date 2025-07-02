import pandas as pd
import os

ARQUIVO = "planilha.xlsx"

def salvar_disco(disco):
    print(">> Tentando salvar disco...")

    if os.path.exists(ARQUIVO):
        df = pd.read_excel(ARQUIVO)
    else:
        df = pd.DataFrame(columns=["Nome", "Artista", "Gênero", "Preço", "Imagem", "Disponível"])

    novo = {
        "Nome": disco["nome"],
        "Artista": disco["artista"],
        "Gênero": disco["genero"],
        "Preço": disco["preco"],
        "Imagem": disco["imagem"],
        "Disponível": disco["disponivel"]
    }

    novo_df = pd.DataFrame([novo])
    df = pd.concat([df, novo_df], ignore_index=True)

    df.to_excel(ARQUIVO, index=False)
    print(">> Disco salvo com sucesso.")

def ordenar_planilha():
    if os.path.exists(ARQUIVO):
        df = pd.read_excel(ARQUIVO)
        df = df.sort_values(by="Nome")
        df.to_excel(ARQUIVO, index=False)
        print(">> Planilha ordenada.")

def carregar_discos():
    if os.path.exists(ARQUIVO):
        return pd.read_excel(ARQUIVO)
    else:
        return pd.DataFrame(columns=["Nome", "Artista", "Gênero", "Preço", "Imagem", "Disponível"])

def excluir_disco(nome):
    if not os.path.exists(ARQUIVO):
        return
    df = pd.read_excel(ARQUIVO)
    df = df[df["Nome"] != nome]
    df.to_excel(ARQUIVO, index=False)
    print(f">> Disco '{nome}' excluído.")
