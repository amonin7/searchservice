from abc import abstractmethod
from typing import List
import requests

import pandas as pd
import json

from common.data_source import AbstractDataSource


def stupid_count_tokens(tokens, text):
    res = 0
    for token in tokens:
        if token in text:
            res += 1
    return res


class BaseSearchService:
    DOCS_COLUMNS = ['document', 'key', 'key_md5']

    @abstractmethod
    def get_search_data(self, search_text, user_data=None, geo_data=None, limit=10) -> pd.DataFrame:
        pass


class SimpleSearchService(BaseSearchService):
    def __init__(self, data_source: AbstractDataSource):
        self._data = pd.DataFrame(
            data_source.read_data(),
            columns=[*self.DOCS_COLUMNS, 'gender', 'age_from', 'age_to', 'region']
        )

    def _build_tokens_count(self, search_text):
        tokens = search_text.split()
        res = self._data['document'].apply(lambda x: stupid_count_tokens(tokens, x))
        res.name = None
        return res

    def _get_geo_mask(self, geo_data=None):
        gd = geo_data.get('region') if geo_data is not None else None
        return self._data['region'] == gd

    def _get_gender_mask(self, user_data=None):
        ud = user_data.get('gender', 'null') if user_data is not None else 'non-existing gender'
        return self._data['gender'].apply(lambda x: stupid_count_tokens([ud], x))

    def _get_age_mask(self, user_data=None):
        user_age = int(user_data['age']) if user_data is not None else -1
        return self._data.apply(lambda x: x['age_from'] <= user_age <= x['age_to'], axis=1)

    def _sort_by_rating_and_tokens(self, rating, tokens_count, key_md5):
        df = pd.concat([tokens_count, rating, key_md5], axis=1)
        return df.sort_values([0, 1, 'key_md5'], ascending=[False, False, False])

    def get_search_data(self, search_text, user_data=None, geo_data=None, limit=10) -> pd.DataFrame:
        # this is some simple algorithm that came to my mind, does not need to be useful or good, just something working
        if search_text is None or search_text == '':
            return pd.DataFrame([], columns=self.DOCS_COLUMNS)
        tokens_count = self._build_tokens_count(search_text)
        geo_mask = self._get_geo_mask(geo_data)
        gender_mask = self._get_gender_mask(user_data)
        age_mask = self._get_age_mask(user_data)
        rating = geo_mask + gender_mask + age_mask
        df = self._sort_by_rating_and_tokens(rating, tokens_count, self._data['key_md5'])
        return self._data.loc[df.head(limit).index]


class SearchInShardsService(SimpleSearchService):
    def __init__(self, shards: List[str]):
        self._shards = shards

    def get_search_data(self, search_text, user_data=None, geo_data=None, limit=10) -> pd.DataFrame:
        shards_responses = []
        user_data = json.dumps(user_data)
        geo_data = json.dumps(geo_data)
        for shard_url in self._shards:
            shard_url = f'{shard_url}?search_text={search_text}&user_data={user_data}&geo_data={geo_data}'
            # shard_url = 'http://0.0.0.0:8011/search?search_text=some_text&user_data={"age": 13,"gender": "female"}&geo_data={"region": "United States"}'
            shard_resp = requests.get(shard_url).json()
            shards_responses.append(pd.DataFrame.from_dict([shard_resp]))
        self._data = pd.concat(shards_responses)  # possible data race in case of multi thread/async usage
        self._data.reset_index(inplace=True, drop=True)
        assert self._data.index.is_unique
        return super().get_search_data(search_text, user_data=None, geo_data=None, limit=10)
