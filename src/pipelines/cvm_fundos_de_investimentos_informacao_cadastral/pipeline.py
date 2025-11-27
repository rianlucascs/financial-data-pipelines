
from src.pipelines.cvm_fundos_de_investimentos_informacao_cadastral import ExtractCVMFundosDeInvestimentosInformacaoCadastral

class PipelineCVMFundosDeInvestimentosInformacaoCadastral:

    def run(self):
        pipeline = "cvm_fundos_de_investimentos_informacao_cadastral"

        extract = ExtractCVMFundosDeInvestimentosInformacaoCadastral(pipeline)
        extract.main()


