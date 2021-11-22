import scrapy

from datetime import datetime
import os

import re
import json

class ImmoscoutSpider(scrapy.Spider):
    name = "immoscout"

    start_urls = [
        # 'https://immobilienscout24.de/',
        'https://immobilienscout24.de/Suche/de/berlin/berlin/haus-kaufen'
    ]

    def parse(self, response):
        house_types = [
            'haus',
            'wohnung',
        ]

        acquisition_types = [
            'mieten',
            'kaufen',
        ]

        states = [
            # 'baden-wuerttemberg',
            # 'bayern',
            # 'berlin',
            # 'brandenburg',
            # 'bremen',
            # 'hamburg',
            # 'hessen',
            'mecklenburg-vorpommern',
            # 'niedersachsen',
            # 'nordrhein-westfalen',
            # 'rheinland-pfalz',
            # 'saarland',
            # 'sachsen',
            # 'sachsen-anhalt',
            # 'schleswig-holstein',
            # 'thueringen'
        ]

        # Format: day month year - hour minute second
        # Example format will be 22112021-110500
        current_time = datetime.today().strftime('%d%m%Y-%H%M%S')

        # Check if the directory is already created or not
        htmlPath = f"html/immoscout24/{current_time}/"

        # Make sure the directory is exist
        os.makedirs(os.path.dirname(htmlPath), exist_ok=True)

        fileName = f"page-1.html"
        filePath = htmlPath + fileName
        
        with open(filePath, 'wb') as f:
            f.write(response.body)

        # for state in states:
        #     for house in house_types:
        #         for acquistion in acquisition_types:
        #             # e.g. https://www.immobilienscout24.de/Suche/de/berlin/haus-kaufen
        #             url_string = f"https://www.immobilienscout24.de/Suche/de/{state}/{house}-{acquistion}"

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
        # Get meta data
        meta_payload = response.meta

        # Use Python regex to extract pagination information
        # pagination_string = re.search("\"pagination\"[ :]+((?=\[)\[[^]]*\]|(?=\{)\{[^\}]*\}|\"[^\"]*\")", response.text)
        # pagination_json   = json.loads(pagination_string.group(1))
        # pagination_count  = int(pagination_json["pagesCount"])

        # for x in range(pagination_count):
        #     page_number = x + 1
        #     meta_payload['page_number'] = page_number

        #     # Append query parameter and page number to the request url
        #     url = meta_payload.get('url_name') + f"?pagenumber={page_number}"

        #     yield scrapy.Request(url, callback=self.parse_final, meta=meta_payload)


    # State pagination handling callback (final)
    # def parse_final(self, response):
    #     # Get meta data
    #     state_name= response.meta.get('state_name')
    #     current_time= response.meta.get('current_time')
    #     page_number= response.meta.get('page_number')
    #     house_type= response.meta.get('house_type')
    #     acquisition_type= response.meta.get('acquisition_type')

    #     # Check if the directory is already created or not
    #     htmlPath = f"html/immoscout24/{state_name}/{house_type}/{acquisition_type}/{current_time}/"

    #     # Make sure the directory is exist
    #     os.makedirs(os.path.dirname(htmlPath), exist_ok=True)

    #     fileName = f"page-{page_number}.html"
    #     filePath = htmlPath + fileName
        
    #     with open(filePath, 'wb') as f:
    #         f.write(response.body)
