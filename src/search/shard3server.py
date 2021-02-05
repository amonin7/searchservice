from common.data_source import CSV
from settings import SEARCH_DOCUMENTS_DATA_FILES3
from search.shard import ChildSearchServer
from search.service import SimpleSearchService


def main():
    shard3_service = SimpleSearchService(CSV(SEARCH_DOCUMENTS_DATA_FILES3))
    server = ChildSearchServer('shard3', shard3_service)
    server.run_server(port=8013, debug=True)


if __name__ == '__main__':
    main()
