
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
from os.path import join, exists
from pandas import read_csv, DataFrame
import logging
from json import load, dump

from src.config import *
from src.utils import (
    find, safe_click, web_driver, retry_on_false, retry_find)

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")

class X:

    # Preparação
    EMPRESAS_ENCONTRADAS =     '//span[contains(text(), "empresas encontradas")]/preceding-sibling::span[1]'
    RESULTADOS_POR_PAGINA =    '//*[@id="selectPage"]/option[@value="120"]'
    QUANTIDADE_DE_BLOCOS =     '//*[contains(@class, "col-12 col-md-3 col-sm-6 mb-4")]'
    QUANTIDADE_DE_PAGINAS =    '(//ul[contains(@class, "ngx-pagination")]//li[a]/a/span[2])[last()]'
    PROXIMA_PAGINA =           '//li[contains(@class, "pagination-next")]/a'
    
    # Pagina 1
    ABRIR_BLOCO =           lambda bloco: f'//*[@id="nav-bloco"]/div/div[{bloco}]/div'
    INFO_BLOCO_TITLE2 =     lambda bloco: f'//*[@id="nav-bloco"]/div/div[{bloco}]/div/div/h5'
    INFO_BLOCO_TITLE =      lambda bloco: f'//*[@id="nav-bloco"]/div/div[{bloco}]/div/div/p[1]'
    INFO_BLOCO_TEXT =       lambda bloco: f'//*[@id="nav-bloco"]/div/div[{bloco}]/div/div/p[2]'

    # Pagina 2
    BTN_OUTROS_CODIGOS =   '//a[contains(@href, "#accordionBody2")]'
    OUTROS_COL1 =          '//*[@id="accordionBody2"]//table/tr/td[1]/p'
    OUTROS_COL2 =          '//*[@id="accordionBody2"]//table/tr/td[2]/p'
                    
    INFO = {
        "nome_pregao":       '//*[@class="card-text"][strong[text()="Nome do Pregão"]]/following-sibling::p[@class="card-linha"]',
        "cod_negociacao":    '//*[@class="card-text"][strong[text()="Código de Negociação"]]/following-sibling::p/a',
        "cod_cvm":           '//*[@id="accordionBody2"]//span[b[text()="Código CVM"]]/p',
        "inicio_negociacao": '//*[@class="card-text"][strong[text()="Início de negociação das ações"]]/following-sibling::p',
        "cnpj":              '//*[@class="card-text"][strong[text()="CNPJ"]]/following-sibling::p',
        "atividade":         '//*[@class="card-text"][strong[text()="Atividade Principal"]]/following-sibling::p',
        "setorial":          '//*[@class="card-text"][strong[text()="Classificação Setorial"]]/following-sibling::p',
        "site":              '//*[@class="card-text"][strong[text()="Site"]]/following-sibling::p/a'
    }

class ExtractB3CompaniesPageAll:

    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.url = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/search?language=pt-br"
        self.driver = None
        self.path_raw = join(PATH_RAW(self.pipeline, "json"), "data.json")
        self.data_json = self.load_json()
        self.siglas_existentes = {e["info_bloco_title2"] for e in self.data_json.get("empresas", [])}
        
    # Pagina 1

    def numero_empresas_encontradas(self):
        return int(find(self.driver, X.EMPRESAS_ENCONTRADAS).text.replace('.', ''))
    
    @retry_on_false(retries=3)
    def resultado_por_pagina(self):
        return safe_click(self.driver, X.RESULTADOS_POR_PAGINA)
        
    def quantidade_de_blocos_da_pagina(self):
        return len(find(self.driver, X.QUANTIDADE_DE_BLOCOS, all=True))
    
    def quantidade_de_paginas(self):
        return int(find(self.driver, X.QUANTIDADE_DE_PAGINAS).text)
    
    @retry_on_false(retries=3)
    def proxima_pagina(self):
        return safe_click(self.driver, X.PROXIMA_PAGINA)

    @retry_on_false(retries=3)
    def abrir_bloco(self, bloco):
        return safe_click(self.driver, X.ABRIR_BLOCO(bloco))
    
    @retry_find(retries=5)
    def info_bloco(self, xpath):
        return find(self.driver, xpath)
    
    # Pagina 2

    def get_info(self, campo):
        xpath = X.INFO[campo]
        elem = find(self.driver, xpath, wait=0.5)
        return elem.text if elem else None
    
    def abrir_outros_codigos(self):
        safe_click(self.driver, X.BTN_OUTROS_CODIGOS, wait=0.5)
        sleep(0.3)

    def get_outros_codigos(self):
        col1 = find(self.driver, X.OUTROS_COL1, all=True, wait=0.5)
        col2 = find(self.driver, X.OUTROS_COL2, all=True, wait=0.2)
        lista = []
        if col1:
            for i in range(len(col1)):
                outros_codigos = [col1[i].text, col2[i].text]
                lista.append(outros_codigos)     
        return lista
    
    # io

    def load_json(self):
        if not exists(self.path_raw):
            return {"empresas": []}
        with open(self.path_raw, "r") as f:
            return load(f)
        
    def save_json(self):
        with open(self.path_raw, "w", encoding="utf-8") as f:
            dump(self.data_json, f, indent=2, ensure_ascii=False)

    def loop(self):
        self.driver = web_driver()
        self.driver.get(self.url)

        numero_empreas_encontradas = self.numero_empresas_encontradas()
        self.resultado_por_pagina()

        quantidade_de_paginas = self.quantidade_de_paginas()


        page = 1
        companies = 1
        while page <= quantidade_de_paginas: # for page in range(1, quantidade_de_paginas + 1):

            quantidade_de_blocos_da_pagina = self.quantidade_de_blocos_da_pagina()
            bloco = 1
            while bloco <= quantidade_de_blocos_da_pagina: # for bloco in range(1, quantidade_de_blocos_da_pagina + 1):

                print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                logging.info(f"pagina = {page} / {quantidade_de_paginas}, bloco = {bloco} / {quantidade_de_blocos_da_pagina}, empresas = {companies} / {numero_empreas_encontradas}")
                
                # Pagina 1 - Seleciona e extrai informações do bloco

                try:
                    info_bloco_title2 = self.info_bloco(X.INFO_BLOCO_TITLE2(bloco)).text # info_bloco_title2 = find(self.driver, X.INFO_BLOCO_TITLE2(bloco)).text
                    info_bloco_title = self.info_bloco(X.INFO_BLOCO_TITLE(bloco)).text # info_bloco_title = find(self.driver, X.INFO_BLOCO_TITLE(bloco)).text
                    info_bloco_text = self.info_bloco(X.INFO_BLOCO_TEXT(bloco)).text # info_bloco_text = find(self.driver, X.INFO_BLOCO_TEXT(bloco)).text
                
                # Retornamos o loop e tentamos executar novamente
                except Exception as error:
                    sleep(10)
                    logging.error(f'info_bloco = error')
                    continue
                
                # Se já tivermos processado esse bloco então pule
                if info_bloco_title2 in self.siglas_existentes:
                    bloco += 1
                    companies += 1
                    logging.info(f"Bloco já processado: {info_bloco_title2}, {info_bloco_title}, {info_bloco_text}")
                    continue
                else:     
                    # Adiciona silga para controle do loop
                    self.siglas_existentes.add(info_bloco_title2)

                # Pagina 2 - Extrai informações da empresa

                self.abrir_bloco(bloco)

                sleep(0.91)

                self.abrir_outros_codigos()
                outros_codigos = self.get_outros_codigos()
                dados_empresa = {
                    "info_bloco_title2": info_bloco_title2,
                    "info_bloco_title": info_bloco_title,
                    "info_bloco_text": info_bloco_text,
                    "nome_pregao": self.get_info("nome_pregao"),
                    "codigo": self.get_info("cod_negociacao"),
                    "cvm": self.get_info("cod_cvm"),
                    "inicio": self.get_info("inicio_negociacao"),
                    "cnpj": self.get_info("cnpj"),
                    "atividade": self.get_info("atividade"),
                    "setorial": self.get_info("setorial"),
                    "site": self.get_info("site"),
                    "outros_codigos_de_negociacao": outros_codigos
                }

                logging.info(dados_empresa)

                # data.append(dados_empresa)
                self.data_json['empresas'].append(dados_empresa)

                # Volta para a seleção de blocos
                self.driver.back()                
                sleep(0.5)

                # Seta novamento o número de informações por pagina
                self.resultado_por_pagina()

                # Proximo bloco
                bloco += 1

                # Contador das empresas
                companies += 1


            self.proxima_pagina()
            page += 1        
        
    def main(self):
        try:
            self.loop()
        except Exception as error:
            self.save_json()
            logging.error(error)
        finally:
            self.driver.quit()
            self.save_json()   
        