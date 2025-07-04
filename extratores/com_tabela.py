"""
Extrator de dados de PDFs que possuem tabelas estruturadas com procedimentos.

Este extrator utiliza tabelas extraídas da página para identificar os procedimentos.
"""

from extratores.base import ExtratorBase
from utils.functions import extrair_nome_e_data, get_valor_by_procedimento

class ExtratorComTabela(ExtratorBase):
    """Extrator para PDFs com tabela de procedimentos."""

    def extrair(self, pagina, valores):
        """
        Extrai dados da página com base em uma tabela de procedimentos.

        Args:
            pagina: Objeto da página do PDF.
            valores (dict): Dicionário com valores por procedimento.

        Returns:
            list[dict]: Lista contendo os dados formatados.
        """
        nome, data = extrair_nome_e_data(pagina)

        try:
            procedimentos = self.extrair_procedimentos_da_tabela(pagina)
        except Exception as e:
            print(f"Erro ao extrair tabela: {e}")
            return []

        linhas = []
        for procedimento in procedimentos:
            linhas.append({
                "Exames": f"{procedimento} - {nome}",
                "Data": data,
                "Valor": get_valor_by_procedimento(procedimento, valores)
            })
        return linhas

    def extrair_procedimentos_da_tabela(self, pagina):
        """
        Extrai os nomes dos procedimentos da primeira tabela encontrada na página.

        Args:
            pagina: Objeto da página do PDF.

        Returns:
            list[str]: Lista de nomes de procedimentos.

        Raises:
            ValueError: Se nenhuma tabela for encontrada.
        """
        tabelas = pagina.extract_tables()
        if not tabelas:
            raise ValueError("Nenhuma tabela encontrada na página.")
        primeira_tabela = tabelas[0]
        procedimentos = []

        for i, linha in enumerate(primeira_tabela):
            if i < 2:
                continue
            if linha and linha[0]:
                procedimentos.append(linha[0].strip())

        return procedimentos
