# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/surfcity/ui/tty.py
# Compiled at: 2019-04-03 14:35:37
# Size of source mod 2**32: 25336 bytes
import asyncio, copy, fcntl, json, logging, os, random, re, shutil, string, subprocess, sys, tempfile, termios, time, traceback, tty
app = None
import surfcity.app.net as net
logger = logging.getLogger('surfcity_ui_tty')
ui_descr = ' (tty ui, v2019-04-02)'
error_message = None
kbd = None
help = [
 "Welcome to SurfCity\n\nBelow you find a table with the keyboard bindings followed\nby a description of SurfCity's philosophy and an explanation\nof the command line options.\n\nYou can leave this screen by typing 'q'.\n\nEnjoy!\n\nSanta Cruz, Feb 2019\n  ssb:   @AiBJDta+4boyh2USNGwIagH/wKjeruTcDX2Aj1r/haM=.ed25519\n  email: <christian.tschudin@unibas.ch>",
 "Keyboard bindings:\n\n?       this text\nq       quit\n\ne       next thread\ny       prev thread\nf       scroll forward 5 threads, <space> does the same\nb       scroll backwards\nnumber  jump to this thread\n\np       toggle private/public threads\nx       extended public thread list\n\nenter   show current thread's content\n\n!       refresh\ns       status\nt       toggle flags\nu       user directory\n_       about SurfCity\n",
 'About SurfCity\n\nSecure Scuttlebutt (SSB) brings to you a deluge of information,\nall appended to the message logs of the respective authors:\n\n     SurfCity is the tool to ride this wavefront.\n\nIt does so (a) in forward as well as (b) in backward direction\nand (c) widens its scan range dynamically, but WITHOUT having\nto store all the participants\' huge log files.\n\nTypically, the storage footprint of SurfCity is in the range of\ntens of MBytes, while a full SSB client easily consumes GigaBytes\nof disk storage. Also, when booting freshly into SurfCity, you\nwill immediately have messages to display: no need to wait for\nlong download times and indexing pauses.  In that sense SurfCity\nis sustainable, riding the wave with roughly constant storage\nspace - at least if YOU behave sustainably, e.g. block or un-\nfollow peers if the list becomes too large ;-)\n\nWhat does "riding the wavefront" mean?\n\na) By this we mean that SurfCity\'s most important task is to\nscan the Scuttleverse for new content in the forward direction.\nSurfCity will process these fresh messages and store them for a\nfew weeks only. It will also take note of a discussion thread\'s\nfirst post and keep this information around for a few months\nso it can later display the thread\'s "title". Finally, SurfCity\nkeeps track of the SSB crypto peer identifiers and the human-\nreadable names that have been assigned to them.\n\nb) SurfCity also is able to scan content in backwards direction.\nFrom these "historic" messages, SurfCity collects essential\ninformation e.g. the name that a peer has assigned to him/herself,\nor the other peers that a peer follows or blocks. Eventually this\nbackground scan bottoms out when the logs of all followed peers\nhave been scanned entirely.\n\nc) Finally, the breadth of the wavefront is enlarged as SurfCity\nlearns about whom you are following. In this case, these peers\nare added to your "following list" and are also scanned. This is\npart of the SSB concept that messages sent by a peer are only\naccessible in that peer\'s log, hence the need to scan it. The\nwidth of the wavefront is even larger than this, as the followed\npeers of a followed peer (FOAF, "friends of a friend") are also\nscanned. SurfCity scans these FOAF peers less frequently by\nrandomly picking some of them, in each round. But it\'s all\nfine because SSB is based on eventual concistency, and random\nselection will eventually lead SurfCity to visit every peer\nwithin the wavefront\'s current breadth.\n\nPrototype and Future Work\n\nBeware, this is experimental software! Its main purpose is to\nvalidate the concept of wavefront riding for SSB and to prepare\nthe ground for a SSB browser that can run on a smartphone but\ndoes not come with a huge GByte storage requirement.\n',
 'Explanation of command-line options\n\n-offline        prevents SurfCity from doing any scans, but also\n                from downloading any message content. This means\n                that only cached messages can be displayed (at\n                most a few weeks old) and that threads look\n                less complete when activating this option.\n\n-narrow         prevents SurfCity to scan the logs of FOAF\n                (friends of a friend): Only peers that you\n                decided to follow will be considered in the\n                scans. This only affects scanning and is not\n                a censoring option: All content that SurfCity\n                already collected will be used and displayed.\n\n-nocatchup      "do not scan backwards": prevents SurfCity from\n                scanning historic messages.\n\n-noextend       "do not scan forwards": prevents SurfCity from\n                probing for new messages that extend the peers\'\n                logs.']

def my_format(txt, style='left'):
    txt = txt.split('\n')
    out = []
    w = shutil.get_terminal_size((80, 25))[0] - 1
    if style == 'center':
        for t in txt:
            out.append(' ' * ((w - len(t)) // 2) + t)

    else:
        if style == 'rule':
            for t in txt:
                t = ' ' + '.' * ((w - len(t)) // 2 - 1) + t
                out.append(t + '.' * (w - len(t)))

        else:
            if style == 'para':
                for t in txt:
                    while len(t) > w - 4:
                        i = w - 5
                        while i > 0 and t[i] not in ' \t':
                            i -= 1

                        if i <= 0:
                            out.append('|  ' + t[0:w - 5])
                            t = t[w - 4:]
                        else:
                            out.append('|  ' + t[0:i])
                            while t[i] in ' \t' and i < len(t) - 1:
                                i += 1

                            t = t[i:]

                    out.append('|  ' + t)

            else:
                if style == 'repeat':
                    out = [
                     (txt[0] * w)[:w]]
                else:
                    out = txt
    return out


class Keyboard:

    def __init__(self, loop=None):
        fd = sys.stdin.fileno()
        self.loop = loop or asyncio.get_event_loop()
        self.q = asyncio.Queue(loop=(self.loop))
        self.old_settings = termios.tcgetattr(fd)
        tty.setcbreak(fd, termios.TCSANOW)
        self.new_settings = termios.tcgetattr(fd)
        self.new_settings[1] |= termios.OPOST | termios.ONLCR
        self.resume()

    def _upcall(self):
        asyncio.ensure_future((self.q.put(sys.stdin.read())), loop=(self.loop))

    async def getcmd(self):
        cmd = await self.q.get()
        if len(cmd) == 1:
            if cmd in ('\r', '\n'):
                return 'enter'
            c = ord(cmd[0])
            if c in (8, 127):
                return 'del'
            if c < 32:
                return f"ctrl-{chr(64 + c)}"
            return cmd
        if cmd.isnumeric():
            return cmd
        return 'key sequence'

    def pause(self):
        self.loop.remove_reader(sys.stdin)
        fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, ~os.O_NONBLOCK)
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, self.old_settings)

    def resume(self):
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.new_settings)
        fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        self.loop.add_reader(sys.stdin, self._upcall)

    def __del__(self):
        sys.stdout.flush()
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_settings)


printable = set(string.printable)

def mk_printable(s):
    return s.encode('ascii', errors='replace').decode()


def render_lines(lns, at_bottom=True):
    global kbd
    with tempfile.NamedTemporaryFile(mode='w+t', suffix='.txt') as (f):
        f.write('\n'.join(lns))
        f.flush()
        kbd.pause()
        if at_bottom:
            cmd = f"set > t.txt; less -c -h0 -S +G -R {f.name}"
        else:
            cmd = f"less -c -h0 -S -R {f.name}".split(' ')
            cmd = f"export TERM=ansi; less {f.name}"
            print(cmd)
        subprocess.run(cmd, shell=True, start_new_session=True)
        kbd.resume()


async def cmd_backward(secr, args, list_state):
    print('backward')
    if list_state['show'] == 'Public':
        tlist = list_state['publ']
    else:
        tlist = list_state['priv']
    if len(tlist) == 0:
        print('no threads')
        return
    current = list_state['current']
    step = list_state['step']
    if current < step:
        list_state['current'] = 0
        return
    current -= step
    step = 5
    low, high = current - step + 1, current
    if low < 0:
        low = 0
    if low != high:
        print(f"{list_state['show']} threads ({low + 1}-{high + 1} of {len(tlist)})")
    for i in range(low, high):
        print('_____')
        print(('#%-3d' % (i + 1)), end='')
        ls2 = copy.copy(list_state)
        ls2['current'] = i
        await cmd_summary(secr, args, ls2)

    list_state['current'] = current
    list_state['step'] = step


async def cmd_bottom(secr, args, list_state):
    print('>')
    current = len(list_state['publ']) - 1
    if current < 0:
        current = 0
    list_state['current'] = current


async def cmd_compose(secr, args, list_state):
    if list_state['show'] == 'Public':
        print('not implemented')
        return
    print('not implemented')


async def cmd_enter(secr, args, list_state):
    global app
    print()
    if list_state['show'] == 'Public':
        t = list_state['publ'][list_state['current']]
        msgs, _, _ = await app.expand_thread(secr, t, args,
          None, ascii=True)
        app.the_db.update_thread_lastread(t)
    else:
        msgs, title, _ = await app.expand_convo(secr, (list_state['priv'][list_state['current']]),
          args,
          True, ascii=True)
    help_text = "[type 'q' to quit, '<' to jump to the beginning, '>' to jump to the end]"
    txt = [
     '']
    txt += my_format(help_text, 'center')
    txt += my_format('---oldest---', 'center')
    if list_state['show'] == 'Public':
        if len(msgs) > 0:
            if 'root' in msgs[0]['content']:
                txt += my_format('[some older messages out of reach]', 'center')
    else:
        txt += ['']
        txt += my_format('private conversation with', 'center')
        txt += my_format(title[0][1][:-1], 'center')
    for m in msgs:
        a = m['author']
        n = app.feed2name(m['author'])
        if not n:
            n = m['author']
        txt += ['']
        txt += my_format(f" {mk_printable(n)} ({app.utc2txt(m['timestamp'], False)}) ", 'rule')
        t = mk_printable(m['content']['text'])
        t = re.sub('\\[([^\\]]*)\\]\\([^\\)]*\\)', '[\\1]', t)
        txt += my_format(t, 'para')
        txt += my_format(f" {m['key']} ", 'rule')

    txt += ['']
    txt += my_format('---newest---', 'center')
    txt += my_format(help_text, 'center')
    txt += ['\n']
    render_lines(txt)


async def cmd_forward(secr, args, list_state):
    print('forward')
    if list_state['show'] == 'Public':
        tlist = list_state['publ']
    else:
        tlist = list_state['priv']
    current = list_state['current']
    if len(tlist) == 0:
        print('no threads')
        return
    low, high = current + 1, current + 5
    if high >= len(tlist):
        high = len(tlist) - 1
    if low > high:
        low = high
    if low != high:
        print(f"{list_state['show']} threads ({low + 1}-{high + 1} of {len(tlist)})")
    for i in range(low, high):
        print('_____')
        print(('#%-3d' % (i + 1)), end='')
        ls2 = copy.copy(list_state)
        ls2['current'] = i
        await cmd_summary(secr, args, ls2)

    list_state['current'] = high
    list_state['step'] = high - low


async def cmd_help(*args):
    print('?')
    print("HELP for the 'tty SurfCity client'" + "\n\n?       this text\nq       quit\n\ne       next thread\ny       prev thread\nf       scroll forward 5 threads, <space> does the same\nb       scroll backwards\nnumber  jump to this thread\n\np       toggle private/public threads\nx       extended public thread list\n\nenter   show current thread's content\n\nc       compose new posting\nr       reply to current posting\n\n!       refresh\ns       status\nt       toggle flags\nu       user directory\n_       about SurfCity\n")


async def cmd_next(secr, args, list_state):
    print('next')
    if list_state['current'] + 1 < len(list_state['publ']):
        list_state['current'] += 1
    list_state['step'] = 1


async def cmd_prev(secr, args, list_state):
    print('previous')
    current = list_state['current']
    list_state['current'] = 0 if current <= 0 else current - 1
    list_state['step'] = 1


async def cmd_privpubl(secr, args, list_state):
    if list_state['show'] == 'Public':
        list_state['show'] = 'Private'
        print('private -- preparing list of conversations ... ', end='', flush=True)
        list_state['priv'] = await app.mk_convo_list(secr, args, cache_only=(args.offline))
    else:
        list_state['show'] = 'Public'
        print('pubic -- preparing list of thread ... ', end='', flush=True)
        list_state['publ'] = app.mk_thread_list(secr, args, cache_only=(args.offline),
          extended_network=(not args.narrow))
    print('done')
    list_state['current'] = 0
    list_state['step'] = 1


async def cmd_refresh(secr, args, list_state):
    print('refresh')
    if app.new_forw == 0:
        if app.new_back == 0:
            return
    else:
        print(f"for FWD={app.new_forw}/BWD={app.new_back} new messages\n")
        app.new_forw = 0
        app.new_back = 0
        t = list_state['publ'][list_state['current']]
        lst = app.mk_thread_list(secr, args, cache_only=(args.offline),
          extended_network=(not args.narrow))
        list_state['publ'] = lst
        if t in lst:
            list_state['current'] = lst.index(t)
            list_state['step'] = 1
        else:
            list_state['current'] = 0


async def cmd_reply(secr, args, list_state):
    print('not implemented')


async def cmd_status(secr, args, list_state):
    print('status')
    s = []
    if args.offline:
        s.append('offline')
    if args.narrow:
        s.append('narrow')
    if not args.nocatchup:
        s.append('catchup')
    if not args.noextend:
        s.append('extend')
    if len(s) > 0:
        print(f"flags: {s}")
    print(f"new msgs: fwd={app.new_forw}, bwd={app.new_back}")
    print()


async def cmd_summary(secr, args, list_state):
    if list_state['show'] == 'Public':
        t = list_state['publ'][list_state['current']]
        _, txt, _ = await app.expand_thread(secr, t, args, None, ascii=True)
    else:
        c = list_state['priv'][list_state['current']]
        _, txt, _ = await app.expand_convo(secr, c, args, True, ascii=True)
    title = txt.pop(0)
    if title[0]:
        print(f"* '{title[1][:71]}'")
    else:
        print(f"  '{title[1][:71]}'")
    for m in txt:
        print('      %-10s  %-46s   %s' % (m[1][:10], m[2][:46], m[0]))


async def cmd_top(secr, args, list_state):
    print('<')
    list_state['current'] = 0


async def cmd_userdir(secr, args, list_state):

    def user2line(feedID, isFriend=False):
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

    hrule = '\n---\n'
    lines = ['## USER DIRECTORY', hrule]
    me = app.the_db.get_config('id')
    lines.append(f"My feedID:\n\n{user2line(me)}")
    lines.append(hrule)
    pubs = app.the_db.list_pubs()
    frnd = app.the_db.get_friends(me)
    fol = app.the_db.get_following(me)
    t = []
    for f in fol:
        if f in pubs:
            t.append(user2line(f, f in frnd))

    t.sort(key=(lambda x: x[2:].lower()))
    t = [f"Accredited pubs: {len(pubs)}\n"] + t
    lines.append('\n'.join(t))
    lines.append(hrule)
    fol = app.the_db.get_following(me)
    t1, t2 = [], []
    for f in fol:
        if f in pubs:
            continue
        ln = user2line(f, f in frnd)
        if ln[2:12] == '?         ':
            t2.append(ln)
        else:
            t1.append(ln)

    t1.sort(key=(lambda x: x[2:].lower()))
    t2.sort(key=(lambda x: x[2:].lower()))
    t = [f"Followed feeds (* =friend/following back): {len(fol) - len(pubs)}\n"] + t1 + t2
    lines.append('\n'.join(t))
    lines.append(hrule)
    folr = app.the_db.get_followers(me)
    t = []
    for f in folr:
        if f in frnd:
            continue
        t.append(user2line(f))

    t.sort(key=(lambda x: x[2:].lower()))
    t = [f"Follower feeds (other than friends): {len(t)}\n"] + t
    lines.append('\n'.join(t))
    lines.append(hrule)
    blk = app.the_db.get_following(me, 2)
    t = []
    for f in blk:
        t.append(user2line(f))

    t.sort(key=(lambda x: x.lower()))
    t = [
     f"Blocked feeds: {len(blk)}\n"] + t
    lines.append('\n'.join(t))
    lines.append(hrule)
    ffol = app.the_db.get_follofollowing(me)
    t = []
    for f in ffol:
        if f in fol:
            continue
        t.append(user2line(f))

    t.sort(key=(lambda x:     if x[2:3] == '?':
'~~~~~' + x[2:].lower() # Avoid dead code: x[2:].lower()))
    t = [f"Number of feeds followed by the feeds I follow: {len(ffol)}\n"] + t
    lines.append('\n'.join(t))
    lines.append(hrule)
    lines.append('END OF USER DIRECTORY')
    render_lines(lines, at_bottom=False)


async def cmd_xtended(secr, args, list_state):
    if list_state['show'] != 'Public':
        print('xtended only valid in public mode')
        return
    list_state['extended'] = ~list_state['extended']
    print("xtended friends' list of threads\nnow ", end='')
    print('enabled' if list_state['extended'] else 'disabled')
    print()


async def cmd_about(secr, args, list_state):
    hrule = '\n-------------------------------------------------------------------------------\n'
    lines = [hrule]
    for t in help:
        lines.append(t)
        lines.append(hrule)

    render_lines(lines, at_bottom=False)


cmds = {'enter':cmd_enter, 
 'summary':cmd_summary, 
 'h':cmd_help, 
 '?':cmd_help, 
 '<':cmd_top, 
 '>':cmd_bottom, 
 'b':cmd_backward, 
 '-':cmd_backward, 
 'f':cmd_forward, 
 ' ':cmd_forward, 
 'e':cmd_next, 
 'y':cmd_prev, 
 '!':cmd_refresh, 
 'p':cmd_privpubl, 
 'c':cmd_compose, 
 'r':cmd_reply, 
 's':cmd_status, 
 'u':cmd_userdir, 
 'x':cmd_xtended, 
 '_':cmd_about}

async def scanner(secr, args):
    while True:
        logger.info('%s', f"surfcity-tty {str(time.ctime())} before wavefront")
        try:
            await app.scan_wavefront(secr.id, secr, args)
        except Exception as e:
            try:
                logger.info(' ** scanner exception %s', str(e))
                logger.info(' ** %s', traceback.format_exc())
            finally:
                e = None
                del e

        logger.info('%s', f"surfcity-tty {str(time.ctime())} after wavefront")
        if app.new_friends_flag:
            await app.process_new_friends(secr)
        logger.info('%s', f"surfcity {str(time.ctime())} before sleeping")
        await asyncio.sleep(5)


async def main(kbd, secr, args):
    global error_message
    try:
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
            if not args.noextend:
                await app.process_new_friends(secr, print)
            asyncio.ensure_future(scanner(secr, args))
        list_state = {'publ':app.mk_thread_list(secr, args, cache_only=args.offline, extended_network=not args.narrow), 
         'current':0, 
         'step':1, 
         'show':'Public', 
         'extended':False}
        while True:
            if list_state['show'] == 'Public':
                if len(list_state['publ']) == 0:
                    print('no threads')
                else:
                    print('_____')
                    print(('#%-3d' % (list_state['current'] + 1)), end='')
                    await cmds['summary'](secr, args, list_state)
                    print()
            else:
                if len(list_state['priv']) == 0:
                    print('no private conversations')
                else:
                    print('_____')
                    print(('#%-3d' % (list_state['current'] + 1)), end='')
                    await cmds['summary'](secr, args, list_state)
                    print()
            prompt = 'sc> '
            if app.new_forw > 0:
                prompt = f"(+{app.new_forw})sc> "
            print(prompt, end='', flush=True)
            num = ''
            while 1:
                cmd = await kbd.getcmd()
                if cmd.isnumeric():
                    num += cmd
                    print(cmd, end='', flush=True)
                    continue
                if cmd == 'del':
                    if num != '':
                        num = num[:-1]
                        print('\x08 \x08', end='', flush=True)
                        continue
                    break

            if num != '':
                if cmd == 'enter':
                    print()
                    num = int(num)
                    t = list_state['publ'] if list_state['show'] == 'Public' else list_state['publ']
                    if num == 0 or num > len(t):
                        print('\nindex out of range.')
                    else:
                        list_state['current'] = num - 1
                        continue
                if cmd in ('q', 'Q', 'ctrl-C', 'ctrl-D'):
                    print('quit')
                    break
                if cmd in cmds:
                    await cmds[cmd](secr, args, list_state)
            else:
                print(f"\nunknown cmd '{cmd}'. Type '?' for help.\n")

    except:
        traceback.print_exc()


def launch(app_core, secr, args):
    global app
    global kbd
    app = app_core
    print(ui_descr)
    the_loop = asyncio.get_event_loop()
    try:
        try:
            kbd = Keyboard()
            the_loop.run_until_complete(main(kbd, secr, args))
        except Exception as e:
            try:
                s = traceback.format_exc()
                logger.info('main exc %s', s)
                print(s)
            finally:
                e = None
                del e

    finally:
        kbd.__del__()

    if error_message:
        print(error_message)