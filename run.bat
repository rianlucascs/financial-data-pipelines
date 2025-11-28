@echo off
title Iniciando Aplicacao Streamlit...

REM Ir para o diretorio onde o script .bat esta
cd /d "%~dp0"

REM Verificar se a venv existe
if not exist ".venv\Scripts\activate.bat" (
    echo [ERRO] Ambiente virtual não encontrado.
    echo Crie com: python -m venv .venv
    pause
    exit /b
)

echo Ativando ambiente virtual...
call ".venv\Scripts\activate.bat"

echo Iniciando aplicacao...

REM python -m jobs.cvm_formulario_informacoes_trismestrais
REM python -m jobs.b3_companies_page_search
REM python -m jobs.b3_companies_page_all
REM python -m jobs.cvm_fundos_de_investimentos_informacao_cadastral
python -m jobs.cvm_fundos_de_investimento_documentos_informe_diario

echo.
echo Aplicacao encerrada.
pause