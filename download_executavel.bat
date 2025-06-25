@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "EXE=gerar_planilha.exe"
set "ZIP=gerar_planilha.zip"
set "URL=https://github.com/LeonardoLBraga/PDF2PlanilhaVet/releases/download/v1.0/%ZIP%"

echo ======================================
echo Verificando se o executável já existe...
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

    echo Executável pronto para uso!
) else (
    echo Executável já está presente. Nenhum download necessário.
)

pause
endlocal
