from common.data_source import CSV
from settings import SEARCH_DOCUMENTS_DATA_FILES1
from search.shard import ChildSearchServer
from search.service import SimpleSearchService


def main():
    shard1_service = SimpleSearchService(CSV(SEARCH_DOCUMENTS_DATA_FILES1))
    server = ChildSearchServer('shard1', shard1_service)
    server.run_server(port=8011, debug=True)


if __name__ == '__main__':
    main()
