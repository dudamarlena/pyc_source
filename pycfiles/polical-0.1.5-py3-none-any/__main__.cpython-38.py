# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/__main__.py
# Compiled at: 2020-05-13 11:31:26
# Size of source mod 2**32: 849 bytes
from polical import TareasCSVToBD
from polical import SendTaskToTrello
from polical import SimpleIcsToCSV
from polical import configuration
import sys
from polical import Get_Trello_MoodleEPN_Keys

def main(argv):
    if len(argv) == 2:
        argument = argv[1]
        if argument == '--addUser':
            Get_Trello_MoodleEPN_Keys.onboard(False)
    else:
        users = None
        while users == None:
            users = configuration.load_config_file('polical.yaml')
            if users == None:
                Get_Trello_MoodleEPN_Keys.onboard(False)

        for user in users.keys():
            SimpleIcsToCSV.convertICStoCSV(users[user]['calendar_url'])
            TareasCSVToBD.LoadCSVTasktoDB(user, users[user])
            SendTaskToTrello.SendTaskToTrello(user, users[user])


if __name__ == '__main__':
    main(sys.argv)