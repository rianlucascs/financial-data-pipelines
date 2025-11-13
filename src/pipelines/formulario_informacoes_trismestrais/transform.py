
from src.config import *
from os.path import join, exists
from pandas import DataFrame, read_csv, concat
from datetime import date
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TransformFormularioInformacoesTrimestrais:

    def __init__(self, pipeline: str) -> None:
        self.pipeline = pipeline
        self.itrs = ['BPA_con', 'BPA_ind', 'BPP_con', 'BPP_ind', 'DFC_MD_con', 'DFC_MD_ind', 'DFC_MI_con', 
                      'DFC_MI_ind', 'DMPL_con', 'DMPL_ind', 'DRA_con', 'DRA_ind', 'DRE_con', 'DRE_ind', 'DVA_con', 'DVA_ind']
        self.year_now = date.today().year

    def _concat_files_csv(self) -> None:
        print(f"\n{__class__.__name__}\n_concat_files_csv\n")

        # --- READ DATA --- 

        for itr_name in self.itrs:
            df = DataFrame()
            
            # Arquivo final
            path_iterim_file_csv = join(PATH_ITERIM(self.pipeline), file_interim_csv:=f'itr_cia_aberta_{itr_name}_2011-{self.year_now}.csv')
            
            if not exists(path_iterim_file_csv):
                for for_year in range(2011, self.year_now + 1):
                    
                    try:
                        name_file_raw_csv = ""
                        name_file_raw_csv = f'itr_cia_aberta_{itr_name}_{for_year}.csv'
                        file_raw_csv = read_csv(join(PATH_RAW(self.pipeline, "csv"), name_file_raw_csv),
                            sep=";", decimal=",", encoding="iso-8859-1")
                        
                    except Exception as erro:
                        logging.error(f"Erro ao abrir o arquivo '{name_file_raw_csv}': {erro}")
                        continue
                    
                    # --- PROCESSED ---

                    df = concat([df, file_raw_csv])
                df.to_csv(path_iterim_file_csv, index=False, encoding='utf-8', mode='w')
                logging.info(f"Arquivo '{file_interim_csv}' criado e salvo com sucesso.")
            else:
                logging.info(f"Arquivo '{file_interim_csv}' já existe.")  

    def _filter_columns(self) -> None:
        print(f"\n{__class__.__name__}\n_filter_columns\n")

        # --- READ DATA --- 

        columns = ['DT_REFER', 'DENOM_CIA', 'CNPJ_CIA', 'VERSAO', 'ORDEM_EXERC', 'DT_FIM_EXERC', 
                   'CD_CONTA', 'DS_CONTA', 'VL_CONTA', 'ST_CONTA_FIXA']
        
        for itr_name in self.itrs:

            path_processed_filter_columns_csv = join(PATH_PROCESSED(self.pipeline, "filter_columns"), 
                                                      file_name:=f'itr_cia_aberta_{itr_name}_2011-{self.year_now}.csv')
            
            if not exists(path_processed_filter_columns_csv):
                try:

                    path_iterim_file_csv = join(PATH_ITERIM(self.pipeline), file_name)
                    iterim_file_csv = read_csv(path_iterim_file_csv, sep=",", decimal=",", encoding="iso-8859-1")
                    
                except Exception as erro:
                    logging.error(f"Erro ao abrir o arquivo '{file_name}': {erro}")
                    continue

                # --- PROCESSED ---

                file_processed_csv = iterim_file_csv[columns]
                file_processed_csv.to_csv(path_processed_filter_columns_csv, index=False, encoding='iso-8859-1', mode='w')
                logging.info(f"Arquivo '{path_iterim_file_csv}' criado e salvo com sucesso.")
            else:
                logging.info(f"Arquivo '{file_name}' já existe.")
                
    def _order_columns_CD_CONTA_e_DS_CONTA(self):
        print(f"\n{__class__.__name__}\n_order_columns_CD_CONTA_e_DS_CONTA\n")

        # --- READ DATA --- 

        for itr_name in self.itrs:

            path_order_columns_CD_CONTA_e_DS_CONTA_txt = join(PATH_PROCESSED(self.pipeline, "order_columns_CD_CONTA_e_DS_CONTA"), 
                                                      f'itr_cia_aberta_{itr_name}.txt')
            
            if not exists(path_order_columns_CD_CONTA_e_DS_CONTA_txt):
                try:

                    name_iterim_file_csv = f'itr_cia_aberta_{itr_name}_2011-{self.year_now}.csv'
                    path_iterim_file_csv = join(PATH_ITERIM(self.pipeline), name_iterim_file_csv)

                    iterim_file_csv = read_csv(path_iterim_file_csv, sep=",", decimal=",", encoding="utf-8")

                except Exception as erro:
                    logging.error(f"Erro ao abrir o arquivo '{name_iterim_file_csv}': {erro}")
                    continue
                
                # --- PROCESSED ---

                iterim_file_csv = iterim_file_csv[iterim_file_csv["ORDEM_EXERC"] == "ÚLTIMO"]
                iterim_file_csv = iterim_file_csv[["CD_CONTA", "DS_CONTA"]].drop_duplicates()
                iterim_file_csv = iterim_file_csv.sort_values(by="CD_CONTA")

                iterim_file_csv["NIVEL"] = iterim_file_csv["CD_CONTA"].apply(lambda codigo: codigo.count("."))

                # Gera o texto hierárquico
                linhas = []
                for _, row in iterim_file_csv.iterrows():
                    indent = "    " * row["NIVEL"]  # 4 espaços por nível
                    linhas.append(f"{indent}{row['CD_CONTA']} -> {row['DS_CONTA']}")

                # Salva em arquivo de texto
                with open(path_order_columns_CD_CONTA_e_DS_CONTA_txt, "w", encoding="utf-8") as f:
                    f.write("\n".join(linhas))
                    
                logging.info(f"Arquivo '{path_order_columns_CD_CONTA_e_DS_CONTA_txt}' criado e salvo com sucesso.")
            else:
                logging.info(f"Arquivo '{path_order_columns_CD_CONTA_e_DS_CONTA_txt}' já existe.")
            

    def main(self) -> None:
        self._concat_files_csv()
        self._filter_columns()
        self._order_columns_CD_CONTA_e_DS_CONTA()
        