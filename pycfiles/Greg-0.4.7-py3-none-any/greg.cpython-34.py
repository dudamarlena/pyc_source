# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/manolo/Scripts/Oggregator/greg/greg/greg.py
# Compiled at: 2014-06-13 10:20:39
# Size of source mod 2**32: 31929 bytes
import configparser, os, pickle, subprocess, sys, time, re, unicodedata, string
from itertools import filterfalse
from urllib.request import urlretrieve
from urllib.parse import urlparse
from urllib.error import URLError
import feedparser
try:
    import stagger
    from stagger.id3 import *
    staggerexists = True
except ImportError:
    staggerexists = False

try:
    from bs4 import BeautifulSoup
    beautifulsoupexists = True
except ImportError:
    beautifulsoupexists = False

config_filename_global = '/etc/greg.conf'

class Session:

    def __init__(self, args):
        self.args = args
        self.config_filename_user = self.retrieve_config_file()
        self.data_dir = self.retrieve_data_directory()
        self.data_filename = os.path.join(self.data_dir, 'data')
        self.feeds = configparser.ConfigParser()
        self.feeds.read(self.data_filename)
        self.config = configparser.ConfigParser()
        self.config.read([config_filename_global, self.config_filename_user])

    def list_feeds(self):
        """
        Output a list of all feed names
        """
        feeds = configparser.ConfigParser()
        feeds.read(self.data_filename)
        return feeds.sections()

    def retrieve_config_file(self):
        """
        Retrieve config file
        """
        try:
            if self.args['configfile']:
                return self.args['configfile']
        except KeyError:
            pass

        return os.path.expanduser('~/.config/greg/greg.conf')

    def retrieve_data_directory(self):
        """
        Retrieve the data directory
        Look first into config_filename_global
        then into config_filename_user. The latter takes preeminence.
        """
        args = self.args
        try:
            if args['datadirectory']:
                ensure_dir(args['datadirectory'])
                return args['datadirectory']
        except KeyError:
            pass

        config = configparser.ConfigParser()
        config.read([config_filename_global, self.config_filename_user])
        section = config.default_section
        data_path = config.get(section, 'Data directory', fallback='~/.local/share/greg')
        data_path_expanded = os.path.expanduser(data_path)
        ensure_dir(data_path_expanded)
        return os.path.expanduser(data_path_expanded)


class Feed:
    __doc__ = '\n    Calculate information about the current feed\n    '

    def __init__(self, session, feed, podcast):
        self.session = session
        self.args = session.args
        self.config = self.session.config
        self.name = feed
        if not podcast:
            self.podcast = parse_podcast(session.feeds[feed]['url'])
        else:
            self.podcast = podcast
        self.sync_by_date = self.has_date()
        self.willtag = self.will_tag()
        if self.willtag:
            self.defaulttagdict = self.default_tag_dict()
        self.mime = self.retrieve_mime()
        try:
            self.wentwrong = 'URLError' in str(self.podcast['bozo_exception'])
        except KeyError:
            self.wentwrong = False

        self.info = os.path.join(session.data_dir, feed)
        self.entrylinks, self.linkdates = parse_feed_info(self.info)

    def retrieve_config(self, value, default):
        """
        Retrieves a value (with a certain fallback) from the config files
        (looks first into config_filename_global
        then into config_filename_user. The latest takes preeminence)
        if the command line flag for the value is use,
        that overrides everything else
        """
        args = self.args
        name = self.name
        try:
            if args[value]:
                return args[value]
        except KeyError:
            pass

        section = name if self.config.has_section(name) else self.config.default_section
        answer = self.config.get(section, value, fallback=default)
        return answer

    def default_tag_dict(self):
        defaultoptions = self.config.defaults()
        tags = [[option.replace('tag_', ''), defaultoptions[option]] for option in defaultoptions if 'tag_' in option]
        return dict(tags)

    def retrieve_download_path(self):
        """
        Retrieves the download path (looks first into config_filename_global
        then into the [DEFAULT], then the [feed], section of
        config_filename_user. The latest takes preeminence)
        """
        section = self.name if self.config.has_section(self.name) else self.config.default_section
        download_path = self.config.get(section, 'Download directory', fallback='~/Podcasts')
        subdirectory = self.config.get(section, 'Create subdirectories', fallback='no')
        return [os.path.expanduser(download_path), subdirectory]

    def has_date(self):
        podcast = self.podcast
        session = self.session
        name = self.name
        try:
            test = podcast.feed.published_parsed
            sync_by_date = True
        except AttributeError:
            try:
                test = podcast.feed.updated_parsed
                sync_by_date = True
            except AttributeError:
                try:
                    test = podcast.entries[0].published_parsed
                    sync_by_date = True
                except (AttributeError, IndexError):
                    print("I cannot parse the time information of this feed.I'll use your current local time instead.", file=sys.stderr, flush=True)
                    sync_by_date = False

        if not sync_by_date:
            session.feeds[name]['date_info'] = 'not available'
            with open(session.data_filename, 'w') as (configfile):
                session.feeds.write(configfile)
        else:
            try:
                if session.feeds[name]['date_info'] == 'not available':
                    print("Either this feed has changed, or greg has improved, but we can now parse its time information. This is good, but it also means that (just this time) it's possible that you have missed some entries. You might do a 'greg check -f {}' to make sure that you're not missing out on anything.".format(name))
            except KeyError:
                pass

            session.feeds[name]['date_info'] = 'available'
            with open(session.data_filename, 'w') as (configfile):
                session.feeds.write(configfile)
        return sync_by_date

    def will_tag(self):
        """
        Check whether the feed should be tagged
        """
        wanttags = self.retrieve_config('Tag', 'no')
        if wanttags == 'yes':
            if staggerexists:
                willtag = True
            else:
                willtag = False
                print('You want me to tag {0}, but you have not installed the Stagger module. I cannot honour your request.'.format(self.name), file=sys.stderr, flush=True)
        else:
            willtag = False
        return willtag

    def how_many(self):
        """
        Ascertain where to start downloading, and how many entries.
        """
        if self.linkdates != []:
            currentdate = max(self.linkdates)
            stop = 12
        else:
            currentdate = [
             1, 1, 1, 0, 0]
            firstsync = self.retrieve_config('firstsync', '1')
            if firstsync == 'all':
                stop = 12
            else:
                stop = int(firstsync)
        return (
         currentdate, stop)

    def fix_linkdate(self, entry):
        """
        Give a date for the entry, depending on feed.sync_by_date
        Save it as feed.linkdate
        """
        if self.sync_by_date:
            try:
                entry.linkdate = list(entry.published_parsed)
                self.linkdate = list(entry.published_parsed)
            except AttributeError:
                try:
                    entry.linkdate = list(entry.updated_parsed)
                    self.linkdate = list(entry.updated_parsed)
                except AttributeError:
                    print("This entry doesn't seem to have a parseable date. I will use your local time instead.", file=sys.stderr, flush=True)
                    entry.linkdate = list(time.localtime())
                    self.linkdate = list(time.localtime())

        else:
            entry.linkdate = list(time.localtime())

    def retrieve_mime(self):
        """
        Check the mime-type to download
        """
        mime = self.retrieve_config('mime', 'audio')
        mimedict = {'number': mime}
        return parse_for_download(mimedict)

    def download_entry(self, entry):
        """
        Find entry link and download entry
        """
        downloadlinks = {}
        ignoreenclosures = self.retrieve_config('ignoreenclosures', 'no')
        if ignoreenclosures == 'no':
            for enclosure in entry.enclosures:
                if any([mimetype in enclosure['type'] for mimetype in self.mime]):
                    downloadlinks[urlparse(enclosure['href']).path.split('/')[(-1)]] = enclosure['href']
                    continue

        else:
            downloadlinks[urlparse(entry.link).query.split('/')[(-1)]] = entry.link
        for podname in downloadlinks:
            if podname not in self.entrylinks:
                try:
                    title = entry.title
                except:
                    title = podname

                try:
                    sanitizedsummary = htmltotext(entry.summary)
                    if sanitizedsummary == '':
                        sanitizedsummary = 'No summary available'
                except:
                    sanitizedsummary = 'No summary available'

                try:
                    placeholders = Placeholders(self, entry, downloadlinks[podname], podname, title, sanitizedsummary)
                    placeholders = check_directory(placeholders)
                    condition = filtercond(placeholders)
                    if condition:
                        print('Downloading {} -- {}'.format(title, podname))
                        download_handler(self, placeholders)
                        if self.willtag:
                            tag(placeholders)
                        if self.info:
                            with open(self.info, 'a') as (current):
                                current.write(''.join([podname, ' ',
                                 str(entry.linkdate), '\n']))
                    else:
                        print('Skipping {} -- {}'.format(title, podname))
                except URLError:
                    sys.exit('... something went wrong.Are you connected to the internet?')

                continue


class Placeholders:

    def __init__(self, feed, entry, link, filename, title, summary):
        self.feed = feed
        self.link = link
        self.filename = filename
        self.title = title
        self.filename_title = sanitize(title)
        try:
            self.podcasttitle = feed.podcast.title
        except AttributeError:
            self.podcasttitle = feed.name

        try:
            self.sanitizedsubtitle = htmltotext(feed.podcast.feed.subtitle)
            if self.sanitizedsubtitle == '':
                self.sanitizedsubtitle = 'No description'
        except AttributeError:
            self.sanitizedsubtitle = 'No description'

        self.entrysummary = summary
        self.filename_podcasttitle = sanitize(self.podcasttitle)
        self.name = feed.name
        self.date = tuple(entry.linkdate)

    def date_string(self):
        date_format = self.feed.retrieve_config('date_format', '%Y-%m-%d')
        return time.strftime(date_format, self.date)


_feedburner_date_pattern = re.compile('\\w+, (\\w+) (\\d{,2}), (\\d{4}) - (\\d{,2}):(\\d{2})')

def FeedburnerDateHandler(aDateString):
    months = {'January': 1,  'February': 2,  'March': 3,  'April': 4,  'May': 5,  'June': 6, 
     'July': 7,  'August': 8,  'September': 9,  'October': 10,  'November': 11, 
     'December': 12}
    try:
        month, day, year, hour, minute = _feedburner_date_pattern.search(aDateString).groups()
        return (
         int(year), int(months[month]),
         int(day), int(hour), int(minute), 0, 0, 0, 0)
    except AttributeError:
        return


feedparser.registerDateHandler(FeedburnerDateHandler)

def sanitize(data):
    sanestring = ''.join((x if x.isalnum() else '_') for x in unicodedata.normalize('NFKD', data) if x in string.printable)
    return sanestring


def ensure_dir(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        if not os.path.isdir(dirname):
            raise


def parse_podcast(url):
    """
    Try to parse podcast
    """
    try:
        podcast = feedparser.parse(url)
        wentwrong = 'urlopen' in str(podcast['bozo_exception'])
    except KeyError:
        wentwrong = False

    if wentwrong:
        sys.exit('I cannot check podcasts now.Are you connected to the internet?')
    return podcast


def htmltotext(data):
    if beautifulsoupexists:
        beautify = BeautifulSoup(data)
        sanitizeddata = beautify.get_text()
    else:
        sanitizeddata = data
    return sanitizeddata


def check_directory(placeholders):
    """
    Find out, and create if needed,
    the directory in which the feed will be downloaded
    """
    feed = placeholders.feed
    args = feed.args
    placeholders.directory = 'This very directory'
    placeholders.fullpath = os.path.join(placeholders.directory, placeholders.filename)
    try:
        if args['downloaddirectory']:
            ensure_dir(args['downloaddirectory'])
            placeholders.directory = args['downloaddirectory']
    except KeyError:
        pass

    download_path = os.path.expanduser(feed.retrieve_config('Download Directory', '~/Podcasts'))
    subdirectory = feed.retrieve_config('Create subdirectory', 'no')
    if 'no' in subdirectory:
        placeholders.directory = download_path
    elif 'yes' in subdirectory:
        subdnametemplate = feed.retrieve_config('subdirectory_name', '{podcasttitle}')
        subdname = substitute_placeholders(subdnametemplate, placeholders)
        placeholders.directory = os.path.join(download_path, subdname)
    ensure_dir(placeholders.directory)
    placeholders.fullpath = os.path.join(placeholders.directory, placeholders.filename)
    return placeholders


def parse_for_download(args):
    """
    Turn an argument such as 4, 6-8, 10 into a list such as [4,6,7,8,10]
    """
    single_arg = ''
    list_of_feeds = []
    for arg in args['number']:
        single_arg = ''.join([single_arg, ' ', arg])

    single_arg = single_arg.translate({32: None})
    for group in single_arg.split(sep=','):
        if '-' not in group:
            list_of_feeds.append(group)
        else:
            extremes = group.split(sep='-')
            list_of_feeds = list_of_feeds + [str(x) for x in range(eval(extremes[0]), eval(extremes[1]) + 1)]

    return list_of_feeds


def tag(placeholders):
    """
    Tag the file at podpath with the information in podcast and entry
    """
    template = placeholders.feed.retrieve_config('file_to_tag', '{filename}')
    filename = substitute_placeholders(template, placeholders)
    podpath = os.path.join(placeholders.directory, filename)
    tagdict = placeholders.feed.defaulttagdict
    feedoptions = placeholders.feed.config.options(placeholders.name)
    tags = [[option.replace('tag_', ''), placeholders.feed.config[placeholders.name][option]] for option in feedoptions if 'tag_' in option]
    if tags == []:
        tagdict = placeholders.feed.defaulttagdict
    else:
        for tag in tags:
            tagdict[tag[0]] = tag[1]

    for tag in tagdict:
        metadata = substitute_placeholders(tagdict[tag], placeholders)
        stagger.util.set_frames(podpath, {tag: metadata})


def filtercond(placeholders):
    template = placeholders.feed.retrieve_config('filter', 'True')
    condition = substitute_placeholders(template, placeholders)
    return eval(condition)


def get_date(line):
    date = eval(line.split(sep=' ', maxsplit=1)[1])
    return date


def transition(args, feed, feeds):
    if 'downloadfrom' in feeds[feed]:
        edit({'downloadfrom': eval(feeds[feed]['downloadfrom']),  'name': feed})
        DATA_DIR = retrieve_data_directory(args)
        DATA_FILENAME = os.path.join(DATA_DIR, 'data')
        feeds.remove_option(feed, 'downloadfrom')
        with open(DATA_FILENAME, 'w') as (configfile):
            feeds.write(configfile)


def download_handler(feed, placeholders):
    """
    Parse and execute the download handler
    """
    value = feed.retrieve_config('downloadhandler', 'greg')
    if value == 'greg':
        while os.path.isfile(placeholders.fullpath):
            placeholders.fullpath = placeholders.fullpath + '_'

        urlretrieve(placeholders.link, placeholders.fullpath)
    else:
        value_list = value.split()
        instruction_list = [substitute_placeholders(part, placeholders) for part in value_list]
        print(instruction_list)
        subprocess.call(instruction_list)


def download_entry(feed, entry):
    """
    Download all enclosures of an entry
    """
    downloadlinks = {}
    for enclosure in entry.enclosures:
        if any([mimetype in enclosure['type'] for mimetype in feed.mime]):
            downloadlinks[urlparse(enclosure['href']).path.split('/')[(-1)]] = enclosure['href']
            continue

    for podname in downloadlinks:
        if podname not in feed.entrylinks:
            try:
                title = entry.title
            except:
                title = podname

            try:
                sanitizedsummary = htmltotext(entry.summary)
                if sanitizedsummary == '':
                    sanitizedsummary = 'No summary available'
            except:
                sanitizedsummary = 'No summary available'

            try:
                placeholders = Placeholders(feed, entry, downloadlinks[podname], podname, title, sanitizedsummary)
                placeholders = check_directory(placeholders)
                condition = filtercond(placeholders)
                if condition:
                    print('Downloading {} -- {}'.format(title, podname))
                    download_handler(feed, placeholders)
                    if feed.willtag:
                        tag(placeholders)
                    if feed.info:
                        with open(feed.info, 'a') as (current):
                            current.write(''.join([podname, ' ',
                             str(feed.linkdate), '\n']))
                else:
                    print('Skipping {} -- {}'.format(title, podname))
            except URLError:
                sys.exit('... something went wrong.Are you connected to the internet?')

            continue


def parse_feed_info(infofile):
    """
    Take a feed file in .local/share/greg/data and return a list of links and
    of dates
    """
    entrylinks = []
    linkdates = []
    try:
        with open(infofile, 'r') as (previous):
            for line in previous:
                entrylinks.append(line.split(sep=' ')[0])
                linkdates.append(eval(line.split(sep=' ', maxsplit=1)[1]))

    except FileNotFoundError:
        pass

    return (entrylinks, linkdates)


def substitute_placeholders(inputstring, placeholders):
    """
    Take a string with placeholders, and return the strings with substitutions.
    """
    newst = inputstring.format(link=placeholders.link, filename=placeholders.filename, directory=placeholders.directory, fullpath=placeholders.fullpath, title=placeholders.title, filename_title=placeholders.filename_title, date=placeholders.date_string(), podcasttitle=placeholders.podcasttitle, filename_podcasttitle=placeholders.filename_podcasttitle, name=placeholders.name, subtitle=placeholders.sanitizedsubtitle, entrysummary=placeholders.entrysummary)
    return newst


def add(args):
    session = Session(args)
    if args['name'] in session.feeds.sections():
        sys.exit('You already have a feed with that name.')
    if args['name'] in ('all', 'DEFAULT'):
        sys.exit('greg uses {} for a special purpose.Please choose another name for your feed.'.format(args['name']))
    entry = {}
    for key, value in args.items():
        if value is not None and key != 'func' and key != 'name':
            entry[key] = value
            continue

    session.feeds[args['name']] = entry
    with open(session.data_filename, 'w') as (configfile):
        session.feeds.write(configfile)


def edit(args):
    session = Session(args)
    feed_info = os.path.join(session.data_dir, args['name'])
    if args['name'] not in session.feeds:
        sys.exit("You don't have a feed with that name.")
    for key, value in args.items():
        if value is not None:
            if key == 'url':
                session.feeds[args['name']][key] = str(value)
                with open(session.data_filename, 'w') as (configfile):
                    session.feeds.write(configfile)
        if value is not None and key == 'downloadfrom':
            try:
                dateinfo = session.feeds[args['name']]['date_info'] == 'not available'
            except KeyError:
                session.feeds[args['name']]['date_info'] = 'available'
                with open(session.data_filename, 'w') as (configfile):
                    session.feeds.write(configfile)
                dateinfo = False

            if dateinfo:
                print('{} has no date information that I can use.Using --downloadfrom might not have theresults that you expect.'.format(args['name']), file=sys.stderr, flush=True)
            line = ' '.join(['currentdate', str(value), '\n'])
            try:
                with open(feed_info, 'r') as (previous):
                    current = list(filterfalse(lambda line: value < get_date(line), previous))
                    if current == []:
                        if dateinfo:
                            current = [
                             line]
                with open(feed_info, 'w') as (currentfile):
                    currentfile.writelines(current)
            except FileNotFoundError:
                with open(feed_info, 'w') as (currentfile):
                    currentfile.write(line)

            continue


def remove(args):
    """
    Remove the feed given in <args>
    """
    session = Session(args)
    if args['name'] not in session.feeds:
        sys.exit("You don't have a feed with that name.")
    inputtext = 'Are you sure you want to remove the {}  feed? (y/N) '.format(args['name'])
    reply = input(inputtext)
    if reply != 'y' and reply != 'Y':
        return 0
    session.feeds.remove_section(args['name'])
    with open(session.data_filename, 'w') as (configfile):
        session.feeds.write(configfile)
    try:
        os.remove(os.path.join(session.data_dir, args['name']))
    except FileNotFoundError:
        pass


def info(args):
    session = Session(args)
    if 'all' in args['names']:
        feeds = session.list_feeds()
    else:
        feeds = args['names']
    for feed in feeds:
        pretty_print(session, feed)


def pretty_print(session, feed):
    print()
    feed_info = os.path.join(session.data_dir, feed)
    entrylinks, linkdates = parse_feed_info(feed_info)
    print(feed)
    print('-' * len(feed))
    print(''.join(['    url: ', session.feeds[feed]['url']]))
    if linkdates != []:
        print(''.join(['    Next sync will download from: ',
         time.strftime('%d %b %Y %H:%M:%S', tuple(max(linkdates))), '.']))


def list_for_user(args):
    session = Session(args)
    for feed in session.list_feeds():
        print(feed, end=' ')

    print()


def sync(args):
    """
    Implement the 'greg sync' command
    """
    import operator
    session = Session(args)
    if 'all' in args['names']:
        targetfeeds = session.list_feeds()
    else:
        targetfeeds = []
        for name in args['names']:
            if name not in session.feeds:
                print("You don't have a feed called {}.".format(name), file=sys.stderr, flush=True)
            else:
                targetfeeds.append(name)

    for target in targetfeeds:
        feed = Feed(session, target, None)
        if not feed.wentwrong:
            try:
                title = feed.podcast.target.title
            except AttributeError:
                title = target

            print('Checking', title, end='...\n')
            currentdate, stop = feed.how_many()
            entrycounter = 0
            entries_to_download = []
            for entry in feed.podcast.entries:
                feed.fix_linkdate(entry)
                if entry.linkdate > currentdate:
                    if entrycounter < stop:
                        entries_to_download.append(entry)
                entrycounter += 1

            entries_to_download.sort(key=operator.attrgetter('linkdate'), reverse=False)
            for entry in entries_to_download:
                download_entry(feed, entry)

            print('Done')
        else:
            msg = ''.join(['I cannot sync ', feed,
             ' just now. Are you connected to the internet?'])
            print(msg, file=sys.stderr, flush=True)


def check(args):
    """
    Implement the 'greg check' command
    """
    session = Session(args)
    if str(args['url']) != 'None':
        url = args['url']
        name = 'DEFAULT'
    else:
        try:
            url = session.feeds[args['feed']]['url']
            name = args['feed']
        except KeyError:
            sys.exit("You don't appear to have a feed with that name.")

    podcast = parse_podcast(url)
    for entry in enumerate(podcast.entries):
        listentry = list(entry)
        print(listentry[0], end=': ')
        try:
            print(listentry[1]['title'], end=' (')
        except:
            print(listentry[1]['link'], end=' (')

        try:
            print(listentry[1]['updated'], end=')')
        except:
            print('', end=')')

        print()

    dumpfilename = os.path.join(session.data_dir, 'feeddump')
    with open(dumpfilename, mode='wb') as (dumpfile):
        dump = [
         name, podcast]
        pickle.dump(dump, dumpfile)


def download(args):
    """
    Implement the 'greg download' command
    """
    session = Session(args)
    issues = parse_for_download(args)
    if issues == ['']:
        sys.exit('You need to give a list of issues, of the form a, b-c, d...')
    dumpfilename = os.path.join(session.data_dir, 'feeddump')
    if not os.path.isfile(dumpfilename):
        sys.exit('You need to run greg check<feed> before using greg download.')
    with open(dumpfilename, mode='rb') as (dumpfile):
        dump = pickle.load(dumpfile)
    try:
        feed = Feed(session, dump[0], dump[1])
    except Exception:
        sys.exit('... something went wrong.Are you sure your last greg check went well?')

    for number in issues:
        entry = dump[1].entries[eval(number)]
        feed.info = []
        feed.entrylinks = []
        feed.fix_linkdate(entry)
        feed.download_entry(entry)