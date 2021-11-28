from immobilien.models import City, State, Zip

import json

def run():
    # Read zipcodes.de.json file
    with open('zipcodes.de.json', encoding='utf-8') as f:
        data = json.load(f)
        
        for zip_code in data:
            # Get state object
            s, created_state = State.objects.get_or_create(name=zip_code['state'], state_code=zip_code['state_code'])

            # Get city object
            c, created_city = City.objects.get_or_create(name=zip_code['place'])

            # Get zip object
            z, created_zip = Zip.objects.get_or_create(code=zip_code['zipcode'], city=c, state=s)

            if created_zip:
                print(f"created zip code: {zip_code['zipcode']} - {zip_code['place']}")