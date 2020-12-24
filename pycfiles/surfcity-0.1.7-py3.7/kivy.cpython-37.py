# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/surfcity/ui/kivy.py
# Compiled at: 2019-04-03 12:54:38
# Size of source mod 2**32: 16570 bytes
import asyncio, kivy
kivy.require('1.10.0')
import logging, threading, traceback
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.scrollview import ScrollView
CONST_start_size = (350, 600)
the_loop = asyncio.get_event_loop()
quit_flag = False
app = None
import surfcity.app.db as db
import surfcity.app.net as net
the_public = None
Builder.load_string('\n<PublicScreen>:\n    id: publ\n    threads: threads\n    BoxLayout:\n        orientation: \'vertical\'\n        BoxLayout:\n            size_hint: 1,None\n            # size: (self.size[0], 90)\n            # size_hint_y : 0.07\n            height: 80\n            RoundedButtonRed:\n                text: \'Public\'\n            RoundedButtonWhite:\n                text: \'Private\'\n                on_press: root.goto(\'private\')\n            RoundedButtonWhite:\n                text: \'Menu\'\n                on_press: root.goto(\'menu\')\n        Label:\n            size_hint: 1,None\n            text_size: (self.size[0], None)\n            height: 60\n            # size: (self.size[0]-10, 50)\n            # size_hint_y : 0.03\n            padding: (20,0)\n            canvas.before:\n                Color:\n                    rgba: .8,.2,.2,1\n                Rectangle:\n                    pos: self.pos\n                    size: self.size\n            color: 0,0,0,1\n            text: \'List of public threads\'\n            \n        ScrollView:\n            id: threads\n            # gl: gl\n            # size_hint: 1,1\n            bar_width: 40\n            effect_cls: "ScrollEffect"\n            scroll_type: [\'bars\']\n            background_normal: \'\'\n            background_color: (.8,.8,.8,1)\n            GridLayout:\n                size_hint_y: None\n                # height: self.minimum_height\n                id: glayout\n                cols: 1\n                spacing: 10\n                canvas.before:\n                    Color:\n                        rgba: .8,.8,.8,1\n                    Rectangle:\n                        pos: self.pos\n                        size: self.size\n\n\n#        RecycleView:\n#            row_controller: row_controller\n#            bar_width: 20\n#            effect_cls: "ScrollEffect"\n#            scroll_type: [\'bars\']\n#            id: rv\n#            viewclass: \'MyThreadListEntry\'\n#            RecycleBoxLayout:\n#                id: row_controller\n#                default_size_hint: 1, None\n#                size_hint: 1, None\n#                height: self.minimum_height\n#                orientation: \'vertical\'\n\n<PrivateScreen>:\n    id: priv\n    BoxLayout:\n        orientation: \'vertical\'\n        BoxLayout:\n            size_hint_y : 0.07\n            RoundedButtonWhite:\n                text: \'Public\'\n                on_press: root.goto(\'public\')\n            RoundedButtonGreen:\n                text: \'Private\'\n            RoundedButtonWhite:\n                text: \'Menu\'\n                on_press: root.goto(\'menu\')\n        BoxLayout:\n            Label:\n                size_hint: 1, 1\n                color: 1,0,0,1\n                text: \'something\'\n                canvas.before:\n                    Color:\n                        rgba: 1,1,1,1\n                    Rectangle:\n                        pos: self.pos\n                        size: self.size\n\n<MenuScreen>:\n    id: menu\n    BoxLayout:\n        orientation: \'vertical\'\n        BoxLayout:\n            size_hint_y : 0.07\n            RoundedButtonWhite:\n                text: \'Public\'\n                on_press: root.goto(\'public\')\n            RoundedButtonWhite:\n                text: \'Private\'\n                on_press: root.goto(\'private\')\n            RoundedButtonOrange:\n                text: \'Menu\'\n        BoxLayout:\n            Label:\n                size_hint: 1, 1\n                color: 1,0,0,1\n                text: \'something\'\n                canvas.before:\n                    Color:\n                        rgba: 1,1,1,1\n                    Rectangle:\n                        pos: self.pos\n                        size: self.size\n\n\n<MyThreadListEntry@GridLayout>:\n    size_hint_y: None\n    cols: 1\n    spacing: 0\n    background_normal: \'\'\n    # background_color: (.7,.7,.9,1) if self.ind%2==0 else (.9,.7,.7,1)\n    # on_release:\n    #     root.print_data(self.ind)\n    #     root.print_data(self.pos)\n    #     root.dump_tree()\n\n\n<Subject@Label>\n    size_hint_y: None\n    font_name: \'Arial Bold\'\n    font_size: \'14sp\'\n    height: 30 # int(1.2*self.texture_size[1])\n    # background_normal: \'\'\n    # background_color: (.7,.7,.9,1)\n    bcolor: (1,1,1,1)\n    padding: (20,0)\n    # size: (self.size[0],20)\n    # pos: self.pos\n    text_size: (self.width, None)\n    color: (1,0,0,1)\n\n<Synopsis@Label>\n    size_hint : 1,None\n    font_name: \'Arial\'\n    font_size: \'12sp\'\n    height: 30 # int(1.2*self.texture_size[1])\n    # background_normal: \'\'\n    # background_color: (.9,.7,.7,1)\n    bcolor: (1,1,1,1)\n    padding: (20,0)\n    # size: (self.parent.size[0],20)\n    # pos: self.pos\n    text_size: (self.width, None)\n    color: (0,1,0,1)\n\n<RoundedButtonRed@Button>:\n    background_color: 0,0,0,0  # the last zero is the critical on, make invisible\n    canvas.before:\n        Color:\n            rgba: (.8,.2,.2,1) if self.state==\'normal\' else (0,.7,.7,1)  # visual feedback of press\n        RoundedRectangle:\n            pos: (self.pos[0]+5, self.pos[1] - 10)\n            size: (self.size[0]-10, self.size[1])\n            radius: [10,]\n\n<RoundedButtonGreen@Button>:\n    background_color: 0,0,0,0  # the last zero is the critical on, make invisible\n    canvas.before:\n        Color:\n            rgba: (.2,.7,.4,1) if self.state==\'normal\' else (0,.7,.7,1)  # visual feedback of press\n        RoundedRectangle:\n            pos: (self.pos[0]+5, self.pos[1] - 10)\n            size: (self.size[0]-10, self.size[1])\n            radius: [10,]\n\n<RoundedButtonOrange@Button>:\n    background_color: 0,0,0,0  # the last zero is the critical on, make invisible\n    canvas.before:\n        Color:\n            rgba: (.7,.5,0,1) if self.state==\'normal\' else (0,.7,.7,1)  # visual feedback of press\n        RoundedRectangle:\n            pos: (self.pos[0]+5, self.pos[1] - 10)\n            size: (self.size[0]-10, self.size[1])\n            radius: [10,]\n\n<RoundedButtonWhite@Button>:\n    background_color: 0,0,0,0  # the last zero is the critical on, make invisible\n    canvas.before:\n        Color:\n            rgba: (.8,.8,.8,1) if self.state==\'normal\' else (0,.7,.7,1)  # visual feedback of press\n        RoundedRectangle:\n            pos: (self.pos[0]+5, self.pos[1] - 10)\n            size: (self.size[0]-10, self.size[1])\n            radius: [10,]\n\n<ScrollableLabel>:\n    GridLayout:\n        cols: 1\n        size_hint_y: None\n        height: self.minimum_height\n        canvas:\n            Color:\n                rgba: (1, 0, 0, .5) # DarkOliveGreen\n            Rectangle:\n                size: self.size\n                pos: self.pos\n        Label:\n            id: bust\n            text: \'a string that is long \' * 10\n            font_size: 50\n            text_size: self.width, None\n            size_hint_y: None\n            height: self.texture_size[1]\n            canvas:\n                Color:\n                    rgba: (0, 1, 0, .5) # DarkOliveGreen\n                Rectangle:\n                    size: self.size\n                    pos: self.pos\n        Label:\n            text: \'2 strings that are long \' * 10\n            text_size: self.width, None\n            size_hint_y: None\n            height: self.texture_size[1]\n        Button:\n            text: \'just testing\'\n')

class PublicScreen(Screen):

    def __init__(self, **kwargs):
        (super(PublicScreen, self).__init__)(**kwargs)

    def goto(self, dest):
        self.manager.current = dest


class PrivateScreen(Screen):

    def __init__(self, **kwargs):
        (super(PrivateScreen, self).__init__)(**kwargs)

    def goto(self, dest):
        self.manager.current = dest


class MenuScreen(Screen):

    def __init__(self, **kwargs):
        (super(MenuScreen, self).__init__)(**kwargs)

    def goto(self, dest):
        self.manager.current = dest


class Subject(Label):
    pass


class Synopsis(Label):
    pass


class MyThreadListEntry(GridLayout):
    ind = NumericProperty(0)

    def print_data(self, data):
        print(self.ind, data)

    def dump_tree(self):
        tree(0, self)


def mk_threadListEntry(ind, t, txt):
    m = GridLayout(cols=1, size_hint_y=None, spacing=0)
    m.bind(minimum_height=(m.setter('height')))
    m.ind = NumericProperty()
    m.ind = ind
    m.thread = ObjectProperty()
    m.thread = t
    l = Button(text=(txt[0][1]), size_hint_y=None, height=45, padding=(10, 10), font_size='28',
      font_name='Arial bold',
      background_normal='',
      background_down='',
      background_color=((0.7, 0.7, 0.9, 1) if ind % 2 == 0 else (0.9, 0.7, 0.7, 1)),
      color=(0, 0, 0, 1),
      text_size=(700, 50),
      shorten=True,
      shorten_from='right')
    l.bind(on_release=(lambda x: print(x.parent.ind)))
    m.add_widget(l)
    g = GridLayout(cols=3, size_hint=(1, None), spacing=0, row_default_height=40)
    g.bind(minimum_height=(g.setter('height')))
    m.add_widget(g)
    for ln in txt[1:]:
        l = Button(text=(' ' + ln[1]), size_hint_x=None, font_size='24',
          background_normal='',
          background_down='',
          background_color=((0.7, 0.7, 0.9, 1) if ind % 2 == 0 else (0.9, 0.7, 0.7,
                                                                     1)),
          color=(0, 0, 0, 1),
          halign='left',
          text_size=(120, None),
          width=140,
          shorten=True,
          shorten_from='right')
        l.bind(on_release=(lambda x: print(x.parent.parent.ind)))
        g.add_widget(l)
        l = Button(text=(ln[2]), size_hint_x=None, padding_x=5, font_size='24',
          font_name='Arial italic',
          background_normal='',
          background_down='',
          background_color=((0.7, 0.7, 0.9, 1) if ind % 2 == 0 else (0.9, 0.7, 0.7,
                                                                     1)),
          color=(0, 0, 0, 1),
          halign='left',
          text_size=(430, None),
          width=430,
          shorten=True,
          shorten_from='right')
        l.bind(on_release=(lambda x: print(x.parent.parent.ind)))
        g.add_widget(l)
        l = Button(text=(' ' + ln[0]), size_hint_x=None, font_size='20',
          background_normal='',
          background_down='',
          background_color=((0.7, 0.7, 0.9, 1) if ind % 2 == 0 else (0.9, 0.7, 0.7,
                                                                     1)),
          color=(0, 0, 0, 1),
          halign='left',
          text_size=(130, None),
          width=130,
          shorten=True,
          shorten_from='right')
        l.bind(on_release=(lambda x: print(x.parent.parent.ind)))
        g.add_widget(l)

    return m


def tree(lvl, node):
    print(' ' * (2 * lvl), node)
    print(' ' * (2 * lvl), f"- pos={node.pos} size={node.size}")
    if type(node) is Label or type(node) is Synopsis or type(node) is Subject:
        print(' ' * (2 * lvl), f"- text={node.text}")
    lvl += 1
    for c in node.children:
        tree(lvl, c)


async def main(sca, secr, args):
    global app
    global quit_flag
    global the_public
    try:
        app.the_db.open(args.db, secr.id)
        host = args.pub.split(':')
        port = 8008 if len(host) < 2 else int(host[1])
        pubID = secr.id if len(host) < 3 else host[2]
        host = host[0]
        if not args.offline:
            net.init(secr.id, None)
            try:
                api = await net.connect(host, port, pubID, secr.keypair)
            except Exception as e:
                try:
                    error_message = str(e)
                    logger.info('exc while connecting')
                    raise e
                finally:
                    e = None
                    del e

            print('connected, scanning will start soon ...')
            asyncio.ensure_future(api)
            await app.scan_my_log(secr, args, print)
        lst = app.mk_thread_list(secr, args, cache_only=(args.offline), extended_network=(not args.narrow))
        items = []
        i = 0
        the_public.ids.glayout.bind(minimum_height=(the_public.ids.glayout.setter('height')))
        the_public.ids.glayout.add_widget(Label(text='-- newest thread --', height=40,
          size_hint_y=None,
          color=(0, 0, 0, 1)))
        for t in lst[:50]:
            _, txt, _ = await app.expand_thread(secr, t, args, True, ascii=True)
            m = mk_threadListEntry(i, t, txt)
            the_public.ids.glayout.add_widget(m)
            i += 1

        the_public.ids.glayout.add_widget(Label(text='-- oldest thread --', height=40,
          size_hint_y=None,
          color=(0, 0, 0, 1)))
        print('---')
        while not quit_flag:
            print('scuttler')
            await asyncio.sleep(1)

    except:
        traceback.print_exc()

    app.the_db.close()
    the_loop.stop()
    sca.end()


class SurfCityApp(App):

    def build(self):
        global the_public
        self.x = threading.Thread(target=(the_loop.run_forever))
        asyncio.set_event_loop(the_loop)
        sm = ScreenManager()
        the_public = PublicScreen(name='public')
        sm.add_widget(the_public)
        sm.add_widget(PrivateScreen(name='private'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.transition = NoTransition()
        Window.size = CONST_start_size
        self.title = 'SurfCity - a log-less SSB client'
        asyncio.ensure_future(main(self, self.secr, self.args))
        self.x.start()
        return sm

    def stop(self):
        global quit_flag
        quit_flag = True
        self.end()

    def end(self):
        super(SurfCityApp, self).stop()


def launch(app_core, secr, args):
    global app
    app = app_core
    try:
        try:
            sc = SurfCityApp()
            sc.secr = secr
            sc.args = args
            sc.run()
        except KeyboardInterrupt:
            pass

    finally:
        sc.stop()