import requests
from urllib.parse import urljoin, urlparse, urlunparse, urlsplit, urlencode
from responses import get_resp_paginated
import mimetypes


class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class DistributionError(Error):
    """Distribution error class. Will be the one used for the Extract class"""

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ExtractData:
    def __init__(self, allowed_formats=[".csv"]):
        self.allowed_formats = allowed_formats


    def determine_readability(self, url_req):
        resp = get_resp_paginated(url_req)

        if "distribution" not in resp["result"]["items"][0][0].keys():
            raise DistributionError("Exception occurred", "No format available")

        access_url = []
        values = []

        for i in resp["result"]["items"][0][0]["distribution"]:
            access_url.append(i["accessURL"])
            values.append(i["format"]["value"])

        url_values = dict(zip(values, access_url))

        for key, value in mimetypes.types_map.items():
            if all([value in url_values.keys(), key in self.allowed_formats]):
                print(key)


    def extract_url_format(self, data_list):
        try:
            if isinstance(data_list["distribution"], dict):
                raw_formats = [data_list["distribution"]["format"]["value"]]
            else:
                raw_formats = [i["format"]["value"] for i in data_list["distribution"]]
        except:
            raise DistributionError("Exception occurred", "No format available")

        raw_extensions = [mimetypes.guess_extension(i) for i in raw_formats]
        correct_formats = list(set([x for x in raw_extensions if x in self.allowed_formats]))

        return correct_formats


    def extract_access_url(self, data_list):
        # resp['result']['items'][0][0]['distribution'][0]['accessURL']
        try:
            if isinstance(data_list["distribution"], dict):
                access_url = [data_list["distribution"]["accessURL"]]
            else:
                access_url = [i["accessURL"] for i in data_list["distribution"]]
        except:
            raise DistributionError("Exception occurred", "No URL available")

        return access_url


    def extract_dataset_name(self, data_list):
        try:
            if isinstance(data_list["distribution"], dict):
                title = [data_list["distribution"]["title"][0]]
            else:
                title = [i["title"][0] for i in data_list["distribution"]]
        except:
            DistributionError("Exception occurred", "No titles available")

        return title


    def extract_language(self, data_list):
        try:
            languages = [i["_lang"] for i in data_list["description"]]
        except:
            DistributionError("Exception occurred", "No languages available")
        return languages


    def extract_release_date(self, data_list):
        # for now, let's keep the date as string
        # but should be changed
        if "issued" not in data_list:
            return "No release date available"
        else:
            return data_list["issued"]


    def extract_modified_date(self, data_list):
        if "modified" not in data_list:
            return "No modification date available"
        else:
            return data_list["modified"]


    def extract_publisher_code(self, data_list):
        if "publisher" in data_list:
            return "No publisher available"
        else:
            return data_list["publisher"].split("/")[-1]


    def extract_publisher_name(self, data_list):
        """TO DO"""


    def extract_endpath(self, data_list):
        if "_about" not in data_list:
            return "No link to the data in datos.gob.es"
        else:
            data_list["_about"].split("/")[-1]

