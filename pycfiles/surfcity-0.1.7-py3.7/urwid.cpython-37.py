# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/surfcity/ui/urwid.py
# Compiled at: 2019-04-08 04:32:47
# Size of source mod 2**32: 60680 bytes
import asyncio
from asyncio import get_event_loop, ensure_future
import base64, copy, hashlib, json, logging, os, random, re, sys, time, traceback, urwid
app = None
import surfcity.app.net as net
import surfcity.app.db as db
logger = logging.getLogger('surfcity_ui_urwid')
ui_descr = ' (urwid ui, v2019-04-06)'
the_loop = None
back_stack = []
urwid_counter = None
urwid_title = None
urwid_footer = None
urwid_frame = None
urwid_threadList = None
urwid_convoList = None
urwid_msgList = None
urwid_privMsgList = None
urwid_userList = None
screen_size = None
widgets4convoList = []
widgets4threadList = []
refresh_focus = None
refresh_focus_pos = 0
show_extended_network = False
error_message = None
arrow_up = [
 'up', 'k']
arrow_down = ['down', 'j']
arrow_left = ['left', '<', 'h']
arrow_right = ['enter', 'right', '>', 'l']
arrow_pg_up = ['-']
arrow_pg_down = [' ']
key_quit = ['q', 'Q']
draft_text = None
draft_private_text = None
draft_private_recpts = []
vacuum_intervall = 604800

def activate_threadList(secr, clear_focus=False):
    global refresh_focus
    global refresh_focus_pos
    global show_extended_network
    global urwid_frame
    global urwid_threadList
    global widgets4threadList
    wl = copy.copy(widgets4threadList)
    urwid_threadList = urwid.AttrMap(ThreadListBox(secr, wl, show_extended_network), 'fill')
    if clear_focus:
        refresh_focus = None
        refresh_focus_pos = 0
    else:
        if len(wl) > 0:
            i = 0
            for w in wl:
                if w.key == refresh_focus:
                    break
                i += 1

            if i >= len(wl):
                i = 0
            urwid_threadList._original_widget.set_focus(i)
    urwid_frame.contents['body'] = (
     urwid_threadList, None)
    output_log('')


def activate_convoList(secr, clearFocus=False):
    global refresh_focus
    global refresh_focus_pos
    global urwid_convoList
    global widgets4convoList
    wl = copy.copy(widgets4convoList)
    urwid_convoList = urwid.AttrMap(PrivateConvoListBox(secr, wl), 'fill')
    if clearFocus:
        refresh_focus = None
        refresh_focus_pos = 0
    else:
        if len(wl) > 0:
            i = 0
            for w in wl:
                if w.key == refresh_focus:
                    break
                i += 1

            if i >= len(wl):
                i = refresh_focus_pos
            urwid_convoList._original_widget.set_focus(i)
    urwid_frame.contents['body'] = (
     urwid_convoList, None)
    output_log('')


def activate_help(old_focus=None):
    global back_stack
    global urwid_helpList
    urwid_helpList = urwid.AttrMap(HelpListBox(old_focus), 'fill')
    urwid_frame.contents['body'] = (urwid_helpList, None)
    output_log('')
    back_stack.append(old_focus)


def activate_user(old_focus=None):
    global urwid_userList
    urwid_userList = urwid.AttrMap(UserListBox(old_focus), 'fill')
    urwid_frame.contents['body'] = (urwid_userList, None)
    output_log('')
    back_stack.append(old_focus)


async def construct_threadList(secr, args, cache_only=False, extended_network=False):
    global app
    widgets = []
    lst = app.mk_thread_list(secr, args, cache_only=cache_only, extended_network=extended_network)
    blocked = app.the_db.get_following(secr.id, 2)
    odd = True
    logger.info(str(lst))
    for t in lst:
        logger.info(f"thread {t}")
        msgs, txt, _ = await app.expand_thread(secr, t, args, cache_only, blocked)
        logger.info(str(msgs))
        logger.info(str(txt))
        widgets.append(ThreadEntry(t, msgs, txt, 'odd' if odd else 'even'))
        odd = not odd

    return widgets


async def construct_convoList(secr, args, cache_only=False):
    widgets = []
    convos = await app.mk_convo_list(secr, args, cache_only)
    odd = True
    for c in convos:
        msgs, txt, new_count = await app.expand_convo(secr, c, args, cache_only)
        widgets.append(ConvoEntry(c, msgs, txt, new_count, 'odd' if odd else 'even'))
        odd = not odd

    return widgets


async def main(secr, args):
    global draft_private_recpts
    global draft_private_text
    global draft_text
    global error_message
    global widgets4convoList
    global widgets4threadList
    draft_text = app.the_db.get_config('draft_post')
    priv = app.the_db.get_config('draft_private_post')
    if priv != None:
        try:
            priv = json.loads(priv)
            draft_private_text, draft_private_recpts = priv
        except:
            pass

    try:
        last_vacuum = app.the_db.get_config('last_vacuum')
        now = int(time.time())
        if not last_vacuum or int(last_vacuum) + vacuum_intervall < now:
            logger.info('removing old posts and compacting database')
            app.the_db.forget_posts(app.frontier_window)
            app.the_db.set_config('last_vacuum', now)
            logger.info('database vacuumed')
    except Exception as e:
        try:
            logger.info(f"*** {str(e)}")
            logger.info(traceback.format_exc())
        finally:
            e = None
            del e

    try:
        host = args.pub.split(':')
        port = 8008 if len(host) < 2 else int(host[1])
        pubID = secr.id if len(host) < 3 else host[2]
        host = host[0]
        send_queue = args.offline or asyncio.Queue(loop=(asyncio.get_event_loop()))
        net.init(secr.id, send_queue)
        try:
            api = await net.connect(host, port, pubID, secr.keypair)
            output_log('connected, scanning will start soon ...')
        except OSError as e:
            try:
                error_message = str(e)
                logger.exception('exc while connecting')
                raise urwid.ExitMainLoop()
                return
            finally:
                e = None
                del e

        except Exception as e:
            try:
                error_message = str(e)
                logger.exception('exc while connecting')
                return
            finally:
                e = None
                del e

        output_log('connected, scanning will start soon ...')
        ensure_future(api)
        await app.scan_my_log(secr, args, output_log, output_counter)
        if not args.noextend:
            await app.process_new_friends(secr, output_log, output_counter)
        widgets4threadList = await construct_threadList(secr, args, cache_only=True)
        activate_threadList(secr)
        widgets4convoList = await construct_convoList(secr, args)
        while 1:
            if not args.offline:
                logger.info(f"surfcity {str(time.ctime())} before wavefront")
                await app.scan_wavefront(secr.id, secr, args, output_log, output_counter)
                logger.info(f"surfcity {str(time.ctime())} after wavefront")
            if app.refresh_requested:
                if urwid_frame.contents['body'][0] == urwid_threadList:
                    output_log('Preparing public content list...')
                    widgets4threadList = await construct_threadList(secr, args, extended_network=show_extended_network)
                    activate_threadList(secr)
                    widgets4convoList = await construct_convoList(secr, args)
                else:
                    if urwid_frame.contents['body'][0] == urwid_convoList:
                        output_log('Preparing private content list...')
                        widgets4convoList = await construct_convoList(secr, args)
                        activate_convoList(secr)
                        widgets4threadList = await construct_threadList(secr, args, extended_network=show_extended_network)
                    app.refresh_requested = False
                    app.counter_reset(output_counter)
            else:
                if urwid_frame.contents['body'][0] == urwid_threadList:
                    widgets4convoList = await construct_convoList(secr, args)
                else:
                    if urwid_frame.contents['body'][0] == urwid_convoList:
                        widgets4threadList = await construct_threadList(secr, args)
                    if app.new_friends_flag:
                        await app.process_new_friends(secr, output_log, output_counter)
                        app.new_friends_flag = False
                    if not args.offline:
                        if urwid_frame.contents['body'][0] == urwid_threadList or urwid_frame.contents['body'][0] == urwid_convoList:
                            if app.new_back + app.new_forw > 0:
                                output_log("Type '!' to refresh screen")
                    else:
                        output_log('')
                    logger.info('%s', f"surfcity {str(time.ctime())} before sleeping")
                    for i in range(50):
                        await asyncio.sleep(0.1)
                        if app.refresh_requested:
                            break

    except Exception as e:
        try:
            logger.info('exception in main()')
            if not error_message:
                s = traceback.format_exc()
                logger.error(s)
                print(s)
                output_log(f"Exception: {str(e)}\n{s}\n\nuse CTRL-C to terminate")
                error_message = str(e)
            else:
                raise urwid.ExitMainLoop()
        finally:
            e = None
            del e


def output_log(txt='', end=None, flush=None):
    global urwid_footer
    if len(txt) > 0:
        if txt[0] == '\r':
            txt = txt[1:]
    if len(txt) > 0:
        if txt[(-1)] == '\r':
            txt = txt[:-1]
    urwid_footer.set_text(txt)


def start_menu():
    global urwid_msgList
    global urwid_privMsgList
    a = 'Q'
    b = urwid_frame.contents['body'][0]
    if b == urwid_threadList:
        a = '!CU?Q'
    else:
        if b == urwid_convoList:
            a = '!CU?Q'
        else:
            if b == urwid_msgList:
                a = 'RC?Q'
            else:
                if b == urwid_privMsgList:
                    a = 'RC?Q'
                else:
                    if b == urwid_userList:
                        a = '?Q'
    Menu(a).open()


def on_unhandled_input(ev):
    global the_loop
    screen_size = urwid.raw_display.Screen().get_cols_rows()
    if ev == 'esc':
        return start_menu()
    if type(ev) == tuple:
        if ev[0] == 'mouse press':
            if type(the_loop.widget) is Menu:
                the_loop.widget.close()
                return
                if ev[3] < 3:
                    if screen_size[0] - ev[2] < 16:
                        start_menu()
            elif len(back_stack) > 0:
                set_frame(back_stack[(-1)])
            else:
                if urwid_frame.contents['body'][0] in [urwid_threadList,
                 urwid_convoList]:
                    urwid_frame.keypress(screen_size, 'p')
        else:
            if ev[3] == screen_size[1] - 1:
                if screen_size[0] - ev[2] < 16:
                    if type(urwid_frame.contents['body'][0]) is HelpListBox:
                        activate_help(urwid_frame.contents['body'][0])
            return
    output_log(f"unhandled event: {str(ev)}")


def output_counter():
    global urwid_counter
    urwid_counter.set_text(f"  FWD={app.new_forw} BWD={app.new_back} ")


def mouse_scroll(obj, size, button):
    if button == 4:
        return obj.keypress(size, 'up')
    if button == 5:
        return obj.keypress(size, 'down')
    return False


def smooth_scroll(obj, size, key):
    lw = obj.body
    if key in arrow_up:
        pos = lw.get_focus()[1]
        try:
            p = lw.get_prev(pos)[1]
            lw.set_focus(p)
            obj.shift_focus(size, 5)
        except:
            pass

        return True
    if key in arrow_down:
        pos = lw.get_focus()[1]
        n = lw.get_next(pos)[1]
        if n:
            lw.set_focus(n)
            obj.shift_focus(size, size[1] - 10)
        return True
    return False


def list_mouse_event(obj, size, event, button, col, row, focus):
    if mouse_scroll(obj, size, button) == True:
        return True
    if event == 'mouse press':
        obj._mouse_down = (
         col, row)
        return True
    if event != 'mouse release' or (col, row) != obj._mouse_down:
        obj._mouse_down = (-1, -1)
        return True
    maxcol, maxrow = size
    middle, top, bottom = obj.calculate_visible((maxcol, maxrow), focus=True)
    if middle is None:
        return False
    _ignore, focus_widget, focus_pos, focus_rows, cursor = middle
    trim_top, fill_above = top
    _ignore, fill_below = bottom
    fill_above.reverse()
    w_list = fill_above + [(focus_widget, focus_pos, focus_rows)] + fill_below
    wrow = -trim_top
    for w, w_pos, w_rows in w_list:
        if wrow + w_rows > row:
            break
        wrow += w_rows
    else:
        return False

    obj.set_focus(w_pos)
    obj.keypress(size, 'enter')
    return True


help = [
 "Welcome to SurfCity\n\nBelow you find a table with the keyboard bindings followed\nby a description of SurfCity's philosophy and an explanation\nof the command line options.\n\nYou can leave this screen by typing '<' or left-arrow.\n\nEnjoy!\n\nSanta Cruz, Feb 2019\n  ssb:   @AiBJDta+4boyh2USNGwIagH/wKjeruTcDX2Aj1r/haM=.ed25519\n  email: <christian.tschudin@unibas.ch>",
 'Keyboard bindings:\n\n?                      this help screen\nq                      quit\nESC                    open menu / exit a popup window\n\n!                      refresh Private or Public screen\np                      toggle between Private and Public screen\ne                      toggle extended network (when in Public screen)\n\nu                      simple user directory\n\nc                      compose new message\nr                      reply in a thread\n\n>, l, rght-arrow, ret  enter detail page\n<, h, left-arrow       leave detail page\ndown/up-arrow, j/k     move upwards/downwards in the list\npage-down, page-up     scroll through the list',
 "Mouse support:\n\nThe mouse can be used to scroll up and down in the list and text\npanels. In the list of public threads, as well as the list of private\nconversations, entries can be clicked on in order to expand them.\n\nClicking in the UPPER LEFT corner is equivalent to either 'back' or\nfor toggling between public threads and private conversations.\n\nClicking in the UPPER RIGHT corner opens a menu with clickable\noptions for trigger a refresh, do a reply, etc without having to\ntype any key.",
 'About SurfCity\n\nSecure Scuttlebutt (SSB) brings to you a deluge of information,\nall appended to the message logs of the respective authors:\n\n     SurfCity is the tool to ride this wavefront.\n\nIt does so (a) in forward as well as (b) in backward direction\nand (c) widens its scan range dynamically, but WITHOUT having\nto store all the participants\' huge log files.\n\nTypically, the storage footprint of SurfCity is in the range of tens\nof MBytes, while a full SSB client easily requires several hundreds of\nMegaBytes of disk storage. Also, when booting freshly into SurfCity,\nyou will immediately have messages to display: no need to wait for\nlong download times and indexing pauses.  In that sense SurfCity is\nsustainable, riding the wave with roughly constant storage space - at\nleast if YOU behave sustainably, e.g. block or un-follow peers if the\nlist becomes too large ;-)\n\nWhat does "riding the wavefront" mean?\n\na) By this we mean that SurfCity\'s most important task is to\nscan the Scuttleverse for new content in the forward direction.\nSurfCity will process these fresh messages and store them for a\nfew weeks only. It will also take note of a discussion thread\'s\nfirst post and keep this information around for a few months\nso it can later display the thread\'s "title". Finally, SurfCity\nkeeps track of the SSB crypto peer identifiers and the human-\nreadable names that have been assigned to them.\n\nb) SurfCity is also able to scan content in backwards direction.\nFrom these "historic" messages, SurfCity collects essential\ninformation e.g. the name that a peer has assigned to him/herself,\nor the other peers that a peer follows or blocks. Eventually this\nbackground scan bottoms out when the logs of all followed peers\nhave been scanned entirely.\n\nc) Finally, the breadth of the wavefront is enlarged as SurfCity\nlearns about whom you are following. In this case, these peers\nare added to your "following list" and are also scanned. This is\npart of the SSB concept that messages sent by a peer are only\naccessible in that peer\'s log, hence the need to scan it. The\nwidth of the wavefront is even larger than this, as the followed\npeers of a followed peer (FOAF, "friends of a friend") are also\nscanned. SurfCity scans these FOAF peers less frequently by\nrandomly picking some of them, in each round. But it\'s all\nfine because SSB is based on eventual concistency, and random\nselection will eventually lead SurfCity to visit every peer\nwithin the wavefront\'s current breadth.\n\nPrototype and Future Work\n\nBeware, this is experimental software! Its main purpose is to\nvalidate the concept of wavefront riding for SSB and to prepare\nthe ground for a SSB browser that can run on a smartphone but\ndoes not come with a huge storage requirement.\n',
 'Explanation of command-line options\n\n-offline        prevents SurfCity from doing any scans, but also\n                from downloading any message content. This means\n                that only cached messages can be displayed (at\n                most a few weeks old) and that threads look\n                less complete when activating this option.\n\n-narrow         prevents SurfCity to scan the logs of FOAF\n                (friends of a friend): Only peers that you\n                decided to follow will be considered in the\n                scans. This only affects scanning and is not\n                a censoring option: All content that SurfCity\n                already collected will be used and displayed.\n\n-nocatchup      "do not scan backwards": prevents SurfCity from\n                scanning historic messages.\n\n-noextend       "do not scan forwards": prevents SurfCity from\n                probing for new messages that extend the peers\'\n                logs.\n\nThis user interface supports four different color modes:\n\n-ui urwid       dark mode (default)\n-ui urwid_light light mode\n-ui urwid_amber monochrome, using a warm amber color on black\n-ui urwid_green monochrome, using classic green on black\n-ui urwid_mono  monochrome, using the terminal\'s default colors']

class HelpListBox(urwid.ListBox):
    _selectable = True

    def __init__(self, goback, lst=[]):
        global urwid_title
        self.goback = goback
        self.title = 'Help Text\n'
        urwid_title.set_text(self.title)
        lst = [urwid.Text('v--- H E L P ---v', 'center')]
        for h in help:
            t = urwid.AttrMap(urwid.Text(h), 'even')
            p = urwid.Pile([urwid.Text(''), t, urwid.Text('')])
            lst.append(urwid.Padding(p, left=2, right=2))

        lst.append(urwid.Text('^--- H E L P ---^', 'center'))
        sflw = urwid.SimpleFocusListWalker(lst)
        sflw.title = self.title
        super().__init__(sflw)

    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key in key_quit:
            raise urwid.ExitMainLoop()
        if key in arrow_pg_down:
            return self.keypress(size, 'page down')
        if key in arrow_pg_up:
            return self.keypress(size, 'page up')
        if key not in arrow_left:
            return key
        set_frame(self.goback)

    def mouse_event(self, size, event, button, x, y, focus):
        mouse_scroll(self, size, button)
        return True


class UserListBox(urwid.ListBox):
    _selectable = True

    def _user2line(self, feedID, isFriend=False):
        prog = '0'
        front, _ = app.the_db.get_id_front(feedID)
        if front > 0:
            low = app.the_db.get_id_low(feedID)
            if low > 0:
                prog = str((front - low + 1) * 100 // front)
        prog = f"  {prog}%"[-4:]
        n = app.feed2name(feedID)
        if not n:
            n = '?'
        fr = '* ' if isFriend else '  '
        return f"{fr}{(n + '          ')[:10]} {feedID}  {prog}"

    def _lines2widget(self, lns):
        t = urwid.AttrMap(urwid.Text('\n'.join(lns)), 'even')
        p = urwid.Pile([urwid.Text(''), t, urwid.Text('')])
        return urwid.Padding(p, left=2, right=2)

    def __init__(self, goback, lst=[]):
        self.goback = goback
        self.title = 'User Directory\n'
        urwid_title.set_text(self.title)
        lst = [urwid.Text('v--- U S E R S ---v', 'center')]
        me = app.the_db.get_config('id')
        lst.append(self._lines2widget([f"My feedID:\n\n{self._user2line(me)}\n"]))
        pubs = app.the_db.list_pubs()
        frnd = app.the_db.get_friends(me)
        fol = app.the_db.get_following(me)
        t = []
        for f in fol:
            if f in pubs:
                t.append(self._user2line(f, f in frnd))

        t.sort(key=(lambda x: x[2:].lower()))
        t = [f"Accredited pubs: {len(pubs)}\n"] + t
        if len(t) > 1:
            t.append('')
        lst.append(self._lines2widget(t))
        fol = app.the_db.get_following(me)
        t1, t2 = [], []
        for f in fol:
            if f in pubs:
                continue
            ln = self._user2line(f, f in frnd)
            if ln[2:12] == '?         ':
                t2.append(ln)
            else:
                t1.append(ln)

        t1.sort(key=(lambda x: x[2:].lower()))
        t2.sort(key=(lambda x: x[2:].lower()))
        t = [f"Followed feeds (* =friend/following back): {len(fol) - len(pubs)}\n"] + t1 + t2
        if len(t) > 1:
            t.append('')
        lst.append(self._lines2widget(t))
        folr = app.the_db.get_followers(me)
        t = []
        for f in folr:
            if f in frnd:
                continue
            t.append(self._user2line(f))

        t.sort(key=(lambda x: x[2:].lower()))
        t = [f"Follower feeds (other than friends): {len(t)}\n"] + t
        if len(t) > 1:
            t.append('')
        lst.append(self._lines2widget(t))
        blk = app.the_db.get_following(me, 2)
        t = []
        for f in blk:
            t.append(self._user2line(f))

        t.sort(key=(lambda x: x.lower()))
        if len(t) > 0:
            t.append('')
        t = [
         f"Blocked feeds: {len(blk)}\n"] + t
        lst.append(self._lines2widget(t))
        ffol = app.the_db.get_follofollowing(me)
        t = []
        for f in ffol:
            if f in fol:
                continue
            t.append(self._user2line(f))

        t.sort(key=(lambda x:         if x[2:3] == '?':
'~~~~~' + x[2:].lower() # Avoid dead code: x[2:].lower()))
        if len(t) > 0:
            t.append('')
        t = [
         f"Number of feeds followed by the feeds I follow: {len(ffol)}\n"] + t
        lst.append(self._lines2widget(t))
        lst.append(urwid.Text('^--- U S E R S ---^', 'center'))
        sflw = urwid.SimpleFocusListWalker(lst)
        sflw.title = self.title
        super().__init__(sflw)

    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key in key_quit:
            raise urwid.ExitMainLoop()
        if key in arrow_pg_down:
            return self.keypress(size, 'page down')
        if key in arrow_pg_up:
            return self.keypress(size, 'page up')
        if key in ('?', ):
            return activate_help(urwid_userList)
        if key not in arrow_left:
            return key
        set_frame(self.goback)

    def mouse_event(self, size, event, button, x, y, focus):
        mouse_scroll(self, size, button)
        return True


class ConvoEntry(urwid.AttrMap):
    _selectable = True

    def __init__(self, convo, msgs, txt, new_count, attr=None):
        self.convo = convo
        self.msgs = msgs
        self.key = self.convo
        self.star = urwid.Text('*' if new_count > 0 else ' ')
        self.count = urwid.Text(('selected',
         f"({new_count} new)" if new_count > 0 else ''), 'right')
        self.title = txt[0][1]
        m = '  (1 msg)' if len(msgs) == 1 else f"  ({len(msgs)} msgs)"
        lines = [
         urwid.Columns([urwid.Text((attr + 'Bold', (f"{self.title[:75]}")), wrap='clip'),
          (
           'pack', urwid.Text(m))])]
        for ln in txt[1:]:
            lines.append(urwid.Columns([
             (
              12, urwid.Text((ln[1][:10] + '  '), 'left', wrap='clip')),
             urwid.Text((ln[2]), 'left', wrap='clip'),
             (
              16, urwid.Text(('   ' + ln[0] + ' '), 'right', wrap='clip'))]))

        lines.append(self.count)
        pile = urwid.AttrMap(urwid.Pile(lines), attr)
        cols = urwid.Columns([(2, self.star), pile])
        super().__init__(cols, None, focus_map='selectedPrivate')


class PrivateConvoListBox(urwid.ListBox):
    _selectable = True
    _mouse_down = (-1, -1)

    def __init__(self, secr, lst=[]):
        self.secr = secr
        self.title = 'PRIVATE conversations'
        urwid_title.set_text(self.title)
        sflw = urwid.SimpleFocusListWalker(lst)
        sflw.title = self.title
        super().__init__(sflw)

    def keypress(self, size, key):
        global refresh_focus
        global refresh_focus_pos
        global urwid_privMsgList
        if smooth_scroll(self, size, key):
            return
            key = super().keypress(size, key)
            if key in key_quit:
                raise urwid.ExitMainLoop()
            if key in arrow_pg_down:
                return self.keypress(size, 'page down')
        else:
            if key in arrow_pg_up:
                return self.keypress(size, 'page up')
                if key in ('!', ):
                    app.refresh_requested = True
                    if self.focus:
                        refresh_focus = self.focus.key
                        refresh_focus_pos = self.get_focus()[1]
            else:
                refresh_focus = None
                refresh_focus_pos = 0
            return
        if key in ('p', 'p'):
            return activate_threadList(self.secr, True)
        if key in ('?', ):
            return activate_help(urwid_convoList)
        if key in ('u', 'U'):
            return activate_user(urwid_convoList)
        if key in ('c', ):
            r = RecptsDialog()
            e = EditDialog('Compose new PRIVATE message', is_private=True)
            c = ConfirmTextDialog(True)
            r.open(draft_private_recpts, lambda recpts: e.open(draft_private_text, lambda x: c.open(x, recpts, lambda : e.reopen(), lambda y: app.submit_private_post(self.secr, y, recpts))))
            return
        if key not in ('enter', '>', 'right'):
            return key
        self.focus.star.set_text('')
        self.focus.count.set_text('')
        back_stack.append(urwid_convoList)
        for t in self.focus.convo['threads']:
            app.the_db.update_thread_lastread(t)

        lst = [
         urwid.Text('---oldest---', 'center')]
        root, branch = (None, None)
        for m in self.focus.msgs:
            branch = m['key']
            root = m['content']['root'] if 'root' in m['content'] else branch
            a = m['author']
            n = app.feed2name(m['author'])
            if not n:
                n = m['author']
            n = urwid.Columns([urwid.Text(n),
             (
              13, urwid.Text(app.utc2txt(m['timestamp'])))])
            t = m['content']['text']
            t = re.sub('\\[([^\\]]*)\\]\\([^\\)]*\\)', '[\\1]', t)
            t = urwid.AttrMap(urwid.Text(t), 'even')
            r = urwid.Text(m['key'], 'right')
            p = urwid.Pile([urwid.Text(''), n, t, r, urwid.Text('')])
            lst.append(urwid.Padding(p, left=2, right=2))

        lst.append(urwid.Text('---newest---', 'center'))
        title = 'Private conversation\n' + f"with {self.focus.title[:50]}"
        urwid_privMsgList = urwid.AttrMap(PrivateMessageBox(self.secr, urwid_convoList, self.focus.convo['recps'], title, lst, root, branch), 'fill')
        urwid_privMsgList._original_widget.set_focus(len(lst) - 1)
        urwid_frame.contents['body'] = (urwid_privMsgList, None)

    def mouse_event(self, size, event, button, col, row, focus):
        return list_mouse_event(self, size, event, button, col, row, focus)


class PrivateMessageBox(urwid.ListBox):
    _selectable = True

    def __init__(self, secr, goback, recpts, title, lst=[], root=None, branch=None):
        self.secr = secr
        self.recpts = recpts
        self.goback = goback
        self.title = title
        urwid_title.set_text(title)
        self.root = root
        self.branch = branch
        sflw = urwid.SimpleFocusListWalker(lst)
        sflw.title = self.title
        super().__init__(sflw)

    def keypress(self, size, key):
        global screen_size
        screen_size = (
         size[0], size[1] + 3)
        key = super().keypress(size, key)
        if key in key_quit:
            raise urwid.ExitMainLoop()
        if key in arrow_pg_down:
            return self.keypress(size, 'page down')
        if key in arrow_pg_up:
            return self.keypress(size, 'page up')
        if key in ('?', ):
            return activate_help(urwid_privMsgList)
        if key in ('c', ):
            r = RecptsDialog()
            e = EditDialog('Compose new PRIVATE message', is_private=True)
            c = ConfirmTextDialog(True)
            r.open(draft_private_recpts, lambda recpts: e.open(draft_private_text, lambda txt: c.open(txt, recpts, lambda : e.reopen(), lambda y: app.submit_private_post(self.secr, y, recpts))))
            return
        if key in ('r', ):
            dest = self.title
            e = EditDialog(f"Compose PRIVATE reply to {dest[dest.index('<'):]}", is_private=True)
            c = ConfirmTextDialog(True)
            e.open(draft_private_text, lambda txt: c.open(txt, self.recpts, lambda : e.reopen(), lambda y: app.submit_private_post(self.secr, y, self.root, self.branch)))
            return
        if key not in arrow_left:
            return key
        set_frame(self.goback)

    def mouse_event(self, size, event, button, col, row, focus):
        mouse_scroll(self, size, button)
        return True


class ThreadEntry(urwid.AttrMap):
    _selectable = True

    def __init__(self, key, msgs, txt, attr=None):
        self.key = key
        self.msgs = msgs
        new_count = txt[0][0]
        self.star = urwid.Text('*' if new_count > 0 else ' ')
        self.count = urwid.Text(('selected',
         f"({new_count} new)" if new_count > 0 else ''), 'right')
        lines = [
         urwid.Text((attr + 'Bold', f"'{txt[0][1][:75]}'"), wrap='clip')]
        for ln in txt[1:]:
            lines.append(urwid.Columns([
             (
              12, urwid.Text((ln[1][:10] + '  '), 'left', wrap='clip')),
             urwid.Text((ln[2]), 'left', wrap='clip'),
             (
              16, urwid.Text(('   ' + ln[0] + ' '), 'right', wrap='clip'))]))

        lines.append(self.count)
        pile = urwid.AttrMap(urwid.Pile(lines), attr)
        cols = urwid.Columns([(2, self.star), pile])
        super().__init__(cols, None, focus_map='selected')


class MessageBox(urwid.ListBox):
    _selectable = True

    def __init__(self, secr, goback, title, lst=[], root=None, branch=None):
        self.secr = secr
        self.goback = goback
        self.title = title
        urwid_title.set_text(title[:screen_size[0] - 1])
        self.root = root
        self.branch = branch
        sflw = urwid.SimpleFocusListWalker(lst)
        sflw.title = self.title
        super().__init__(sflw)

    def keypress(self, size, key):
        key = super().keypress(size, key)
        if key in key_quit:
            raise urwid.ExitMainLoop()
        if key in arrow_pg_down:
            return self.keypress(size, 'page down')
        if key in arrow_pg_up:
            return self.keypress(size, 'page up')
        if key in ('?', ):
            return activate_help(urwid_msgList)
        if key in ('c', 'r'):
            if key == 'c':
                e = EditDialog('Compose PUBLIC message in new thread')
                root, branch = (None, None)
            else:
                e = EditDialog('Compose PUBLIC reply in chat\n' + f"{self.title[8:50]}'")
                root, branch = self.root, self.branch
            c = ConfirmTextDialog(False)
            e.open(draft_text, lambda txt: c.open(txt, None, lambda : e.reopen(), lambda y: app.submit_public_post(self.secr, y, root, branch)))
            return
        if key not in arrow_left:
            return key
        set_frame(self.goback)

    def mouse_event(self, size, event, button, col, row, focus):
        mouse_scroll(self, size, button)
        return True


def set_frame(goback):
    back_stack.pop()
    urwid_frame.contents['body'] = (goback, None)
    urwid_title.set_text(goback._original_widget.title)


class ThreadListBox(urwid.ListBox):
    _selectable = True
    _mouse_down = (-1, -1)

    def __init__(self, secr, lst=[], show_extended_network=False):
        self.secr = secr
        self.title = 'PUBLIC chats (extended network)' if show_extended_network else 'PUBLIC chats (with or from people I follow)'
        urwid_title.set_text(self.title)
        sflw = urwid.SimpleFocusListWalker(lst)
        sflw.title = self.title
        super().__init__(sflw)

    def keypress(self, size, key):
        global refresh_focus
        global refresh_focus_pos
        global screen_size
        global show_extended_network
        global urwid_msgList
        screen_size = (
         size[0], size[1] + 3)
        if smooth_scroll(self, size, key):
            return
        key = super().keypress(size, key)
        if key in key_quit:
            raise urwid.ExitMainLoop()
        if key in arrow_pg_down:
            return self.keypress(size, 'page down')
        if key in arrow_pg_up:
            return self.keypress(size, 'page up')
        if key in ('e', 'E'):
            show_extended_network = not show_extended_network
            key = '!'
        elif key in ('!', ):
            app.refresh_requested = True
            if self.focus:
                refresh_focus = self.focus.key
                refresh_focus_pos = self.get_focus()[1]
            else:
                refresh_focus = None
                refresh_focus_pos = 0
            return
            if key in ('?', ):
                return activate_help(urwid_threadList)
            if key in ('u', 'U'):
                return activate_user(urwid_threadList)
            if key in ('p', 'P'):
                return activate_convoList(self.secr, True)
            if key in ('c', ):
                e = EditDialog('Compose PUBLIC message in new thread')
                c = ConfirmTextDialog(False)
                e.open(draft_text, lambda txt: c.open(txt, None, lambda : e.reopen(), lambda y: app.submit_public_post(self.secr, y)))
                return
            if key not in arrow_right:
                return key
            self.focus.star.set_text('')
            self.focus.count.set_text('')
            back_stack.append(urwid_threadList)
            app.the_db.update_thread_lastread(self.focus.key)
            lst = [urwid.Text('---oldest---', 'center')]
            if len(self.focus.msgs) > 0:
                if 'root' in self.focus.msgs[0]['content']:
                    lst.append(urwid.Text('[some older messages out of reach]', 'center'))
            root, branch = (None, None)
            for m in self.focus.msgs:
                branch = m['key']
                root = m['content']['root'] if 'root' in m['content'] else branch
                a = m['author']
                n = app.feed2name(m['author'])
                if not n:
                    n = m['author']
                n = urwid.Columns([urwid.Text(n),
                 (
                  13, urwid.Text(app.utc2txt(m['timestamp'])))])
                t = m['content']['text']
                t = re.sub('\\[([^\\]]*)\\]\\([^\\)]*\\)', '[\\1]', t)
                t = urwid.AttrMap(urwid.Text(t), 'even')
                r = urwid.Text(m['key'], 'right')
                p = urwid.Pile([urwid.Text(''), n, t, r, urwid.Text('')])
                lst.append(urwid.Padding(p, left=2, right=2))

            lst.append(urwid.Text('---newest---', 'center'))
            title = app.the_db.get_thread_title(self.focus.key)
            if title:
                title = 'Public:\n' + f"'{app.text2synopsis(title)}'"
        else:
            title = 'Public:\n<unknown first post>'
        urwid_msgList = urwid.AttrMap(MessageBox(self.secr, urwid_threadList, title, lst, root, branch), 'fill')
        urwid_msgList._original_widget.set_focus(len(lst) - 1)
        urwid_frame.contents['body'] = (urwid_msgList, None)

    def mouse_event(self, size, event, button, col, row, focus):
        return list_mouse_event(self, size, event, button, col, row, focus)
        if event == 'mouse press':
            self._mouse_down = (
             col, row)
            return True
        if event != 'mouse release' or (col, row) != self._mouse_down:
            self._mouse_down = (-1, -1)
            return True
        maxcol, maxrow = size
        middle, top, bottom = self.calculate_visible((maxcol, maxrow), focus=True)
        if middle is None:
            return False
        _ignore, focus_widget, focus_pos, focus_rows, cursor = middle
        trim_top, fill_above = top
        _ignore, fill_below = bottom
        fill_above.reverse()
        w_list = fill_above + [(focus_widget, focus_pos, focus_rows)] + fill_below
        wrow = -trim_top
        for w, w_pos, w_rows in w_list:
            if wrow + w_rows > row:
                break
            wrow += w_rows
        else:
            return False

        self.set_focus(w_pos)
        self.keypress(size, 'enter')
        return True


def save_draft(txt, recpts):
    global draft_private_recpts
    global draft_private_text
    global draft_text
    if recpts != None:
        draft_private_text = txt
        draft_private_recpts = recpts
        app.the_db.set_config('draft_private_post', json.dumps((txt, recpts)))
    else:
        draft_text = txt
        app.the_db.set_config('draft_post', txt)


class EditDialog(urwid.Overlay):

    def __init__(self, bannerTxt, is_private=False):
        self.is_private = is_private
        header = urwid.Text((bannerTxt + '\n(use TAB to select buttons)'), align='center')
        self.edit = urwid.Edit(multiline=True)
        body_filler = urwid.Filler((self.edit), valign='top')
        body_padding = urwid.Padding(body_filler,
          left=1,
          right=1)
        body = urwid.LineBox(body_padding)
        w = the_loop.widget
        footer1 = urwid.AttrMap((urwid.Button('Cancel ', lambda x: self.close())),
          None,
          focus_map='selected')
        footer2 = urwid.AttrMap((urwid.Button('Preview', lambda x: self._callback())),
          None,
          focus_map='selected')
        footer = urwid.GridFlow([footer1, footer2], 11, 1, 1, 'center')
        lb = urwid.LineBox(urwid.Frame(body, header=header, footer=footer))
        super().__init__((urwid.AttrMap(lb, 'fill')), w, align='center',
          valign='middle',
          width=(screen_size[0] - 2),
          height=(screen_size[1] - 2))

    def keypress(self, size, key):
        if key in ('esc', ):
            self.close()
        if key in ('tab', 'shift tab'):
            paths = [
             [
              1, 'body'], [1, 'footer', 0], [1, 'footer', 1]]
            fp = self.get_focus_path()
            if key == 'tab':
                i = (paths.index(fp) + 1) % len(paths)
            else:
                i = (paths.index(fp) + len(paths) - 1) % len(paths)
            self.set_focus_path(paths[i])
            return
        key = super().keypress(size, key)

    def open(self, txt, ok_callback):
        if txt:
            self.edit.set_edit_text(txt)
            self.edit.set_edit_pos(len(txt))
        else:
            if self.is_private:
                if draft_private_recpts:
                    if not draft_private_text or draft_private_text == '':
                        t = ', '.join(draft_private_recpts) + '\n\n'
                        self.edit.set_edit_text(t)
                        self.edit.set_edit_pos(len(t))
        self.callback = ok_callback
        self.set_focus_path([1, 'body'])
        the_loop.widget = self

    def reopen(self):
        self.set_focus_path([1, 'body'])
        the_loop.widget = self

    def _callback(self):
        self.close()
        self.callback(self.edit.get_edit_text())

    def close(self):
        recpts = None
        if self.is_private:
            recpts = draft_private_recpts
        save_draft(self.edit.get_edit_text(), recpts)
        the_loop.widget = urwid_frame
        the_loop.draw_screen()


class ConfirmTextDialog(urwid.Overlay):

    def __init__(self, is_private=False):
        self.is_private = is_private
        txt = 'PRIVATE' if is_private else 'PUBLIC'
        header = urwid.Text(('selected',
         f" Really post this {txt} message? " + '\n(use up/down arrows to scroll, ' + 'TAB to select buttons)'),
          align='center')
        self.body_text = urwid.Text('', align='left')
        self.recpts_text = urwid.Text('', align='left')
        if self.is_private:
            lst = [
             urwid.AttrMap(self.recpts_text, 'selected'),
             urwid.Divider()]
        else:
            lst = []
        lst.append(urwid.AttrMap(self.body_text, 'even'))
        body_filler = urwid.ListBox(urwid.SimpleFocusListWalker(lst))
        body_padding = urwid.Padding(body_filler, left=1, right=1)
        body = urwid.LineBox(body_padding)
        w = the_loop.widget
        footer1 = urwid.AttrMap((urwid.Button(' back ', lambda x: self._back_callback())),
          None,
          focus_map='selected')
        footer2 = urwid.AttrMap((urwid.Button('cancel', lambda x: self.close())),
          None,
          focus_map='selected')
        footer3 = urwid.AttrMap((urwid.Button(' send!', lambda x: self._send_callback())),
          None,
          focus_map='selected')
        footer = urwid.GridFlow([footer1, footer2, footer3], 10, 1, 1, 'center')
        lb = urwid.LineBox(urwid.Frame(body, header=header, footer=footer))
        super().__init__((urwid.AttrMap(lb, 'fill')), w, align='center',
          valign='middle',
          width=(screen_size[0] - 2),
          height=(screen_size[1] - 2))

    def keypress(self, size, key):
        if key in ('esc', ):
            self.close()
        if key in ('tab', 'shift tab'):
            paths = [
             [
              1, 'body', 0], [1, 'footer', 0],
             [
              1, 'footer', 1], [1, 'footer', 2]]
            fp = self.get_focus_path()
            if fp[1] == 'body':
                fp = [
                 1, 'body', 0]
            elif key == 'tab':
                i = (paths.index(fp) + 1) % len(paths)
            else:
                i = (paths.index(fp) + len(paths) - 1) % len(paths)
            self.set_focus_path(paths[i])
            return
        key = super().keypress(size, key)

    def mouse_event(self, size, event, button, x, y, focus):
        if mouse_scroll(self, size, button):
            return True
        return super().mouse_event(size, event, button, x, y, focus)

    def open(self, text, recpts, back_callback, send_callback):
        self.back_callback = back_callback
        self.send_callback = send_callback
        r = '(#[a-zA-Z0-9\\-_\\.]+)|((\\&|%).{44}\\.sha256)|(@.{44}.ed25519)|(\\(([^\\)]+)\\)\\[[^\\]]+\\])|(\\[[^\\]]+\\]\\([^\\)]+\\))'
        all = []
        pos = 0
        for i in re.finditer(r, text):
            s = i.span()
            if s[0] > pos:
                all.append(i.string[pos:s[0]])
            else:
                m = i.string[i.start(0):i.end(0)]
                if m[0] in ('@', '%', '&'):
                    m = f"{m[:8]}.."
                else:
                    if m[0] in ('(', ):
                        m = re.match('\\(([^\\)]+)\\)\\[([^\\]]+)\\]', m)
                        m = m.group(1)
                    else:
                        if m[0] in ('[', ):
                            m = re.match('\\[([^\\]]+)\\]\\(([^\\)]+)\\)', m)
                            m = m.group(1)
            all.append(('cypherlink', m))
            pos = s[1]

        if pos < len(text):
            all.append(text[pos:len(text)])
        self.body_text.set_text(all)
        if recpts:
            lst = [
             'Recipients:']
            for r in recpts:
                nm = app.feed2name(r)
                if nm:
                    r = f"[@{nm}]({r})"
                lst.append('  ' + r)

            self.recpts_text.set_text('\n'.join(lst))
        self.set_focus_path([1, 'body'])
        the_loop.widget = self

    def _back_callback(self):
        self.close()
        self.back_callback()

    def _send_callback(self):
        logger.info('send_callback')
        self.close()
        self.send_callback(str(self.body_text.get_text()[0]))
        save_draft(None, [] if self.is_private else None)

    def close(self):
        the_loop.widget = urwid_frame
        the_loop.draw_screen()


class RecptsDialog(urwid.Overlay):

    def __init__(self):
        header = urwid.Text('Enter the recipients for a private msg, one per line\n(use TAB to select buttons)', align='center')
        self.edit = urwid.Edit(multiline=True)
        self.edit.set_edit_pos(0)
        body_filler = urwid.Filler((self.edit), valign='top')
        body_padding = urwid.Padding(body_filler, left=1, right=1)
        body = urwid.LineBox(body_padding)
        w = the_loop.widget
        footer1 = urwid.AttrMap((urwid.Button('Cancel', lambda x: self.close())),
          None,
          focus_map='selected')
        footer2 = urwid.AttrMap((urwid.Button(' Done ', lambda x: self._callback())),
          None,
          focus_map='selected')
        footer = urwid.GridFlow([footer1, footer2], 11, 1, 1, 'center')
        lb = urwid.LineBox(urwid.Frame(body, header=header, footer=footer))
        super().__init__((urwid.AttrMap(lb, 'fill')), w, align='center',
          valign='middle',
          width=(screen_size[0] - 2),
          height=(screen_size[1] - 2))

    def keypress(self, size, key):
        if key in ('esc', ):
            self.close()
        if key in ('tab', 'shift tab'):
            paths = [
             [
              1, 'body'], [1, 'footer', 0], [1, 'footer', 1]]
            fp = self.get_focus_path()
            output_log(str(fp))
            if key == 'tab':
                i = (paths.index(fp) + 1) % len(paths)
            else:
                i = (paths.index(fp) + len(paths) - 1) % len(paths)
            self.set_focus_path(paths[i])
            return
        key = super().keypress(size, key)

    def open(self, recpts, ok_callback):
        if recpts:
            self.edit.set_edit_text('\n'.join(recpts))
        self.callback = ok_callback
        self.set_focus_path([1, 'body'])
        the_loop.widget = self

    def reopen(self):
        self.set_focus_path([1, 'body'])
        the_loop.widget = self

    def _callback(self):
        recpts = self.edit.get_edit_text().replace(',', '\n').split('\n')
        good, bad = [], []
        addr = re.compile('(@.{44}.ed25519)')
        for r in recpts:
            r = r.strip()
            if len(r) == 0:
                continue
            for i in addr.findall(r):
                good.append(i)
                break
            else:
                users = app.the_db.match_about_name(f"^{r[1:]}$" if r[0] == '@' else r)
                logger.info(f"users: <{r}> {str(users)}")
                if len(users) == 1:
                    good.append(users[0])
                else:
                    bad.append(f"? {r}" if len(users) == 0 else f"?+ {r}")

        lst = []
        for r in list(set(good)):
            nm = app.feed2name(r)
            if nm:
                r = f"[@{nm}]({r})"
            lst.append(r)

        good = lst
        if len(good) + len(bad) == 0:
            bad = [
             'add one recipient']
        else:
            if len(good) + len(bad) >= 7:
                bad = [
                 'max 7 recipients'] + bad
            if len(bad) > 0:
                self.edit.set_edit_text('\n'.join(bad + lst))
                self.edit.set_edit_pos(len(bad[0]))
                self.set_focus_path([1, 'body'])
            else:
                self.edit.set_edit_text('\n'.join(good))
                self.close()
                self.callback(good)

    def close(self):
        save_draft(draft_private_text, self.edit.get_edit_text().split('\n'))
        the_loop.widget = urwid_frame
        the_loop.draw_screen()


class Menu(urwid.Overlay):
    _labels = [
     '',
     'refresh   !',
     '',
     'reply     R',
     'compose   C',
     '',
     'directory U',
     'help      ?',
     '',
     'quit      Q']

    def cb(self, button):
        screen_size = urwid.raw_display.Screen().get_cols_rows()
        l = button.get_label()[(-1)].lower()
        self.close()
        urwid_frame.keypress(screen_size, l)

    def open(self):
        the_loop.widget = self

    def close(self):
        the_loop.widget = urwid_frame
        the_loop.draw_screen()

    def __init__(self, active=None):
        self._active = active
        body = [urwid.Text('    M E N U')]
        for l in self._labels:
            if l == '':
                body.append(urwid.Text('---------------'))
            elif not active or l[(-1)] in active:
                body.append(urwid.AttrMap(urwid.Button(l, self.cb), None, 'selected'))
            else:
                body.append(urwid.Text(('even', f"  {l}  ")))

        lb = urwid.ListBox(urwid.SimpleFocusListWalker(body))
        super().__init__((urwid.AttrMap(urwid.LineBox(lb), 'fill')), (the_loop.widget),
          align='right', valign='top', width=('relative', 5),
          height=('relative', 5),
          min_width=17,
          min_height=13)

    def keypress(self, size, key):
        if key in ('shift tab', ):
            return super().keypress(size, 'up')
        if key in ('tab', ):
            return super().keypress(size, 'down')
        if key in ['esc'] + arrow_left:
            self.close()
            return
        k = key.upper()
        for l in self._labels:
            if l == '':
                continue
            if k == l[(-1)]:
                if not self._active or k in self._active:
                    self.close()
                    urwid_frame.keypress(screen_size, key)
                    return

        return super().keypress(size, key)


def launch(app_core, secr, args):
    global app
    global the_loop
    global urwid_convoList
    global urwid_counter
    global urwid_footer
    global urwid_frame
    global urwid_header
    global urwid_threadList
    global urwid_title
    app = app_core
    print(ui_descr)
    amber_palette = [
     ('fill', 'dark gray', 'black', 'default', '#d80', '#000'),
     ('even', 'black', 'dark gray', 'standout', '#000', '#d80'),
     ('evenBold', 'black,underline', 'dark gray', 'standout,underline', '#000,underline',
 '#d80'),
     ('odd', 'dark gray', 'black', 'default', '#d80', '#000'),
     ('oddBold', 'dark gray,underline', 'black', 'underline', '#d80,underline', '#000'),
     ('header', 'black', 'light gray', 'standout', '#000', '#fa0'),
     ('selected', 'black', 'light gray', 'standout', '#000', '#fa0'),
     ('selectedPrivate', 'black', 'light gray', 'standout', '#000', '#fa0'),
     ('cypherlink', 'dark red,underline', 'black', 'standout', '#fa0,underline', '#d80')]
    green_palette = [
     ('fill', 'dark green', 'black'),
     ('even', 'black', 'dark green'),
     ('evenBold', 'black,underline', 'dark green'),
     ('odd', 'dark green', 'black'),
     ('oddBold', 'dark green,underline', 'black'),
     ('header', 'black', 'light green'),
     ('selected', 'black', 'light green'),
     ('selectedPrivate', 'black', 'light green'),
     ('cypherlink', 'black,underline', 'dark green')]
    mono_palette = [
     ('fill', 'default', 'default'),
     ('even', 'standout', 'default'),
     ('evenBold', 'standout,underline', 'default'),
     ('odd', 'default', 'default'),
     ('oddBold', 'underline', 'default'),
     ('header', 'standout', 'default'),
     ('selected', 'standout', 'default'),
     ('selectedPrivate', 'standout', 'default'),
     ('cypherlink', 'standout,underline', 'default')]
    light_palette = [
     ('fill', 'black', 'white'),
     ('even', 'black', 'light gray', 'standout'),
     ('evenBold', 'black,underline', 'light gray', 'standout'),
     ('odd', 'black', 'white'),
     ('oddBold', 'black,underline', 'white'),
     ('header', 'white', 'light blue', 'underline'),
     ('selected', 'white', 'light red', 'standout'),
     ('selectedPrivate', 'white', 'light green', 'standout'),
     ('cypherlink', 'light blue,underline', 'light gray', 'standout')]
    dark_palette = [
     ('fill', 'white', 'black'),
     ('even', 'white', 'dark gray', 'standout'),
     ('evenBold', 'white,underline', 'dark gray', 'standout'),
     ('odd', 'white', 'black', 'standout'),
     ('oddBold', 'white,underline', 'black', 'standout'),
     ('header', 'black', 'dark green', 'underline'),
     ('selected', 'black', 'light red', 'standout'),
     ('selectedPrivate', 'black', 'light blue', 'standout'),
     ('cypherlink', 'light blue,underline', 'dark gray', 'standout')]
    palette = {'mono':mono_palette, 
     'green':green_palette, 
     'amber':amber_palette, 
     'light':light_palette, 
     'dark':dark_palette}[args.style]
    screen = urwid.raw_display.Screen()
    screen.set_terminal_properties(256)
    screen.register_palette(palette)
    urwid_counter = urwid.Text('  FWD=0 BWD=0 ', 'right', wrap='clip')
    urwid_title = urwid.Text('PUBLIC chats:', wrap='clip')
    urwid_header = urwid.Pile([
     urwid.Columns([urwid.Text(f"SurfCity - a log-less SSB client{ui_descr}", wrap='clip'),
      (
       'pack', urwid_counter)]),
     urwid_title])
    urwid_hdrmap = urwid.AttrMap(urwid_header, 'header')
    if args.offline:
        urwid_footer = urwid.Text('Offline')
    else:
        urwid_footer = urwid.Text('Welcome, please stand by ...', wrap='clip')
    urwid_ftrmap = urwid.AttrMap(urwid.Columns([
     urwid_footer,
     (
      'pack', urwid.Text(" Type '?' for help.", 'right'))]), 'header')
    urwid_threadList = urwid.ListBox([urwid.Text('Almost there ...')])
    urwid_convoList = PrivateConvoListBox(secr, [urwid.Text('Just a moment...')])
    urwid_frame = urwid.Frame(urwid_threadList, header=urwid_hdrmap, footer=urwid_ftrmap,
      focus_part='body')
    logger.info('%s', f"surfcity {str(time.ctime())} starting")
    evl = urwid.AsyncioEventLoop(loop=(asyncio.get_event_loop()))
    ensure_future(main(secr, args))
    the_loop = urwid.MainLoop((urwid.AttrMap(urwid_frame, 'fill')), screen=screen,
      event_loop=evl,
      unhandled_input=on_unhandled_input)
    try:
        the_loop.run()
    except Exception as e:
        try:
            s = traceback.format_exc()
            logger.info('main exc %s', s)
            print(s)
        finally:
            e = None
            del e

    if error_message:
        print(error_message)