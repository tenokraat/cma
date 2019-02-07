#!/usr/bin/python3

import json,requests,csv,os

 #Using Python requests and TomTom Search/Geocode API.

 #API Key oliver.wehrli@gmail.com: KR3oOGSM59aMJBOSKAxTlxoJvYBjrENU


api_key = 'KR3oOGSM59aMJBOSKAxTlxoJvYBjrENU'
address = 'dietlikonstrasse 35 duebendorf'

geocode_api_url = f'https://api.tomtom.com/search/2/geocode/{address}.json'

#query syntax /search/{versionNumber}/geocode/{query}.{ext}
#https://api.tomtom.com/search/2/geocode/coop pronto Bassersdorferstrasse 113 8302.json?countrySet=CH&lat=37.337&lon=-121.89&topLeft=37.553%2C-122.453&btmRight=37.4%2C-122.55&key=*****

params = {
    'countrySet': 'CH',
    #'lat': '46.204391',
    #'lon': '6.143158',
    'key': api_key
}

# Do the request and get the response data
req = requests.get(geocode_api_url, params=params)
print (req.url)

res = req.json()
print (res)

summary = res['summary'][0]
print (summary)

# Use the first result
result = res['results'][0]
print (result)

geodata {}
geodata['lat'] = result['geometry']['location']['lat']
geodata['lng'] = result['geometry']['location']['lng']
geodata['address'] = result['formatted_address']

print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))