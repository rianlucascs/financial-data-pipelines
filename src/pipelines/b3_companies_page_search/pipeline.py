
from src.pipelines.b3_companies_page_search import ExtractB3CompaniesPage
from src.pipelines.b3_companies_page_search import TransformB3CompaniesPage

class PipelineB3CompaniesPage:

    def run(self) -> None:
        pipeline = "b3_companies_page"

        extract = ExtractB3CompaniesPage(
            pipeline, 
            update=False)
        extract.main()

        transform = TransformB3CompaniesPage(pipeline)
        transform.main()