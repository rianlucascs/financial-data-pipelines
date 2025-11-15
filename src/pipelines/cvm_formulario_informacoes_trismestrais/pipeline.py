
from src.pipelines.cvm_formulario_informacoes_trismestrais import ExtractFormularioInformacoesTrimestrais
from src.pipelines.cvm_formulario_informacoes_trismestrais import TransformFormularioInformacoesTrimestrais

class PipelineFormularioInformacoesTrimestrais:

    def run(self) -> None:
        pipeline = "cvm_formulario_informacoes_trimestrais"

        extract = ExtractFormularioInformacoesTrimestrais(pipeline)
        extract.main()

        transform = TransformFormularioInformacoesTrimestrais(pipeline)
        transform.main()


