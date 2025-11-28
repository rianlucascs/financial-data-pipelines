
from src.pipelines.cvm_fundos_de_investimento_documentos_informe_diario import ExtractCVMFundosDeInvestimentoDocumentoInformeDiario

class PipelineCVMFundosDeInvestimentoDocumentoInformeDiario:

    def run(self):
        pipeline = "cvm_fundos_de_investimento_documentos_informe_diario"

        extract = ExtractCVMFundosDeInvestimentoDocumentoInformeDiario(pipeline)
        extract.main()



