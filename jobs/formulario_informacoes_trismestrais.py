
from src.pipelines.cvm_formulario_informacoes_trismestrais import PipelineFormularioInformacoesTrimestrais

class JobFormularioInformacoesTrimestrais:

    def __init__(self):
        self.pipeline = PipelineFormularioInformacoesTrimestrais()

    def should_run(self):
        """Regra de execução"""

        run = False
        
        print(f"JobFormularioInformacoesTrimestrais.should_run = {run}")
        return run

    def run(self):
        if self.should_run():
            self.pipeline.run()

if __name__ == "__main__":
    JobFormularioInformacoesTrimestrais().run()
