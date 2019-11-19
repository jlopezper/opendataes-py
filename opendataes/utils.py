from urllib.parse import urljoin, urlparse, urlunparse, urlsplit
import unidecode


class MakeURL:
    def __init__(self):
        # self.base_url = 'https://datos.gob.es/apidata'
        self.__scheme = "https"
        self.__netloc = "datos.gob.es/apidata"

    def path_catalog(self, path, params="", query="", fragment=""):
        return urlunparse(
            (self.__scheme, self.__netloc, "catalog/" + path, params, query, fragment)
        )

    def path_catalog_dataset(self, path, params="", query="", fragment=""):
        return urlunparse(
            (
                self.__scheme,
                self.__netloc,
                "catalog/dataset/" + path,
                params,
                query,
                fragment,
            )
        )

    def path_datasets(self, params=""):
        return self.path_catalog("dataset", params=params)

    def path_publishers(self, params=""):
        return self.path_catalog("publisher", params=params)

    def path_distribution(self, params=""):
        return self.path_catalog("distribution", params=params)

    def path_dataset_id(self, id, params=""):
        url_parts = urlparse(self.path_datasets())
        current_path = url_parts.path
        url_parts = url_parts._replace(path=current_path + "/" + id, query=params)
        return url_parts.geturl()

    def path_explore_keyword(self, keyword):
        keyword = unidecode.unidecode(keyword)
        return self.path_catalog_dataset("keyword/" + keyword)

    
