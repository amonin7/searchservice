from flask import Flask, request
from geo.service import GeoService
# from common.data_source import CSV
# from settings import GEO_DATA_FILE
# from src.search.common.data_source import CSV
# from src.search.settings import GEO_DATA_FILE


class GeoServer(Flask):
    def __init__(self, name: str, geo_service: GeoService):
        super().__init__(name)
        self._geo_service = geo_service
        urls = [
            ('/geo_data', self.geo_data, {}),
        ]
        for url in urls:
            if len(url) == 3:
                self.add_url_rule(url[0], url[1].__name__, url[1], **url[2])

    def geo_data(self):
        ip = request.args.get('ip_addr')
        if ip is None:
            ip = request.remote_addr
        gd = self._geo_service.get_geo_data(ip)
        if gd is None:
            return {}
        else:
            return gd

    def run_server(self, **kwargs):
        super().run(host='0.0.0.0', port=8002, **kwargs)


# if __name__ == "__main__":
#     geo_service = GeoService(CSV(GEO_DATA_FILE))
#     server = GeoServer('geosearch', geo_service=geo_service)
#     server.run_server(debug=True)
