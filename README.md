# PDF2PlanilhaVet

**PDF2PlanilhaVet** é uma ferramenta em Python que automatiza a extração de dados de exames em PDF (provenientes de clínicas veterinárias) e gera uma planilha Excel organizada com os resultados.

## ✅ Funcionalidades

- Extrai o nome do paciente, data do exame e tipo de exame por posição no PDF
- Processa múltiplos PDFs de uma vez (em lote)
- Gera uma planilha `dd/mm/aaaa.xlsx` pronta para uso com o nome sendo a data de quando ela foi gerada
- Automatização via `.bat` para rodar com duplo clique
- Instala automaticamente as dependências necessárias se não estiverem presentes

## 📁 Estrutura do Projeto

```plaintext
PDF2PlanilhaVet/
├── gerar_planilha.py       # Script Python principal
├── gerar_planilha.bat      # Script .bat para rodar tudo com 2 cliques
├── arquivos/               # Coloque aqui os PDFs dos exames
├── planilhas_geradas/      # Arquivos Excel gerados automaticamente
```

## ⚙️ Pré-requisitos

- Python 3.8 ou superior
- Pip configurado no PATH

As dependências necessárias serão instaladas automaticamente ao rodar o `.bat`, mas você também pode instalar manualmente com:

```pip install pdfplumber pandas openpyxl```

## 🚀 Como usar

1. Coloque seus arquivos `.pdf` de exames na pasta `arquivos/`.
2. Dê **duplo clique** em `gerar_planilha.bat`.
3. A planilha `dd/mm/aaaa.xlsx` será gerada com os dados extraídos.

## ⚠️ Possíveis erros tratados

- A pasta `arquivos` não existe
- Não há arquivos `.pdf` na pasta
- Falha ao ler algum arquivo corrompido
- Exceções genéricas com mensagens amigáveis (sem traceback do Python)

## 📊 Exemplo de resultado

| Exames                              | Data       | Valor |
|-------------------------------------|------------|-------|
| Raspado de pele - Zaia              | 25/04/2025 |       |
| Pesquisa de hematozoários - Meg     | 26/04/2025 |       |

## 💡 Melhorias futuras (sugestões)

- Exportar para `.csv`
- Interface gráfica com tkinter
- Reconhecimento OCR para PDFs escaneados
- Detecção automática de campos sem posição fixa

## 📜 Licença

Este projeto é livre para uso pessoal ou comercial. Nenhuma garantia é fornecida.

---

Desenvolvido com 💚 para facilitar a rotina de clínicas veterinárias.
