from server.config.path import CONFIG_PATH
from server.config.path import FILE_PATH
import json
import os


class User(object):
    def __init__(self, username, password):

        self.username = str(username)
        self.password = password

    def login(self):
        login_result = False
        with open(CONFIG_PATH, 'r') as foo:
            res = json.loads(foo.read())
        for i in res:
            config_user = i["username"]
            config_passwd = i["password"]
            if config_user == self.username:
                if config_passwd == self.password:
                    print("login ok!!!")
                    login_result = True
                    file_path = self.create_file_path()
                    return login_result, file_path
        return login_result, None

    def create_file_path(self):
        user_path = FILE_PATH  + self.username
        if os.path.exists(user_path):
            return user_path
        os.mkdir(user_path)
        return user_path

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
        total_size = 0
        print(123)
        # user_path = CONFIG_PATH + '/' + username
        for i , j ,k in os.walk(username):
            for x in k:
                total_size += os.stat(x).st_size

        return total_size

def FileSize(path):
    size = 0
    for root , dirs, files in os.walk(path, True):

        size += sum([os.stat(os.path.join(root, name)).st_size for name in files])
    #目录下文件大小累加
    return size
print(FileSize("/home/pliu/study/51CTO/FTP/client/"))





