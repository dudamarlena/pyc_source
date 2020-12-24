# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Trello_Project\trello.py
# Compiled at: 2020-03-29 12:15:41
# Size of source mod 2**32: 11758 bytes
"""
This project allows interaction with the Trello application via the command line.
This project is written in python scripting language and implements the web service rest api to ensure interaction with the Trello application.
This project contains four features which are:
*Add a list to a board.
*Add a Trello card to a column.
*Be able to label on a card (X column of board Y).
*Be able to comment on a card (X column of board Y).
"""
import argparse, sys
try:
    import requests
except ImportError:
    print('Trying to Install required module: requests\n')
    os.system('python -m pip install requests')
    import requests

class TrelloInterractorCLI(object):
    FAIL, SUCCESS = (0, 1)

    def __init__(self, mode='normal', test_param=None):
        """
                defines the way of executing the code in the command line.
                First: the funtion name
                Second: the parameters  
                """
        self.status = self.FAIL
        parseArgumentOk = self.parse_args(mode, test_param)
        if parseArgumentOk:
            getattr(self, self.command)()

    def parse_args(self, mode, test_param):
        """
                Defines the way of executing the code in the command line
                in normal mode and simulating arguments values in case
                of unit-test mode.
                """
        returnValue = True
        if mode == 'unittest':
            if test_param is None:
                print('Missing test parameters !!!')
                sys.exit()
            else:
                self.command = test_param['command']
                if self.command == 'addList':
                    self.boardId = test_param['board_id']
                    self.listName = test_param['list_name']
                else:
                    if self.command == 'addCard':
                        self.listId = test_param['list_id']
                        self.cardName = test_param['card_name']
                        self.cardDescription = test_param['card_desc']
                    else:
                        if self.command == 'labelCard':
                            self.cardId = test_param['card_id']
                            self.labelId = test_param['label_id']
                        else:
                            if self.command == 'commentCard':
                                self.cardId = test_param['card_id']
                                self.commentText = test_param['comment_text']
                            else:
                                returnValue = False
            self.key = test_param['app_key']
            self.token = test_param['app_token']
        else:
            parser = argparse.ArgumentParser(description='Project interaction with trello',
              usage='trello <command> [<args>]\n\n\t\t\tThe only available trello commands for now are:\n\t\t\t\taddList\t\t Add a new list to an existing board\n\t\t\t\taddCard\t\t Add a new card to an existing list\n\t\t\t\tlabelCard\t Add a label to an existing card\n\t\t\t\tcommentCard\t Add a comment to an existing card\n\t\t\t')
            parser.add_argument('command', help='Subcommand to run')
            args = parser.parse_args(sys.argv[1:2])
            if not hasattr(self, args.command):
                print('Unrecognized command')
                parser.print_help()
                exit(1)
            else:
                self.command = args.command
                if self.command == 'addList':
                    parser = argparse.ArgumentParser(description='Add a trello list to an existing board')
                    parser.add_argument('-i', '--board_id', required=True, help='trello board id')
                    parser.add_argument('-n', '--list_name', type=str, required=True, help='trello name list of board, in case of multiple string please put it between two " "')
                    parser.add_argument('-k', '--app_key', required=True, help='trello key')
                    parser.add_argument('-t', '--app_token', required=True, help='trello token')
                    args = parser.parse_args(sys.argv[2:])
                    self.boardId = args.board_id
                    self.listName = args.list_name
                    self.key = args.app_key
                    self.token = args.app_token
                else:
                    if self.command == 'addCard':
                        parser = argparse.ArgumentParser(description='Add a trello card to an existing list')
                        parser.add_argument('-i', '--list_id', required=True, help='trello list id')
                        parser.add_argument('-n', '--card_name', type=str, required=True, help='trello card name')
                        parser.add_argument('-d', '--card_desc', type=str, required=False, help='trello card description')
                        parser.add_argument('-k', '--app_key', required=True, help='trello key')
                        parser.add_argument('-t', '--app_token', required=True, help='trello token')
                        args = parser.parse_args(sys.argv[2:])
                        self.listId = args.list_id
                        self.cardName = args.card_name
                        self.cardDescription = args.card_desc
                        self.key = args.app_key
                        self.token = args.app_token
                    else:
                        if self.command == 'labelCard':
                            parser = argparse.ArgumentParser(description='Add a trello label to an existing card')
                            parser.add_argument('-c', '--card_id', required=True)
                            parser.add_argument('-l', '--label_id', required=True)
                            parser.add_argument('-k', '--app_key', required=True)
                            parser.add_argument('-t', '--app_token', required=True)
                            args = parser.parse_args(sys.argv[2:])
                            self.cardId = args.card_id
                            self.labelId = args.label_id
                            self.key = args.app_key
                            self.token = args.app_token
                        else:
                            if self.command == 'commentCard':
                                parser = argparse.ArgumentParser(description='Add a comment to an existing card')
                                parser.add_argument('-i', '--id_card', required=True)
                                parser.add_argument('-c', '--comment_text', type=str, required=True)
                                parser.add_argument('-k', '--app_key', required=True)
                                parser.add_argument('-t', '--app_token', required=True)
                                args = parser.parse_args(sys.argv[2:])
                                self.cardId = args.card_id
                                self.commentText = args.comment_text
                                self.key = args.app_key
                                self.token = args.app_token
                            else:
                                print('Invalid command !!!')
                                returnValue = False
                                sys.exit(1)
        return returnValue

    def addList(self):
        """
                Allows adding a trello list to a board.
                To add the list the following parameters are required 
                board_id ---> The board identifier to which we will add a list
                list_name ---> The name of the list to be added
                app_key ---> The key of the application
                app_token ---> The token of the application
                These parameters are entered via the command line
                Example of command to add a list to a board: 
                python trello.py addList -i 5e7a49129485c7470316045a -n "Coding features" -k e84fd113f9554e16c58ac2652984eef4 -t 21c74bc55f315e804cd455935b4e91c17a9fb38670bf26ae9a84e62a20acc358
                """
        baseRestServiceUrl = 'https://trello.com/1/boards/'
        PostData = {'name':self.listName, 
         'key':self.key,  'token':self.token}
        postUrl = baseRestServiceUrl + self.boardId + '/lists'
        try:
            responseAddList = requests.post(url=postUrl, data=PostData)
            if responseAddList.ok:
                self.status = self.SUCCESS
        except requests.exceptions.HTTPError as errh:
            try:
                print('Http Error:', errh)
            finally:
                errh = None
                del errh

        except requests.exceptions.ConnectionError as errc:
            try:
                print('Error Connecting:', errc)
            finally:
                errc = None
                del errc

        except requests.exceptions.Timeout as errt:
            try:
                print('Timeout Error:', errt)
            finally:
                errt = None
                del errt

        except requests.exceptions.RequestException as err:
            try:
                print('OOps: Something Else', err)
            finally:
                err = None
                del err

    def addCard(self):
        """
                Allows adding a card to a column.
                To be able to add a card the following parameters are required
                list_id ---> The list identifier to which we will add a card
                card_name ---> The name of the card to be added
                card_desc ---> The dexcription of the card which is not required
                app_key ---> The key of the application
                app_token ---> The token of the application
                These parameters are entered via the command line
                Example of command to add a card to a column(a list).
                C:      rello>python trello.py addCard -i 5e7d0c995478192bc367c2d2 -n "AddCardFeature" -d "add a card to a list" -k e84fd113f9554e16c58ac2652984eef4 -t 21c74bc55f315e804cd455935b4e91c17a9fb38670bf26ae9a84e62a20acc358
                """
        baseRestServiceUrl = 'https://api.trello.com/1/lists/'
        PostData = {'name':self.cardName, 
         'desc':self.cardDescription,  'key':self.key,  'token':self.token}
        postUrl = baseRestServiceUrl + self.listId + '/cards'
        try:
            responseAddCard = requests.post(url=postUrl, data=PostData)
            if responseAddCard.ok:
                self.status = self.SUCCESS
        except requests.exceptions.HTTPError as errh:
            try:
                print('Http Error:', errh)
            finally:
                errh = None
                del errh

        except requests.exceptions.ConnectionError as errc:
            try:
                print('Error Connecting:', errc)
            finally:
                errc = None
                del errc

        except requests.exceptions.Timeout as errt:
            try:
                print('Timeout Error:', errt)
            finally:
                errt = None
                del errt

        except requests.exceptions.RequestException as err:
            try:
                print('OOps: Something Else', err)
            finally:
                err = None
                del err

    def labelCard(self):
        """
                Allows to label on a a card.
                To be able to label on a card the following parameters are required
                card_id ---> The identifier of the card to which we will add a label
                label_id ---> The identifier of the label color to be added
                app_key ---> The key of the application
                app_token ---> The token of the application
                These parameters are entered via the command line
                Example of command to label on a card.
                C:      rello>C:        rello>python trello.py labelCard -c 5e7d0f97b042ac75bd0e4137 -l 5e7a49127669b22549aa63b6        -k e84fd113f9554e16c58ac2652984eef4 -t 21c74bc55f315e804cd455935b4e91c17a9fb38670bf26ae9a84e62a20acc358
                """
        baseRestServiceUrl = 'https://api.trello.com/1/cards/'
        PostData = {'value':self.labelId, 
         'key':self.key,  'token':self.token}
        postUrl = baseRestServiceUrl + self.cardId + '/idLabels'
        try:
            responseLabelCard = requests.post(url=postUrl, data=PostData)
            if responseLabelCard.ok:
                self.status = self.SUCCESS
        except requests.exceptions.HTTPError as errh:
            try:
                print('Http Error:', errh)
            finally:
                errh = None
                del errh

        except requests.exceptions.ConnectionError as errc:
            try:
                print('Error Connecting:', errc)
            finally:
                errc = None
                del errc

        except requests.exceptions.Timeout as errt:
            try:
                print('Timeout Error:', errt)
            finally:
                errt = None
                del errt

        except requests.exceptions.RequestException as err:
            try:
                print('OOps: Something Else', err)
            finally:
                err = None
                del err

    def commentCard(self):
        """
                Allows to comment on a card.
                To be able to comment on a card the following parameters are required
                card_id ---> The identifier of the card to which we will add a label
                comment_text ---> The comment text to be added
                app_key ---> The key of the application
                app_token ---> The token of the application
                These parameters are entered via the command line
                Example of command to comment on a card.
                C:      rello>python trello.py commentCard -i 5e7d0f97b042ac75bd0e4137 -c "must be ended this day"      -k e84fd113f9554e16c58ac2652984eef4 -t 21c74bc55f315e804cd455935b4e91c17a9fb38670bf26ae9a84e62a20acc358
                """
        baseRestServiceUrl = 'https://api.trello.com/1/cards/'
        PostData = {'text':self.commentText, 
         'key':self.key,  'token':self.token}
        postUrl = baseRestServiceUrl + self.cardId + '/actions/comments'
        try:
            responseCommentCard = requests.post(url=postUrl, data=PostData)
            if responseCommentCard.ok:
                self.status = self.SUCCESS
        except requests.exceptions.HTTPError as errh:
            try:
                print('Http Error:', errh)
            finally:
                errh = None
                del errh

        except requests.exceptions.ConnectionError as errc:
            try:
                print('Error Connecting:', errc)
            finally:
                errc = None
                del errc

        except requests.exceptions.Timeout as errt:
            try:
                print('Timeout Error:', errt)
            finally:
                errt = None
                del errt

        except requests.exceptions.RequestException as err:
            try:
                print('OOps: Something Else', err)
            finally:
                err = None
                del err

    def getStatus(self):
        """
                Returns the status of last class invokation.
                This function is added to be able to do unit test. 
                """
        print('status= %s' % self.status)
        return self.status


if __name__ == '__main__':
    trelloInterractorCli = TrelloInterractorCLI()