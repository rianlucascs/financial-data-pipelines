
from src.pipelines.cvm_fundos_de_investimentos_informacao_cadastral import PipelineCVMFundosDeInvestimentosInformacaoCadastral

class JobCVMFundosDeInvestimentosInformacaoCadastral:

    def __init__(self):
        self.pipeline = PipelineCVMFundosDeInvestimentosInformacaoCadastral()

    def should_run(self):
        """Regra de execução"""

        run = True
        
        print(f"JobCVMFundosDeInvestimentosInformacaoCadastral.should_run = {run}")
        return run

    def run(self):
        if self.should_run():
            self.pipeline.run()

if __name__ == "__main__":
    JobCVMFundosDeInvestimentosInformacaoCadastral().run()
