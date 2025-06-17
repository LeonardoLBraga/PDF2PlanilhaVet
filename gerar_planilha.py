import pdfplumber
import pandas as pd
from datetime import datetime
import re
import os
import sys

# TAMANHO_PADRAO_A4 = (595.28, 841.89)
TAMANHO_ESPERADO = (841.92, 1191.12)

dados = []
pasta_pdfs = "arquivos"
pasta_saida = "planilhas_geradas"
 

def verifica_tamanho_da_pagina(primeira_pagina):
    largura = primeira_pagina.width
    altura = primeira_pagina.height

    # print("Largura: ", largura, "\nAltura: ", altura)

    # tolerância de margem, para pequenas variações
    margem = 5

    if (abs(largura - TAMANHO_ESPERADO[0]) > margem or
        abs(altura - TAMANHO_ESPERADO[1]) > margem):
        print(
            f"Erro: o tamanho da página é {largura:.2f} x {altura:.2f}, "
            f"mas o esperado era {TAMANHO_ESPERADO[0]} x {TAMANHO_ESPERADO[1]}"
        )
        sys.exit(1)


def extrair_dados_por_posicao(pagina):
    # (x0, y0, x1, y1) => (esquerda, topo, direita, base)
    
    # Coordenadas para o nome do paciente
    caixa_paciente = (50, 150, 348, 175)
    texto_paciente = pagina.within_bbox(caixa_paciente).extract_text()

    # Coordenadas para a data
    caixa_data = (620, 150, 800, 250)
    texto_data = pagina.within_bbox(caixa_data).extract_text()

    # Coordenadas para o (título) procedimento do exame
    caixa_procedimento = (50, 280, 800, 330)
    texto_procedimento = pagina.within_bbox(caixa_procedimento).extract_text()

    # (opcional) Salvar imagem para debug
    pagina.to_image().draw_rect(caixa_paciente).draw_rect(caixa_data).draw_rect(caixa_procedimento).save("debug_posicoes.png")

    texto_paciente = re.sub(r"Paciente:\s*", "", texto_paciente).strip().splitlines()[0] if texto_paciente else ""
    data = re.sub(r"Data do exame:\s*", "", texto_data).strip().splitlines()[0] if texto_data else ""
    procedimento = texto_procedimento.strip().splitlines()[0] if texto_procedimento else ""
    
    print("Paciente: " + texto_paciente, " - Data: " + data, " - Procedimento: " + procedimento)

    return texto_paciente, data, procedimento

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

            verifica_tamanho_da_pagina(primeira_pagina)

            nome_paciente, data_exame, procedimento = extrair_dados_por_posicao(primeira_pagina)
            dados.append({
                "Exames": f"{procedimento} - {nome_paciente}",
                "Data": data_exame,
                "Valor": ""
            })

    df = pd.DataFrame(dados)
    os.makedirs(pasta_saida, exist_ok=True)

    data_hoje = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = f"{data_hoje}.xlsx"
    caminho_completo = os.path.join(pasta_saida, nome_arquivo)

    df.to_excel(caminho_completo, index=False)
    print(f"Planilha salva em: {caminho_completo}")

except Exception as e:
    print(f"Erro: {str(e)}")
    sys.exit(1)
