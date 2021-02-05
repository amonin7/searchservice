from flask import Flask, request
from user.service import UserService
# from src.search.common.data_source import CSV
# from src.search.settings import USER_DATA_FILE


class UserServer(Flask):
    def __init__(self, name: str, user_service: UserService):
        super().__init__(name)
        self._user_service = user_service
        urls = [
            ('/user_data', self.user_data, {}),
        ]
        for url in urls:
            if len(url) == 3:
                self.add_url_rule(url[0], url[1].__name__, url[1], **url[2])

    def user_data(self):
        user_id = request.args.get('user_id')
        if user_id is None or user_id == 'None':
            return {}
        else:
            user_id = int(user_id)
        ud = self._user_service.get_user_data(user_id)
        return ud

    def run_server(self, **kwargs):
        super().run(host='0.0.0.0', port=8001, **kwargs)

#
# if __name__ == "__main__":
#     user_service = UserService(CSV(USER_DATA_FILE))
#     server = UserServer('usersearch', user_service=user_service)
#     server.run_server(debug=True)
