
from src.pipelines.b3_companies_page_all import PipelineB3CompaniesPageAll

class JobB3CompaniesPageAll:
    
    def __init__(self):
        self.pipeline = PipelineB3CompaniesPageAll()

    def should_run(self):
        """
        Regra de execução
        """

        run = True

        print(f"JobB3CompaniesPageAll.should_run = {run}")
        return run

    def run(self):
        if self.should_run():
            self.pipeline.run()

if __name__ == "__main__":
    JobB3CompaniesPageAll().run()
