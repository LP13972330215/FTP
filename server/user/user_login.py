from FTP.server.config.path import CONFIG_PATH
import json


class UserLogin(object):
    def __init__(self):
        pass

    def login(self, username, password):
        login_result = False
        with open(CONFIG_PATH, 'r') as foo:
            res = json.loads(foo.read())
        for i in res:
            config_user = i["username"]
            config_passwd = i["password"]
            if config_user == username:
                if config_passwd == password:
                    print("login ok!!!")
                    login_result = True
                    return login_result
        return login_result
