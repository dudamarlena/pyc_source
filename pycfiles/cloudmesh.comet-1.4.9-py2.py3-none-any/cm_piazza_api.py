# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/big/ENV2/lib/python2.7/site-packages/cloudmesh_piazza/cm_piazza_api.py
# Compiled at: 2016-09-12 11:57:52
import requests, json, getpass, sys, yaml, os

class PiazzaExtractor:
    api_url = 'https://piazza.com/logic/api'
    login_cookie = None

    def __init__(self, id=None):
        if id is None:
            self.class_id = 'irqfvh1ctrg2vt'
        else:
            self.class_id = id
        return

    def get_login(self, filename='.piazza'):
        with open(filename, 'r') as (stream):
            try:
                config = yaml.load(stream)
            except yaml.YAMLError as exc:
                print exc

            print config
        password = config['piazza']['password']
        email = config['piazza']['email']
        print (email, password)
        return (
         email, password)

    def login(self, email='', password=''):
        email = email if email else raw_input('Enter login email: ')
        password = password if password else getpass.getpass('Enter your password')
        print 'logging in...'
        login_data = json.dumps({'method': 'user.login', 'params': {'email': email, 
                      'pass': password}})
        login = requests.post(self.api_url, data=login_data)
        self.login_cookie = login.cookies

    def get_folder_posts(self, folder):
        print 'getting items from folder...'
        data = json.dumps({'method': 'network.filter_feed', 'params': {'nid': self.class_id, 
                      'filter_folder': folder, 
                      'folder': '1'}})
        folder_request = requests.post(self.api_url, data=data, cookies=self.login_cookie)
        feed = json.loads(folder_request.content)['result']['feed']
        feed_list = []
        for index, post in enumerate(feed):
            data = json.dumps({'method': 'content.get', 'params': {'cid': post['id'], 'nid': self.class_id}})
            r = requests.post(self.api_url, data=data, cookies=self.login_cookie)
            post_json = json.loads(r.content)['result']['history'][0]
            uid = post_json['uid']
            created = post_json['created']
            subject = post_json['subject']
            content = post_json['content']
            feed_list.append({'uid': uid, 'created': created, 'subject': subject, 'content': content})
            sys.stdout.write('\r')
            sys.stdout.write(str(index) + '/' + str(len(feed)))
            sys.stdout.flush()

        text = json.dumps({'feed': feed_list}, indent=4)
        text = unicode(text, 'UTF-8')
        text = text.replace('\\u00a0', ' ')
        text = text.encode('ascii', errors='ignore')
        return text

    def save_folder_posts(self, folder):
        posts = self.get_folder_posts(folder)
        print 'writing file...'
        f = open(folder + '.json', 'w+')
        f.write(posts)
        f.close