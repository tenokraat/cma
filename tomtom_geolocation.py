import json,requests,os
import logging

logging.basicConfig(level=logging.DEBUG)

class geolocation:
    def __init__ (self):
 
        #This Script needs to connect to the internet, hence requires proxy.

        self.cma_proxy = 'http://192.168.205.163:8080/'
        os.environ['http_proxy'] = self.cma_proxy 
        os.environ['https_proxy'] = self.cma_proxy

        #Using Python requests and TomTom Search/Geocode API to retrieve geo location.

        #API Key oliver.wehrli@gmail.com

        self.api_key = 'KR3oOGSM59aMJBOSKAxTlxoJvYBjrENU'

        self.vowel_dict = {
                '\xc3\xa4': 'ae',  # U+00E4	   \xc3\xa4
                '\xc3\xb6': 'oe',  # U+00F6	   \xc3\xb6
                '\xc3\xbc': 'ue',  # U+00FC	   \xc3\xbc
                '\xc3\x84': 'Ae',  # U+00C4	   \xc3\x84
                '\xc3\x96': 'Oe',  # U+00D6	   \xc3\x96
                '\xc3\x9c': 'Ue',  # U+00DC	   \xc3\x9c
                '\xc3\x9f': 'ss',  # U+00DF	   \xc3\x9f
            }

    def replace_de_vowel_mutation(self, unicode_string):
        
        utf8_string = unicode_string.encode('utf-8')

        for k in self.vowel_dict.keys():
            utf8_string = utf8_string.replace(k, self.vowel_dict[k])

        return utf8_string.decode()

    def get_geolocation(self, shop_address):
        
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

        return geodata