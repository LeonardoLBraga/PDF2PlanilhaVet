@echo off
chcp 65001 >nul

setlocal

echo ======================================
echo Iniciando geração da planilha
echo ======================================

REM Nome do executável desejado
set EXECUTAVEL=gerar_planilha.exe

REM Verifica se o executável existe na pasta atual
if not exist "%EXECUTAVEL%" (
    echo Executável não encontrado. Criando...
    
    REM Verifica se o PyInstaller está instalado
    pip show pyinstaller >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo PyInstaller nao encontrado. Instalando...
        pip install pyinstaller
    )

    REM Roda o PyInstaller para gerar o exe NA PASTA ATUAL
    pyinstaller --onefile --distpath . --workpath build --specpath build gerar_planilha.py

    REM Verifica se o exe foi criado
    if not exist "%EXECUTAVEL%" (
        echo ERRO: Falha ao criar o executavel.
        pause
        exit /b
    )
    echo Executavel criado com sucesso.
) else (
    echo Executavel encontrado.
)

echo.
echo Executando o programa...

REM Executa o .exe e captura o código de saída
"%EXECUTAVEL%"
set ERRO=%ERRORLEVEL%

echo.
if %ERRO% NEQ 0 (
    echo ======================================
    echo Opa! Algo deu errado 😢
    echo Codigo de erro: %ERRO%
    echo Verifique se os arquivos PDF estão corretos
    echo ou se o executavel teve algum problema.
    echo ======================================
) else (
    echo ======================================
    echo Planilha gerada com sucesso! ✅
    echo ======================================
)

pause
endlocal
