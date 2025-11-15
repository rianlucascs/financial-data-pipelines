from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from os.path import join, exists
from os import makedirs, listdir, remove
from pandas import read_csv

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
    WebDriverException,
)

from src.config import *
import logging
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExtractB3CompaniesPage:
    """
    b3_companies_page é dependente dos dados de cvm_formulario_informacoes_trismestrais.
    """
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.url = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesPage/?language=pt-br"
        self.driver = None
    
    def _options(self):
        options = Options()
        options.add_argument("--start-maximized") # Abre o navegador maximizado (muitos sites ajustam layout com base no viewport)
        options.add_argument("--disable-infobars") # Remove barras do Chrome que podem atrapalhar cliques
        options.add_argument("--disable-extensions") # Remove extensões (caso existam)
        options.add_argument("--incognito") # Evita usar cache ou cookies antigos
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ) # Define um User-Agent comum para evitar bloqueios
        options.add_argument("--disable-popup-blocking") # Torna o scraping mais suave e reduz erros
        options.add_argument("--disable-notifications")
        # Rodar sem abrir o navegador # options.add_argument("--headless=new")
        return options

    def _company_data(self):
        path = PATH_PROCESSED("cvm_formulario_informacoes_trimestrais", "filter_columns_DENOM_CIA_e_CNPJ_CIA")
        path = join(path, "denom_cnpj_unicos.csv")
        if exists(path):
            try:
                df = read_csv(path, sep=",", encoding="utf-8")
                return df.values
            except Exception as error:
                logging.error(f"Erro ao abrir o arquivo '{path}': {error}")
                pass
        else:
            logging.warning(f"Arquivo '{path}' não encontrado no diretório de origem.")
            return None

    def _input_nome_da_empresa(self, company_name):
        xpath = '//*[@id="keyword"]'
        input_text = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        input_text.clear()
        sleep(2)
        input_text.send_keys(company_name)
    
    def _press_button_buscar(self):
        xpath = '//*[@id="accordionName"]/div/app-companies-home-filter-name/form/div/div[3]/button'
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.XPATH  , xpath))
            )
        except:
            pass  # se não existir backdrop, segue normal
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        button.click()
        logging.info("Clicando em 'buscar'")
        sleep(1)

    def _select_resultado_da_busca(self, names, company_cnpj):

        logging.info(f"Page 2 - Resultado da busca")
        logging.info(f"Var: names = {names}")

        # Controle quantidade de blocos
        xpath_empresas_encontradas = '//*[@id="divContainerIframeB3"]/form/div[1]/div/div/div[1]/p/span[1]'
        try:
            numero_empresas_encontradas = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH, xpath_empresas_encontradas)))
            numero_empresas_encontradas = int(numero_empresas_encontradas.text)
        except:
            numero_empresas_encontradas = 1
        
        logging.info(f"Número de empreas encontradas na busca 'resultados': '{numero_empresas_encontradas}'")
        
        # Controle do bloco em questao
        for n_bloco in list(range(numero_empresas_encontradas)):
            n_bloco = n_bloco + 1

            logging.info(f"BLOCO: {n_bloco}")
            
            if numero_empresas_encontradas == 1:
                xpath = '//*[@id="nav-bloco"]/div/div/div/div/p[%2]'

            else:
                xpath = f'//*[@id="nav-bloco"]/div/div[{n_bloco}]/div/div/p[%2]'
            
            # Informações dentro do bloco
            for n_info_bloco in [1, 2]:

                xpath_bloco = xpath.replace("%2", str(n_info_bloco))

                # //*[@id="nav-bloco"]/div/div/div/div/p[1]
                logging.info(f"XPATH_BLOCO: {xpath_bloco}")
                
                output_bloco_text = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_bloco))).text

                logging.info(f"BLOCO = {n_bloco}, N_INFO_BLOCO = {n_info_bloco}, INFO = {output_bloco_text}")
                
                # Informações
                for name in names:

                    if name == None:
                        continue

                    logging.info(f"for var: nome = {name}")

                    if name in output_bloco_text:
                        press_box_text = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_bloco)))
                        press_box_text.click()

                        logging.info(f"Encontrado em: N_INFO_BLOCO = {n_info_bloco}, = BLOCO = {n_bloco}")

                        dados_da_companhia_cnpj = self._get_dados_da_companhia_cnpj()
                        logging.info(f"CNPJ informado = '{company_cnpj}', CNPJ page = '{dados_da_companhia_cnpj}'")

                        if company_cnpj == dados_da_companhia_cnpj:

                            logging.info("Bloco selecionado contem o cnpj correto!")

                            return {"status": True, "page": 3}
                        else:

                            # ...
                            
                            logging.error(f"Bloco selecionado não contem o cnpj correto!.")

                            
                            # Se não encontrar dentro do bloco então voltar e continuar procurando
                            self._back_page(1)
                        
                            # return {"status": None, "page": 3}
                    
                logging.info(f"Não encontrado: N_INFO_BLOCO = {n_info_bloco}, = {n_bloco}")

        return {"status": None, "page": 2}
                

    def _check_and_transform_company_name(self, company_name):

        # Se o nome conter informação de restrição
        palavras = ["EM RECUPERAÇÃO JUDICIAL", "EM RECUPERAÇÃO JUDICIAL", "EM LIQUIDAÇÃO"]
        if any(p in company_name for p in palavras):
            logging.error("Empresa com restrição no nome.")
            return None
        
        # Se o nome contiver 2 nomes (abreviações, siglas)
        elif " - " in company_name:
            logging.info("Nome empresa contem abreviações ou siglas.")
            company_name = company_name.split(" - ")
            return [company_name[0], company_name[1]]

        else:
            return [company_name, None]
    
    def _check_message_nao_ha_dados_disponiveis(self):
        xpath = '//*[@id="accordionName"]/div/app-companies-home-filter-name/form/div[2]/div/div'
        try:
            message = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            logging.info(f"Não há dados disponíveis para esta consulta.")
            return True
        except:
            logging.info("Existe dados.")
            return False
    
    def _back_page(self, qtd):
        for _ in range(qtd):
            sleep(1)
            logging.info("Voltar página.")
            self.driver.back()
            

    # --- get infos --- #
    
    def _get_dados_da_companhia_cnpj(self):
        
        # Buscando a informação do cnpj nas divs dinamicas da página
        for i in range(10):
            i += 1

            xpath = f'//*[@id="divContainerIframeB3"]/app-companies-overview/div/div[1]/div/div/div[{i}]/p[2]'
            try:
                dados_da_companhia_cnpj = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath))).text
            except:
                dados_da_companhia_cnpj = "error"
            if "-" in dados_da_companhia_cnpj and "/" in dados_da_companhia_cnpj and "." in dados_da_companhia_cnpj:
                return dados_da_companhia_cnpj
            
        return None

    def _save_dados_da_companhia(self):
        pass

        

    def main(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self._options())
        self.driver.get(self.url)
        company_data = self._company_data()
        try:
            i = 0
            while i < len(company_data):
                
                # Controla a posição
                if i < 31:
                    i += 1
                    continue

                company_name = company_data[i][0]
                company_cnpj = company_data[i][1]

                logging.info(f"{ '===' * 20}")
                logging.info(f"Page 1 - Index: {i}, Name: {company_name}, CNPJ: {company_cnpj}")

                # -----------------------------------------------------------------------------

                check_company_name = self._check_and_transform_company_name(company_name)

                # Se tiver informações no nome da empresa que indique o estado do ativo 
                if check_company_name == None:

                    # Pular para a proxima empresa
                    i += 1
                    continue
                
                names = check_company_name if isinstance(check_company_name, list) else [check_company_name]

                found = False

                for name in names:
                    
                    # Trata a saida 'else' da função '_check_and_transform_company_name'
                    if name == None:
                        found = False
                        break

                    self._input_nome_da_empresa(name)
                    sleep(1)
                    self._press_button_buscar()
                    
                    if self._check_message_nao_ha_dados_disponiveis():
                        logging.info(f"Nome não encontrado: {name}.")
                        continue
                    else:
                        logging.info(f"Nome encontrado: {name}.")
                        found = True
                        break
                
                # Se nenhum nome funcionou → vai para a próxima empresa
                if not found:
                    i += 1
                    continue
                
                # -----------------------------------------------------------------------------

                select_resultado_da_busca = self._select_resultado_da_busca(names, company_cnpj)

                logging.info(f"var: select_resultado_da_busca = {select_resultado_da_busca}")
                
                if select_resultado_da_busca["page"] == 3:
                    self._back_page(2)
                elif select_resultado_da_busca["page"] == 2:
                    self._back_page(1)

                if select_resultado_da_busca["status"] == None:
                    i += 1
                    continue

                i += 1

        finally:
            # self.driver.quit()
            pass



# [Simples, Objetivo, Profissional, Explicação simples]