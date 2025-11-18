from pathlib import Path

# Diretório base do projeto (raiz do repositório)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Diretório principal onde ficam todos os dados do projeto
DATA_DIR = BASE_DIR / "data"

# Diretório onde ficam as pastas de cada pipeline
PIPELINES = DATA_DIR / "pipelines"

# Retorna o caminho dos dados brutos (raw) de um pipeline específico
# Args:
#   pipeline (str): Nome do pipeline.
#   type_file (str): Tipo de arquivo (ex: 'csv', 'zip', 'xlsx').
PATH_RAW = lambda pipeline, type_file: PIPELINES / pipeline / "raw" / type_file

# Retorna o caminho dos dados intermediários (interim)
# Args:
#   pipeline (str): Nome do pipeline.
PATH_ITERIM = lambda pipeline: PIPELINES / pipeline / "interim"

# Retorna o caminho dos dados processados (processed)
# Args:
#   pipeline (str): Nome do pipeline.
#   process (str): Nome do tipo de processamento ou subetapa.
PATH_PROCESSED = lambda pipeline, process: PIPELINES / pipeline / "processed" / process

