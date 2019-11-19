import requests
from urllib.parse import urljoin, urlparse, urlunparse, urlsplit, urlencode
from responses import get_resp_paginated
import mimetypes


allowed_formats = ['.csv']

class DistributionError(Exception):
    pass

def determine_readability(url_req):
    resp = get_resp_paginated(url_req)

    if 'distribution' not in resp['result']['items'][0][0].keys():
        raise DistributionError('No format available')

    access_url = list()
    values = list()

    for i in resp['result']['items'][0][0]['distribution']:
        access_url.append(i['accessURL'])
        values.append(i['format']['value'])

    url_values = dict(zip(values, access_url))

    for key, value in mimetypes.types_map.items():
        if all([value in url_values.keys(), key in allowed_formats]):
            print (key)


    












    

resp['result']['items'][0][0]['distribution'][0]['accessURL']