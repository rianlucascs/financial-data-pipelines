from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
from os.path import join, exists
from pandas import read_csv, DataFrame
import logging

from src.config import *
from src.utils import options, find, safe_click, web_driver

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")

class X:

    INPUT_EMPRESA =                 '//*[@id="keyword"]'
    BUTTON_BUSCAR =                 '//*[@id="accordionName"]/div/app-companies-home-filter-name/form/div/div[3]/button'
    MSG_NAO_HA_DADOS =              '//*[@id="accordionName"]/div/app-companies-home-filter-name/form/div[2]/div/div'

    RESULT_NUMERO_EMPRESAS =        '//*[@id="divContainerIframeB3"]/form/div[1]/div/div/div[1]/p/span[1]'
    BLOCOS =                        '//*[@id="nav-bloco"]/div/div'

    BTN_OUTROS_CODIGOS =            '//a[contains(@href, "#accordionBody2")]'
    OUTROS_COL1 =                   '//*[@id="accordionBody2"]//table/tr/td[1]/p'
    OUTROS_COL2 =                   '//*[@id="accordionBody2"]//table/tr/td[2]/p'
                    
    INFO = {
        "nome_pregao":         '//*[@class="card-text"][strong[text()="Nome do Pregão"]]/following-sibling::p[@class="card-linha"]',
        "cod_negociacao":      '//*[@class="card-text"][strong[text()="Código de Negociação"]]/following-sibling::p/a',
        "cod_cvm":             '//*[@id="accordionBody2"]//span[b[text()="Código CVM"]]/p',
        "inicio_negociacao":   '//*[@class="card-text"][strong[text()="Início de negociação das ações"]]/following-sibling::p',
        "cnpj":                '//*[@class="card-text"][strong[text()="CNPJ"]]/following-sibling::p',
        "atividade":           '//*[@class="card-text"][strong[text()="Atividade Principal"]]/following-sibling::p',
        "setorial":            '//*[@class="card-text"][strong[text()="Classificação Setorial"]]/following-sibling::p',
        "site":                '//*[@class="card-text"][strong[text()="Site"]]/following-sibling::p/a'
    }

class ExtractB3CompaniesPageSearch:

    def __init__(self, pipeline, update=False):
        self.pipeline = pipeline
        self.update = update
        self.url = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/?language=pt-br"
        self.driver = None
        self.registros = []

    # leitura do arquivo

    def dados_empresa(self):
        path = PATH_PROCESSED("cvm_formulario_informacoes_trimestrais", "filter_columns_DENOM_CIA_e_CNPJ_CIA")
        path = join(path, "denom_cnpj_unicos.csv")
        if not exists(path):
            logging.warning(f"Arquivo não encontrado: {path}")
            return None
        df = read_csv(path, sep=",", encoding="utf-8")
        return df.values
    
    # pagina 1

    def input_empresa(self, name):
        campo = find(self.driver, X.INPUT_EMPRESA)
        campo.clear()
        sleep(0.5)
        campo.send_keys(name)

    def buscar(self):
        safe_click(self.driver, X.BUTTON_BUSCAR)
        sleep(0.7)

    def nao_ha_dados(self):
        return find(self.driver, X.MSG_NAO_HA_DADOS, wait=3) is not None
    
    # pagina 2

    def numero_blocos(self):
        elem = find(self.driver, X.RESULT_NUMERO_EMPRESAS, wait=5)
        return int(elem.text) if elem else 1

    def xpath_info_bloco(self, bloco, linha):
        """
        bloco = 1, 2, 3...
        linha = 1 ou 2
        """
        return f'//*[@id="nav-bloco"]/div/div[{bloco}]/div/div/p[{linha}]'
    
    def selecionar_bloco_correto(self, nomes, cnpj):
        qtd_blocos = self.numero_blocos()

        logging.info(f"qtd_blocos = {qtd_blocos}")

        for bloco in range(1, qtd_blocos + 1):


            for linha in [1, 2]:
                
                logging.warning(f"page 2, bloco = {bloco}, linha = {linha}")

                xpath_info = self.xpath_info_bloco(bloco, linha)
                info = find(self.driver, xpath_info, wait=5)
                if not info:
                    continue

                texto = info.text

                for nome in nomes:
                    if nome and nome in texto:

                        logging.info(f"page 2, bloco = {bloco}, linha = {linha}, nome = '{nome}', texto = '{texto}'")

                        # click
                        safe_click(self.driver, xpath_info)

                        # verifica CNPJ
                        cnpj_page = self.get_info("cnpj")

                        if cnpj_page == cnpj:
                            logging.info("cnpj == cnpj_page")
                            return True 
                        else: 
                            logging.warning(f"cnpj != cnpj_page")
                            self.driver.back()
                            sleep(0.5)

        logging.warning("informação não encontrada em nenhum dos blocos")
        return False

    # pagina 3

    def get_info(self, campo):
        xpath = X.INFO[campo]
        elem = find(self.driver, xpath)
        return elem.text if elem else None

    def abrir_outros_codigos(self):
        safe_click(self.driver, X.BTN_OUTROS_CODIGOS)
        sleep(0.5)

    def get_outros_codigos(self):
        col1 = find(self.driver, X.OUTROS_COL1, all=True)
        col2 = find(self.driver, X.OUTROS_COL2, all=True)

        lista = []
        
        if col1:
            for i in range(len(col1)):
                outros_codigos = [col1[i].text, col2[i].text]
                lista.append(outros_codigos)     

        return lista
        
    # utils

    def tratar_nome(self, nome):
        restritos = ["EM RECUPERAÇÃO JUDICIAL", "EM LIQUIDAÇÃO"]
        if any(r in nome for r in restritos):
            return None

        if " - " in nome:
            a, b = nome.split(" - ")
            return [a, b]

        return [nome]

    def se_nao_tiver_dados(self, nome, cnpj):
        return {
            "nome_pregao": nome,
            "codigo": "nan",
            "cvm": "nan",
            "inicio": "nan",
            "cnpj": cnpj,
            "atividade": "nan",
            "setorial": "nan",
            "site": "nan",
            "outros_codigos_de_negociacao": "nan"
        }
    
    def main(self):
        if self.update is False:
            logging.warning("update = False")
            return
        
        self.driver = web_driver()
        self.driver.get(self.url)

        dados = self.dados_empresa()

        if dados is None:
            return
        
        index = 0      
 
        while index < len(dados):

            try:
                # if index < 728:
                #     index += 1
                #     continue

                # if index > 728:
                #     return

                empresa = dados[index][0]
                cnpj = dados[index][1]

                logging.info(f"{'-'*40}")
                logging.info(f"index = {index}")
                logging.info(f"pagina 1")
                logging.info(f"empresa = {empresa}, cnpj = {cnpj}")

                nomes = self.tratar_nome(empresa)

                # --- Página 1 ---

                if nomes is None: # empresa com restrição
                    index += 1
                    self.registros.append(self.se_nao_tiver_dados(empresa, cnpj))
                    continue

                achou = False
                
                # Tentativa com nome pricipal e variações
                for nome in nomes:

                    self.input_empresa(nome)
                    self.buscar()

                    if self.nao_ha_dados():
                        continue
                    
                    achou = True
                    break

                if not achou:
                    index += 1
                    self.registros.append(self.se_nao_tiver_dados(empresa, cnpj))
                    continue

                # --- Página 2 ---

                correto = self.selecionar_bloco_correto(nomes, cnpj)

                # Se não enctroou o bloco
                if not correto:
                    self.driver.back()
                    index += 1
                    self.registros.append(self.se_nao_tiver_dados(empresa, cnpj))
                    sleep(0.5)
                    continue

                # --- Página 3 ---

                self.abrir_outros_codigos()
                outros_codigos = self.get_outros_codigos()

                dados_empresa = {
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

                logging.info(f"Dados coletados: {dados_empresa}")

                self.registros.append(dados_empresa)

                self.driver.back()
                sleep(0.3)
                self.driver.back()
                index += 1
                sleep(0.5)

            except Exception as error:
                
                logging.warning(f"erro no código, reiniciando... {error}")
                self.driver.quit()
                sleep(50)
                self.driver = web_driver()
                self.driver.get(self.url)

                continue

        # --- salvar ---

        df = DataFrame(self.registros)
        path = join(PATH_RAW(self.pipeline, "csv"), "dados.csv")
        df.to_csv(path, index=False, encoding="utf-8", mode="w")
        logging.info(f"Arquivo salvo em: {path}")

            
