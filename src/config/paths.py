from pathlib import Path

# Base do projeto (subindo direto até o root do repo)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Diretório principal onde ficam os dados
DATA_DIR = BASE_DIR / "data"

# Pasta principal de pipelines
PIPELINES = DATA_DIR / "pipelines"

# Retorna o caminho onde ficam os dados crus de um pipeline.
# pipeline = nome do pipeline
# type_file = tipo dos arquivos: csv, zip, xlsx,...
PATH_RAW = lambda pipeline, type_file: PIPELINES / pipeline / "raw" / type_file

# Retorna o caminho dos dados intermediários.
PATH_ITERIM = lambda pipeline: PIPELINES / pipeline / "interim"

# Retorna o caminho dos dados já processados.
# process = nome do processamento feito para separa os dados.
PATH_PROCESSED = lambda pipeline, process: PIPELINES / pipeline / "processed" / process

