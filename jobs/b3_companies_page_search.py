
from src.pipelines.b3_companies_page_search import PipelineB3CompaniesPageSearch

class JobB3CompaniesPageSearch:
    
    def __init__(self):
        self.pipeline = PipelineB3CompaniesPageSearch()

    def should_run(self):
        """
        Regra de execução
        """

        run = False
        
        print(f"PipelineB3CompaniesPageSearch.should_run = {run}")
        return run

    def run(self):
        if self.should_run():
            self.pipeline.run()

if __name__ == "__main__":
    JobB3CompaniesPageSearch().run()
