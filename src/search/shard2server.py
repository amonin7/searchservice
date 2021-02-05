from common.data_source import CSV
from settings import SEARCH_DOCUMENTS_DATA_FILES2
from search.shard import ChildSearchServer
from search.service import SimpleSearchService


def main():
    shard2_service = SimpleSearchService(CSV(SEARCH_DOCUMENTS_DATA_FILES2))
    server = ChildSearchServer('shard2', shard2_service)
    server.run_server(port=8012, debug=True)


if __name__ == '__main__':
    main()
