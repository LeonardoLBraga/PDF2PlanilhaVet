import pdfplumber
import pandas as pd
from datetime import datetime
import os
import sys

from functions import *

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

    for arquivo in arquivos_pdf:
        caminho_pdf = os.path.join(pasta_pdfs, arquivo)
        with pdfplumber.open(caminho_pdf) as pdf:
            primeira_pagina = pdf.pages[0]

            if not verifica_tamanho_da_pagina(primeira_pagina):
                continue

            nome_paciente, data_exame, procedimento = extrair_dados_por_posicao(primeira_pagina)

            valor = get_valor_by_procedimento(procedimento, caminho_valores)

            dados_da_planilha.append({
                "Exames": f"{procedimento} - {nome_paciente}",
                "Data": data_exame,
                "Valor": valor
            })

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
