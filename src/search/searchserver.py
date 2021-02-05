from search.server import FatherSearchServer
from search.service import SearchInShardsService


def main():
    searchservice = SearchInShardsService(shards=[f'http://0.0.0.0:801{i}/search' for i in range(1, 4)])
    # searchservice = SearchInShardsService(shards=[f'http://shard{i}:801{i}/search' for i in range(1, 4)])
    server = FatherSearchServer('searchserver', searchservice)
    server.run_server(port=8010, debug=True)


if __name__ == '__main__':
    main()
