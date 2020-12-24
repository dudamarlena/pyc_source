# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/errormiddleware.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 2233 bytes
MGOBLIN_ERROR_MESSAGE = '<div style="text-align:center;font-family: monospace">\n  <h1>YEOWCH... that\'s an error!</h1>\n  <pre>\n.-------------------------.\n|     __            _     |\n|    -, \\_,------,_//     |\n|     <\\  ,--   --.\\      |\n|      / (x  ) ( X )      |\n|      \'  \'--, ,--\'\\      |\n|     / \\ -v-v-u-v /      |\n|     .  \'.__.--__\'.\\     |\n|    / \',___/ / \\__/\'     |\n|    | |   ,\'\\_\'/, ||     |\n|    \\_|   | | | | ||     |\n|     W\',_ ||| |||_\'\'     |\n|      |  \'------\'|       |\n|      |__|     |_|_      |\n|     ,,,-\'     \'-,,,     |\n\'-------------------------\'\n  </pre>\n  <p>Something bad happened, and things broke.</p>\n  <p>If this is not your website, you may want to alert the owner.</p>\n  <br><br>\n  <p>\n    Powered... er broken... by\n    <a href="http://www.mediagoblin.org">MediaGoblin</a>,\n    a <a href="http://www.gnu.org">GNU Project</a>.\n  </p>\n</div>'

def mgoblin_error_middleware(app, global_conf, **kw):
    """
    MediaGoblin wrapped error middleware.

    This is really just wrapping the error middleware from Paste.
    It should take all of Paste's default options, so see:
      http://pythonpaste.org/modules/exceptions.html
    """
    try:
        from paste.exceptions.errormiddleware import make_error_middleware
    except ImportError:
        return app

    kw['error_message'] = MGOBLIN_ERROR_MESSAGE
    return make_error_middleware(app, global_conf, **kw)