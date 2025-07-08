from extratores.sem_tabela import ExtratorSemTabela
from utils import functions

class FakePaginaSemTabela:
    def within_bbox(self, box):
        self.last_box = box
        return self

    def extract_text(self):
        if self.last_box == (50, 280, 800, 330):
            return "ALT TGP"
        elif self.last_box == (50, 150, 348, 175):
            return "Paciente: João da Silva"
        elif self.last_box == (620, 150, 800, 250):
            return "Data do exame: 01/07/2025"
        return ""

def test_extrator_sem_tabela():
    pagina = FakePaginaSemTabela()
    valores = functions.normalizar_valores({"transaminase piruvica - alt": "R$ 40,00"})

    extrator = ExtratorSemTabela()
    resultado = extrator.extrair(pagina, valores)

    assert resultado[0]["Exames"] == "alt tgp - João da Silva"
    assert resultado[0]["Data"] == "01/07/2025"
    assert resultado[0]["Valor"] == "R$ 40,00"
