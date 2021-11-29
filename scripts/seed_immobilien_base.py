from immobilien.models import *

def run():
    property_types = [
        'flat',
        'house',
        'flat-sharing'
    ]

    acquisiton_types = [
        'buy',
        'rent'
    ]

    sources = [
        {'name': 'immonet', 'baseUrl': 'https://immonet.de'},
        {'name': 'immowelt', 'baseUrl': 'https://immowelt.de'}
    ]

    for type in property_types:
        property_type=PropertyType.objects.get_or_create(name=type)

    for type in acquisiton_types:
        property_acquisiton_type=PropertyAcquisitionType.objects.get_or_create(name=type)

    for source in sources:
        source=Source.objects.get_or_create(name=source['name'], base_url=source['baseUrl'])