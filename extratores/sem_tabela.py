"""
Extrator de dados de PDFs que não possuem tabelas.

Este extrator utiliza coordenadas fixas para localizar o procedimento.
"""

from extratores.base import ExtratorBase
from utils.functions import extrair_nome_e_data, get_valor_by_procedimento, normalizar

class ExtratorSemTabela(ExtratorBase):
    """Extrator para PDFs sem tabela, utilizando posição fixa para o procedimento."""

    def extrair(self, pagina, valores):
        """
        Extrai dados da página baseado em uma área específica do PDF.

        Args:
            pagina: Objeto da página do PDF.
            valores (dict): Dicionário com valores por procedimento.

        Returns:
            list[dict]: Lista contendo os dados formatados.
        """
        nome, data = extrair_nome_e_data(pagina)
        procedimento = self.extrair_procedimento_por_posicao(pagina)
        return [{
            "Exames": f"{procedimento} - {nome}",
            "Data": data,
            "Valor": get_valor_by_procedimento(procedimento, valores)
        }]

    def extrair_procedimento_por_posicao(self, pagina):
        """
        Extrai o nome do procedimento a partir de uma região delimitada da página.

        Args:
            pagina: Objeto da página do PDF.

        Returns:
            str: Nome do procedimento extraído.
        """
        caixa_procedimento = (50, 280, 800, 330)
        texto_procedimento = pagina.within_bbox(caixa_procedimento).extract_text()
        return normalizar(texto_procedimento.splitlines()[0]) if texto_procedimento else ""
