# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/metadata/disc/CDDB.py
# Compiled at: 2008-10-26 20:23:09
import urllib, string, socket, os, re
name = 'CDDB.py'
version = 1.3
if os.environ.has_key('EMAIL'):
    (default_user, hostname) = string.split(os.environ['EMAIL'], '@')
else:
    default_user = os.geteuid() or os.environ['USER'] or 'user'
    hostname = socket.gethostname() or 'host'
proto = 6
default_server = 'http://freedb.freedb.org/~cddb/cddb.cgi'

def query(track_info, server_url=default_server, user=default_user, host=hostname, client_name=name, client_version=version):
    disc_id = track_info[0]
    num_tracks = track_info[1]
    query_str = '%08lx %d ' % (disc_id, num_tracks)
    for i in track_info[2:]:
        query_str = query_str + '%d ' % i

    query_str = urllib.quote_plus(string.rstrip(query_str))
    url = '%s?cmd=cddb+query+%s&hello=%s+%s+%s+%s&proto=%i' % (
     server_url, query_str, user, host, client_name,
     client_version, proto)
    response = urllib.urlopen(url)
    encoding = ''
    if response.headers.has_key('content-type'):
        for value in response.headers['content-type'].split(';'):
            if value.strip().lower().startswith('charset='):
                encoding = value[value.find('=') + 1:].strip().lower()

    header = string.split(string.rstrip(response.readline()), ' ', 3)
    header[0] = string.atoi(header[0])
    if header[0] == 200:
        try:
            title = unicode(header[3], encoding)
        except UnicodeDecodeError:
            title = unicode(header[3], errors='replace')

        result = {'category': header[1], 'disc_id': header[2], 'title': title}
        return [
         header[0], result]
    else:
        if header[0] == 211 or header[0] == 210:
            result = []
            for line in response.readlines():
                line = string.rstrip(line)
                if line == '.':
                    break
                match = string.split(line, ' ', 2)
                try:
                    title = unicode(match[2], encoding)
                except UnicodeDecodeError:
                    title = unicode(match[2], errors='replace')

                result.append({'category': unicode(match[0]), 'disc_id': match[1], 'title': title})

            return [
             header[0], result]
        else:
            return [
             header[0], None]
        return


def read(category, disc_id, server_url=default_server, user=default_user, host=hostname, client_name=name, client_version=version):
    url = '%s?cmd=cddb+read+%s+%s&hello=%s+%s+%s+%s&proto=%i' % (
     server_url, category, disc_id, user, host, client_name,
     client_version, proto)
    response = urllib.urlopen(url)
    encoding = ''
    if response.headers.has_key('content-type'):
        for value in response.headers['content-type'].split(';'):
            if value.strip().lower().startswith('charset='):
                encoding = value[value.find('=') + 1:].strip().lower()

    header = string.split(string.rstrip(response.readline()), ' ', 3)
    header[0] = string.atoi(header[0])
    if header[0] == 210 or header[0] == 417:
        reply = []
        for line in response.readlines():
            line = string.rstrip(line)
            if line == '.':
                break
            line = string.replace(line, '\\t', '\t')
            line = string.replace(line, '\\n', '\n')
            line = string.replace(line, '\\\\', '\\')
            reply.append(line)

        if header[0] == 210:
            reply = parse_read_reply(reply)
            for (key, value) in reply.items():
                if isinstance(value, str):
                    try:
                        reply[key] = unicode(reply[key], encoding)
                    except UnicodeDecodeError:
                        reply[key] = unicode(reply[key], errors='replace')

            return [
             header[0], reply]
        return [header[0], reply]
    else:
        return [
         header[0], None]
    return


def parse_read_reply(comments):
    len_re = re.compile('#\\s*Disc length:\\s*(\\d+)\\s*seconds')
    revis_re = re.compile('#\\s*Revision:\\s*(\\d+)')
    submit_re = re.compile('#\\s*Submitted via:\\s*(.+)')
    keyword_re = re.compile('([^=]+)=(.*)')
    result = {}
    for line in comments:
        keyword_match = keyword_re.match(line)
        if keyword_match:
            (keyword, data) = keyword_match.groups()
            if result.has_key(keyword):
                result[keyword] = result[keyword] + data
            else:
                result[keyword] = data
            continue
        len_match = len_re.match(line)
        if len_match:
            result['disc_len'] = int(len_match.group(1))
            continue
        revis_match = revis_re.match(line)
        if revis_match:
            result['revision'] = int(revis_match.group(1))
            continue
        submit_match = submit_re.match(line)
        if submit_match:
            result['submitted_via'] = submit_match.group(1)
            continue

    return result