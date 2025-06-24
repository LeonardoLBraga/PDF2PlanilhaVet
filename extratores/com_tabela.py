from extratores.base import ExtratorBase
from utils.functions import extrair_nome_e_data, get_valor_by_procedimento

class ExtratorComTabela(ExtratorBase):
    def extrair(self, pagina, valores):
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