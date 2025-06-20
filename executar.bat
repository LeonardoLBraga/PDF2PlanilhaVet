@echo off
chcp 65001 >nul
setlocal

set "EXE=gerar_planilha.exe"
set "ZIP=gerar_planilha.zip"
set "URL=https://github.com/LeonardoLBraga/PDF2PlanilhaVet/releases/download/v1.0/%ZIP%"

echo ======================================
echo Iniciando geração da planilha
echo ======================================

REM Se o executável não existir, baixa e extrai do release
if not exist "%EXE%" (
    echo Executável não encontrado. Baixando do GitHub...

    powershell -Command "Invoke-WebRequest -Uri '%URL%' -OutFile '%ZIP%'"
    
    if not exist "%ZIP%" (
        echo ERRO: Falha ao baixar o arquivo ZIP
        pause
        exit /b
    )

    echo Descompactando...
    powershell -Command "Expand-Archive -Path '%ZIP%' -DestinationPath '.' -Force"
)

REM Executa o programa
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
