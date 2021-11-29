from immobilien.models import *

import json

def run():
    # Read zipcodes.de.json file
    with open('zipcodes.de.json', encoding='utf-8') as f:
        data = json.load(f)
        
        for zip_code in data:
            # Get state object
            s, created_state = State.objects.get_or_create(name=zip_code['state'], state_code=zip_code['state_code'])

            lon = float(zip_code['longitude'])
            lat = float(zip_code['latitude'])
            
            # Get zip object
            z, created_zip = Zip.objects.get_or_create(code=zip_code['zipcode'], name=zip_code['place'], state=s, longitude=lon, latitude=lat)

            if created_zip:
                print(f"created zip code: {z.code} {z.name} {z.state.name}")