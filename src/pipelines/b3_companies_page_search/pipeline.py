
from src.pipelines.b3_companies_page_search import ExtractB3CompaniesPageSearch
from src.pipelines.b3_companies_page_search import TransformB3CompaniesPageSearch

class PipelineB3CompaniesPageSearch:

    def run(self) -> None:
        pipeline = "b3_companies_page_search"

        extract = ExtractB3CompaniesPageSearch(
            pipeline, 
            update=False
            )
        extract.main()

        transform = TransformB3CompaniesPageSearch(pipeline)
        transform.main()