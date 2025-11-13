
    project/
    │
    ├── src/                                 # Código principal do pipeline
    │   │
    │   ├── config/                           # Arquivos de configuração
    │   │   ├── settings.yaml                 # Ex.: caminhos, credenciais (nunca sensíveis no Git)
    │   │   ├── paths.py
    │   │   └── __init__.py
    │   │
    │   ├── pipelines/                        # Cada pipeline é um módulo isolado
    │   │   ├── formulario_informacoes_trimestrais/
    │   │   │   ├── __init__.py
    │   │   │   ├── extract.py                # Extração de dados (APIs, DBs, arquivos)
    │   │   │   ├── transform.py              # Limpeza e transformação
    │   │   │   ├── load.py                   # Carga para DW/Data Lake/DB
    │   │   │   └── pipeline.py               # Orquestra Extract → Transform → Load
    │   │   │
    │   │   └── exemplo/
    │   │       ├── __init__.py
    │   │       ├── extract.py
    │   │       ├── transform.py
    │   │       ├── load.py
    │   │       └── pipeline.py
    │   │
    │   └── utils/                              # Funções auxiliares reutilizáveis
    │       └── db.py                           # Conexão com bancos de dados
    │
    │
    ├── jobs/                                   # Onde você define quando e como rodar cada pipeline
    │   ├── formulario_informacoes_trimestrais.py
    │   └── exemplo.py
    │
    │
    ├── tests/                                  # Testes unitários e de integração
    │   ├── test_formulario_extract.py
    │   ├── test_formulario_transform.py
    │   └── test_utils_db.py
    │
    ├── notebooks/                               # Estudos e protótipos
    │   └── explore_finance_data.ipynb
    │
    │
    ├── run.bat                                  # Script Windows para executar jobs
    ├── requirements.txt                         # Dependências
    └── README.md                                # Documentação do projeto
