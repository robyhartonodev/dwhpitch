import scrapy

from datetime import datetime
import os

from immobilien.models import *

# How to run: 
# scrapy crawl immonet -a bundesland=<state-name> (lower case)
# e.g. scrapy crawl immonet -a bundesland=bayern
class ImmonetSpider(scrapy.Spider):
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
            # 1, # schleswig-holstein
            # 2, # hamburg
            # 3, # niedersachsen
            # 4, # bremen
            # 5, # nordrhein-westfalen
            # 6, # hessen
            # 7, # rheinland-pfalz
            # 8, # baden-wuerttemberg
            # 9, # bayern
            # 10, # saarland
            # 11, # berlin
            # 12, # brandenburg
            # 13, # mecklenburg-vorpommern
            # 14, # sachsen
            # 15, # sachsen-anhalt
            # 16, # thueringen
        ]

        # If not bundesland argument not null then append it to states array
        if self.bundesland:
            state_id = self.get_state_id(self.bundesland)
            states.append(state_id)

        # Format: day month year - hour minute second
        # Example format will be 22112021-110500
        current_time = datetime.today().strftime('%d%m%Y-%H%M%S')

        # Debug detail parsing
        # url_string = 'https://www.immonet.de/immobiliensuche/sel.do?&sortby=0&suchart=1&objecttype=1&marketingtype=1&parentcat=1&federalstate=4&page=1'
        # yield scrapy.Request(url_string, self.parse_detail_url)

        # url_string = 'https://www.immonet.de/angebot/45891041' # test 1 (buy)
        # url_string = 'https://www.immonet.de/angebot/46022645' # test 2 (rent)
        # yield scrapy.Request(url_string, self.parse_detail_data)

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

                    yield scrapy.Request(url_string, callback=self.parse_pagination, meta=meta_payload)

    # Pagination parsing callback
    def parse_pagination(self, response):
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

            yield scrapy.Request(url, callback=self.parse_detail_url, meta=meta_payload)

    def parse_detail_url(self, response):
        # Get meta data
        meta_payload = response.meta

        base_url = "https://immonet.de"

        # Get all detail links from the page
        detail_links = response.xpath('//a[contains(@class, "block ellipsis text-225 text-default")]/@href').getall()

        for link in detail_links:
            # e.g. https://immonet/angebot/123123
            url_string=f"{base_url}{link}"

            split_url=link.split("/")[-1]

            # Add more payload to meta data
            meta_payload['details_url'] = url_string
            meta_payload['angebot_id'] = split_url

            # Go into all the detail links
            yield scrapy.Request(url_string, callback=self.parse_detail_data, meta=meta_payload)

    def parse_detail_data(self, response):
        # Get meta data details url
        detailUrl = response.meta.get('details_url')
        detailId  = response.meta.get('angebot_id')

        houseType= response.meta.get('house_type')
        acquisitionType= response.meta.get('acquisition_type')
        stateName = self.get_state_name(int(response.meta.get('state_name')))
        # stateName = 'bremen'

        houseType = 'house' if houseType == 2 else 'flat'
        acquisitionType = 'buy' if acquisitionType == 1 else 'rent'

        if not detailId:
            detailId = 'dummy'

        # Get data from html response text
        htmlTitle = response.xpath('//h1[@id="expose-headline"]/text()').get()
        htmlDescription = response.xpath('//p[@id="objectDescription"]/text()').get()
        htmlOther = response.xpath('//p[@id="otherDescription"]/text()').get()
        htmlProviderName = response.xpath('//span[@id="bdBrokerFirmname"]/text()').get()
        htmlTelephoneNumber = response.xpath('normalize-space(//p[@id="bdContactPhone"])').get()
        htmlRoomCount = response.xpath('normalize-space(//span[@id="kfroomsValue"])').get()
        htmlPriceShow = response.xpath('normalize-space(//span[@id="kfpriceValue"])').get()
        htmlSizeInSquareMeter = response.xpath('normalize-space(//span[@id="kffirstareaValue"])').get()
        htmlFeatures = response.xpath('//span[contains(@class,"block padding-left-21")]/text()').getall()
        htmlImages = response.xpath('//div[@id="fotorama"]/div/@data-img').getall()

        htmlPriceTypeNames = response.xpath('//div[starts-with(@id, "pricename_")]/text()').getall()
        htmlPriceTypeValues = response.xpath('//div[starts-with(@id, "priceid_")]/text()').getall()

        htmlPlz = response.xpath('normalize-space(//p[contains(@class,"text-100 pull-left")])').get()
        
        # PLZ, Location name extraction
        splitPlz = htmlPlz.split(' ')

        splitPlz = splitPlz[:-3] # remove "Auf" "Karte" "anzeigen"

        plzCode = splitPlz[-2][:5]
        plzName = splitPlz[-1]

        splitPlz = splitPlz[:-2] # remove plz code and location name

        # Find state object (ignore case)
        states = State.objects.filter(name__iexact=stateName)
        detailState = states.first() if states.exists() else State.objects.create(name=stateName)

        # Find zip object with place name and plz code
        zips = Zip.objects.filter(name__iexact=plzName, code=plzCode, state=detailState)
        detailZip = zips.first() if zips.exists() else Zip.objects.create(name=plzName, code=plzCode, state=detailState)

        # Get or create address object for property detail
        detailAddress, _ = Address.objects.get_or_create(zip=detailZip)

        if splitPlz:
            streetName = ' '.join(str(x) for x in splitPlz)
            detailAddress.street_name=streetName

        detailAddress.save()

        # Get or create vendor object for property detail
        detailVendor, _ = PropertyVendor.objects.get_or_create(name=htmlProviderName)

        if htmlTelephoneNumber:
            splitTelephoneNumber = htmlTelephoneNumber.split(': ')[1]
            detailVendor.telephone_number=splitTelephoneNumber

        detailVendor.save()

        # Get or create property detail object
        propertyDetail, _ = PropertyDetail.objects.get_or_create(details_url=detailUrl, vendor=detailVendor, address=detailAddress)

        # Update property detail if necessary
        propertyDetail.title=htmlTitle
        propertyDetail.other=htmlOther
        propertyDetail.description=htmlDescription
        
        if htmlRoomCount:
            detailRoomCount = float(htmlRoomCount)
            propertyDetail.room_count=detailRoomCount
        
        if htmlSizeInSquareMeter:
            detailSizeInSquareMeter = float(htmlSizeInSquareMeter[:-2]) # Remove m^2 char before type casting
            propertyDetail.size_in_meter_square=detailSizeInSquareMeter

        if htmlPriceShow:
            detailPriceShow = float(htmlPriceShow[:-2].replace(',', '')) # Remove euro sign, remove comma
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

        if htmlPriceTypeNames and htmlPriceTypeValues:
            priceTypeNames = []
            priceTypeValues = []

            for name in htmlPriceTypeNames:
                nm = name.strip()
                priceTypeNames.append(nm)

            for val in htmlPriceTypeValues:
                vl = float(val.strip()[:-2].replace(',','')) # Remove euro sign, \xa0 and comma thousand separator (,)
                priceTypeValues.append(vl)

            priceDict = dict(zip(priceTypeNames, priceTypeValues))

            for key, value in priceDict.items():
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
        source, _=Source.objects.get_or_create(name='immonet')  # From immonet site  
        propertyIdentifier, _ = PropertyIdentifier.objects.get_or_create(identifier=detailId, source=source)

        # Property final object
        property = Property.objects.get_or_create(
            property_identifier=propertyIdentifier, 
            property_detail=propertyDetail,
            property_type=propertyType,
            property_acquisition_type=propertyAcquisitionType
        )

    def parse_detail_html(self, response):
        angebotId = response.meta.get('angebotid')

        # Check if the directory is already created or not
        htmlPath = f"html/immonet/detail/"

        # Make sure the directory is exist
        os.makedirs(os.path.dirname(htmlPath), exist_ok=True)

        fileName = f"angebot-{angebotId}.html"
        filePath = htmlPath + fileName
        
        with open(filePath, 'wb') as f:
            f.write(response.body)

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

    def get_state_id(self, name):
        if name == 'schleswig-holstein':
            return 1
        if name == 'hamburg':
            return 2
        if name == 'niedersachsen':
            return 3
        if name == 'bremen':
            return 4
        if name == 'nordrhein-westfalen':
            return 5
        if name == 'hessen':
            return 6
        if name == 'rheinland-pfalz':
            return 7
        if name == 'baden-wuerttemberg':
            return 8
        if name == 'bayern':
            return 9
        if name == 'saarland':
            return 10
        if name == 'berlin':
            return 11
        if name == 'brandenburg':
            return 12
        if name == 'mecklenburg-vorpommern':
            return 13
        if name == 'sachsen':
            return 14
        if name == 'sachsen-anhalt':
            return 15
        if name == 'thueringen':
            return 16      
        return 20


