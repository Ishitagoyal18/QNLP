import scrapy
from scrapy.http import FormRequest



class PdfspiderSpider(scrapy.Spider):
    name = "pdfspider"
    allowed_domains = ["trendlyne.com"]
    start_urls = ["https://trendlyne.com/conference-calls/"]
    
    def parse(self, response):
        # Fill in the form details as needed
        return FormRequest.from_response(
            response,
            formdata={
                "username": "your_username",
                "password": "your_password"
            },
            callback=self.after_login
        )

    def after_login(self, response):
        # Check if login was successful by inspecting the response
        if "authentication failed" in response.body.decode('utf-8').lower():
            self.logger.error("Login failed")
            return

        # Proceed to the page where PDFs are listed
        yield scrapy.Request(url="https://trendlyne.com/conference-calls/", callback=self.parse_pdf_page)

    def parse_pdf_page(self, response):
        companies = response.css(".panel-post")
        
        for company in companies:
            org_name = company.css(".post-head .row a.post-head-title::text").get()
            org_pdf_url = company.css(".pdf-pill-container a.pdf-pill-link::attr(data-redirecturl)").get()
            
            if org_name and org_pdf_url:
                yield {
                    "Orgname": org_name,
                    "file_urls": [org_pdf_url],  # This key must be 'file_urls' for the FilesPipeline
                }
                
        next_page = response.css(".endless_container .row a.endless_more::attr(href)").get()
        if next_page is not None:
            next_page_url = "https://trendlyne.com" + next_page
            yield response.follow(next_page_url, self.parse_pdf_page)

    # def parse(self, response):
    #     companies = response.css(".panel-post")
        
    #     for company in companies:
    #         org_name = company.css(".post-head .row a.post-head-title::text").get()
    #         org_pdf_url = company.css(".pdf-pill-container a.pdf-pill-link::attr(data-redirecturl)").get()  
    #         if org_name:
    #             yield {
    #                 "Orgname": org_name,
    #                 "file_urls": [org_pdf_url], 
    #                 }
                
    #     next_page = response.css(".endless_container .row a.endless_more::attr(href)").get()
    #     if next_page is not None:
    #         next_page_url =  "https://trendlyne.com" + next_page
    #         yield response.follow(next_page_url, self.parse)
                
            
