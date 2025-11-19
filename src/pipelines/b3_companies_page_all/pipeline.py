from src.pipelines.b3_companies_page_all import ExtractB3CompaniesPageAll


class PipelineB3CompaniesPageAll:


    def run(self) -> None:
        pipeline = "B3_companies_page_all"
        extract = ExtractB3CompaniesPageAll(pipeline)
        extract.main()

