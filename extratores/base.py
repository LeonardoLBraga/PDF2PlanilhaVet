class ExtratorBase:
    def extrair(self, pagina, valores) -> list[dict]:
        raise NotImplementedError("Classe abstrata, implemente 'extrair'")
