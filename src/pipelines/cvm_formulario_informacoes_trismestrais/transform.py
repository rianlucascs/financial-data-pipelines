
from src.config import *
from os.path import join, exists
from os import listdir
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

    def concats_csv(self) -> None:
        """Concatena os arquivos CSV anuais de cada demonstração e salva um arquivo consolidado."""
        print(f"\n{__class__.__name__}\n_concats_csv\n")

        # leitura dos dados

        for itr_name in self.itrs:
            df = DataFrame()
            
            # caminho destino
            name_interim_csv = f'itr_cia_aberta_{itr_name}_2011-{self.year_now}.csv'
            path_iterim_csv = join(PATH_ITERIM(self.pipeline), name_interim_csv)
            
            if not exists(path_iterim_csv):
                for for_year in range(2011, self.year_now + 1):
                    
                    try:
                        
                        name_raw_csv = f'itr_cia_aberta_{itr_name}_{for_year}.csv' 
                        path_raw_csv = join(PATH_RAW(self.pipeline, "csv"), name_raw_csv)

                        df_raw_csv = read_csv(path_raw_csv, sep=";", decimal=",", encoding="iso-8859-1")
                        
                    except Exception as erro:
                        logging.error(f"Erro ao abrir o arquivo '{name_raw_csv}': {erro}")
                        continue
                    
                    # processamento

                    df = concat([df, df_raw_csv])
                df.to_csv(path_iterim_csv, index=False, encoding='utf-8', mode='w')

                logging.info(f"Arquivo '{name_interim_csv}' criado e salvo com sucesso.")
            else:
                logging.info(f"Arquivo '{name_interim_csv}' já existe.")  
                
    def order_columns_CD_CONTA_e_DS_CONTA(self):
        """Gera arquivos de texto hierárquicos com as contas contábeis (CD_CONTA e DS_CONTA)."""
        print(f"\n{__class__.__name__}\n_order_columns_CD_CONTA_e_DS_CONTA\n")

        # leitura dos dados

        for itr_name in self.itrs:
            
            # caminho destino
            name_order_columns_txt = join(f'itr_cia_aberta_{itr_name}.txt')
            path_processed_order_columns_txt = join(PATH_PROCESSED(self.pipeline, "order_columns_CD_CONTA_e_DS_CONTA"), name_order_columns_txt)
            
            if not exists(path_processed_order_columns_txt):
                try:

                    name_iterim_csv = f'itr_cia_aberta_{itr_name}_2011-{self.year_now}.csv'
                    path_iterim_csv = join(PATH_ITERIM(self.pipeline), name_iterim_csv)

                    df_iterim_csv = read_csv(path_iterim_csv, sep=",", decimal=",", encoding="utf-8")

                except Exception as erro:
                    logging.error(f"Erro ao abrir o arquivo '{name_iterim_csv}': {erro}")
                    continue
                
                # processamento

                df_iterim_csv = df_iterim_csv[df_iterim_csv["ORDEM_EXERC"] == "ÚLTIMO"]
                df_iterim_csv = df_iterim_csv[["CD_CONTA", "DS_CONTA"]].drop_duplicates()
                df_iterim_csv = df_iterim_csv.sort_values(by="CD_CONTA")

                df_iterim_csv["NIVEL"] = df_iterim_csv["CD_CONTA"].apply(lambda codigo: codigo.count("."))

                # Gera o texto hierárquico
                linhas = []
                for _, row in df_iterim_csv.iterrows():
                    indent = "    " * row["NIVEL"]  # 4 espaços por nível
                    linhas.append(f"{indent}{row['CD_CONTA']} -> {row['DS_CONTA']}")

                # Salva em arquivo de texto
                with open(path_processed_order_columns_txt, "w", encoding="utf-8") as f:
                    f.write("\n".join(linhas))
                    
                logging.info(f"Arquivo '{name_order_columns_txt}' criado e salvo com sucesso.")
            else:
                logging.info(f"Arquivo '{name_order_columns_txt}' já existe.")
    
    def filter_columns_DENOM_CIA_e_CNPJ_CIA(self):
        """Cria um arquivo CSV com a lista única de companhias (DENOM_CIA)."""
        print(f"\n{__class__.__name__}\n_filter_columns_DENOM_CIA_e_CNPJ_CIA\n")

        # --- READ DATA --- #

        name_lista_denom_cia_csv = join(f'denom_cnpj_unicos.csv')
        path_processed_lista_denom_cia_csv = join(PATH_PROCESSED(self.pipeline, "filter_columns_DENOM_CIA_e_CNPJ_CIA"), name_lista_denom_cia_csv)
        
        if not exists(path_processed_lista_denom_cia_csv):

            name_interim_csv = f'itr_cia_aberta_BPA_con_2011-{self.year_now}.csv'
            path_iterim_csv = join(PATH_ITERIM(self.pipeline), name_interim_csv)

            try:

                df_iterim_csv = read_csv(path_iterim_csv, sep=",", decimal=",", encoding="utf-8")

            except Exception as erro:
                logging.error(f"Erro ao abrir o arquivo '{name_interim_csv}': {erro}")
                return
            
            # --- PROCESSED --- #
            df_iterim_csv[["DENOM_CIA", "CNPJ_CIA"]].drop_duplicates().to_csv(path_processed_lista_denom_cia_csv, index=False)

            logging.info(f"Arquivo '{name_lista_denom_cia_csv}' criado e salvo com sucesso.")
        
        else:
            logging.info(f"Arquivo '{name_lista_denom_cia_csv}' já existe.")


    def main(self) -> None:
        self.concats_csv()
        self.order_columns_CD_CONTA_e_DS_CONTA()
        