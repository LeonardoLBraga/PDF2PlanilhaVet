@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "EXE=gerar_planilha.exe"
set "ZIP=gerar_planilha.zip"
set "URL=https://github.com/LeonardoLBraga/PDF2PlanilhaVet/releases/download/v1.0/%ZIP%"

echo ======================================
echo Iniciando geração da planilha...
echo ======================================

if not exist "!EXE!" (
    echo Executável não encontrado.
    echo Verificando conexão com GitHub...

    powershell -Command "try { $r = Invoke-WebRequest -Uri '!URL!' -Method Head -UseBasicParsing -TimeoutSec 10; if ($r.StatusCode -ne 200) { exit 1 } } catch { exit 1 }"

    if errorlevel 1 (
        echo ERRO: Não foi possível acessar o link do ZIP.
        pause
        exit /b
    )

    echo Conectado com sucesso.
    echo Baixando arquivo...
    powershell -Command "Invoke-WebRequest -Uri '!URL!' -OutFile '!ZIP!'"

    if not exist "!ZIP!" (
        echo ERRO: Falha ao baixar o ZIP.
        pause
        exit /b
    )

    echo Descompactando...
    powershell -Command "Expand-Archive -Path '!ZIP!' -DestinationPath '.' -Force"

    if errorlevel 1 (
        echo ERRO ao descompactar o arquivo.
        pause
        exit /b
    )
)

echo Executando o programa...
"!EXE!"
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
