from extratores.com_tabela import ExtratorComTabela

class FakePagina:
    def __init__(self, tabelas):
        self._tabelas = tabelas
        self.call_count = 0

    def extract_tables(self):
        return [self._tabelas]

    def within_bbox(self, box):
        self._last_box = box
        return self

    def extract_text(self):
        if self.call_count == 0:
            self.call_count += 1
            return "Paciente: João da Silva"
        else:
            return "Data do exame: 01/07/2025"


def test_extrator_com_tabela():
    # Simula uma tabela com cabeçalho (2 primeiras linhas ignoradas)
    pagina = FakePagina([
        ["Cabeçalho", "Qualquer coisa"],
        ["Outro cabeçalho", "Ignorado"],
        ["Hemograma", ""],
        ["ALT", ""]
    ])

    valores = {
        "hemograma": "R$ 30,00",
        "transaminase piruvica - alt": "R$ 50,00"
    }

    extrator = ExtratorComTabela()
    linhas = extrator.extrair(pagina, valores)

    assert isinstance(linhas, list)
    assert len(linhas) == 2
    assert linhas[0]['Exames'] == 'Hemograma - João da Silva'
    assert linhas[0]['Valor'] == 'R$ 30,00'
    assert linhas[1]['Exames'] == 'ALT - João da Silva'
    assert linhas[1]['Valor'] == 'R$ 50,00'
