from . import Config
from ..helpers import pwd_prompt
from librusapi import Token
from librusapi.exceptions import LoginError


class Setup:
    """
    All you need for inital run of the program
    """

    def __init__(self):
        self.config = Config()

    def begin(self):
        try:
            self.config.username = input("Username: ")
        except KeyboardInterrupt:
            exit(1)
        logged = False
        while not logged:
            try:
                pwd = pwd_prompt()
            except KeyboardInterrupt:
                exit(1)

            try:
                self.config.token = Token.get(self.config.username, pwd)
            except LoginError as ex:
                print("Login failed!")
                print(f"Username is '{self.config.username}'")
            except Exception as ex:
                print(ex)
                exit(1)
            else:
                logged = True
        try:
            self.config.write()
        except Exception as ex:
            print(ex)
            exit(1)
