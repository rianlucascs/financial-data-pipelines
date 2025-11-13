
from src.pipelines.formulario_informacoes_trismestrais import ExtractFormularioInformacoesTrimestrais
from src.pipelines.formulario_informacoes_trismestrais import TransformFormularioInformacoesTrimestrais

class PipelineFormularioInformacoesTrimestrais:

    def run(self) -> None:
        pipeline = "formulario_informacoes_trimestrais"

        extract = ExtractFormularioInformacoesTrimestrais(pipeline)
        extract.main()

        transform = TransformFormularioInformacoesTrimestrais(pipeline)
        transform.main()


