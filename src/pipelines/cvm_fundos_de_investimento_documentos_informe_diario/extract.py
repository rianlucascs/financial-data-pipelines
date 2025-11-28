
from os.path import join, exists
from src.config import *
import wget
from zipfile import ZipFile
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExtractCVMFundosDeInvestimentoDocumentoInformeDiario:
    # https://dados.cvm.gov.br/dataset/fi-doc-inf_diario
    def __init__(self, pipeline):
        
        # historico desde 2000
        self.pipeline = pipeline
        self.url = "https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/HIST/"
        self.archives_hist_zip = [f"inf_diario_fi_{year}.zip" for year in range(2000, 2021)]
        self.folder_hist_desde_2000_zip = "hist_desde_2000_zip"
        self.folder_hist_desde_2000_csv = "hist_desde_2000_csv"
        
    
    def wget_zip_hist_desde_2000(self):
        logging.info(f"\n{__class__.__name__}\nwget_zip_hist_desde_2000\n")
        for file in self.archives_hist_zip:

            path_hist_zip = join(PATH_RAW(self.pipeline, self.folder_hist_desde_2000_zip), file)

            if not exists(path_hist_zip):
                try:
                    wget.download(self.url+file, path_hist_zip, bar=False)
                    logging.info(f"Download realizado com sucesso: {file}")
                except Exception as error:
                    logging.error(f"Erro ao fazer o download do arquivo '{file}': {error}")
            else:
                logging.info(f"Arquivo '{file}' já existe. Nenhum download necessário.")

    def extract_hist_desde_2000(self):
        logging.info(f"\n{__class__.__name__}\nextract_hist_desde_2000\n")
        for file in self.archives_hist_zip:

            path_hist_zip = join(PATH_RAW(self.pipeline, self.folder_hist_desde_2000_zip), file)

            if exists(path_hist_zip):
                try:
                    with ZipFile(path_hist_zip, "r") as zip_ref:
                        arquivos_no_zip = zip_ref.namelist()
                        for file_zip in arquivos_no_zip:
                            try:
                                if not exists(join(PATH_RAW(self.pipeline, self.folder_hist_desde_2000_csv), file_zip)):
                                    zip_ref.extract(file_zip, PATH_RAW(self.pipeline, self.folder_hist_desde_2000_csv))
                                    logging.info(f"Arquivo '{file_zip}' do ZIP '{file}' extraído com sucesso.")
                                else:
                                    logging.info(f"Arquivo '{file_zip}' do ZIP '{file}' já existe. Nenhum download necessário.")
                            except Exception as error:
                                logging.error(f"Erro ao extrair o arquivo '{file_zip}' do ZIP '{file}': {error}")
                except Exception as error:
                    logging.error(f"Erro ao abrir o arquivo ZIP '{file}': {error}")
            else:
                logging.warning(f"Arquivo '{file}' não encontrado no diretório de origem.")

    def main(self):
        self.wget_zip_hist_desde_2000()
        self.extract_hist_desde_2000()