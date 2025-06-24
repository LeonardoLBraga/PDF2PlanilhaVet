import pdfplumber
import pandas as pd
from datetime import datetime
import os
import sys

from utils.functions import *
from extratores.fabrica import escolher_extrator

dados_da_planilha = []
pasta_pdfs = "arquivos"
pasta_saida = "planilhas_geradas"
caminho_valores = "pdf_valores_exames/valores.pdf"

try:
    # Verifica se a pasta existe
    if not os.path.isdir(pasta_pdfs):
        print(f'Erro: A pasta "{pasta_pdfs}" não foi encontrada.')
        sys.exit(1)

    # Filtra apenas arquivos PDF na pasta
    arquivos_pdf = [f for f in os.listdir(pasta_pdfs) if f.lower().endswith(".pdf")]

    # Verifica se há pelo menos um PDF
    if not arquivos_pdf:
        print(f'Erro: Nenhum arquivo PDF encontrado na pasta "{pasta_pdfs}".')
        sys.exit(1)

    valores_dos_exames_dict = get_valores_do_pdf(caminho_valores)
    valores_normalizados_dict = {
        normalizar(nome_exame): valor_exame
        for nome_exame, valor_exame in valores_dos_exames_dict.items()
    }
    # print(valores_normalizados_dict)

    for arquivo in arquivos_pdf:
        caminho_pdf = os.path.join(pasta_pdfs, arquivo)
        with pdfplumber.open(caminho_pdf) as pdf:
            primeira_pagina = pdf.pages[0]

            if not verifica_tamanho_da_pagina(primeira_pagina):
                continue

            extrator = escolher_extrator(caminho_pdf)

            try:
                linhas = extrator.extrair(primeira_pagina, valores_normalizados_dict)
                dados_da_planilha.extend(linhas)
            except Exception as e:
                print(f"Erro ao extrair dados de {arquivo}: {e}")
                continue

    data_frame_da_planilha = pd.DataFrame(dados_da_planilha)
    os.makedirs(pasta_saida, exist_ok=True)

    data_hoje = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = f"{data_hoje}.xlsx"
    caminho_completo = os.path.join(pasta_saida, nome_arquivo)

    data_frame_da_planilha.to_excel(caminho_completo, index=False)
    print(f"Planilha salva em: {caminho_completo}")
    print("Tudo pronto! Relatório gerado com sucesso.")
    input("Pressione Enter para sair...")

except Exception as e:
    print(f"Erro: {str(e)}")
    sys.exit(1)
