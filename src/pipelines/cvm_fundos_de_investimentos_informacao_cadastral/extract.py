import wget
from zipfile import ZipFile
from os.path import join, exists
from src.config import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExtractCVMFundosDeInvestimentosInformacaoCadastral:

    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.file = "registro_fundo_classe.zip"
        self.url = "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/registro_fundo_classe.zip"
        self.path_raw_zip = join(PATH_RAW(self.pipeline, "zip"), self.file)

    def wget_zip(self):
        
        if not exists(self.path_raw_zip):
            wget.download(self.url, self.path_raw_zip, bar=False)
            logging.info(f"Download realizado com sucesso: {self.file}")
        else:
            logging.info(f"Arquivo '{self.file}' já existe. Nenhum download necessário.")
    
    def extract_zip(self):
        if exists(self.path_raw_zip):
            try:
                with ZipFile(self.path_raw_zip, "r") as zip_ref:
                    arquivos_no_zip = zip_ref.namelist()
                    for file_zip in arquivos_no_zip:
                        if not exists(join(PATH_RAW(self.pipeline, "csv"), file_zip)):
                            try:
                                zip_ref.extract(file_zip, PATH_RAW(self.pipeline, "csv"))
                                logging.info(f"Arquivo '{file_zip}' do ZIP '{self.file}' extraído com sucesso.")
                            except Exception as error:
                                logging.error(f"Erro ao extrair o arquivo '{file_zip}' do ZIP '{self.file}': {error}")
                        else:
                            logging.info(f"Arquivo '{file_zip}' do ZIP '{self.file}' já existe. Nenhum download necessário.")
            except Exception as error:
                logging.error(f"Erro ao abrir o arquivo ZIP '{self.file}': {error}")
        else:
            logging.warning(f"Arquivo '{self.file}' não encontrado no diretório de origem.")

    def main(self):
        self.wget_zip()
        self.extract_zip()
    


    