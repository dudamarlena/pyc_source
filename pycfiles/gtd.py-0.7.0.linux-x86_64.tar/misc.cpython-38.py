# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/delucks/.pyenv/versions/3.8.1/lib/python3.8/site-packages/todo/misc.py
# Compiled at: 2020-02-21 23:12:22
# Size of source mod 2**32: 5204 bytes
import os, re
from datetime import datetime
try:
    from random import choice
except OSError:
    choice = lambda n: n.pop()
else:
    import requests
    from todo import __version__, __author__
    VALID_URL_REGEX = re.compile('https?://.*\\.')

    def mongo_id_to_date(item_id: str) -> int:
        """Trello uses MongoDB ids for the card IDs, which have an embedded timestamp.
    This function extracts that embedded timestamp, which is the card creation time.
    Based on https://steveridout.github.io/mongo-object-time/
    """
        ts = int(item_id[:8], 16)
        return datetime.fromtimestamp(ts)


    def return_on_eof(func):

        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except EOFError:
                return

        return wrapper


    def build_name_lookup(sequence):
        """Creates a mapping between each object's name in "sequence" and
    the object itself. Useful for selecting label or list objects.
    """
        return {o:o.name for o in sequence}


    class Colors:
        esc = '\x1b'
        black = esc + '[0;30m'
        red = esc + '[0;31m'
        green = esc + '[0;32m'
        yellow = esc + '[0;33m'
        blue = esc + '[0;34m'
        purple = esc + '[0;35m'
        cyan = esc + '[0;36m'
        white = esc + '[0;37m'
        reset = esc + '[0m'

        @staticmethod
        def all_colors():
            return [Colors.red, Colors.green, Colors.yellow, Colors.blue, Colors.purple, Colors.cyan]


    def get_title_of_webpage--- This code section failed: ---

 L.  63         0  LOAD_STR                 'User-Agent'
                2  LOAD_STR                 'gtd.py version '
                4  LOAD_GLOBAL              __version__
                6  BINARY_ADD       
                8  BUILD_MAP_1           1 
               10  STORE_FAST               'headers'

 L.  64        12  SETUP_FINALLY        88  'to 88'

 L.  65        14  LOAD_GLOBAL              requests
               16  LOAD_ATTR                get
               18  LOAD_FAST                'url'
               20  LOAD_FAST                'headers'
               22  LOAD_CONST               ('headers',)
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  STORE_FAST               'resp'

 L.  66        28  LOAD_STR                 'text/html'
               30  LOAD_FAST                'resp'
               32  LOAD_ATTR                headers
               34  LOAD_METHOD              get
               36  LOAD_STR                 'Content-Type'
               38  LOAD_STR                 ''
               40  CALL_METHOD_2         2  ''
               42  COMPARE_OP               not-in
               44  POP_JUMP_IF_FALSE    52  'to 52'

 L.  67        46  POP_BLOCK        
               48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            44  '44'

 L.  68        52  LOAD_FAST                'resp'
               54  LOAD_ATTR                text
               56  STORE_FAST               'as_text'

 L.  69        58  LOAD_FAST                'as_text'
               60  LOAD_FAST                'as_text'
               62  LOAD_METHOD              find
               64  LOAD_STR                 '<title>'
               66  CALL_METHOD_1         1  ''
               68  LOAD_CONST               7
               70  BINARY_ADD       
               72  LOAD_FAST                'as_text'
               74  LOAD_METHOD              find
               76  LOAD_STR                 '</title>'
               78  CALL_METHOD_1         1  ''
               80  BUILD_SLICE_2         2 
               82  BINARY_SUBSCR    
               84  POP_BLOCK        
               86  RETURN_VALUE     
             88_0  COME_FROM_FINALLY    12  '12'

 L.  70        88  DUP_TOP          
               90  LOAD_GLOBAL              requests
               92  LOAD_ATTR                exceptions
               94  LOAD_ATTR                ConnectionError
               96  COMPARE_OP               exception-match
               98  POP_JUMP_IF_FALSE   112  'to 112'
              100  POP_TOP          
              102  POP_TOP          
              104  POP_TOP          

 L.  71       106  POP_EXCEPT       
              108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            98  '98'
              112  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 48


    class DevNullRedirect:
        __doc__ = 'Temporarily eat stdout/stderr to allow no output.\n    This is used to suppress browser messages in webbrowser.open'

        def __enter__(self):
            self.old_stderr = os.dup(2)
            self.old_stdout = os.dup(1)
            os.close(2)
            os.close(1)
            os.openos.devnullos.O_RDWR

        def __exit__(self, exc_type, exc_value, traceback):
            os.dup2self.old_stderr2
            os.dup2self.old_stdout1


    WORKFLOW_TEXT = '1. Collect absolutely everything that can take your attention into "Inbound"\n2. Filter:\n    Nonactionable -> Static Reference or Delete\n    Takes < 2 minutes -> Do now, then Delete\n    Not your responsibility -> "Holding" or "Blocked" with follow-up\n    Something to communicate -> messaging lists\n    Your responsibility -> Your lists\n3. Write "final" state of each task and "next" state of each task\n4. Categorize inbound items into lists based on action type required (call x, talk to x, meet x...)\n5. Reviews:\n    Daily -> Go through "Inbound" and "Doing"\n    Weekly -> Additionally, go through "Holding", "Blocked", and messaging lists\n6. Do\n\nThe goal is to get everything except the current task out of your head\nand into a trusted system external to your mind.'

    def get_banner(version=__version__, use_color=True):
        """Hold a buncha poorly done ASCII banners and display one at random!"""
        if use_color:
            on = choice(Colors.all_colors())
            off = Colors.reset
        else:
            on = off = ''
        b1 = ' __|_ _| ._     version {on}{0}{off}\n(_||_(_|{on}o{off}|_)\\/  by {on}delucks{off}\n _|      |  /\n'.format(version,
          on=on, off=off)
        b2 = '  ___  ____  ____    ____  _  _\n / __)(_  _)(  _ \\  (  _ \\( \\/ )\n( (_-.  )(   )(_) )  )___/ \\  /\n \\___/ (__) (____/{on}(){off}(__)   (__)\n   version {on}{0}{off}\n'.format(version,
          on=on, off=off)
        b3 = '        __      __   version {on}{0}{off}\n.-----.|  |_.--|  |  .-----.--.--.\n|  _  ||   _|  _  |{on}__{off}|  _  |  |  |\n|___  ||____|_____{on}|__|{off}   __|___  |\n|_____|              |__|  |_____|\n'.format(version,
          on=on, off=off)
        b4 = '         __      .___  version {on}{0}{off}\n   _____/  |_  __| _/______ ___.__.\n  / ___\\   __\\/ __ | \\____ <   |  |\n / /_/  >  | / /_/ | |  |_> >___  |\n \\___  /|__| \\____ |{on}/\\{off}   __// ____|\n/_____/           \\/{on}\\/{off}__|   \\/\n'.format(version,
          on=on, off=off)
        b5 = f"67 74 64 {on}2e{off} 70 79\n76 65 72 73 69 6f 6e {on}{version}{off}\n"
        b6 = f"--. - -.. {on}.-.-.-{off} .--. -.--\n...- . .-. ... .. --- -. {on}{version}{off}\n"
        b7 = '     _     _\n ___| |_ _| |  ___ _ _\n| . |  _| . |{on}_{off}| . | | |\n|_  |_| |___{on}|_|{off}  _|_  |\n|___|         |_| |___|\n     version {on}{0}{off}\n'.format(version,
          on=on, off=off)
        banner_choices = [b1, b2, b3, b4, b5, b6, b7]
        return choice(banner_choices)