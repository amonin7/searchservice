from flask import Flask, request
import json

from search.service import SimpleSearchService


class ChildSearchServer(Flask):
    def __init__(self, name: str, child_search: SimpleSearchService):
        super().__init__(name)
        self._child_search = child_search
        urls = [
            ('/search', self.search, {}),
        ]
        for url in urls:
            if len(url) == 3:
                self.add_url_rule(url[0], url[1].__name__, url[1], **url[2])

    def search(self):
        text = request.args.get('search_text')
        if text is None or text == 'None':
            return {}
        user_data = request.args.get('user_data')
        if user_data is None or user_data == 'None':
            user_data = None
        elif user_data is not None:
            user_data = json.loads(user_data)
        geo_data = request.args.get('geo_data')
        if geo_data is None or geo_data == 'None':
            user_data = None
        elif geo_data is not None:
            geo_data = json.loads(geo_data)
        limit = int(request.args.get('limit', 10))
        sd = self._child_search.get_search_data(search_text=text, user_data=user_data, geo_data=geo_data, limit=limit)

        return sd.to_dict('records')[0]

    def run_server(self, **kwargs):
        super().run(host='0.0.0.0', **kwargs)
