import scrapy

from datetime import datetime
import os

class ImmoMarktSpider(scrapy.Spider):
    name = "immomarkt"

    # start_urls = [
    #     # 'https://1a-immobilienmarkt.de'
    #     # 'https://www.1a-immobilienmarkt.de/suchen/schleswig-holstein/wohnung-mieten.html'
    # ]    

    def start_requests(self):
        return [scrapy.FormRequest("https://1a-immobilienmarkt.de/suchen/schleswig-holstein/wohnung-mieten.html", 
        formdata={'seite': 2}, 
        callback=self.parse)]

    def parse(self, response):
        print('cokc')

        # formdata = dict()
        # formdata['seite'] = 2

        # url = 'https://www.1a-immobilienmarkt.de/suchen/schleswig-holstein/wohnung-mieten.html'

        # return FormRequest.from_response(response, formdata=formdata, callback=self.parse_bundesland)
        # house_types = [
        # ]

        # acquisition_types = [
        # ]

        # states = [
        # ]

        # # Format: day month year - hour minute second
        # # Example format will be 22112021-110500
        # current_time = datetime.today().strftime('%d%m%Y-%H%M%S')

        # url_string = f"https://www.1a-immobilienmarkt.de/suchen/schleswig-holstein/wohnung-mieten.html"

        # formdata = dict()
        # formdata['seite'] = 2

        # yield scrapy.FormRequest(url_string, formdata=formdata, method='POST', callback=self.parse_bundesland)

        # for state in states:
        #     for house in house_types:
        #         for acquistion in acquisition_types:
        #             url_string = f""

        #             meta_payload = {
        #                 'state_name': state,
        #                 'current_time': current_time,
        #                 'url_name': url_string,
        #                 'house_type': house,
        #                 'acquisition_type': acquistion
        #             }

        #             yield scrapy.Request(url_string, callback=self.parse_bundesland, meta=meta_payload)

    # State (Bundesland) parsing callback
    def parse_bundesland(self, response):
        # Check if the directory is already created or not
        htmlPath = f"html/immomarkt/"

        # Make sure the directory is exist
        os.makedirs(os.path.dirname(htmlPath), exist_ok=True)

        fileName = f"page-1.html"
        filePath = htmlPath + fileName
        
        with open(filePath, 'wb') as f:
            f.write(response.body)

        # # Get meta data
        # meta_payload = response.meta

        # # Scrapy response xpath api to extract pagination last number
        # elements = response.xpath('//li[contains(@class, "pagination-item")]/a/text()').getall()

        # pagination_count = 1

        # # Handle if there is pagination (only 1 page result)
        # if elements:
        #     pagination_count = int(elements[-1])

        # print(f"page {pagination_count}")

        # for x in range(pagination_count):
        #     page_number = x + 1
        #     meta_payload['page_number'] = page_number

        #     # Append query parameter and page number to the request url
        #     url = meta_payload.get('url_name') + f"&page={page_number}"

        #     yield scrapy.Request(url, callback=self.parse_final, meta=meta_payload)


    # # State pagination handling callback (final)
    # def parse_final(self, response):
    #     # Get meta data
    #     state_name= response.meta.get('state_name')
    #     current_time= response.meta.get('current_time')
    #     page_number= response.meta.get('page_number')
    #     house_type= response.meta.get('house_type')
    #     acquisition_type= response.meta.get('acquisition_type')

    #     house_type = self.get_house_type_name(int(house_type))
    #     acquisition_type = self.get_acquisition_type_name(int(acquisition_type))
    #     state_name = self.get_state_name(int(state_name))

    #     # Check if the directory is already created or not
    #     htmlPath = f"html/immonet/{state_name}/{house_type}/{acquisition_type}/{current_time}/"

    #     # Make sure the directory is exist
    #     os.makedirs(os.path.dirname(htmlPath), exist_ok=True)

    #     fileName = f"page-{page_number}.html"
    #     filePath = htmlPath + fileName
        
    #     with open(filePath, 'wb') as f:
    #         f.write(response.body)


