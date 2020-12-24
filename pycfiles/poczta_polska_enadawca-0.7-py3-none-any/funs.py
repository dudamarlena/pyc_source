# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/utils/funs.py
# Compiled at: 2018-12-07 04:32:38
__doc__ = "\nCopyright (c) 2014-2016 pocsuite developers (https://seebug.org)\nSee the file 'docs/COPYING' for copying permission\n"
import re, ast, codecs, string, random
from socket import gethostbyname
from urlparse import urlparse
from pocsuite.lib.core.data import logger
from pocsuite.lib.core.data import conf
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from pocsuite.api.request import req

def url2ip(url, with_port=False):
    """
    works like turning 'http://baidu.com' => '180.149.132.47'
    """
    url_prased = urlparse(url)
    if url_prased.port:
        ret = (
         gethostbyname(url_prased.hostname), url_prased.port)
    else:
        if not url_prased.port and url_prased.scheme == 'https':
            ret = (
             gethostbyname(url_prased.hostname), 443)
        else:
            ret = (
             gethostbyname(url_prased.hostname), 80)
        if with_port:
            return ret
    return ret[0]


def writeText(fileName, content, encoding='utf8'):
    """
    write file with given fileName and encoding
    """
    try:
        fp = codecs.open(fileName, mode='w+', encoding=encoding)
        fp.write(content)
        fp.close()
        logger.log(CUSTOM_LOGGING.SYSINFO, '"%s" write to Text file "%s"' % (content, fileName))
    except Exception as e:
        logger.log(CUSTOM_LOGGING.WARNING, e)


def loadText(fileName, encoding='utf8'):
    """
    read file with given fileName and encoding
    """
    try:
        fp = codecs.open(fileName, mode='r', encoding=encoding)
        content = fp.readlines()
        fp.close()
        logger.log(CUSTOM_LOGGING.SYSINFO, 'return file "%s" content .' % fileName)
        return content
    except Exception as e:
        logger.log(CUSTOM_LOGGING.WARNING, e)


def writeBinary(fileName, content, encoding='utf8'):
    """
    write file with given fileName and encoding
    """
    try:
        fp = codecs.open(fileName, mode='wb+', encoding=encoding)
        fp.write(content)
        fp.close()
        logger.log(CUSTOM_LOGGING.SYSINFO, '"%s" write to Text file "%s"' % (content, fileName))
    except Exception as e:
        logger.log(CUSTOM_LOGGING.WARNING, e)


def getExtPar():
    return conf.params


def strToDict(string):
    try:
        return ast.literal_eval(string)
    except ValueError as e:
        logger.log(CUSTOM_LOGGING.ERROR, 'conv string failed : %s' % e)


def randomStr(length=10, chars=string.ascii_letters + string.digits):
    return ('').join(random.sample(chars, length))


def resolve_js_redirects(url):
    meta_regx = '(?is)\\<meta[^<>]*?url\\s*=([\\d\\w://\\\\.?=&;%-]*)[^<>]*'
    body_regx = '(?is)\\<body[^<>]*?location[\\s\\.\\w]*=[\'"]?([\\d\\w://\\\\.?=&;%-]*)[\'"]?[^<>]*'
    js_regx = '(?is)<script.*?>[^<>]*?window\\.location\\.(?:replace|href|assign)[\\("\']*([\\d\\w://\\\\.?=&;%-]*)[^<>]*?</script>'
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    res = req.get(url)
    true_url = res.url
    for regx in [meta_regx, body_regx, js_regx]:
        result = re.search(regx, res.text)
        if result:
            true_url = result.group(1)
            break

    return true_url