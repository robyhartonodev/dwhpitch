import scrapy

from datetime import datetime
import os

import re
import json

class ImmoscoutSpider(scrapy.Spider):
    name = "immonet"

    start_urls = [
        'https://www.immonet.de'
    ]

    def parse(self, response):
        house_types = [
            1, # wohnung
            2, # haueser
        ]

        acquisition_types = [
            1, # kaufen
            2  # mieten
        ]

        states = [
            # 1, # scleswig-holstein
            # 2, # hamburg
            # 3, # niedersachsen
            # 4, # bremen
            # 5, # nordrheinwestfalen
            # 6, # hessen
            # 7, # rheinland-pfalz
            # 8, # baden-wuerttemberg
            # 9, # bayern
            # 10, # saarland
            # 11, # berlin
            # 12, # brandenburg
            13, # mecklenburg-vorpommern
            # 14, # sachsen
            # 15, # sachsen-anhalt
            # 16, # thueringen
        ]

        # Format: day month year - hour minute second
        # Example format will be 22112021-110500
        current_time = datetime.today().strftime('%d%m%Y-%H%M%S')

        for state in states:
            for house in house_types:
                for acquistion in acquisition_types:
                    # e.g. https://www.immonet.de/immobiliensuche/sel.do?&sortby=0&suchart=1&objecttype=1&marketingtype=1&parentcat=1&federalstate=13
                    url_string = f"https://www.immonet.de/immobiliensuche/sel.do?&sortby=0&suchart=1&objecttype=1&marketingtype={acquistion}&parentcat={house}&federalstate={state}"

                    meta_payload = {
                        'state_name': state,
                        'current_time': current_time,
                        'url_name': url_string,
                        'house_type': house,
                        'acquisition_type': acquistion
                    }

                    yield scrapy.Request(url_string, callback=self.parse_bundesland, meta=meta_payload)

    # State (Bundesland) parsing callback
    def parse_bundesland(self, response):
        # Get meta data
        meta_payload = response.meta

        # Scrapy response xpath api to extract pagination last number
        elements = response.xpath('//li[contains(@class, "pagination-item")]/a/text()').getall()

        pagination_count = 1

        # Handle if there is pagination (only 1 page result)
        if elements:
            pagination_count = int(elements[-1])

        print(f"page {pagination_count}")

        for x in range(pagination_count):
            page_number = x + 1
            meta_payload['page_number'] = page_number

            # Append query parameter and page number to the request url
            url = meta_payload.get('url_name') + f"&page={page_number}"

            yield scrapy.Request(url, callback=self.parse_final, meta=meta_payload)


    # State pagination handling callback (final)
    def parse_final(self, response):
        # Get meta data
        state_name= response.meta.get('state_name')
        current_time= response.meta.get('current_time')
        page_number= response.meta.get('page_number')
        house_type= response.meta.get('house_type')
        acquisition_type= response.meta.get('acquisition_type')

        house_type = self.get_house_type_name(int(house_type))
        acquisition_type = self.get_acquisition_type_name(int(acquisition_type))
        state_name = self.get_state_name(int(state_name))

        # Check if the directory is already created or not
        htmlPath = f"html/immonet/{state_name}/{house_type}/{acquisition_type}/{current_time}/"

        # Make sure the directory is exist
        os.makedirs(os.path.dirname(htmlPath), exist_ok=True)

        fileName = f"page-{page_number}.html"
        filePath = htmlPath + fileName
        
        with open(filePath, 'wb') as f:
            f.write(response.body)

    def get_acquisition_type_name(self, id):
        if id == 1:
            return 'kaufen'
        if id == 2:
            return 'mieten'
        
        return 'ipsum'

    def get_house_type_name(self, id):
        if id == 1:
            return 'wohnungen'
        if id == 2:
            return 'haueser'
        
        return 'ipsum'

    def get_state_name(self, id):
        if id == 1:
            return 'schleswig-holstein'
        if id == 2:
            return 'hamburg'
        if id == 3:
            return 'niedersachsen'
        if id == 4:
            return 'bremen'
        if id == 5:
            return 'nordrhein-westfalen'
        if id == 6:
            return 'hessen'
        if id == 7:
            return 'rheinland-pfalz'
        if id == 8:
            return 'baden-wuerttemberg'
        if id == 9:
            return 'bayern'
        if id == 10:
            return 'saarland'
        if id == 11:
            return 'berlin'
        if id == 12:
            return 'brandenburg'
        if id == 13:
            return 'mecklenburg-vorpommern'
        if id == 14:
            return 'sachsen'
        if id == 15:
            return 'sachsen-anhalt'
        if id == 16:
            return 'thueringen'
        
        return 'ipsum'


