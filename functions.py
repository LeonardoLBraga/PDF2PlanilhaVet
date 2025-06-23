import re
import pdfplumber

import difflib
import unicodedata

# TAMANHO_PADRAO_A4 = (595.28, 841.89)
TAMANHO_ESPERADO = (841.92, 1191.12)


def normalizar(texto):
    # Remove acentos e converte para minúsculas
    return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII").lower()


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


def get_valor_by_procedimento(procedimento, caminho_valores):
    valor_do_procedimento = ""
    valores_dos_exames_dict = get_valores_do_pdf(caminho_valores)

    valores_normalizados = {
        normalizar(nome_exame): valor_exame
        for nome_exame, valor_exame in valores_dos_exames_dict.items()
    }

    procedimento_norm = normalizar(procedimento)

    # Buscar a melhor correspondência com difflib
    candidatos = difflib.get_close_matches(procedimento_norm, valores_normalizados.keys(), n=1, cutoff=0.6)

    if candidatos:
        valor_do_procedimento = valores_normalizados[candidatos[0]]
        print(f"Match encontrado: {candidatos[0]} → {valor_do_procedimento}")
    else:
        print(f"Nenhuma correspondência encontrada para: {candidatos[0]}")

    return valor_do_procedimento
