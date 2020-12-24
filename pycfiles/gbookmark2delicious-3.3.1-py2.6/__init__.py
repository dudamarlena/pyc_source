# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gbookmark2delicious/__init__.py
# Compiled at: 2012-03-07 05:11:55
"""Synchronize your Delicious bookmarks against your Google Bookmarks.  By
default, this script will read the credentials file for your logins, fetch all
Google bookmarks, determine if anything changed since the last successful sync,
and perform the necessary adds/removes/updates to delicious."""
from __future__ import print_function, unicode_literals
import BeautifulSoup, cgi, codecs, copy, cPickle as pickle, datetime, itertools, logging, mechanize, optparse, pydelicious, re, sys, time
from functools import partial
import commons.log
from commons import files, networking, strs, structs
from commons.path import path
spaces = re.compile(b' {2,}')
ws = re.compile(b'\\s')
wss = re.compile(b'\\s{2,}')
log = logging.getLogger(__name__)

def squeeze(s):
    return wss.sub(b' ', s)


def process_args(argv):
    """
  Process the command-line arguments.
  """
    parser = optparse.OptionParser(description=__doc__)
    parser.add_option(b'--goog-user', help=b'Google username.')
    parser.add_option(b'--goog-pass', help=b'Google password.')
    parser.add_option(b'--dlcs-user', help=b'delicious username.')
    parser.add_option(b'--dlcs-pass', help=b'delicious username.')
    parser.add_option(b'--pretend', action=b'store_true', help=b"Don't actually make changes to delicious.")
    parser.add_option(b'--no-remove', action=b'store_true', help=b"Don't remove any bookmarks, only add/update.")
    parser.add_option(b'--cred-file', default=path(b'~/.gbookmark2delicious.auth').expanduser(), help=squeeze(b'File containing the four username/password arguments in\n      the above order, one per line.  Remember to chmod 600! (The command-line\n      arguments get precedence.)'))
    parser.add_option(b'--ignore-snapshot', action=b'store_true', help=squeeze(b"Ignore any snapshot of last successful sync and force\n      the program to continue with the comparison/sync as if it didn't\n      exist."))
    parser.add_option(b'--force-dlcs', action=b'store_true', help=squeeze(b"Force re-fetch of delicious bookmarks instead of using\n      the cache. Only applicable if snapshot is missing/stale/ignored.\n      Otherwise, delicious bookmarks are only fetched the first time (cache\n      doesn't exist). This option is useful if the cache is corrupted or if\n      changes were made to the delicious account out-of-band."))
    parser.add_option(b'--cache-dir', default=path(b'~/.gbookmark2delicious.cache').expanduser(), help=squeeze(b"Local cache for both Google and delicious. Google cache\n      is by default ignored (see --use-goog-cache). delicious cache is used if\n      it's not obsolete, and refreshed if it's out of date."))
    parser.add_option(b'--use-goog-cache', action=b'store_true', help=squeeze(b'Whether to read from any available local cache of the\n      Google posts instead of actually downloading the posts from Google.  This\n      is useful as a timesaver for development/debugging purposes.'))
    parser.add_option(b'--debug', action=b'store_true', help=squeeze(b'Enable debug logging.'))
    return parser.parse_args(argv[1:])


def setup_config(options):
    config = copy.copy(options)
    if config.goog_user is None or config.goog_pass is None or config.dlcs_user is None or config.dlcs_pass is None:
        with open(config.cred_file) as (f):
            c = config
            (c.goog_user, c.goog_pass, c.dlcs_user, c.dlcs_pass) = map(str.strip, f.readlines())
    config.goog_path = config.cache_dir / b'goog.html'
    config.dlcs_path = config.cache_dir / b'dlcs.html'
    config.to_dlcs_path = config.cache_dir / b'to-dlcs.html'
    config.snapshot_path = config.cache_dir / b'snapshot.pickle'
    commons.log.config_logging(level=logging.DEBUG if config.debug else logging.INFO, do_console=True)
    if log.isEnabledFor(logging.DEBUG):
        to_show = copy.copy(config)
        del to_show.goog_pass
        del to_show.dlcs_pass
        log.debug(b'config: %s', to_show)
    return config


def create_browser():
    b = mechanize.Browser()
    b.set_handle_robots(False)
    b.addheaders = [
     ('User-agent', 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.7 Safari/533.2'),
     ('Accept-Language', 'en-US,en;q=0.8'),
     ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]
    return b


def dlcs_retry(func):

    def helper():
        try:
            res = func()
        except pydelicious.PyDeliciousException:
            log.exception(b'got an exception from delicious API')
            return
        else:
            if res is not None:
                raise Exception(b'expecting pydelicious to return None, got %r', res)

        return True
        return

    return networking.retry_exp_backoff(300, 5, helper)


def tidy(s):
    """
  This does two things: resolve HTML entity/character references, and
  squeeze consecutive spaces.

  Delicious returns HTML references that start with an extraneous 0, such
  as &#039; instead of &#39;.

  Google Bookmarks returns strings with multiple neighboring spaces.
  Delicious appears to be stripping them out (or expects that they be
  &nbsp; characters).
  """
    return spaces.sub(b' ', strs.html2unicode(s or b'').strip())


def is_trunc(a, b, dots):
    """Whether a is a truncated copy of b but with a suffix such as "...\""""
    return len(a) < len(b) and a.endswith(dots) and b.startswith(a[:-len(dots)])


class bkmk(structs.free_struct):
    pass


def fetch_goog(config):
    log.info(b'getting google bookmarks')
    log.info(b'authenticating with google')
    b = create_browser()
    b.open(b'https://www.google.com/bookmarks/bookmarks.html')
    b.select_form(nr=0)
    b.set_value(config.goog_user, b'Email')
    b.set_value(config.goog_pass, b'Passwd')
    resp = b.submit()
    html = resp.read()
    if b'<!DOCTYPE NETSCAPE-Bookmark-file-1>' not in html:
        print(html)
        raise Exception(b'google authentication failed')
    log.info(b'google authenticated, got all bookmarks')
    with open(config.goog_path, b'w') as (f):
        f.write(html)


def try_unicode(s):
    if unicode(s) == b'None':
        return b''
    return unicode(s)


def parse_goog(config):
    log.info(b'parsing google bookmarks')
    with codecs.open(config.goog_path, encoding=b'utf-8') as (f):
        bs = BeautifulSoup.BeautifulSoup(f)
    log.info(b'building google bookmarks into data structure')
    gurl2bkmk = {}
    for group in bs.dl.findAll(b'dt', recursive=False):
        label = ws.sub(b'_', strs.html2unicode(group.h3.string))
        for dt in group.findAll(b'dt'):
            url = try_unicode(dt.a[b'href'])
            name = try_unicode(dt.a.string)
            sib = dt.nextSibling
            desc = try_unicode(sib.string if sib is not None and sib.name == b'dd' else None)
            g = gurl2bkmk.setdefault(url, bkmk(name=name, desc=desc, labels=[]))
            assert g.name == name and g.desc == desc and label not in g.labels, b'%r vs %r' % (g, (name, desc, label))
            g.labels.append(label)

    return gurl2bkmk


def dlcs_open(b, config, url, expected):
    html = b.open(url).read().decode(b'utf8')
    if expected not in html:
        log.debug(html)
        log.info(b'authenticating with delicious')
        b.open(b'https://delicious.com/login')
        r = b.response()
        c = r._seek_wrapper__cache
        id(b.forms())
        c.seek(0)
        rep = b'\n    <form method="post" action="login" id="login-form">\n    <input type="text" name="username" class="textInput" id="firstInput"/>\n    <input type="password" name="password"class="textInput"/>\n    <input type="submit" style="visibility:hidden;"/>\n    </form>\n    '
        c.write(c.read().decode(b'utf8').replace(b'<hr/>', rep).encode(b'utf8'))
        c.truncate()
        c.seek(0)
        b._factory._forms_genf = None
        b.select_form(nr=1)
        b.set_value(config.dlcs_user, b'username')
        b.set_value(config.dlcs_pass, b'password')
        html = b.submit().read().decode(b'utf8')
        if b'is_logged_in' not in html:
            log.debug(html)
            raise Exception(b'delicious authentication failed')
        log.info(b'delicious authenticated')
        html = b.open(url).read().decode(b'utf8')
    return html


def fetch_dlcs(b, config):
    log.info(b'getting all delicious bookmarks')
    dlcs_open(b, config, b'https://export.delicious.com/settings/bookmarks/export', b'Export / Download Your Delicious Bookmarks')
    b.select_form(nr=1)
    resp = b.submit()
    log.info(b'got all delicious bookmarks')
    with open(config.dlcs_path, b'w') as (f):
        f.write(resp.read())


def parse_dlcs(config):
    log.info(b'parsing delicious bookmarks')
    with codecs.open(config.dlcs_path, encoding=b'utf-8') as (f):
        bs = BeautifulSoup.BeautifulSoup(f)
    log.info(b'building delicious bookmarks data structure')
    durl2bkmk = {}
    for dt in bs.findAll(b'dt'):
        url = try_unicode(dt.a[b'href'])
        name = try_unicode(dt.a.string)
        labels = dt.a[b'tags'].split(b',')
        sib = dt.nextSibling
        desc = try_unicode(sib.string if sib is not None and sib.name == b'dd' else None)
        assert url not in durl2bkmk, url
        durl2bkmk[url] = bkmk(name=name, desc=desc, labels=labels)

    return durl2bkmk


def compare(gurl2bkmk, durl2bkmk):

    def diff(url):
        """Whether goog and dlcs *meaningfully* differ on the given URL."""
        g = copy.copy(gurl2bkmk[url])
        d = copy.copy(durl2bkmk[url])
        g.labels = [ ws.sub(b'_', label) for label in g.labels ]
        g.desc = tidy(g.desc)
        d.desc = tidy(d.desc)
        g.name = tidy(g.name)
        d.name = tidy(d.name)
        if g.name == b'' and d.name == url:
            d.name = b''
        if is_trunc(d.desc, g.desc, b'...'):
            d.desc = g.desc
        if is_trunc(d.name, g.name, b'..'):
            d.name = g.name
        return g != d

    gurls = set(gurl2bkmk.keys())
    durls = set(durl2bkmk.keys())
    to_add = gurls - durls
    to_rem = durls - gurls
    to_upd = [ url for url in durls.intersection(gurls) if diff(url) ]
    log.info(b'add %d rem %d upd %', len(to_add), len(to_rem), len(to_upd))
    puts = [ (url, gurl2bkmk[url]) for url in itertools.chain(to_add, to_upd) ]
    if log.isEnabledFor(logging.DEBUG):
        for url in to_add:
            log.debug(b'to add: %s', dict(url=url) + gurl2bkmk[url])

        for url in to_rem:
            log.debug(b'to remove: %s', dict(url=url) + durl2bkmk[url])

        for url in to_upd:
            log.debug(b'to update: %s on goog, %s on dlcs', bkmk(url=url) + gurl2bkmk[url], bkmk(url=url) + durl2bkmk[url])

    return (
     to_add, to_rem, to_upd, puts)


def mk_import(to_dlcs_path, puts):
    log.info(b'generating file to import into delicious')
    hdr = b'<!DOCTYPE NETSCAPE-Bookmark-file-1>\n<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n<!-- This is an automatically generated file.\nIt will be read and overwritten.\nDo Not Edit! -->\n<TITLE>Bookmarks</TITLE>\n<DL><p>'
    ftr = b'</DL><p>'
    log.info(b'producing page for delicious to import')
    with codecs.open(to_dlcs_path, b'w', b'utf-8') as (f):
        print(hdr, file=f)
        for (url, g) in puts:
            try:
                labels = (b',').join(map(cgi.escape, g.labels))
                print(b'<DT><A HREF="%s" TAGS="%s">%s</A>' % (
                 cgi.escape(url), labels, g.name), file=f)
                if g.desc is not None:
                    print(b'<DD>' + g.desc, file=f)
            except:
                log.exception(b'problem writing %s', g + bkmk(url=url))
                raise

        print(ftr, file=f)
    return


def do_import(b, config):
    log.info(b'importing bookmarks to delicious')
    dlcs_open(b, config, b'https://export.delicious.com/settings/bookmarks/import', b'Import Your Bookmarks to Delicious')
    with open(config.to_dlcs_path) as (f):
        b.select_form(nr=1)
        b.add_file(f, b'text/html', config.to_dlcs_path.basename())
        b.set_value(b'', b'tags')
        b.set_value([b'no'], b'private')
        resp = b.submit()
    html = resp.read().decode(b'utf-8')
    if b'Success! Your bookmark import has begun.' not in html:
        raise Exception(b'could not import bookmarks to delicious, instead got: ' + html)
    log.info(b'successfully imported to delicious')


def read_snapshot(config):
    try:
        with open(config.snapshot_path) as (f):
            return pickle.load(f)
    except:
        return (None, None)

    return


def write_snapshot(gurl2bkmk, config):
    with open(config.snapshot_path, b'w') as (f):
        pickle.dump((time.time(), gurl2bkmk), f, protocol=2)


def main(argv=sys.argv):
    (options, args) = process_args(argv)
    config = setup_config(options)
    files.soft_makedirs(config.cache_dir)
    if not (config.use_goog_cache and config.goog_path.exists()):
        fetch_goog(config)
    gurl2bkmk = parse_goog(config)
    b = create_browser()
    (timestamp, durl2bkmk) = read_snapshot(config)
    if config.ignore_snapshot or durl2bkmk is None:
        if config.force_dlcs or not config.dlcs_path.exists():
            fetch_dlcs(b, config)
        durl2bkmk = parse_dlcs(config)
    else:
        log.info(b'using sync snapshot from %s', datetime.datetime.fromtimestamp(timestamp))
    (to_add, to_rem, to_upd, puts) = compare(gurl2bkmk, durl2bkmk)
    if len(puts) > 0:
        mk_import(config.to_dlcs_path, puts)
        if not config.pretend:
            do_import(b, config)
    if not config.pretend and not config.no_remove:
        dlcs_api = pydelicious.DeliciousAPI(config.dlcs_user, config.dlcs_pass, b'utf-8')
        for url in to_rem:
            dlcs_retry(lambda : dlcs_api.posts_delete(url))
            time.sleep(1)

    write_snapshot(gurl2bkmk, config)
    return