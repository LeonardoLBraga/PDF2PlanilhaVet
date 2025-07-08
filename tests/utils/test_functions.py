from utils import functions

def test_normalizar():
    assert functions.normalizar("  ÁçÊ!@# texto ") == "ace texto"


def test_calcula_total():
    dados = [
        {"Exames": "Exame 1", "Data": "", "Valor": "R$ 10,00"},
        {"Exames": "Exame 2", "Data": "", "Valor": "R$ 20,00"},
    ]
    total = functions.calcula_total(dados)
    assert total[-1]["Exames"] == "TOTAL"
    assert total[-1]["Valor"] == "R$ 30,00"


def test_get_valor_by_procedimento_match_exato():
    valores = functions.normalizar_valores({"hemograma": "R$ 25,00"})
    val = functions.get_valor_by_procedimento("Hemograma", valores)
    assert val == "R$ 25,00"


def test_get_valor_by_procedimento_sinonimo():
    valores = functions.normalizar_valores({"transaminase piruvica - alt": "R$ 50,00"})
    val = functions.get_valor_by_procedimento("ALT", valores)
    assert val == "R$ 50,00"


def test_get_valor_by_procedimento_invalido():
    valores = functions.normalizar_valores({"hemograma": "R$ 25,00"})
    val = functions.get_valor_by_procedimento("Exame inexistente", valores)
    assert val == ""