# 🐾 PDF2PlanilhaVet

**PDF2PlanilhaVet** é uma ferramenta em Python que automatiza a extração de dados de exames veterinários em PDF e gera uma planilha Excel estruturada, facilitando o controle financeiro e o arquivamento.

---

## ✅ Funcionalidades

- 🗂️ Suporte a múltiplos layouts de PDF (com ou sem tabela), via padrão **Strategy**
- 🔍 Extração automática de:
  - Nome do paciente
  - Data do exame
  - Procedimentos e seus respectivos valores
- 🔄 Processamento em lote de diversos PDFs
- 📊 Geração automática de planilhas `.xlsx` com o nome baseado na data atual
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
        │   └── functions.py            # Funções auxiliares de extração e normalização
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
4. A planilha será gerada automaticamente em `planilhas_geradas/`, com o nome no formato `aaaa-mm-dd.xlsx`

---

## ⚙️ Requisitos

- **Nenhum!** O `.exe` funciona sem instalar nada.
- Para uso via Python:
  - Python 3.10+
  - Bibliotecas: `pdfplumber`, `pandas`

---

## ⚠️ Tratativas de Erro

- Verifica se há arquivos na pasta `arquivos/`
- Verifica o tamanho esperado das páginas
- Detecta e ignora arquivos mal formatados
- Mostra mensagens de erro amigáveis
- Exibe logs de sinônimos e correspondências por similaridade

---

## 🔍 Exemplo de Resultado

| Exames                           | Data       | Valor    |
|----------------------------------|------------|----------|
| Fosfatase Alcalina - Meg         | 06/04/2024 | R$ 20,00 |
| A.L.T. (TGP) - Meg               | 06/04/2024 | R$ 20,00 |
| Pesquisa de hemoparasitas - Meg  | 26/04/2025 | R$ 30,00 |
| **TOTAL**                        |            | **R$ 70,00** |

---

## 🧠 Estratégia de Extração

A seleção do método de extração é feita dinamicamente:

- `ExtratorComTabela`: usa a primeira tabela da página para extrair os procedimentos
- `ExtratorSemTabela`: extrai com base em posições fixas no layout

Tudo isso é implementado com o **Strategy Pattern**, facilitando a adição de novos tipos de layout no futuro.

---

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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Desenvolvido com 💚 para facilitar a rotina de clínicas veterinárias.
