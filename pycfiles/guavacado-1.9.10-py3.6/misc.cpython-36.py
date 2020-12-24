# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/guavacado/misc.py
# Compiled at: 2019-07-08 18:47:49
# Size of source mod 2**32: 4529 bytes
import time, logging, sys, urllib

def generate_redirect_page(dest):
    """returns a minimal HTML redirect page to quickly redirect the web browser to a specified destination"""
    return '\n\t\t<!DOCTYPE html>\n\t\t<html>\n\t\t\t<head>\n\t\t\t\t<META http-equiv="refresh" content="0;URL={dest}">\n\t\t\t\t<title>Guavacado Web Redirect</title>\n\t\t\t</head>\n\t\t\t<body>\n\t\t\t\tThere is no information at this page.\n\t\t\t\tIf you are not redirected to {dest} immediately, you can click <a href="{dest}">here</a>.\n\t\t\t\t<script>\n\t\t\t\t\twindow.location = "{dest}";\n\t\t\t\t\twindow.location.replace("{dest}");\n\t\t\t\t\twindow.location.href = "{dest}";\n\t\t\t\t</script>\n\t\t\t</body>\n\t\t</html>\n\t'.format(dest=dest)


def generate_redirect_page_w_statuscode(dest, use_code=301):
    """returns a redirect page, using the specified status code to potentially redirect the page faster"""
    extra_keys = {}
    if use_code in (301, 308, 302, 303, 307):
        extra_keys['Location'] = dest
    return (
     {'status_code':use_code, 
      'url':'redirect.html',  'extra_header_keys':extra_keys}, generate_redirect_page(dest))


ALL_LOGGER_NAMES = []
CURRENT_LOGLEVEL = logging.NOTSET

def set_loglevel(levelstr):
    global ALL_LOGGER_NAMES
    global CURRENT_LOGLEVEL
    if levelstr is None:
        level = None
    else:
        if isinstance(levelstr, int):
            level = levelstr
        else:
            level = getattr(logging, levelstr, None)
    if level is None:
        extra_levels = {}
        if levelstr in extra_levels:
            level = extra_levels[levelstr]
        else:
            level = 1000000
    CURRENT_LOGLEVEL = level
    for logname in ALL_LOGGER_NAMES:
        logger = logging.getLogger(logname)
        logger.setLevel(CURRENT_LOGLEVEL)


def init_logger(name):
    fmt = '%(asctime)s | %(levelname)-8s | %(filename)-20s | line:%(lineno)-3s | %(message)s'
    logger = logging.getLogger(name)
    if name not in ALL_LOGGER_NAMES:
        ALL_LOGGER_NAMES.append(name)
        logger.setLevel(CURRENT_LOGLEVEL)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def addr_rep(addr, pretty=False):
    """
        return a representation of the given address tuple
        if the optional argument pretty=True is specified, presents the address in a way that can be 
        """

    def tls_rep(addr):
        if addr is None:
            return 'disabled'
        if type(addr) in [tuple]:
            return 'cert:{cert},key:{key}'.format(cert=(addr[0]), key=(addr[1]))

    if addr is None:
        return '[None]'
    else:
        if type(addr) in [list]:
            if len(addr) == 1:
                return addr_rep(addr[0])
            else:
                if pretty:
                    if len(addr) > 2:
                        return ', '.join([addr_rep(a, pretty=True) for a in addr[:-1]]) + ', and ' + addr_rep((addr[(-1)]), pretty=True)
                    else:
                        return ' and '.join([addr_rep(a, pretty=True) for a in addr])
                else:
                    return '[{}]'.format(','.join([addr_rep(a) for a in addr]))
        else:
            if type(addr) in [tuple]:
                if addr[0] is None:
                    return addr_rep(('', addr[1]))
                if type(addr[0]) in [tuple]:
                    if addr[1] is None:
                        return addr_rep(addr[0])
                    else:
                        if pretty:
                            return '{addr} (https)'.format(addr=addr_rep((addr[0]), pretty=True))
                        return '{addr}(tls:[{tls}])'.format(addr=(addr_rep(addr[0])), tls=(tls_rep(addr[1])))
                else:
                    if pretty:
                        return '{ip} port {port}'.format(ip=(addr[0]), port=(addr[1]))
                    else:
                        return '{ip}:{port}'.format(ip=(addr[0]), port=(addr[1]))
            else:
                if type(addr) in [dict]:
                    ip = addr.get('addr')
                    port = addr.get('port')
                    TLS = addr.get('TLS')
                    UDP = addr.get('UDP')
                    addr_copy = addr.copy()
                    if ip is None:
                        addr_copy.update({'addr': ''})
                        return addr_rep(addr_copy, pretty=pretty)
                    if TLS is not None:
                        addr_copy.update({'TLS': None})
                        if pretty:
                            return '{addr} (https)'.format(addr=addr_rep(addr_copy, pretty=True))
                        else:
                            return '{addr}(tls:[{tls}])'.format(addr=(addr_rep(addr_copy)), tls=(tls_rep(TLS)))
                    elif UDP is not None:
                        if UDP:
                            addr_copy.update({'UDP': None})
                            if pretty:
                                return '{addr} (UDP)'.format(addr=addr_rep(addr_copy, pretty=True))
                            else:
                                return '{addr}(UDP)'.format(addr=(addr_rep(addr_copy)))
                    else:
                        if pretty:
                            return '{ip} port {port}'.format(ip=ip, port=port)
                        else:
                            return '{ip}:{port}'.format(ip=ip, port=port)
                else:
                    if pretty:
                        return ''
                    else:
                        return str(addr)


def url_decode(url):
    urllib_parse = getattr(urllib, 'parse', urllib)
    return urllib_parse.unquote(url)


def wait_for_keyboardinterrupt():
    try:
        while True:
            time.sleep(86400)

    except KeyboardInterrupt:
        pass