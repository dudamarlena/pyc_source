# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/okay/tonka/src/closed_caption_player/src/srtgetter.py
# Compiled at: 2018-01-04 12:15:41
import untangle, requests, requests_cache, StringIO, zipfile, os
try:
    os.makedirs(os.path.expanduser('~/.config/closed_caption_player/'))
except:
    pass

cache_path = os.path.expanduser('~/.config/closed_caption_player/subtitle_cache')
requests_cache.install_cache(cache_path)
URL = 'subsmax.com/api/10/'

def download_subtitles(sub, filename):
    download_link = sub.link.cdata
    tokens = download_link.split('/')
    base = tokens.pop()
    tokens.append('download-subtitle')
    tokens.append(base)
    download_link = ('/').join(tokens)
    print 'DOWNLOADING', download_link
    r = requests.get(download_link)
    zipdata = StringIO.StringIO()
    zipdata.write(r.content)
    zfobj = zipfile.ZipFile(zipdata)
    for name in zfobj.namelist():
        if name == filename:
            uncompressed = zfobj.read(name)
            break

    tokens = tokens.replace('\r', '')
    tokens = uncompressed.split('\n')
    return tokens


def run_query(*args):
    arg_str = ('-').join(args)
    print 'QUERY IS', arg_str
    url = '%s/%s' % (URL, arg_str)
    url = url.replace('//', '/')
    url = 'http://%s' % url
    print 'URL IS', url
    r = requests.get(url)
    return select_download(r.content)


def select_filename(item, files, data):
    i = 0
    for file in files:
        i += 1
        print '%i) %s' % (i, file)

    while True:
        a = raw_input()
        try:
            if a == 'q':
                return select_download(data)
            id = int(a)
            break
        except KeyboardInterrupt:
            break
        except:
            print 'Please enter an ID to use'

    id = int(id)
    file = files[(id - 1)]
    print 'RETRIEVING AND PLAYING', id, file
    return download_subtitles(item, file)


def select_download(data):
    obj = untangle.parse(data)
    print 'LOAD WHICH SUBTITLES?'
    i = 0
    items = obj.SubsMaxAPI.items.item
    items.sort(key=lambda w: w.added_on.cdata, reverse=True)
    labeled_items = []
    for item in items:
        i += 1
        files_in_archive = [ x.split(',')[0] for x in item.files_in_archive.cdata.split('|') ]
        files_in_archive.sort()
        languages = [ l for l in item.languages.cdata.replace('unknown', '???').split(',') ]
        languages = (',').join(map(lambda l: l[:2], languages))
        labeled_items.append((item, files_in_archive))
        print '%i) %s' % (i, item.filename.cdata)
        print '    %s file(s), uploaded on %s, lang: %s' % (len(files_in_archive), item.added_on.cdata,
         languages)

    print '\nEnter an ID to use, press q to exit:'
    while True:
        a = raw_input()
        try:
            if a == 'q':
                break
            id = int(a)
            break
        except KeyboardInterrupt:
            break
        except:
            print 'Please enter an ID to use'

    print 'RETRIEVING AND PLAYING ARCHIVE', id, item.title.cdata
    id = int(id)
    item, files = labeled_items[(id - 1)]
    return select_filename(item, files, data)


if __name__ == '__main__':
    select_download()