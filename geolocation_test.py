import json,requests,os, urllib3
import logging

logging.basicConfig(level=logging.DEBUG)

'''#This Script needs to connect to the internet, hence requires proxy.

cma_proxy = 'http://192.168.205.163:8080/'
os.environ['http_proxy'] = cma_proxy 
os.environ['HTTP_PROXY'] = cma_proxy
os.environ['https_proxy'] = cma_proxy
os.environ['HTTPS_PROXY'] = cma_proxy'''

#API Key oliver.wehrli@gmail.com

api_key = 'KR3oOGSM59aMJBOSKAxTlxoJvYBjrENU'


        
#TomTom API query syntax /search/{versionNumber}/geocode/{query}.{ext}
#https://developer.tomtom.com/content/search-api-explorer

#Restrict TomTom search to Switzerland
tomtom_search_params = {
        'countrySet': 'CH',
        'lat': '46.204391',
        'lon': '6.143158',
        'key': self.api_key
    }

geocode_api_url = f'https://api.tomtom.com/search/2/geocode/{shop_address}.json'

# Do the request to TomTom URL, pass search parameters and retrieve the response data
req = requests.get(geocode_api_url, params=tomtom_search_params)
logging.debug (req.url)

res = req.json()
        
#summary = res['summary']
#print(summary)

# Use the first result
result = res['results'][0]
logging.debug (result)

geodata = dict()
        
geodata['lat'] = result['position']['lat']
geodata['lon'] = result['position']['lon']
geodata['address'] = result['address']['freeformAddress']

logging.debug('{address}. (lat, lng) = ({lat}, {lon})'.format(**geodata))

print (geodata)