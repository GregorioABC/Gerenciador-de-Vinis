import pandas as pd
from openpyxl import load_workbook
import os

ARQUIVO = "planilha.xlsx"

def inicializar_planilha():
    if not os.path.exists(ARQUIVO):
        df = pd.DataFrame(columns=["Nome","Artista", "Preço", "Disponibilidade", "Imagem"])
        df.to_excel(ARQUIVO, index=False)

def salvar_disco(disco):
    df = pd.read_excel(ARQUIVO)
    novo = pd.DataFrame([disco])
    df = pd.concat([df, novo], ignore_index=True)
    df.to_excel(ARQUIVO, index=False)

def carregar_discos():
    if os.path.exists(ARQUIVO):
        return pd.read_excel(ARQUIVO)
    return pd.DataFrame(columns=["Nome","Artista", "Preço", "Disponibilidade", "Imagem"])

def excluir_disco(indice):
    df = carregar_discos()
    df = df.drop(index=indice)
    df.to_excel(ARQUIVO, index=False)
