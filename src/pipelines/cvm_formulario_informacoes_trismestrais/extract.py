
from datetime import date
from src.config import *
from os.path import join, exists
import wget
from zipfile import ZipFile
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExtractFormularioInformacoesTrimestrais:
    
    def __init__(self, pipeline: str) -> None:
        self.pipeline = pipeline
        self.url = "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/"

        self.year_now = date.today().year
        self.archives_zip = [f'itr_cia_aberta_{year_now}.zip' for year_now in range(2011, self.year_now + 1)]

    def wget_zip(self):
        """Faz o download dos arquivos ZIP de dados trimestrais (ITR) do site da CVM."""
        print(f"\n{__class__.__name__}\n_wget_zip\n")
        for file in self.archives_zip:
            
            path = join(PATH_RAW(self.pipeline, "zip"), file)

            if not exists(path):
                try:
                    wget.download(self.url+file, path, bar=False)
                    logging.info(f"Download realizado com sucesso: {file}")
                except Exception as erro:
                    logging.error(f"Erro ao fazer o download do arquivo '{file}': {erro}")
            else:
                logging.info(f"Arquivo '{file}' já existe. Nenhum download necessário.")

    def extract_zip(self) -> None:
        """Extrai os arquivos CSV contidos nos arquivos ZIP baixados."""
        print(f"\n{__class__.__name__}\n_extract_zip\n")
        for file in self.archives_zip:
            
            path_zip = join(PATH_RAW(self.pipeline, "zip"), file)
            
            if exists(path_zip):
                try:
                    with ZipFile(path_zip, 'r') as zip_ref:
                        
                        arquivos_no_zip = zip_ref.namelist() # lista todos os arquivos dentro do .ZIP
                        
                        for file_zip in arquivos_no_zip:
                            try:
                                if not exists(join(PATH_RAW(self.pipeline, "csv"), file_zip)):
                                    zip_ref.extract(file_zip, PATH_RAW(self.pipeline, "csv"))
                                    logging.info(f"Arquivo '{file_zip}' do ZIP '{file}' extraído com sucesso.")
                                else:
                                    logging.info(f"Arquivo '{file_zip}' do ZIP '{file}' já existe. Nenhum download necessário.")
                            except Exception as erro:
                                logging.error(f"Erro ao extrair o arquivo '{file_zip}' do ZIP '{file}': {erro}")
                except Exception as erro:
                    logging.error(f"Erro ao abrir o arquivo ZIP '{file}': {erro}")
            else:
                logging.warning(f"Arquivo '{file}' não encontrado no diretório de origem.")

    def main(self) -> None:
        self.wget_zip()
        self.extract_zip()




