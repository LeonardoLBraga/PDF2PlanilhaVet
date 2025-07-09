# 🐾 PDF2PlanilhaVet

![CI](https://github.com/leonardolbraga/PDF2PlanilhaVet/actions/workflows/ci.yml/badge.svg)

**PDF2PlanilhaVet** é uma ferramenta em Python que automatiza a extração de dados de exames veterinários em PDF e gera uma planilha Excel estruturada, facilitando o controle financeiro e o arquivamento.

---

## ✅ Funcionalidades

- 🗂️ Suporte a múltiplos layouts de PDF (com ou sem tabela), via padrão **Strategy**
- 🔍 Extração automática de:
  - Nome do paciente
  - Data do exame
  - Procedimentos e seus respectivos valores
- 🧠 Correspondência inteligente de exames usando sinônimos e similaridade
- 🔄 Processamento em lote de diversos PDFs
- 📊 Geração automática de planilhas `.xlsx` com:
  - Aba **"Dados completos"** com todos os exames
  - Aba **"Resumo"** com contagem por procedimento
- 💻 Executável `.exe` incluído para uso sem precisar instalar Python

---

## 📁 Estrutura do Projeto

    PDF2PlanilhaVet/
        ├── arquivos/                   # PDFs dos exames a serem processados
        ├── planilhas_geradas/          # Planilhas de saída
        ├── pdf_valores_exames/
        │   └── valores.pdf             # PDF com os valores dos exames
        ├── extratores/
        │   ├── base.py                 # Classe base abstrata (interface)
        │   ├── com_tabela.py           # Extrator para PDFs com tabela
        │   ├── sem_tabela.py           # Extrator para PDFs sem tabela
        │   └── fabrica.py              # Fábrica que escolhe o extrator adequado
        ├── utils/
        │   └── functions.py            # Funções auxiliares (normalização, resumo, etc.)
        ├── gerar_planilha.py           # Script principal
        ├── download_executavel.bat     # Script para baixar o executável
        ├── README.md                   # Este arquivo

---

## 🚀 Como Usar

1. Coloque seus arquivos `.pdf` de exames na pasta `arquivos/`
2. Insira o PDF com os valores de exames em `pdf_valores_exames/valores.pdf`
3. Execute:
   - Via `.exe`:
     - Clique em `download_executavel.bat`
     - Extraia o `.zip`
     - Clique em `gerar_planilha.exe`
   - Ou via terminal com Python (ver seção abaixo)
4. A planilha será gerada automaticamente em `planilhas_geradas/`, com o nome no formato `aaaa-mm-dd.xlsx`, contendo:
   - Aba **"Dados completos"** com todos os exames
   - Aba **"Resumo"** com a quantidade total de cada procedimento

---

## ⚙️ Requisitos

- **Nenhum!** O `.exe` funciona sem instalar nada.
- Para uso via Python:
  - Python 3.10+
  - Bibliotecas: `pdfplumber`, `pandas`, `openpyxl`

---

## ⚠️ Tratativas de Erro

- Verifica se há arquivos na pasta `arquivos/`
- Verifica o tamanho esperado das páginas
- Detecta e ignora arquivos mal formatados
- Exibe logs detalhados com:
  - Match por sinônimo
  - Match por similaridade
  - Procedimentos sem valor encontrado

---

## 🔍 Exemplo de Resultado

### 📄 Aba 1 – Dados completos

| Exames                           | Data       | Valor    |
|----------------------------------|------------|----------|
| fosfatase alcalina - Meg         | 06/04/2024 | R$ 20,00 |
| alt tgp - Meg                    | 06/04/2024 | R$ 20,00 |
| pesquisa de hemoparasitas - Meg | 26/04/2025 | R$ 30,00 |
| **TOTAL**                        |            | **R$ 70,00** |

### 📄 Aba 2 – Resumo por Procedimento

| Procedimento          | Quantidade |
|-----------------------|------------|
| alt tgp               | 3          |
| creatinina            | 5          |
| ureia                 | 5          |
| fosfatase alcalina    | 3          |

---

## 🧠 Estratégia de Extração

A seleção do método de extração é feita dinamicamente:

- `ExtratorComTabela`: usa a primeira tabela da página para extrair os procedimentos
- `ExtratorSemTabela`: extrai com base em posições fixas no layout

Implementado com o padrão de projeto **Strategy**, facilitando a adição de novos tipos de layout no futuro.

---

## 🧰 Dicionário de Sinônimos

Correspondência robusta com apoio de sinônimos para identificar exames mesmo com variações no nome, como:

```python
"alt tgp" → "transaminase piruvica - alt"
"ggt", "gama gt" → "ggt - gama glutamil transferase"
"colesterol" → "colesterol total"
"triglicerideos" → "triglicerides"
"raspado de pele" → "raspado pele"
```

## 💡 Melhorias Futuras

- Exportação opcional em `.csv`
- Interface gráfica com Tkinter
- OCR para leitura de PDFs digitalizados
- Reconhecimento inteligente de sinônimos e variantes
- Exportação de log detalhado (erros, correspondências, etc.)

---

## 🛠️ Como Gerar o Executável

### 1. Instale o PyInstaller

```
pip install pyinstaller
```

### 2. Gere o `.exe` na raiz do projeto

```
pyinstaller --onefile gerar_planilha.py --distpath .
```

> Isso criará `gerar_planilha.exe` direto na pasta principal (sem `dist/`).

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT – veja o arquivo [LICENSE](LICENSE) para mais detalhes.
