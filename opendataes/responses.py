import requests
from urllib.parse import urljoin, urlparse, urlunparse, urlsplit, urlencode


class BadStatusCode(Exception):
    pass


class BadJSONParsing(Exception):
    pass


class Responses:
    def __init__(self):
        pass


    def get_resp(self, url_req):

        rq = requests.get(url_req, verify=False)

        if rq.status_code != 200:
            raise BadStatusCode(f"Not successful request. Returned code: {rq.status_code}")

        try:
            rq.json()
        except:
            raise BadJSONParsing("Returned format is unusual and not JSON")

        return rq.json()


    def get_resp_paginated(self, url_req, num_pages=1, page=0):

        whole_list = []

        while num_pages > 0:
            url_parts = urlparse(url_req)

            query_ = urlencode({"_pageSize": 50, "_page": page})
            url_req_query = url_parts._replace(query=query_)

            parsed_response = self.get_resp(url_req_query.geturl())

            data_list = parsed_response['result']['items']
            whole_list.append(data_list)

            try:
                parsed_response['result']['next']
            except:
                break

            page += 1
            num_pages -= 1

        parsed_response['result']['items'] = whole_list[:]

        return parsed_response



