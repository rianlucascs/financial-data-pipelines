

from pandas import read_csv

df = read_csv("Q:\\financial_data_pipelines\data\\pipelines\\b3_companies_page\\raw\\csv\\b3_dados_empresa.csv", sep=",", encoding="utf-8")

print(df)