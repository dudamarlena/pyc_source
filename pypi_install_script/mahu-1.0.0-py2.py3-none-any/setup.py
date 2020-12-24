"""The Setup command."""

import os
from .base import *

class Setup(Base):

    def clone_install_and_give_permission(self, repo_name, repo_link):
        os.chdir(os.path.join(USER_HOME, MAHU))
        print("Start fetching {}".format(repo_name))
        os.system("git clone {}".format(repo_link))
        print("Done fetching ".format(repo_name))

        os.chdir(os.path.join(USER_HOME, MAHU, repo_name))

        print("Start installing dependencies")
        self.activate_virtualenv()
        os.system("sudo pip install -e .")
        self.deactivate_virtualenv()
        print("Done installing dependencies")

        print("Give permission to run {}:".format(repo_name))
        os.system("sudo chmod 777 run.sh")
        print("Permission got!")

    def run(self):
        print("Start installing Mahu Search Plugin at User Home {}".format(USER_HOME))
        os.chdir(USER_HOME)

        if os.path.exists(MAHU):
            print("previously installed version detected, removing...")
            os.system("rm -rf {}".format(MAHU))

        os.system("mkdir {}".format(MAHU))
        

        self.clone_install_and_give_permission(MAHU_QUESTION_ANALYZER, MAHU_QUESTION_ANALYZER_GITHUB)
        self.clone_install_and_give_permission(MAHU_PAGE_PARSER, MAHU_PAGE_PARSER_GITHUB)

