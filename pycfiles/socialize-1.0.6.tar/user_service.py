# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/socialize/socialize/services/user_service.py
# Compiled at: 2016-09-26 07:20:46
from .service import Service
from click import secho

class UserService(Service):

    def get_current_user(self):
        r = self.get('user/')
        self.print_user_info(r)

    def set_attr(self, slogan=None, website=None, interests=None, skills=None):
        r = self.post('user/', data={'slogan': slogan, 
           'website': website, 
           'interests': interests, 
           'skills': skills})
        self.check_reponse(r, 'Profile successfully updated.')

    def get_user(self, name):
        r = self.get('user/' + name + '/')
        if r != 404:
            self.print_user_info(r)
        else:
            print 'The user was not found. Maybe you typed the username wrong?'

    def display_groups(self, groups):
        groups.pop(0)
        for group in groups:
            secho('\t\t' + str(group))

    def print_user_info(self, r):
        try:
            initial_group = r['groups'][0]
        except:
            initial_group = 'None'

        secho('')
        secho('********** ' + r['username'] + ' **********', bg='blue', fg='white')
        secho('')
        secho('Slogan: \t' + str(r['slogan']))
        secho('Website:\t' + str(r['website']))
        secho('Interests:\t' + str(r['interests']))
        secho('Skills:   \t' + str(r['skills']))
        secho('')
        secho('Status:   \t' + str(r['status']))
        secho('Groups:   \t' + str(initial_group))
        if initial_group != 'None':
            self.display_groups(r['groups'])
        secho('')
        secho('Followers:\t' + str(r['followers']))
        secho('Following:\t' + str(r['following']))
        secho('')

    def follow_user(self, username):
        r = self.post('user/follow/' + username + '/', data={})
        self.check_reponse(r, success='Successfully followed user ' + username, error='Unable to follow user ' + username + '.')

    def unfollow_user(self, username):
        r = self.post('user/unfollow/' + username + '/', data={})
        self.check_reponse(r, success='Successfully unfollowed user ' + username, error='Unable to cancel follow for user ' + username + '. Are you really following this user?')


usermanagement = UserService()