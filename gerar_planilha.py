"""
Script principal para gerar planilha Excel a partir de arquivos PDF com exames veterinários.

Este script:
- Lê PDFs da pasta `arquivos/`;
- Verifica tamanho e estrutura dos PDFs;
- Usa extratores personalizados para obter dados dos exames;
- Calcula o total dos valores extraídos;
- Gera uma planilha `.xlsx` na pasta `planilhas_geradas/`.

Pré-requisitos:
- PDF de referência com valores em `pdf_valores_exames/valores.pdf`.
- PDFs de exames organizados em `arquivos/`.
"""

import pdfplumber
import os
import sys

from utils.functions import *
from extratores.fabrica import escolher_extrator

dados_da_planilha = []
pasta_pdfs = "arquivos"
pasta_saida = "planilhas_geradas"
caminho_valores = "pdf_valores_exames/valores.pdf"

try:
    # Verifica se a pasta de PDFs existe
    if not os.path.isdir(pasta_pdfs):
        print(f'Erro: A pasta "{pasta_pdfs}" não foi encontrada.')
        sys.exit(1)

    # Lista apenas arquivos PDF
    arquivos_pdf = [f for f in os.listdir(pasta_pdfs) if f.lower().endswith(".pdf")]

    if not arquivos_pdf:
        print(f'Erro: Nenhum arquivo PDF encontrado na pasta "{pasta_pdfs}".')
        sys.exit(1)

    # Lê e normaliza os valores do PDF de referência
    valores_dos_exames_dict = get_valores_do_pdf(caminho_valores)
    valores_normalizados_dict = {
        normalizar(nome_exame): valor_exame
        for nome_exame, valor_exame in valores_dos_exames_dict.items()
    }

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

    dados_da_planilha_com_total = calcula_total(dados_da_planilha)
    data_frame_da_planilha = criar_dataframe_dados(dados_da_planilha_com_total)
    df_resumo = gerar_resumo_por_procedimento(data_frame_da_planilha)
    caminho_completo = definir_caminho_arquivo_excel(pasta_saida)
    salvar_planilha_com_abas(data_frame_da_planilha, df_resumo, caminho_completo)

    print(f"Planilha salva em: {caminho_completo}")
    print("Tudo pronto! Relatório gerado com sucesso.")
    input("Pressione Enter para sair...")


except Exception as e:
    print(f"Erro: {str(e)}")
    sys.exit(1)
