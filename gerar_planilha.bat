@echo off
chcp 65001 >nul

echo ======================================
echo Iniciando geração da planilha
echo ======================================

REM Verifica se o Python está instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERRO: Python não está instalado ou não está no PATH.
    pause
    exit /b
)

echo.
echo Instalando dependências necessárias...
pip install --quiet pdfplumber pandas openpyxl

echo.
echo ======================================
echo Executando script Python...
python gerar_planilha.py

echo.
echo ======================================
echo Se os dados não estiverem corretos,
echo verifique a imagem debug_posicoes.png
echo ======================================

REM Verifica se o script Python teve erro
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ======================================
    echo Opa! Algo deu errado 😢
    echo Verifique se os arquivos PDF estão corretos
    echo ou se o script teve algum problema.
    echo ======================================
) ELSE (
    echo.
    echo ======================================
    echo Planilha gerada com sucesso! ✅
    echo ======================================
)
pause