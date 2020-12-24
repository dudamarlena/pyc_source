# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dpopowich/work/googlewsgiservlets/tutorial/sessions.py
# Compiled at: 2011-10-14 15:54:51
from TutorialBase import *
from time import ctime

class sessions(HTMLPage):
    """How to manage sessions."""
    title = 'State Management, Part 2: Sessions'
    use_session = True
    session_config = {'timeout': 180}
    session_cookie_secret = 'wsgisrv tutorial'
    expirenow = GET_var('', bool)
    deletenow = GET_var('', bool)

    def prep(self):
        HTMLPage.prep(self)
        if self.expirenow:
            self.session.expire()
            self.redirect(self.script_name)
        if self.deletenow:
            self.response = HTTPTemporaryRedirect(location=self.script_name)
            self.del_cookie(self.session_cookie_name)
            raise self.response

    def write_content(self):
        found = self.found()
        visits = self.session['visits'] = self.session.get('visits', 0) + 1
        self.writeln(FORMRESULTS.format(visits=visits, plural='s' if visits > 1 else '', cookiename=self.session_cookie_name, found=found, expire=EXPIRELINK, delete=DELETELINK))
        self.writeln(OVERVIEW)

    def found(self):
        """Piece together parts of the output based on cookie/session
        existance and validity"""
        c = self.cookies.get(self.session_cookie_name)
        if c:
            c = c.value
            if c[40:] == self.session.sid:
                valid = 'It is valid and will expire %s' % ctime(self.session.expires)
            else:
                valid = 'It expired, so a new session was generated.  Refresh the page to see the new cookie value'
            isnew = 'It is a new session.' if self.session.is_new else 'It is a reloaded session.'
            found = 'found with value: <em>%s</em><strong>%s</strong>.<br>%s.<br>%s' % (
             c[:40], c[40:], valid, isnew)
        else:
            found = 'not found.  A new session was generated.  Refresh the page to see the new cookie value.'
        return found

    css = '#floatbox {  \n    float: right;\n    width: 50%;\n    padding: 10px;\n    margin: 10px;            \n    background-color:lightgreen;\n    }'


OVERVIEW = make_overview(('\nEach servlet has a `session` attribute; its value is controlled by the\nvalue of another attribute, `use_session`.  If `use_session` evaluates\nto `False` (the default) then sessions are not used and the value of\nthe `session` attribute will be `None`.  If `use_session` evaluates to\n`True` then the `session` attribute will be an instance of `Session`\nwhich is a subclass of the standard python `dict` and can be used in\nyour servlets like any other mapping; the only restriction is that its\nkeys and values must be pickleable.\n\nA Session has a `save()` method which is automatically called at the\nend of a request and saves the `dict` server-side for future retrieval\nby subsequent requests using the same session ID. The session ID is\nstored on the client via a cookie (yes, cookies must be enabled to use\nsession management).  If the cookie expires or the session times out,\nthen a new session will be created automatically.  The session cookie\nstored on the client is a signed cookie using a SHA1 digest; the first\n40 characters is the digest, the last 32 characters is the session ID.\n\nA Session has two other methods: `revert()` reverts the items in the\nsession to the contents it had at the beginning of the request.\n`expire()` expires the session, clearing its items and flagging the\nsession cookie for deletion.\n\nA Session has three attributes: `sid`, the session ID; `expires`, a\ntimestamp (seconds since the epoch) indicating when the session will\nexpire; `is_new`, a boolean indicating if the session was newly\ncreated for this request.\n\nSession timeout is controlled by the `timeout` item of\n`session_config`, an attribute of servlets (view the source to see how\nit is set for this tutorial).  The value is in seconds (default: 1800,\nor thirty minutes) and for this demo is set to three minutes.\n\nOther servlet attributes that affect sessions:\n\n  * `session_cookie_name`: the name of the cookie stored on the\n    client.  The default value is `wsgisrv_sid`.\n  * `session_cookie_secret`: THIS MUST BE SET to use sessions.  This is\n     the seed for the signed cookie digest.\n  * `session_config`: mentioned above, this is a mapping containing\n    items that configure general session behaviour\n  * `session_backend`: a class that subclasses\n    `wsgiservlets.SessionBackend` and manages the backend storage of\n    sessions.  As of this writing there is only one backend,\n    `FileSessionBackend`, which stores sessions as pickled data in a\n    directory hierarchy.\n  * `session_backend_init`: a mapping which configures the session\n    backend.  For FileSessionBackend there is only one item in the\n    mapping, `cachedir` which is the root directory for saving\n    sessions.  The default value is `{cachedir}`.\n  \nThis servlet demonstrates using sessions with a trivial\n*how-many-times-have-I-visited-this-page* counter.  Reload the page\nand watch the counter.\n').format(cachedir=FILESESSION_CACHEDIR))
FORMRESULTS = '<div id="floatbox">\n<p>The session cookie name is <code>{cookiename}</code> and it was {found}</p>\n\nYou can expire it by clicking {expire}.<br>\nYou can delete the cookie by clicking {delete}.\n\n<p>You have visited this page <strong>{visits}</strong> time{plural}.</p>\n</div>\n'
EXPIRELINK = '<a href="?expirenow=1">here</a>'
DELETELINK = '<a href="?deletenow=1">here</a>'