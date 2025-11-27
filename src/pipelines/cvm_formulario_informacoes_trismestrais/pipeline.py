
from src.pipelines.cvm_formulario_informacoes_trismestrais import ExtractCVMFormularioInformacoesTrimestrais
from src.pipelines.cvm_formulario_informacoes_trismestrais import TransformCVMFormularioInformacoesTrimestrais


class PipelineCVMFormularioInformacoesTrimestrais:

    def run(self):
        pipeline = "cvm_formulario_informacoes_trimestrais"

        extract = ExtractCVMFormularioInformacoesTrimestrais(pipeline)
        extract.main()

        transform = TransformCVMFormularioInformacoesTrimestrais(pipeline)
        transform.main()


