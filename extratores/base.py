"""
Módulo base que define a interface para os extratores de dados de páginas PDF.

Contém a classe abstrata `ExtratorBase` que deve ser herdada por extratores específicos,
fornecendo um método `extrair` a ser implementado.
"""

class ExtratorBase:
    """Classe base abstrata para extratores de dados de páginas PDF."""

    def extrair(self, pagina, valores) -> list[dict]:
        """
        Extrai informações de uma página PDF.

        Este método deve ser implementado pelas subclasses.

        Args:
            pagina: Objeto da página do PDF.
            valores (dict): Dicionário com os valores de procedimentos.

        Returns:
            list[dict]: Lista de dicionários com os dados extraídos.
        """
        raise NotImplementedError("Classe abstrata, implemente 'extrair'")
