
from src.config import *
from os.path import join
import json
from pandas import DataFrame

class TransformB3CompaniesPageAll:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def load_data_json(self):
        path = join(PATH_RAW(self.pipeline, "json"), "data.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def main(self):
        data = self.load_data_json()
        print(DataFrame(data["empresas"]))