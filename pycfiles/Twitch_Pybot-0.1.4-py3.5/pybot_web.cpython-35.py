# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/web/pybot_web.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 5915 bytes
import tornado.ioloop, tornado.web, tornado.websocket, tornado.escape, os, pybot.web.uimodules as uimodules, random
from pybot.data import *
import pybot.globals as globals, threading

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        title = 'Pybot'
        self.render('templates/index.html', title=title)


class SocketHandler(tornado.websocket.WebSocketHandler):

    def on_message(self, message):
        split = ''
        delim = '---!---'
        for msg in globals.data.logs:
            split += msg + delim

        self.write_message(split)

    def check_origin(self, origin):
        return True


class BotHandler(tornado.web.RequestHandler):

    def get(self, command):
        if command == 'rejoin':
            threading.Thread(target=globals.con.retry).start()
        elif command == 'leave':
            globals.con.close()
        self.redirect('/hub')


class RaffleHandler(tornado.web.RequestHandler):

    def get(self, action):
        split = action.split('/')
        data = globals.data
        if len(split) >= 2:
            act = split[0]
            raff = split[1]
            if act == 'select':
                raffle = data.getRaffle(raff)
                if raffle != False:
                    winner = raffle.users[random.randint(0, len(raffle.users) - 1)]
                    self.render('templates/raffle.html', message='The winner is: ' + winner)
                else:
                    self.render('templates/raffle.html', message='Raffle ' + raff + ' doesnt exist :(')
        else:
            if act == 'cancel':
                raffle = data.getRaffle(raff)
                if raffle != False:
                    data.raffles.remove(raffle)
                    self.render('templates/raffle.html', message='Raffle ' + raff + ' removed')
            else:
                self.render('templates/raffle.html', message='Raffle ' + raff + ' doesnt exist :(')


class FilterHandler(tornado.web.RequestHandler):

    def get(self, action):
        split = action.split('/')
        data = globals.data
        if len(split) >= 2:
            act = split[0]
            filter = split[1]
            if act == 'disable':
                globals.settings.removeFilter(filter)
                self.redirect('/hub/filters')
        elif act == 'enable':
            globals.settings.addFilter(filter)
            self.redirect('/hub/filters')

    def post(self, args):
        filter = tornado.escape.to_basestring(self.request.arguments['addfilter'][0])
        globals.settings.addFilter(filter)
        self.redirect('/hub/filters')


class LinkHandler(tornado.web.RequestHandler):

    def get(self, action):
        split = action.split('/')
        data = globals.data
        if len(split) >= 1:
            act = split[0]
            if act == 'remove':
                user = split[1]
                del globals.data.links[user]
                self.redirect('/hub/links')
            elif act == 'random':
                if len(data.links) > 0:
                    globals.data.currentRandomLink = data.links[random.sample(list(data.links), 1)[0]]
                self.redirect('/hub/links')
        elif act == 'removeall':
            data.links.clear()
            self.redirect('/hub/links')


class HubHandler(tornado.web.RequestHandler):

    def get(self, page):
        data = globals.data
        settings = globals.settings
        self.render('templates/hub.html', data=data, settings=settings, page=page)

    def post(self, page):
        data = globals.data
        settings = globals.settings
        if page == 'settings':
            config = settings.getConf()
            for arg in self.request.arguments.keys():
                split = arg.split('.')
                config.set(split[0], split[1], tornado.escape.to_basestring(self.request.arguments[arg][0]))

            settings.saveConf(config)
            self.render('templates/hub.html', data=data, settings=settings, page=page)
        if page == 'links':
            inputFilter = self.get_argument('inputFilter', '')
            if inputFilter:
                settings.config['linkgrabber']['filter'] = inputFilter
                settings.saveConf()
            self.redirect('/hub/links')


class SettingsHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('Settings test')


def make_app():
    settings = {'static_path': os.path.dirname(__file__), 
     'ui_modules': uimodules}
    return tornado.web.Application([
     (
      '/', MainHandler),
     (
      '/settings', SettingsHandler),
     (
      '/hub/?(.*)', HubHandler),
     (
      '/bot/(.*)', BotHandler),
     (
      '/websocket', SocketHandler),
     (
      '/raffle/(.*)', RaffleHandler),
     (
      '/filters/(.*)', FilterHandler),
     (
      '/links/(.*)', LinkHandler)], **settings)


class pybot_web:

    def __init__(self, con):
        self.settings = globals.settings

    def startWebService(self):
        print('[pybot.tornado.web] Web services starting on port ' + str(globals.settings.config['web']['port']))
        app = make_app()
        app.listen(int(globals.settings.config['web']['port']))
        tornado.ioloop.IOLoop.current().start()