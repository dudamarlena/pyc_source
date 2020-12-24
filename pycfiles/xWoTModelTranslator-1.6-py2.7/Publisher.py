# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/xwot1/REST-Server-Skeleton/Publisher.py
# Compiled at: 2015-04-15 10:48:25
import sqlite3, requests, json, logging

class Publisher:

    def __init__(self):
        self.__database = 'clients.db'

    def __getClients(self, query):
        conn = sqlite3.connect('clients.db')
        c = conn.cursor()
        c.execute('Select * from Subscriber where resourceid=1 order by id')
        result = c.fetchall()
        c.close()
        conn.close()
        return result

    def __getConditions(self, clientid):
        conn = sqlite3.connect('clients.db')
        c = conn.cursor()
        c.execute("select * from SensorEvent where subscriberid='" + str(clientid) + "'")
        result = c.fetchall()
        c.close()
        conn.close()
        return result

    def publish(self, values):
        """Entry point for external scripts to send a notification to all subscribers"""
        clients = self.__getClients('Select * from Subscriber where resourceid=1 order by id')
        for client in clients:
            conditions = self.__getConditions(client[0])
            self.__updateClient(client, values)

    def __updateClient(self, client, values):
        """Updates each individual client by sending the corresponding request"""
        data = json.dumps(values)
        logging.debug('Updating client: ' + client[1])
        try:
            if client[2] == 'POST':
                r = requests.post(client[1], data, auth=('user', '*****'), timeout=2)
            if client[2] == 'PUT':
                r = requests.put(client[1], data, auth=('user', '*****'), timeout=2)
            if client[2] == 'GET':
                urlencoded = ''
                for key in values:
                    urlencoded = urlencoded + key + '=' + str(values[key]) + '&'

                urlencoded = '?' + urlencoded[:-1]
                r = requests.get(client[1] + urlencoded, auth=('user', '*****'), timeout=2)
        except requests.exceptions.RequestException as e:
            logging.error('Could not update Client :-(')
            logging.debug(e.errno)
        else:
            logging.debug(r.json)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname) -7s] %(asctime)s  %(module) -20s:%(lineno)4s %(funcName)-20s %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    p = Publisher()
    p.publish({'three': 3, 'two': 2, 'one': 1})