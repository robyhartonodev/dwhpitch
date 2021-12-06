import scrapy
import scrapy_splash

from datetime import datetime
import os

import re
import json

from immobilien.models import *

# How to run: 
# scrapy crawl immowelt -a bundesland=<state-name> (lower case)
# e.g. scrapy crawl immowelt -a bundesland=bayern
class ImmoweltSpider(scrapy.Spider):
    name = "immowelt"

    start_urls = [
        'https://immowelt.de/',
    ]

    def parse(self, response):
        house_types = [
            'haeuser',
            'wohnungen',
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
            # 'mecklenburg-vorpommern',
            # 'niedersachsen',
            # 'nordrhein-westfalen',
            # 'rheinland-pfalz',
            # 'saarland',
            # 'sachsen',
            # 'sachsen-anhalt',
            # 'schleswig-holstein',
            # 'thueringen'
        ]

        # If not bundesland argument not null then append it to states array
        if self.bundesland:
            state_name = self.bundesland
            states.append(state_name)

        # Format: day month year - hour minute second
        # Example format will be 22112021-110500
        current_time = datetime.today().strftime('%d%m%Y-%H%M%S')

        # Debug details parsing
        # url_string = f"https://www.immowelt.de/liste/bl-hessen/wohnungen/mieten" # test 1
        # url_string = f"https://immowelt.de/liste/bl-bremen/wohnungen/kaufen" # test 2
        # yield scrapy.Request(url_string, callback=self.parse_detail_url)

        # url_string = f"https://www.immowelt.de/expose/23qlr57"
        # url_string = "https://www.immowelt.de/expose/239865m"
        # url_string = "https://www.immowelt.de/expose/23p435f"
        # payload = {
        #     'details_url': url_string,
        #     'angebot_id': url_string.split('/')[-1],
        # }
        # yield scrapy_splash.SplashRequest(url_string, self.parse_detail_data, meta=payload, args={
        #     'wait': 2.0
        # })

        for state in states:
            for house in house_types:
                for acquistion in acquisition_types:
                    # e.g. https://www.immowelt.de/liste/bl-mecklenburg-vorpommern/wohnungen/mieten
                    url_string = f"https://www.immowelt.de/liste/bl-{state}/{house}/{acquistion}"

                    meta_payload = {
                        'state_name': state,
                        'current_time': current_time,
                        'url_name': url_string,
                        'house_type': house,
                        'acquisition_type': acquistion
                    }

                    yield scrapy.Request(url_string, callback=self.parse_pagination, meta=meta_payload)

    # State (Bundesland) parsing callback
    def parse_pagination(self, response):
        # Get meta data
        meta_payload = response.meta

        # Use Python regex to extract pagination information
        pagination_string = re.search("\"pagination\"[ :]+((?=\[)\[[^]]*\]|(?=\{)\{[^\}]*\}|\"[^\"]*\")", response.text)
        pagination_json   = json.loads(pagination_string.group(1))
        pagination_count  = int(pagination_json["pagesCount"])
        
        for x in range(pagination_count):
            page_number = x + 1

            meta_payload['page_number'] = page_number

            # Append query parameter and page number to the request url
            url = meta_payload.get('url_name') + f"?d=true&sd=DESC&sf=RELEVANCE&sp={page_number}"

            # yield scrapy.Request(url, callback=self.parse_final, meta=meta_payload)
            yield scrapy.Request(url, callback=self.parse_detail_url, meta=meta_payload)
    
    def parse_detail_url(self, response):
        # Get meta data
        meta_payload = response.meta

        detail_links_one = response.xpath('//a[starts-with(@id, "estate_")]/@href').getall()
        detail_links_two = response.xpath('//a[starts-with(@class, "EstatesListItem-")]/@href').getall()
        detail_links_three = response.xpath('//div[starts-with(@class, "EstateItem-")]/a/@href').getall()

        # Concat two array string containing detail url
        detail_links = detail_links_one + detail_links_two + detail_links_three

        print(detail_links)

        for link in detail_links:
            angebotId = link.split('/')[-1]

            meta_payload['details_url'] = link
            meta_payload['angebot_id'] = angebotId

            yield scrapy_splash.SplashRequest(link, self.parse_detail_data, meta=meta_payload, args={
                'wait': 2.0
            })


    def parse_detail_data(self, response):
        # Get meta data details url
        detailUrl = response.meta.get('details_url')
        detailId  = response.meta.get('angebot_id')

        houseType= response.meta.get('house_type')
        acquisitionType= response.meta.get('acquisition_type')
        stateName = response.meta.get('state_name')

        houseType = 'flat' if houseType == 'wohnungen' else 'house'
        acquisitionType = 'buy' if acquisitionType == 'kaufen' else 'mieten'
        # stateName = 'bremen'

        if not detailId:
            detailId = 'dummy'

        # Get data from html response text
        htmlTitle = response.xpath('//meta[@name="og:title"]/@content').get()
        htmlProviderName = response.xpath('//p[@class="offerer"]/text()').get()
        # htmlContactPerson = response.xpath('//p[@class="contactperson"]/text()').get()
        
        htmlPriceShow = response.xpath('//div[@class="has-font-300"]/strong/text()').get()
        htmlFacts = response.xpath('//span[@class="has-font-300"]/text()').getall()

        htmlStreetName = response.xpath('//span[@data-cy="address-street"]/text()').get()

        htmlSizeInSquareMeter=htmlFacts[0][:-3] # Remove m^2 and space
        htmlRoomCount=htmlFacts[1]

        htmlFeatures = response.xpath('//div[contains(@class,"textlist textlist--icon card-content ng-star-inserted")]/ul/li/text()').getall()
        htmlImages = response.xpath('//img[contains(@class,"swiper-lazy ng-star-inserted swiper-lazy-loaded")]/@src').getall()

        htmlPriceOne = response.xpath('//sd-cell-col[contains(@class, "cell__col")]/strong/text()').getall()
        htmlPriceTwo = response.xpath('//sd-card[contains(@class, "price card")]/sd-cell/sd-cell-row/sd-cell-col[contains(@class, "cell__col")]/text()').getall()

        # Kaution (Deposit)
        htmlDepositText = response.xpath('//div[@data-cy="deposit"]/h3/text()').getall()
        htmlDepositValue = response.xpath('//div[@data-cy="deposit"]/p/text()').getall()

        # Concat price related string
        htmlPrices = htmlPriceOne + htmlPriceTwo

        htmlPlz = response.xpath('normalize-space(//span[@data-cy="address-city"])').get()

        splitPlz = htmlPlz.split(' ')

        plzCode = splitPlz[0]
        plzName = splitPlz[1].replace(u'\xa0', ' ')

        # Find state object (ignore case)
        states = State.objects.filter(name__iexact=stateName)
        detailState = states.first() if states.exists() else State.objects.create(name=stateName)

        # Find zip object with place name and plz code
        zips = Zip.objects.filter(name__iexact=plzName, code=plzCode, state=detailState)
        detailZip = zips.first() if zips.exists() else Zip.objects.create(name=plzName, code=plzCode, state=detailState)

        # Get or create address object for property detail
        detailAddress, _ = Address.objects.get_or_create(zip=detailZip, street_name=htmlStreetName)

        # Get or create vendor object for property detail
        detailVendor, _ = PropertyVendor.objects.get_or_create(name=htmlProviderName)

        # Get or create property detail object
        propertyDetail, _ = PropertyDetail.objects.get_or_create(details_url=detailUrl, vendor=detailVendor, address=detailAddress)

        # Update property detail if necessary
        propertyDetail.title=htmlTitle
        # propertyDetail.other=htmlOther
        # propertyDetail.description=htmlDescription
        
        if htmlRoomCount:
            containsDigit = any(str.isdigit(c) for c in htmlRoomCount)

            if containsDigit:
                detailRoomCount = float(htmlRoomCount.replace(',','.')) # Change comma to point
                propertyDetail.room_count=detailRoomCount
        
        if htmlSizeInSquareMeter:
            containsDigit = any(str.isdigit(c) for c in htmlSizeInSquareMeter)

            if containsDigit:
                detailSizeInSquareMeter = float(htmlSizeInSquareMeter.replace('.', '').replace(',', '.')) # Change comma separator to point and remove dot thousand separator
                propertyDetail.size_in_meter_square = detailSizeInSquareMeter

        if htmlPriceShow:
            containsDigit = any(str.isdigit(c) for c in htmlPriceShow)

            if containsDigit:
                text = htmlPriceShow[:-2].replace('.', '').replace(',', '.')

                detailPriceShow = float(text)
                propertyDetail.price_show=detailPriceShow

        if htmlFeatures:
            detailFeatures = []
            
            for feature in htmlFeatures:
                test = feature.strip()
                detailFeatures.append(test)

            for feature in detailFeatures:
                ftr, _ = PropertyFeature.objects.get_or_create(name=feature)
                propertyDetail.features.add(ftr)

        if htmlImages:
            for image in htmlImages:
                img, _ = PropertyImage.objects.get_or_create(image_url=image)
                propertyDetail.images.add(img)

        if htmlPrices:
            name = []
            price = []

            for index, item in enumerate(htmlPrices):
                if index % 2 == 0:
                    text = item.strip()
                    name.append(text)
                if index % 2 != 0:
                    containsDigit = any(str.isdigit(c) for c in item)

                    if containsDigit:
                        val = item[:-2].replace('.','').replace(',','.') # Remove euro sign, \xa0 and convert comma into dot for float
                        price.append(val)
                    else:
                        price.append(item)

            priceDict = dict(zip(name, price))

            for key, value in priceDict.items():
                
                containsDigit = any(str.isdigit(c) for c in value)

                if containsDigit:
                    priceType, _ = PropertyPriceType.objects.get_or_create(name=key)
                    
                    property_detail_price, _ = PropertyDetailPrice.objects.get_or_create(detail=propertyDetail, price_type=priceType)
                    
                    property_detail_price.value = value
                    property_detail_price.save()

        propertyDetail.save()

        # Acquisition Type
        propertyAcquisitionType, _ = PropertyAcquisitionType.objects.get_or_create(name=acquisitionType)

        # Property Type
        propertyType, _ = PropertyType.objects.get_or_create(name=houseType)

        # Identifier
        source, _=Source.objects.get_or_create(name='immowelt')  # From immowelt site  
        propertyIdentifier, _ = PropertyIdentifier.objects.get_or_create(identifier=detailId, source=source)

        # Property final object
        property = Property.objects.get_or_create(
            property_identifier=propertyIdentifier, 
            property_detail=propertyDetail,
            property_type=propertyType,
            property_acquisition_type=propertyAcquisitionType
        )


    # State pagination handling callback (final)
    def parse_final(self, response):
        # Get meta data
        state_name= response.meta.get('state_name')
        current_time= response.meta.get('current_time')
        page_number= response.meta.get('page_number')
        house_type= response.meta.get('house_type')
        acquisition_type= response.meta.get('acquisition_type')

        # Check if the directory is already created or not
        htmlPath = f"html/immowelt/{state_name}/{house_type}/{acquisition_type}/{current_time}/"

        # Make sure the directory is exist
        os.makedirs(os.path.dirname(htmlPath), exist_ok=True)

        fileName = f"page-{page_number}.html"
        filePath = htmlPath + fileName
        
        with open(filePath, 'wb') as f:
            f.write(response.body)

    def parse_detail_html(self, response):
        angebotId = response.meta.get('angebotid')

        # Check if the directory is already created or not
        htmlPath = f"html/immowelt/detail/"

        # Make sure the directory is exist
        os.makedirs(os.path.dirname(htmlPath), exist_ok=True)

        fileName = f"angebot-{angebotId}.html"
        filePath = htmlPath + fileName
        
        with open(filePath, 'wb') as f:
            f.write(response.body)
