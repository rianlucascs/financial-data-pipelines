
from os.path import join
from src.config import *
from pandas import read_csv

class TransformB3CompaniesPageSearch:

    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.path = join(PATH_RAW(self.pipeline, "csv"), "b3_dados_empresa.csv")

    def load_data(self):
        df = read_csv(self.path, encoding="utf-8", sep=',')
        return df

    def main(self):
        pass