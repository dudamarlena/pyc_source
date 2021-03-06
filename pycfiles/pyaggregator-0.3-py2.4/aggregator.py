# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyaggregator/aggregator.py
# Compiled at: 2007-05-10 02:57:10
import feedparser
from datetime import datetime
import time, sys, logging

class Aggregator(object):
    __module__ = __name__

    def __init__(self, **options):
        self.options = options
        self.user_agent = options.get('user_agent', 'pyaggregator/0.1')
        self.log = options.get('log', None)
        self.verbose = options.get('verbose', False)
        if not self.log:
            self.log = logging.getLogger('pyaggregator/%d' % (hash(self),))
            self.log.propagate = False
            if self.verbose:
                self.log.level = logging.DEBUG
            else:
                self.log.level = logging.WARNING
            self.log.addHandler(logging.StreamHandler(sys.stderr))
        self.reraiseentryexceptions = options.get('reraiseentryexceptions', False)
        self.tags = {}
        return

    def process_feed(self, feed):
        self.log.info('Processing feed: %s', feed.feed_url)
        self.log.debug('Feed %s last checked at: %s', feed.feed_url, feed.last_checked)
        feed.last_checked = datetime.now()
        feedparser_options = {'agent': self.user_agent, 'etag': feed.etag}
        if feed.last_modified:
            feedparser_options['modified'] = feed.last_modified.timetuple()
        parsed_data = feedparser.parse(feed.feed_url, **feedparser_options)
        if 'status' in parsed_data:
            self.log.info('Feed %s status: %s', feed.feed_url, parsed_data.status)
            self.handle_status(feed, parsed_data.status, parsed_data)
            if parsed_data.status == 301:
                self.log.warning('Feed %s permanently (301) moved to %s', feed.feed_url, parsed_data.href)
            if parsed_data.status == 302:
                self.log.debug('Feed %s temporarily (302) moved to %s', feed.feed_url, parsed_data.href)
            if parsed_data.status == 304:
                self.log.debug('Feed %s unchanged', feed.feed_url)
                return False
            if parsed_data.status == 410:
                self.log.error('Feed %s has gone away (410)', feed.feed_url)
                return False
            if parsed_data.status >= 400:
                self.log.warning('Feed %s has error status %s', feed.feed_url, parsed_data.status)
                return False
        feed.etag = parsed_data.get('etag', '')
        feed.title = parsed_data.feed.get('title', '')
        feed.description = parsed_data.feed.get('tagline', '')
        feed.link = parsed_data.feed.get('link', '')
        posts = self.existing_posts_for_entries(feed, parsed_data.entries)
        updated = False
        for entry in parsed_data.entries:
            try:
                entry_updated = self.process_entry(feed, entry, posts, parsed_data)
                updated = updated or entry_updated
            except:
                self.log.warning('Entry %s could not be processed', entry.link)
                if self.reraiseentryexceptions:
                    raise

        last_modified = self.feed_last_modified(feed, parsed_data, updated)
        if last_modified:
            feed.last_modified = last_modified
        feed.save()
        self.post_process_feed(feed, parsed_data)
        return updated

    def process_entry(self, feed, entry, posts, parsed_data):
        """ Process a post in a feed and saves it in the DB if necessary.
        """
        postdata = self.get_entry_data(entry, parsed_data, feed)
        self.log.info('Considering entry: %s', postdata['link'])
        self.log.debug('%s - title: %s', postdata['link'], postdata['title'])
        self.log.debug('%s - guid: %s', postdata['link'], postdata['guid'])
        if postdata['guid'] in posts:
            post = posts[postdata['guid']]
            if not self.has_entry_changed(post, postdata, parsed_data):
                self.log.info('Entry %s exists, and is unchanged', postdata['link'])
                return False
            self.log.info('Entry %s exists, but is changed, updating', postdata['link'])
            if not postdata['date_modified']:
                postdata['date_modified'] = post.date_modified
            for (k, v) in postdata.items():
                setattr(post, k, v)

        else:
            self.log.info('Entry %s is a new entry', postdata['link'])
            postdata['date_modified'] = self.entry_last_modified(feed, postdata, entry, parsed_data)
            postdata['date_created'] = postdata['date_modified']
            post = self.create_post(**postdata)
        post.save()
        self.post_process_entry(post, feed, entry, posts, parsed_data)
        return True

    def create_post(self, **kw):
        raise RuntimeError

    def posts_for_guids(self, feed, guids):
        raise RuntimeError

    def handle_status(self, feed, status, parsed_data):
        pass

    def existing_posts_for_entries(self, feed, entries):
        guids = []
        for entry in entries:
            guid = self.guid_for_entry(feed, entry)
            if guid:
                guids.append(guid)

        return dict([ (post.guid, post) for post in self.posts_for_guids(feed, guids) ])

    def entry_last_modified(self, feed, postdata, entry, parsed_data):
        if postdata['date_modified']:
            return postdata['date_modified']
        if parsed_data.feed.has_key('modified_parsed'):
            return self.tuple_to_datetime(parsed_data.feed.modified_parsed)
        if parsed_data.has_key('modified'):
            return self.tuple_to_datetime(parsed_data.modified)
        return datetime.datetime.now()

    def feed_last_modified(self, feed, parsed_data, updated):
        last_modified = None
        try:
            last_modified = self.tuple_to_datetime(parsed_data.feed.updated_parsed)
        except AttributeError:
            pass

        if not feed.last_modified:
            updated = True
        if not last_modified:
            for entry in parsed_data.entries:
                if hasattr(entry, 'updated_parsed'):
                    e_updated = self.tuple_to_datetime(entry.updated_parsed)
                    if not last_modified or e_updated > last_modified:
                        last_modified = e_updated

        if not last_modified and updated:
            last_modified = datetime.now()
        return last_modified

    def guid_for_entry(self, feed, entry):
        if entry.get('id', ''):
            return entry.get('id', '')
        if entry.get('guid', ''):
            return entry.get('guid', '')
        if entry.link:
            return entry.link
        if entry.title:
            return entry.title

    def tuple_to_datetime(self, timetuple):
        return datetime.fromtimestamp(time.mktime(timetuple))

    def has_entry_changed(self, post, postdata, parsed_data):
        if post.content != postdata['content']:
            return True
        if postdata['date_modified'] and post.date_modified != postdata['date_modified']:
            print post.date_modified
            print postdata['date_modified']
            sys.exit(1)
            return True
        return False

    def get_entry_data(self, entry, parsed_data, feed):
        try:
            link = entry.link
        except AttributeError:
            link = feed.link

        try:
            title = entry.title
        except AttributeError:
            title = link

        guid = self.guid_for_entry(feed, entry)
        if entry.has_key('author_detail'):
            author = entry.author_detail.get('name', '')
            author_email = entry.author_detail.get('email', '')
        else:
            (author, author_email) = ('', '')
        if not author:
            author = entry.get('author', entry.get('creator', ''))
        if not author_email:
            author_email = 'nospam@nospam.com'
        try:
            content = entry.content[0].value
        except:
            content = entry.get('summary', entry.get('description', ''))

        if entry.has_key('modified_parsed'):
            date_modified = self.tuple_to_datetime(entry.modified_parsed)
        else:
            date_modified = None
        comments_url = entry.get('comments', '')
        return dict(title=title, link=link, content=content, guid=guid, date_modified=date_modified or post.date_modified, author=author, author_email=author_email, comments_url=comments_url, feed_id=feed.feed_id)

    def post_process_feed(self, feed, parsed_data):
        funcnames = [ a for a in dir(self) if a.startswith('process_feed_') ]
        for funcname in funcnames:
            func = getattr(self, funcname)
            func(feed, parsed_data)

    def post_process_entry(self, post, feed, entry, posts, parsed_data):
        funcnames = [ a for a in dir(self) if a.startswith('process_entry_') ]
        for funcname in funcnames:
            func = getattr(self, funcname)
            func(post, feed, entry, posts, parsed_data)

    def process_entry_tags(self, post, feed, entry, posts, parsed_data):
        if not hasattr(self, 'set_tags_for_post'):
            return
        if not hasattr(self, 'get_or_create_tag'):
            return
        entry_tags = self.get_tags(entry)
        self.log.debug('%s - tags: %s', post.link, [ tag.name for tag in entry_tags ])
        self.set_tags_for_post(post, entry_tags)

    def get_tags(self, entry):
        """Returns a list of tag objects from an entry."""
        if 'tags' not in entry:
            return []
        entry_tags = []
        for tag in entry.tags:
            if tag.label != None:
                terms = tag.label
            else:
                terms = tag.term
            terms = terms.strip()
            if ',' in terms or '/' in terms:
                terms = terms.replace(',', '/').split('/')
            else:
                terms = [
                 terms]
            for tagname in terms:
                tagname = tagname.lower()
                while '  ' in tagname:
                    tagname = tagname.replace('  ', ' ')

                if not tagname or tagname == ' ':
                    continue
                if tagname not in self.tags:
                    tagobj = self.get_or_create_tag(tagname)
                    self.tags[tagname] = tagobj
                entry_tags.append(self.tags[tagname])

        return entry_tags

    def process_entry_enclosures(self, post, feed, entry, posts, parsed_data):
        if not hasattr(self, 'save_enclosure'):
            return
        if not hasattr(self, 'clear_enclosures_for_post'):
            return
        self.clear_enclosures_for_post(post)
        if 'enclosures' in entry:
            for e in entry.enclosures:
                ed = dict(url=e.href, size=e.length, type=e.type, post=post)
                ed['date_created'] = post.date_created
                ed['date_modified'] = post.date_modified
                if hasattr(entry, 'itunes_duration'):
                    ed['duration'] = 0
                self.save_enclosure(**ed)