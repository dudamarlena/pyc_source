# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/polical.py
# Compiled at: 2020-05-12 16:47:43
# Size of source mod 2**32: 641 bytes
import TareasCSVToBD, SendTaskToTrello, SimpleIcsToCSV, configuration, sys, Get_Trello_MoodleEPN_Keys

def main(argv):
    if len(argv) == 2:
        argument = argv[1]
        if argument == '--addUser':
            Get_Trello_MoodleEPN_Keys.onboard(True)
    else:
        users = configuration.load_config_file('polical.yaml')
        for user in users.keys():
            SimpleIcsToCSV.convertICStoCSV(users[user]['calendar_url'])
            TareasCSVToBD.LoadCSVTasktoDB(user, users[user])
            SendTaskToTrello.SendTaskToTrello(user, users[user])


if __name__ == '__main__':
    main(sys.argv)