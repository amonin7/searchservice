from common.data_source import CSV
from metasearch.http import Server
from metasearch.service import MetaSearchService
from search.service import SearchInShardsService, SimpleSearchService
from settings import SEARCH_DOCUMENTS_DATA_FILES


def main():
    # user_service = UserService(CSV(USER_DATA_FILE))
    # geo_service = GeoService(CSV(GEO_DATA_FILE))
    # search = SearchInShardsService(shards=[f'http://shard{i}:801{i}/search' for i in range(1, 4)])
    metasearch = MetaSearchService()
    # metasearch = MetaSearchService(search)
    # metasearch = MetaSearchService(search, user_service, geo_service)
    server = Server('metasearch', metasearch=metasearch)
    server.run_server(debug=True)


if __name__ == '__main__':
    main()
