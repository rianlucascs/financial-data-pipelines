
from src.pipelines.cvm_fundos_de_investimento_documentos_informe_diario import PipelineCVMFundosDeInvestimentoDocumentoInformeDiario

class JobCVMFundosDeInvestimentoDocumentoInformeDiario:

    def __init__(self):
        self.pipeline = PipelineCVMFundosDeInvestimentoDocumentoInformeDiario()

    def should_run(self):
        """
        Regra de execução
        """

        run = True
        
        print(f"JobCVMFundosDeInvestimentosInformacaoCadastral.should_run = {run}")
        return run

    def run(self):
        if self.should_run():
            self.pipeline.run()

if __name__ == "__main__":
    JobCVMFundosDeInvestimentoDocumentoInformeDiario().run()
