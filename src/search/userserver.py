from common.data_source import CSV

from settings import USER_DATA_FILE
from user.service import UserService
from user.server import UserServer


def main():
    user_service = UserService(CSV(USER_DATA_FILE))
    server = UserServer('usersearch', user_service=user_service)
    server.run_server(debug=True)

if __name__ == '__main__':
    main()
