from time import sleep
from os.path import join, exists
import logging
from json import load, dump
from selenium.webdriver.common.by import By
from src.config import *
from src.utils import find, safe_click, web_driver, retry

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

    def __init__(self, pipeline, update=False):
        self.pipeline = pipeline
        self.update = update
        self.url = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/search?language=pt-br"
        self.driver = None
        self.companies = 1
        self.page = 1

        self.path_raw = join(PATH_RAW(self.pipeline, "json"), "data.json")
        self.data_json = self.load_json()
        self.siglas_existentes = {e["info_bloco_title2"] for e in self.data_json.get("empresas", [])}
        logging.info(f'Empresas processadas: {len(self.siglas_existentes)}')

    # Pagina 1

    def numero_empresas_encontradas(self):
        return int(find(self.driver, X.EMPRESAS_ENCONTRADAS).text.replace('.', ''))
    
    @retry(retries=3, type="Bool")
    def resultado_por_pagina(self):
        return safe_click(self.driver, X.RESULTADOS_POR_PAGINA)
        
    def quantidade_de_blocos_da_pagina(self):
        return len(find(self.driver, X.QUANTIDADE_DE_BLOCOS, all=True))
    
    def quantidade_de_paginas(self):
        return int(find(self.driver, X.QUANTIDADE_DE_PAGINAS).text)
    

    def proxima_pagina(self, wait=10):
        return safe_click(self.driver, X.PROXIMA_PAGINA, wait)

    @retry(retries=3, type="Bool")
    def abrir_bloco(self, bloco):
        return safe_click(self.driver, X.ABRIR_BLOCO(bloco))
    
    @retry(retries=3, type="None")
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
    
    def pagina_atual(self):
        current_page_elem = self.driver.find_element(By.CSS_SELECTOR, "ul.ngx-pagination li.current span:nth-of-type(2)")
        current_page = int(current_page_elem.text)
        return current_page
    
    # io

    def load_json(self):
        if not exists(self.path_raw):
            return {"empresas": []}
        with open(self.path_raw, "r", encoding="utf-8") as f:
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

        while self.page <= quantidade_de_paginas:

            quantidade_de_blocos_da_pagina = self.quantidade_de_blocos_da_pagina()
            bloco = 1
            while bloco <= quantidade_de_blocos_da_pagina:
                
                print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

                # Paginação

                self.resultado_por_pagina()

                pagina_atual = self.pagina_atual()

                logging.info(f"pagina_atual = {pagina_atual}")

                if pagina_atual < self.page:
                    
                    if self.page > 1:
                        for _ in range(self.page-1):
                            self.proxima_pagina(wait=15)
                            sleep(2.5)
                            pagina_atual = self.pagina_atual()
                            if self.page == pagina_atual:
                                break

                if pagina_atual > self.page:
                    self.driver.get(self.url)
                    sleep(5)
                    logging.warning(f"pagina_atual = {pagina_atual} > self.page = {self.page}")
                    continue
                
                pagina_atual = self.pagina_atual()

                logging.info(f"pagina_atual = {pagina_atual}")
                
                logging.info(f"pagina_contador = {self.page} / {quantidade_de_paginas}, bloco = {bloco} / {quantidade_de_blocos_da_pagina}, empresas = {self.companies} / {numero_empreas_encontradas}")
                
                # Pagina 1 - Seleciona e extrai informações do bloco

                try:
                    info_bloco_title2 = self.info_bloco(X.INFO_BLOCO_TITLE2(bloco)).text 
                    info_bloco_title = self.info_bloco(X.INFO_BLOCO_TITLE(bloco)).text 
                    info_bloco_text = self.info_bloco(X.INFO_BLOCO_TEXT(bloco)).text
                
                # Retornamos o loop, salva os dados e tenta executar novamente
                except Exception as error:
                    logging.error(f'info_bloco = error')
                    self.driver.close()
                    sleep(1.3)
                    self.driver = web_driver()
                    self.driver.get(self.url)
                    sleep(0.9)
                    continue
                
                # Se já tivermos processado esse bloco então pule
                if info_bloco_title2 in self.siglas_existentes:
                    bloco += 1
                    logging.info(f"Bloco já processado: {info_bloco_title2}, {info_bloco_title}, {info_bloco_text}")
                    self.companies += 1
                    sleep(0.3)
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

                # Salva progresso
                self.data_json['empresas'].append(dados_empresa)
                self.save_json()

                # Volta para a seleção de blocos
                self.driver.get(self.url) # self.driver.back()                
                sleep(3)

                # Seta novamento o número de informações por pagina
                self.resultado_por_pagina()

                sleep(1)

                # Proximo bloco
                bloco += 1

                # Contador das empresas
                self.companies += 1

            self.page += 1        
            sleep(1.3)

        
    def main(self):
        if self.update is False:
            logging.warning(f"{self.__class__.__name__}, update = False")
            return
        try:
            self.loop()
        except Exception as error:
            self.driver.close()
            logging.error(error)
            self.main()
        finally:
            self.driver.quit() 
