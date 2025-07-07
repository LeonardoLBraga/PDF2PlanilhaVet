"""
Funções utilitárias para extração e normalização de dados de arquivos PDF veterinários.

Inclui funções para:
- Normalizar texto.
- Extrair nome do paciente e data do exame.
- Verificar tamanho de página.
- Ler e mapear valores de exames a partir de um PDF de referência.
- Buscar valores por procedimentos com sinônimos e similaridade.
- Detectar presença de tabelas.
- Calcular total de valores extraídos.
"""

import os
import pandas as pd
from datetime import datetime
import re
import pdfplumber
import difflib
import unicodedata

TAMANHO_ESPERADO = (841.92, 1191.12)

SINONIMOS = {
    "alt": "transaminase piruvica - alt",
    "tgp": "transaminase piruvica - alt",
    "alt tgp": "transaminase piruvica - alt",
    "ast": "transaminase oxalacetica - ast",
    "got": "transaminase oxalacetica - ast",
    "gama gt": "ggt - gama glutamil transferase",
    "ggt": "ggt - gama glutamil transferase",
    "ureia": "ureia",
    "creatinina": "creatinina",
    "colesterol": "colesterol total",
    "triglicerideos": "triglicerides",
    "fosfatase": "fosfatase alcalina",
    "raspado de pele": "raspado pele",
    "hemoparasitas": "pesquisa hematozoarios",
}


def normalizar(texto):
    """
    Remove acentos, caracteres especiais e deixa o texto em minúsculo.

    Args:
        texto (str): Texto original.

    Returns:
        str: Texto normalizado.
    """
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8")
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    texto = texto.strip()
    return texto


def extrair_nome_e_data(pagina):
    """
    Extrai o nome do paciente e a data do exame a partir de regiões específicas da página.

    Args:
        pagina: Objeto da página (pdfplumber.Page).

    Returns:
        tuple[str, str]: Nome do paciente e data do exame.
    """
    caixa_paciente = (50, 150, 348, 175)
    caixa_data = (620, 150, 800, 250)

    texto_paciente = pagina.within_bbox(caixa_paciente).extract_text()
    texto_data = pagina.within_bbox(caixa_data).extract_text()

    nome = re.sub(r"Paciente:\s*", "", texto_paciente).strip().splitlines()[0] if texto_paciente else ""
    data = re.sub(r"Data do exame:\s*", "", texto_data).strip().splitlines()[0] if texto_data else ""

    print("Paciente: " + texto_paciente, " - Data: " + data)

    return nome, data


def verifica_tamanho_da_pagina(primeira_pagina):
    """
    Verifica se o tamanho da página corresponde ao esperado (A3 retrato).

    Args:
        primeira_pagina: Objeto da página (pdfplumber.Page).

    Returns:
        bool: True se o tamanho for aceitável, False caso contrário.
    """
    largura = primeira_pagina.width
    altura = primeira_pagina.height

    margem = 5

    if (abs(largura - TAMANHO_ESPERADO[0]) > margem or
        abs(altura - TAMANHO_ESPERADO[1]) > margem):
        print(
            f"Erro: o tamanho da página é {largura:.2f} x {altura:.2f}, "
            f"mas o esperado era {TAMANHO_ESPERADO[0]} x {TAMANHO_ESPERADO[1]}"
        )
        return False
    return True


def get_valores_do_pdf(caminho_valores):
    """
    Lê um PDF de referência e extrai os valores monetários por nome de exame.

    Args:
        caminho_valores (str): Caminho do PDF com a tabela de valores.

    Returns:
        dict: Dicionário mapeando nomes de exames para valores (ex: "R$ 50,00").
    """
    exames_dict = {}
    with pdfplumber.open(caminho_valores) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row or len(row) < 4:
                        continue

                    nome = row[0].strip() if row[0] else ""
                    valor = row[3].strip() if row[3] else ""

                    if nome and "R$" in valor:
                        exames_dict[nome] = valor
    return exames_dict


def get_valor_by_procedimento(procedimento, valores):
    """
    Obtém o valor associado a um procedimento, usando sinônimos ou similaridade.

    Args:
        procedimento (str): Nome do exame a buscar.
        valores (dict): Dicionário com nomes de exames e seus respectivos valores.

    Returns:
        str: Valor encontrado (ex: "R$ 45,00") ou string vazia se não encontrado.
    """
    procedimento_norm = normalizar(procedimento)

    if procedimento_norm in SINONIMOS:
        sinonimo = SINONIMOS[procedimento_norm]
        if sinonimo in valores:
            valor = valores[sinonimo]
            print(f"Match via sinônimo: {procedimento_norm} → {sinonimo} → {valor}")
            return valor
        else:
            print(f"Sinônimo '{sinonimo}' não encontrado em valores: {list(valores.keys())}")

    candidatos = difflib.get_close_matches(procedimento_norm, valores.keys(), n=1, cutoff=0.6)

    if candidatos:
        match = candidatos[0]
        valor = valores[match]
        print(f"Match por similaridade: {procedimento_norm} → {match} → {valor}")
        return valor
    else:
        print(f"Nenhuma correspondência encontrada para: {procedimento} ({procedimento_norm})")
        return ""


def verifica_se_tem_tabela(caminho_pdf):
    """
    Verifica se há alguma tabela presente no PDF.

    Args:
        caminho_pdf (str): Caminho para o arquivo PDF.

    Returns:
        bool: True se alguma tabela for encontrada, False caso contrário.
    """
    with pdfplumber.open(caminho_pdf) as pdf:
        tem_tabela = any(page.extract_tables() for page in pdf.pages)
        if tem_tabela:
            return True
    return False


def calcula_total(dados_da_planilha):
    """
    Calcula o total dos valores monetários contidos nos dados extraídos e adiciona uma linha "TOTAL".

    Args:
        dados_da_planilha (list[dict]): Lista de dados com as chaves 'Exames', 'Data' e 'Valor'.

    Returns:
        list[dict]: Mesma lista com uma linha adicional indicando o total.
    """
    total = 0

    for item in dados_da_planilha:
        valor_str = item['Valor'].replace('R$', '').replace(',', '.').strip()
        if valor_str:
            try:
                total += float(valor_str)
            except ValueError:
                pass

    total_formatado = f'R$ {total:.2f}'.replace('.', ',')

    dados_da_planilha.append({
        'Exames': 'TOTAL',
        'Data': '',
        'Valor': total_formatado
    })

    print("Total: ", total_formatado)

    return dados_da_planilha


def criar_dataframe_dados(dados_com_total: list[dict]) -> pd.DataFrame:
    """
    Cria um DataFrame principal com os dados extraídos dos PDFs e processados com totais.

    Args:
        dados_com_total (list[dict]): Lista de dicionários contendo os dados dos exames, já processados com totais.

    Returns:
        pd.DataFrame: DataFrame com os dados completos prontos para exportação.
    """
    return pd.DataFrame(dados_com_total)


def gerar_resumo_por_procedimento(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera um resumo com a contagem de procedimentos a partir da coluna 'Exames',
    extraindo apenas o nome do procedimento (parte antes do ' - '). O DataFrame original
    não é modificado.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados completos com a coluna 'Exames'.

    Returns:
        pd.DataFrame: DataFrame com duas colunas: 'Procedimento' e 'Quantidade', representando
                      o total de ocorrências de cada procedimento.
    """
    df_temp = df.copy()
    df_temp['Procedimento'] = df_temp['Exames'].str.split(' - ').str[0]
    resumo = df_temp['Procedimento'].value_counts().reset_index()
    resumo.columns = ['Procedimento', 'Quantidade']
    return resumo


def definir_caminho_arquivo_excel(pasta_saida: str) -> str:
    """
    Define o caminho completo para salvar o arquivo Excel com base na data atual.
    Cria a pasta de saída, se ela ainda não existir.

    Args:
        pasta_saida (str): Caminho da pasta onde o arquivo Excel será salvo.

    Returns:
        str: Caminho completo do arquivo Excel com o nome no formato 'YYYY-MM-DD.xlsx'.
    """
    os.makedirs(pasta_saida, exist_ok=True)
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = f"{data_hoje}.xlsx"
    return os.path.join(pasta_saida, nome_arquivo)


def salvar_planilha_com_abas(df_dados: pd.DataFrame, df_resumo: pd.DataFrame, caminho: str) -> None:
    """
    Salva os dados em um arquivo Excel contendo duas abas:
    - 'Dados completos' com as informações detalhadas dos exames.
    - 'Resumo' com a contagem de procedimentos.

    Args:
        df_dados (pd.DataFrame): DataFrame com os dados completos dos exames.
        df_resumo (pd.DataFrame): DataFrame com o resumo de procedimentos.
        caminho (str): Caminho completo onde o arquivo Excel será salvo.

    Returns:
        None
    """
    with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
        df_dados.to_excel(writer, index=False, sheet_name='Dados completos')
        df_resumo.to_excel(writer, index=False, sheet_name='Resumo')