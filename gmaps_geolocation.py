#!/usr/bin/python3

import json,requests,csv,os

 #Using Python requests and the Google Maps Geocoding API.

 #API Key oliver.wehrli@gmail.com: AIzaSyDRp31ECaNFQIbtmQT0rRPpiV6JA6PQhcw

api_key = 'AIzaSyDRp31ECaNFQIbtmQT0rRPpiV6JA6PQhcw'

gmaps_api_url = 'https://maps.googleapis.com/maps/api/geocode/json?key='+api_key

params = {
    'address': 'dietlikonstrasse 35 duebendorf',
    'sensor': 'false',
    'region': 'switzerland'
}

# Do the request and get the response data
req = requests.get(gmaps_api_url, params=params)
res = req.json()

# Use the first result
result = res['results'][0]

geodata = dict()
geodata['lat'] = result['geometry']['location']['lat']
geodata['lng'] = result['geometry']['location']['lng']
geodata['address'] = result['formatted_address']

print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))