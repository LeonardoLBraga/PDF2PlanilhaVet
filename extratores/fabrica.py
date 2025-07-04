"""
Módulo fábrica para selecionar o extrator adequado com base na presença de tabela no PDF.
"""

from extratores.com_tabela import ExtratorComTabela
from extratores.sem_tabela import ExtratorSemTabela
from utils.functions import verifica_se_tem_tabela

def escolher_extrator(caminho_pdf):
    """
    Retorna a instância do extrator apropriado com base na presença de tabelas no PDF.

    Args:
        caminho_pdf (str): Caminho para o arquivo PDF.

    Returns:
        ExtratorBase: Instância de `ExtratorComTabela` ou `ExtratorSemTabela`.
    """
    if verifica_se_tem_tabela(caminho_pdf):
        return ExtratorComTabela()
    return ExtratorSemTabela()
