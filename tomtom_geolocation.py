#!/usr/bin/python3

import json,requests

 #Using Python requests and TomTom Search/Geocode API to retrieve geo location.

 #API Key oliver.wehrli@gmail.com

api_key = 'KR3oOGSM59aMJBOSKAxTlxoJvYBjrENU'


def get_geolocation(address):

    #TomTom API query syntax /search/{versionNumber}/geocode/{query}.{ext}
    #https://developer.tomtom.com/content/search-api-explorer


    #Restrict TomTom search to Switzerland
    tomtom_search_params = {
        'countrySet': 'CH',
        'lat': '46.204391',
        'lon': '6.143158',
        'key': api_key
    }

    geocode_api_url = f'https://api.tomtom.com/search/2/geocode/{address}.json'

    # Do the request to TomTom URL, pass search parameters and retrieve the response data
    req = requests.get(geocode_api_url, params=tomtom_search_params)
    print (req.url)

    res = req.json()
    print (res)

    summary = res['summary']
    print (summary)

    # Use the first result
    result = res['results'][0]
    print (result)

    geodata = dict()
    
    geodata['lat'] = result['position']['lat']
    geodata['lon'] = result['position']['lon']
    geodata['address'] = result['address']['freeformAddress']

    print('{address}. (lat, lng) = ({lat}, {lon})'.format(**geodata))

    return geodata

#get_geolocation('dietlikonstrasse 35')