import re
import pdfplumber
import difflib
import unicodedata

# TAMANHO_PADRAO_A4 = (595.28, 841.89)
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
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8")
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9\s]", "", texto)
    texto = texto.strip()
    return texto


def extrair_nome_e_data(pagina):
    caixa_paciente = (50, 150, 348, 175)
    caixa_data = (620, 150, 800, 250)

    texto_paciente = pagina.within_bbox(caixa_paciente).extract_text()
    texto_data = pagina.within_bbox(caixa_data).extract_text()

    nome = re.sub(r"Paciente:\s*", "", texto_paciente).strip().splitlines()[0] if texto_paciente else ""
    data = re.sub(r"Data do exame:\s*", "", texto_data).strip().splitlines()[0] if texto_data else ""

    print("Paciente: " + texto_paciente, " - Data: " + data)

    return nome, data


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
        return False
    return True


def get_valores_do_pdf(caminho_valores):
    exames_dict = {}
    with pdfplumber.open(caminho_valores) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Ignorar linhas vazias ou com menos de 2 colunas úteis
                    if not row or len(row) < 4:
                        continue

                    nome = row[0].strip() if row[0] else ""
                    valor = row[3].strip() if row[3] else ""

                    # Validar: nome e valor devem existir e valor deve conter "R$"
                    if nome and "R$" in valor:
                        exames_dict[nome] = valor
    return exames_dict


def get_valor_by_procedimento(procedimento, valores):
    procedimento_norm = normalizar(procedimento)

    # Tenta encontrar sinônimo exato
    if procedimento_norm in SINONIMOS:
        chave_certa = normalizar(SINONIMOS[procedimento_norm])
        if chave_certa in valores:
            valor = valores[chave_certa]
            print(f"Match via sinônimo: {procedimento_norm} → {chave_certa} → {valor}")
            return valor

    # Se não houver sinônimo, tenta por similaridade
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
    with pdfplumber.open(caminho_pdf) as pdf:
        tem_tabela = any(page.extract_tables() for page in pdf.pages)
        if tem_tabela:
            return True
    return False


def calcula_total(dados_da_planilha):
    total = 0

    for item in dados_da_planilha:
        valor_str = item['Valor'].replace('R$', '').replace(',', '.').strip()
        if valor_str:
            try:
                total += float(valor_str)
            except ValueError:
                pass  # ignora se não for número válido
    
    total_formatado = f'R$ {total:.2f}'.replace('.', ',')

    dados_da_planilha.append({
        'Exames': 'TOTAL',
        'Data': '',
        'Valor': total_formatado
    })

    print("Total: ", total_formatado)

    return dados_da_planilha