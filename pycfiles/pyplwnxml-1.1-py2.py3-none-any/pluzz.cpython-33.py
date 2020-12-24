# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pluzz/pluzz.py
# Compiled at: 2014-05-18 10:39:52
# Size of source mod 2**32: 14415 bytes
__doc__ = 'Pluzz Downloader\n\nDownloads a movie from the French Television VOD\n\nUsage:\n  pluzz_downloader.py gui [<id>] [-t <target>] [--avconv <avconv>] [--verbose]\n  pluzz_downloader.py fetch <id> [-t <target>] [--avconv <avconv>] [--verbose]\n  pluzz_downloader.py get <id> [<key>]\n  pluzz_downloader.py show <id>\n  pluzz_downloader.py list [<category>] [<channel>] [-l <limit>] [-s <sort>] [-i]\n  pluzz_downloader.py search <query> [<category>] [<channel>] [-l <limit>] [-s <sort>] [-i]\n\nCommands:\n  gui                    Launch graphical user interface.\n  get                    Get list of keys.\n  get <key>              Get value for key.\n  show                   Give summary for key.\n  fetch                  Download the TV show.\n  list                   List TV shows.\n  search <query>         Search a TV show.\n\nOptions for `list` and `search` commands:\n  <query>                Terms of the show to look up.\n  <category>             Category to list. `help` or no value gives the list.\n  <channel>              Channels to list. `help` or no value gives the list.\n  -l --limit <limit>     Number of shows to output. [default: 100]\n  -s --sort <sort>       Sort the output (alpha, date, relevance) [default: alpha]\n  -i --image             Show thumbnail image URL for the show\n\nOptions for `get`, `show` and `fetch` commands:\n  <id>                   URL or ID of the TV show\n  -t --target <target>   Target directory to download the file to [default: ~/Downloads]\n  --avconv <avconv>      Sets full path to avconv binary [default: /usr/bin/avconv]\n  -V --verbose           Show more output.\n  -h --help              Show this screen.\n\n(c)2014 Bernard `Guyzmo` Pratz\nUnder the WTFPL <http://wtfpl.net>\n'
import io, os, re, sys, json, time, select, requests, textwrap, functools, itertools, subprocess, collections
from lxml import etree

class PluzzSearch:
    SORT = {'relevance': 'pertinence',  'date': 'date',  'alpha': 'alpha'}
    url = 'http://pluzz.francetv.fr/ajax/launchsearch/{filter}/{sort}/nb/{limit}'
    filter_category = 'rubrique/{}'
    filter_channel = 'chaine/{}'
    filter_query = 'requete/{}'
    filter_page = 'debut/{}'
    sort = 'tri/{}'

    def __init__(self, out=None, verbose=False):
        self.out = out
        self.verbose = verbose
        self._main_page_cache = None
        return

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def get_categories(self):
        if self._main_page_cache is None:
            self._main_page_cache = etree.HTML(requests.get('http://pluzz.francetv.fr/a-z').text)
        return [i.attrib['value'] for i in self._main_page_cache.xpath('id("chx_rubrique")/li/input')] + ['all']

    def get_channels(self):
        if self._main_page_cache is None:
            self._main_page_cache = etree.HTML(requests.get('http://pluzz.francetv.fr/a-z').text)
        return [i.attrib['data-chaine'] for i in self._main_page_cache.xpath('id("chx_chaine")/li')] + ['all']

    def list(self, query=None, category=None, channel=None, limit=100, sort='', page=0):
        print(_('Get data…'), end='\r', file=self.out)
        filter_ = ['']
        if category == 'all':
            category = None
        if channel == 'all':
            channel = None
        if query:
            filter_ += [self.filter_query.format(query)]
        if category:
            filter_ += [self.filter_category.format(category)]
        if channel:
            filter_ += [self.filter_channel.format(channel)]
        if sort:
            try:
                sort = self.SORT[sort]
            except KeyError:
                sort = ''

        url = self.url.format(filter='/'.join(filter_), sort=self.sort.format(sort), limit=limit)
        h = etree.HTML(requests.get(url).text)
        if h.xpath('//span[@class="noresult-big"]/text()'):
            if self.verbose:
                print(h.xpath('//span[@class="noresult-big"]/text()'), file=sys.stderr)
            raise Exception('No results found')
        l = h.xpath('//article/h3/a|//article/a/img')
        return [{'id': i[0].attrib['href'].split(',')[(-1)].split('.')[0],  'title': i[0].text.strip(),  'image': i[1].attrib['data-src']} for i in itertools.zip_longest(*([iter(l)] * 2), fillvalue=None)]


class PluzzMovie:
    data_url = 'http://webservices.francetelevisions.fr/tools/getInfosOeuvre/v2/?idDiffusion={show}&catalogue=Pluzz'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:19.0) Gecko/20100101 Firefox/19.0'}
    avconv_args = ['-y', '-vcodec', 'copy', '-acodec', 'copy']

    def __init__(self, uri, out=None):
        print(_('Init…'), end='\r', file=out)
        if uri.startswith('http://'):
            self.url = uri
            self.show_id = None
        else:
            self.url = None
            self.show_id = uri
        self.data = {}
        self.out = out
        return

    def __enter__(self):
        print(_('Get data…'), end='\r', file=self.out)
        self.retrieve_data()
        return self

    def __exit__(self, *args):
        pass

    def retrieve_data(self):
        if self.url:
            p = etree.HTML(requests.get(self.url, headers=self.headers).text)
            self.show_id = p.xpath('//meta[@property="og:url"]/@content')[0].split(',')[(-1)].split('.')[0]
        self.data = json.loads(requests.get(self.data_url.format(show=self.show_id), headers=self.headers).text)

    duration_r = re.compile('.*Duration: (\\d\\d):(\\d\\d):(\\d\\d.\\d\\d), .*')
    processd_r = re.compile('.* time=(\\d+.\\d\\d) .*')
    overwrite_r = re.compile(".*File '([^']+)' already exists.*")

    def save(self, target_path='~/Downloads', callback=lambda p, t, d, s: print(p, t, d, s), avconv_path='/usr/bin/avconv', verbose=False):
        if not os.path.isdir(os.path.expanduser(target_path)):
            raise Exception("Can't download and convert: target directory '{}' does not exists".format(target_path))

        def output_parser(output, env={}):
            if verbose:
                print(output, file=sys.stderr, end='')
                return
            duration_m = self.duration_r.match(output)
            if duration_m:
                h, m, s = duration_m.groups()
                env['duration'] = int(h) * 3600 + int(m) * 60 + float(s)
                env['start'] = time.time()
            elif 'duration' in env.keys():
                processd_m = self.processd_r.match(output)
                if processd_m:
                    pos = float(processd_m.groups()[0])
                    spt = int(time.time() - env['start'])
                    callback(pos, env['duration'], spt, env['start'])
                else:
                    overwrite_m = self.overwrite_r.match(output)
                    if overwrite_m:
                        path = overwrite_m.groups()[0]
                        raise Exception('Output file "{}" already exists in target directory.'.format(path))

        p = requests.get(list(filter(lambda x: x['format'] == 'm3u8-download', self.data['videos']))[0]['url'], headers=self.headers).text
        video_url = list(filter(lambda l: 'index_2' in l, p.split()))[0]
        dest_file = '{}_{}.mkv'.format(self.data['code_programme'], self.show_id)
        self.dest_file = os.path.join(os.path.expanduser(target_path), dest_file)
        p = subprocess.Popen([avconv_path, '-i', video_url] + self.avconv_args + [self.dest_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = io.TextIOWrapper(p.stdout)
        err = io.TextIOWrapper(p.stderr)
        while p.poll() == None:
            ret = select.select([out.fileno(), err.fileno()], [], [])
            for fd in ret[0]:
                if fd == out.fileno():
                    output_parser(out.readline())
                if fd == err.fileno():
                    output_parser(err.readline())
                    continue

        for line in out.read().split('\n'):
            output_parser(line)

        for line in err.read().split('\n'):
            output_parser(line)

        return

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def __getitem__(self, it):
        return self.data[it]

    def __setitem__(self, it, val):
        raise Exception('Movie data are immutables')


def get_term_size():
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return

        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass

    if not cr:
        cr = (
         env.get('LINES', 25), env.get('COLUMNS', 80))
    return (int(cr[1]), int(cr[0]))


def show_progress(position, total, spent, start):
    width = get_term_size()[0] * 0.6
    adv = position / total
    eta = int((time.time() - start) * total / position)
    print((_('Download and convert') + ': [{: <' + str(int(width)) + 's}] {:0.0%} ETA: {}s/{}s').format('#' * int(width * adv), adv, spent, eta), end='\r')


def main():
    from docopt import docopt
    try:
        args = docopt(__doc__)
        if args['gui']:
            try:
                import pluzz.qtpluzz
                pluzz.qtpluzz.main(args)
            except ImportError:
                raise Exception(_("Couldn't load Qt libraries. Impossible to run the GUI, sorry."))

        elif args['fetch']:
            if not args['<id>']:
                raise Exception(_('Missing URL!'))
            with PluzzMovie(args['<id>'], out=sys.stderr) as (m):
                print(_('Download and convert…'), end='\r', file=sys.stderr)
                m.save(args['--target'], callback=show_progress, avconv_path=args['--avconv'], verbose=args['--verbose'])
                print(('{: <' + str(int(get_term_size()[0])) + '}').format("Download and convertion done: '{}' saved".format(m.dest_file)))
        elif args['get']:
            if not args['<id>']:
                raise Exception(_('Missing URL!'))
            with PluzzMovie(args['<id>'], out=sys.stderr) as (m):
                if args['<key>'] and args['<key>'] in m.keys():
                    print((_('Showing {}:') + '               ').format(args['<key>']))
                    if m[args['<key>']]:
                        if isinstance(m[args['<key>']], collections.Iterable) and len(m[args['<key>']]) > 70:
                            for line in textwrap.wrap(m[args['<key>']]):
                                print('  {}'.format(line))

                        else:
                            print('  {}'.format(str(m[args['<key>']])))
                else:
                    print(_("List of all keys for the show: '{}'").format(m['titre']))
                    for k in m.keys():
                        print('  {}'.format(k))

        elif args['show']:
            with PluzzMovie(args['<id>'], out=sys.stderr) as (m):
                t = time.strftime(_('On %d %h %Y at %H:%M'), time.localtime(m['diffusion']['timestamp']))
                print(_("Summary of the show '{}'").format(m['titre']))
                print(_('        id: {:<30}').format(m['id']), end='')
                print(_('  id AEDRA: {:<30}').format(m['id_aedra']))
                print(_(' Broadcast: {:<30}').format(t), end='')
                print(_('    Length: {:<30}').format(m['duree']))
                print(_('     Genre: {:<30}').format(m['genre']), end='')
                print(_('    Season: {:<30}').format(m['saison']))
                print(_('   Website: {:<30}').format(m['url_site']))
                print(_('     Pluzz: {:<30}').format(m['url_reference']))
                print(_('   Channel: {:<30}').format(m['chaine']), end='')
                print(_('   Picture: {:<30}').format(m['image']))
                print(_('    Rights: {:<30}').format(m['droit']['csa']))
                print(_('      Crew:'))
                for p in m['personnes']:
                    print(_('{f:>24}: {n}, {p}').format(f=', '.join(p['fonctions']), p=p['prenom'], n=p['nom']))

                print(_('  Synopsis:'))
                for line in textwrap.wrap(m['synopsis'], initial_indent='    '):
                    print('  {}'.format(line))

        if args['list'] or args['search']:
            with PluzzSearch(out=sys.stderr) as (s):
                if args['search']:
                    args['--sort'] = 'relevance'
                items = ('<query>', '<category>', '<channel>', '--limit', '--sort',
                         '--page')
                list_args = dict((k.strip('<>-'), args[k]) for k in filter(lambda x: x in items, args.keys()))
                if list_args['category'] == 'help' or list_args['channel'] == 'help' or args['list'] and not list_args['category']:
                    print(_('Categories:'))
                    for cat in s.get_categories():
                        print('{:>20}'.format(cat))

                    print('')
                    print(_('Channels:'))
                    for cat in s.get_channels():
                        print('{:>20}'.format(cat))

                    return
                if list_args['category'] == 'all':
                    list_args['category'] = None
                if list_args['channel'] == 'all':
                    list_args['category'] = None
                if args['--image']:
                    for mm in s.list(**list_args):
                        print('{id:>12} -- {title:<40} {image}'.format(**mm))

                else:
                    for mm in s.list(**list_args):
                        print('{id:>12} -- {title:<40}'.format(**mm))

    except Exception as err:
        print('', file=sys.stderr)
        print(_('Error:'), err, file=sys.stderr)
        if args['--verbose']:
            import traceback
            traceback.print_exc()
        sys.exit(2)

    return


if __name__ == '__main__':
    main()