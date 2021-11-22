import scrapy

from datetime import datetime
import os

class ImmoweltSpider(scrapy.Spider):
    name = "immowelt"
    start_urls = [
        'https://immowelt.de/liste/bl-bayern/wohnungen/mieten',
    ]

    house_types = [
        'haeuser',
        'wohnungen',
        'wg'
    ]

    acquisition_types = [
        'kaufen',
        'mieten'
    ]

    states = [
        'baden-wuerttemberg',
        'bayern',
        'berlin',
        'brandenburg',
        'bremen',
        'hamburg',
        'hessen',
        'mecklenburg-vorpommern',
        'niedersachsen',
        'nordrhein-westfalen',
        'rheinland-pfalz',
        'saarland',
        'sachsen',
        'sachsen-anhalt',
        'schleswig-holstein',
        'thueringen'
    ]

    for state in states:
        url_string = f"https://www.immowelt.de/liste/bl-{state}/wohnungen/mieten"
        start_urls.append(url_string)

    def parse(self, response):
        # Example format will be 22112021-110500
        current_time = datetime.today().strftime('-%d%m%Y-%H%M%S')

        htmlPath = 'html/immowelt/'

        fileName = response.url.split('/')[-3] + current_time + '.html'
        filePath = htmlPath + fileName

        # Check if the directory is already created or not
        os.makedirs(os.path.dirname(filePath), exist_ok=True)

        with open(filePath, 'wb') as f:
            f.write(response.body)
