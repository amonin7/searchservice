from typing import List, Dict
import requests
import json

from geo.service import GeoService
from search.service import BaseSearchService
from user.service import UserService
# from src.search.geo.service import GeoService
# from src.search.search.service import BaseSearchService
# from src.search.user.service import UserService


class MetaSearchService:
    # def __init__(self, search: BaseSearchService, user_service: UserService, geo_service: GeoService):
    def __init__(self):
        pass
        # self._search = search
        # self._user_service = user_service
        # self._geo_service = geo_service

    def search(self, search_text, user_id, ip, limit=10) -> List[Dict]:
        user_service_url = f'http://0.0.0.0:8001/user_data?user_id={user_id}'
        geo_service_url = f'http://0.0.0.0:8002/geo_data?ip_addr={ip}'
        user_data = requests.get(user_service_url).json()
        user_data = json.dumps(user_data)
        # user_data = self._user_service.get_user_data(user_id)  # {'gender': ..., 'age': ...}
        geo_data = requests.get(geo_service_url).json()
        geo_data = json.dumps(geo_data)
        # geo_data = self._geo_service.get_geo_data(ip)  # {'region': ...}
        if user_data == {} or geo_data == {}:
            return [{}]
        search_service_url = f'http://0.0.0.0:8010/search?search_text={search_text}&user_data={user_data}&geo_data={geo_data}'
        # search_service_url = 'http://0.0.0.0:8010/search?search_text=United&user_data={"age": 56, "gender": "male"}&geo_data={"region": "United States"}'
        search_result = requests.get(search_service_url).json()
        # df = self._search.get_search_data(search_text, user_data, geo_data, limit)
        return search_result
        # return df[self._search.DOCS_COLUMNS].to_dict('records')
