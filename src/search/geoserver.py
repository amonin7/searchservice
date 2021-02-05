from common.data_source import CSV
from geo.service import GeoService
from geo.server import GeoServer
from settings import GEO_DATA_FILE


def main():
    geo_service = GeoService(CSV(GEO_DATA_FILE))
    server = GeoServer('geosearch', geo_service=geo_service)
    server.run_server(debug=True)


if __name__ == '__main__':
    main()
