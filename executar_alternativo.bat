@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ======================================
echo Iniciando geração da planilha...
echo ======================================

if not exist "gerar_planilha.exe" (
    echo Executável não encontrado.

    echo Baixando ...
    certutil -urlcache -split -f "https://github.com/LeonardoLBraga/PDF2PlanilhaVet/releases/download/v1.0/gerar_planilha.zip" "gerar_planilha.zip"
    
    if not exist "gerar_planilha.zip" (
        echo ERRO: Falha ao baixar o ZIP.
        pause
        exit /b
    )
)

echo Arquivo baixado. Por favor, descompacte o arquivo zip manualmente.
pause

echo.
echo Executando o programa...

gerar_planilha.exe

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
