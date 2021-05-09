from opendataes.utils import MakeURL
from opendataes.responses import Responses
from opendataes.extract import ExtractData
import urllib3

publishers_available = {
    "Ayuntamiento de Barcelona": "L01080193",
    "Ayuntamiento de Madrid": "L01280796",
    "Ayuntamiento de Valencia": "L01462508",
}


def openes_keywords(keyword, publisher):

    keyword = 'vivienda'
    publisher = 'L01080193'
    lower_publisher = publisher.lower()

    assert isinstance(keyword, str), "keyword argument must be a string"
    assert isinstance(publisher, str), "publisher argument must be a string"
    assert (
        lower_publisher
        in {v.lower(): k for k, v in publishers_available.items()}.keys()
    ), "Publiser not available"

    url_paths = MakeURL()
    url_paths.path_explore_keyword("economia")

    urllib3.disable_warnings()
    responses = Responses()
    tst = responses.get_resp_paginated(
        url_paths.path_explore_keyword("vivienda"), num_pages=1000
    )

    data_list = tst["result"]["items"]

    tst2 = ExtractData()

    data_list[1][1].keys()

    data_list[1][1]['title'][1]

    tst2.extract_publisher_code(data_list[3][1])

    tst2.extract_dataset_name(data_list[1])
    
    tst2.extract_access_url(data_list[1][1])

    data_list[1][1]

    type(data_list[1][1])


    for v in data_list:
        ExtractData.extract_publisher_code(v)

