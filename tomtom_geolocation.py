#!/usr/bin/python3

import json,requests,csv,os

 #Using Python requests and TomTom Search/Geocode API.

 #API Key oliver.wehrli@gmail.com

api_key = 'KR3oOGSM59aMJBOSKAxTlxoJvYBjrENU'
address = 'dorfstrasse 28 allenwinden'

geocode_api_url = f'https://api.tomtom.com/search/2/geocode/{address}.json'

#TomTom API query syntax /search/{versionNumber}/geocode/{query}.{ext}
#https://developer.tomtom.com/content/search-api-explorer

params = {
    'countrySet': 'CH',
    'lat': '46.204391',
    'lon': '6.143158',
    'key': api_key
}

# Do the request and get the response data
req = requests.get(geocode_api_url, params=params)
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