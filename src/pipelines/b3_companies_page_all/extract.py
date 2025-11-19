
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from time import sleep
from os.path import join, exists
from pandas import read_csv, DataFrame
import logging

from src.config import *
from src.utils import options, find, safe_click, web_driver

class ExtractB3CompaniesPageAll:

    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.url = "https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm"
        self.driver = None


    def main(self):
        self.driver = web_driver()
        self.driver.get(self.url)
        sleep(20)
        