from extratores.base import ExtratorBase
from utils.functions import extrair_nome_e_data, get_valor_by_procedimento

class ExtratorSemTabela(ExtratorBase):
    def extrair(self, pagina, valores):
        nome, data = extrair_nome_e_data(pagina)
        procedimento = self.extrair_procedimento_por_posicao(pagina)
        return [{
            "Exames": f"{procedimento} - {nome}",
            "Data": data,
            "Valor": get_valor_by_procedimento(procedimento, valores)
        }]

    def extrair_procedimento_por_posicao(self, pagina):
        caixa_procedimento = (50, 280, 800, 330)
        texto_procedimento = pagina.within_bbox(caixa_procedimento).extract_text()
        return texto_procedimento.strip().splitlines()[0] if texto_procedimento else ""
