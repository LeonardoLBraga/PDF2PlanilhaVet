# PDF2PlanilhaVet

# 🐾 PDF2PlanilhaVet

**PDF2PlanilhaVet** é uma ferramenta em Python que automatiza a extração de dados de exames veterinários em PDF e gera uma planilha Excel limpa e estruturada.

## ✅ Funcionalidades

- 🗂️ Suporte a diferentes layouts de PDF (com ou sem tabela), utilizando o padrão de projeto **Strategy**
- 📥 Extração de nome do paciente, data e procedimentos
- 🔄 Processa múltiplos PDFs em lote
- 📊 Geração automática de planilhas `.xlsx` nomeadas pela data atual
- ⚙️ Execução simples com **duplo clique** via `.bat` (WIP)
- 📦 Instalação automática de dependências se necessário (WIP)
- 📌 Executável `.exe` incluso para uso sem precisar instalar Python

---

## 📁 Estrutura do Projeto

```plaintext
PDF2PlanilhaVet/
├── arquivos/                 # PDFs dos exames
├── planilhas_geradas/        # Planilhas geradas automaticamente
├── extratores/               # Módulo com extratores base e especializados
│   ├── base.py               # Interface base do extrator
|   ├── fabrica.py            # O uso do padrão Strategy com fabrica.py
│   ├── com_tabela.py         # Extrator para PDFs com tabela
│   └── sem_tabela.py         # Extrator para PDFs sem tabela
├── utils/                    # Funções auxiliares
├── img/                      # Imagens de debug (opcional)
├── gerar_planilha.py         # Script principal
├── executar.bat              # Script .bat principal (recomendo)
├── executar_alternativo.bat  # Versão alternativa (sem .exe)
├── README.md
```

---

## 🚀 Como usar

1. Copie seus arquivos `.pdf` de exames para a pasta `arquivos/`.
2. Copie o `.pdf` de valores dos exames para a pasta `pdf_valores_exames` com o nome de `valores`, ficando assim: `pdf_valores_exames/valores.pdf`
3. Dê **duplo clique** em `executar.bat` (usa o `.exe`) ou `executar_alternativo.bat` (roda com Python).
4. A planilha será criada na pasta `planilhas_geradas/`, com o nome no formato `dd-mm-aaaa.xlsx`.

---

## ⚙️ Requisitos

- **Nada!** O `.exe` funciona sem precisar instalar Python.

---

## ⚠️ Tratativas de Erro

- Verifica se há PDFs na pasta `arquivos/`
- Detecta PDFs inválidos ou com tamanhos inesperados
- Informa visualmente se não foi possível extrair o conteúdo
- Gera imagem de debug (`debug_posicoes.png`) para auxiliar na correção

---

## 🔍 Exemplo de Resultado

| Exames                           | Data       | Valor    |
|----------------------------------|------------|----------|
| Fosfatase Alcalina - Meg         | 06/04/2024 | R$ 20,00 |
| A.L.T. (TGP) - Meg               | 06/04/2024 | R$ 20,00 |
| Pesquisa de hemoparasitas - Meg | 26/04/2025 | R$ 30,00 |

---

## 🧠 Estratégia de Extração

- 🧩 **Strategy Pattern**: implementado para alternar entre:
  - `ExtratorComTabela` – para PDFs com tabelas de exames
  - `ExtratorSemTabela` – para PDFs com layout posicional
- Fácil de expandir para novos tipos de layout apenas criando uma nova classe.

---

## 💡 Melhorias Futuras

- Exportação para `.csv`
- Interface gráfica com Tkinter
- OCR para PDFs digitalizados
- Melhor heurística de correspondência dos procedimentos
- Melhor tratamento de erros, mais detalhado

---

## 🛠️ Como gerar o instalador `.exe`

 Como gerar o executável da aplicação **PDF2PlanilhaVet**, de forma que o usuário final não precise instalar Python nem dependências.

### 1. Instale o PyInstaller

Se ainda não tiver instalado, abra o terminal (ou `cmd`) e execute:

```bash
pip install pyinstaller
```

### 2. Gere o executável diretamente na raiz do projeto

Navegue até a pasta do projeto e execute:

```bash
pyinstaller --onefile gerar_planilha.py --distpath .
```

Isso criará o arquivo `gerar_planilha.exe` na **pasta principal do projeto**, evitando a criação da subpasta `dist/`.

---
## 📜 Licença

Este projeto é livre para uso pessoal ou comercial. Nenhuma garantia é fornecida.

---
### Desenvolvido com 💚 para facilitar a rotina de clínicas veterinárias.
