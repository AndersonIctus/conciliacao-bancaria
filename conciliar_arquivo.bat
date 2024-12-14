@echo off
REM Verifica se um arquivo foi arrastado
if "%~1"=="" (
    echo Nenhum arquivo foi fornecido. Arraste um arquivo .csv para este script.
    pause
    exit /b
)

REM Obtém o caminho completo do arquivo arrastado
set bank_file=%~1

REM Chama o make, passando o caminho do arquivo como uma variável
conciliacao-bancaria.exe --bank-file "%bank_file%"
pause
