from extratores.com_tabela import ExtratorComTabela
from extratores.sem_tabela import ExtratorSemTabela
from utils.functions import verifica_se_tem_tabela

def escolher_extrator(caminho_pdf):
    if verifica_se_tem_tabela(caminho_pdf):
        return ExtratorComTabela()
    return ExtratorSemTabela()
