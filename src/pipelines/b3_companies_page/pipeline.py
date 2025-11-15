
from src.pipelines.b3_companies_page import ExtractB3CompaniesPage

class PipelineB3CompaniesPage:

    def run(self) -> None:
        pipeline = "b3_companies_page"

        extract = ExtractB3CompaniesPage(pipeline)
        extract.main()