@echo off
chcp 65001 >nul

echo ======================================
echo Iniciando geração da planilha
echo ======================================

REM Caminho para o executável gerado pelo PyInstaller
set EXECUTAVEL=gerar_planilha.exe

REM Verifica se o executável existe
if not exist %EXECUTAVEL% (
    echo ERRO: O executável "%EXECUTAVEL%" não foi encontrado.
    echo Certifique-se de que ele esteja na mesma pasta que este .bat
    pause
    exit /b
)

echo.
echo Executando o programa...

REM Executa o .exe e redireciona erros para o console
%EXECUTAVEL%
set ERRO=%ERRORLEVEL%

echo.
if %ERRO% NEQ 0 (
    echo ======================================
    echo Opa! Algo deu errado 😢
    echo Código de erro: %ERRO%
    echo Verifique se os arquivos PDF estão corretos
    echo ou se o executável teve algum problema.
    echo ======================================
) else (
    echo ======================================
    echo Planilha gerada com sucesso! ✅
    echo ======================================
)

pause
