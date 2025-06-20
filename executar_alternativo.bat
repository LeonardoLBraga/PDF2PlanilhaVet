@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "EXE=gerar_planilha.exe"
set "ZIP=gerar_planilha.zip"
set "URL=https://github.com/LeonardoLBraga/PDF2PlanilhaVet/releases/download/v1.0/%ZIP%"

echo ======================================
echo Iniciando geração da planilha...
echo ======================================

REM Verifica se o executável já existe
if not exist "%EXE%" (
    echo Executável não encontrado.

    echo Baixando o arquivo ZIP...
    curl -L -o "%ZIP%" "%URL%"
    
    if not exist "%ZIP%" (
        echo ERRO: Falha ao baixar o ZIP.
        pause
        exit /b
    )

    echo Descompactando...
    tar -xf "%ZIP%" >nul 2>&1
    if errorlevel 1 (
        echo ERRO ao descompactar o ZIP.
        pause
        exit /b
    )
)

echo.
echo Executando o programa...
"%EXE%"
set ERRO=%ERRORLEVEL%

echo.
if %ERRO% NEQ 0 (
    echo ======================================
    echo Algo deu errado 😢
    echo Código de erro: %ERRO%
    echo ======================================
) else (
    echo ======================================
    echo Planilha gerada com sucesso! ✅
    echo ======================================
)

pause
endlocal
