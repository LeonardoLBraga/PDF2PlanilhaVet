@echo off
chcp 65001 >nul
setlocal

echo ======================================
echo Iniciando geração da planilha
echo ======================================

REM Caminho absoluto do diretório onde está este .bat
set "DIR_ATUAL=%~dp0"
set "EXE_CAMINHO=%DIR_ATUAL%gerar_planilha.exe"

REM Remove aspas duplas extras se houver
set EXE_CAMINHO=%EXE_CAMINHO:"=%

REM Verifica se o .exe existe
if not exist "%EXE_CAMINHO%" (
    echo ERRO: O executável gerar_planilha.exe nao foi encontrado em: 
    echo %EXE_CAMINHO%
    pause
    exit /b
)

echo Executando o programa...
"%EXE_CAMINHO%"
set ERRO=%ERRORLEVEL%

echo.
if %ERRO% NEQ 0 (
    echo ======================================
    echo Opa! Algo deu errado 😢
    echo Código de erro: %ERRO%
    echo Verifique os arquivos PDF ou se houve falha no executável.
    echo ======================================
) else (
    echo ======================================
    echo Planilha gerada com sucesso! ✅
    echo ======================================
)

pause
endlocal
