from server.config.path import CONFIG_PATH
from server.config.path import FILE_PATH
from server.config.setting import USER_INFO
from server.config.setting import HOME_PATH
import json
import os


class User_operation(object):
    def authentication(self, login_info):
        login_name = login_info['username']
        login_passwd = login_info["password"]
        result = False
        if os.path.isfile(USER_INFO):
            user_database = self.cat_database(USER_INFO)
            for user in user_database:
                if login_name == user["username"]:
                    if login_passwd == user["password"]:
                        result = True
                        return result, HOME_PATH + '/' + login_name
        return result, None

    def cat_database(self, DB_FILE):
        with open(DB_FILE, "r") as file:
            data = json.loads(file.read())
            return data

    def check_user_is_exist(self, username):
        exit_user = []
        if os.path.isfile(USER_INFO):
            user_database = self.cat_database(USER_INFO)
            for line in user_database:
                exit_user.append(line['username'])
            if username in exit_user:
                return False
            else:
                return True


    @staticmethod
    def get_disk_size(username):
        disk_size = 0
        with open(CONFIG_PATH, 'r') as foo:
            res = json.loads(foo.read())
        for i in res:
            if i['username'] == username:
                disk_size = i["disk_size"]
                break
        return disk_size

    @staticmethod
    def count_disk_size(username):
        size = 0
        path = FILE_PATH + '/' + username
        for root, dirs, files in os.walk(path, True):
            for file in files:
                print(file, os.stat(os.path.join(root, file)).st_size)
                size += os.stat(os.path.join(root, file)).st_size
        return size
