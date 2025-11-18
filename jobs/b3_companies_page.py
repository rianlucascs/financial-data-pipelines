
from src.pipelines.b3_companies_page_search import PipelineB3CompaniesPage

class JobB3CompaniesPage:
    
    def __init__(self):
        self.pipeline = PipelineB3CompaniesPage()

    def should_run(self):
        return False

    def run(self):
        if self.should_run():
            self.pipeline.run()

if __name__ == "__main__":
    JobB3CompaniesPage().run()
