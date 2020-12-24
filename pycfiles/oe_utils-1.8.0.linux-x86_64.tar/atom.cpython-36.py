# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/views/atom.py
# Compiled at: 2020-03-25 06:12:47
# Size of source mod 2**32: 3949 bytes
import abc
from feedgen.feed import FeedGenerator

class AbstractAtomFeedView:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_current_atom_feed(self):
        """
        Retrieve the current atom feed.

        :return: JSON representation of the feed
        """
        pass

    @abc.abstractmethod
    def get_atom_feed(self):
        """
        Retrieve a feed identified by its id, identical to the source.

        :return: JSON representation of the feed
        """
        pass

    @abc.abstractmethod
    def get_atom_feed_entry(self):
        """
        Retrieve a feed entry identified by its id, identical to the source.

        :return: JSON representation of the feed entry
        """
        pass


class AtomFeedView(AbstractAtomFeedView):
    __doc__ = '\n    Class with pyramid support.\n\n    This is an implementation of the :class:`AbstractAtomFeedView` that adds a\n    generic methods in a pylons pyramid application\n    '
    __metaclass__ = abc.ABCMeta

    def __init__(self, request, atom_feed_manager, get_atom_feed_url, generate_atom_feed=None):
        """
        Functions that can be used in a pylons pyramid application.

        :param request:
        :param atom_feed_manager:
        object of class oe_daemonutils.data.data_manager.AtomFeedManager
        :param get_atom_feed_url:
        the route name of the pyramid application to retrieve the atom feed
        """
        self.request = request
        self.atom_feed_manager = atom_feed_manager
        self.get_atom_feed_url = get_atom_feed_url
        self.generate_atom_feed = generate_atom_feed if generate_atom_feed else self._generate_atom_feed

    def get_current_atom_feed(self):
        return self.request.route_url((self.get_atom_feed_url),
          id=(self.atom_feed_manager.current_feed_id))

    def get_atom_feed(self):
        feed_id = int(self.request.matchdict['id'])
        return self.generate_atom_feed(feed_id).atom_str(pretty=True)

    def get_atom_feed_entry(self):
        return self.atom_feed_manager.get_atom_feed_entry(int(self.request.matchdict['id']))

    def link_to_sibling(self, feed_id, sibling_type, atom_feed):
        """
        Adding previous or next links to the given feed.

        self._link_to_sibling(feed, 'previous', atom_feed)
        self._link_to_sibling(feed, 'next', atom_feed)

        :param feed_id: a feed_id
        :param sibling_type: 'previous' or 'next'
        :param atom_feed: an atom feed like `feedgen.feed.FeedGenerator`
        """
        sibling = self.atom_feed_manager.get_sibling_id(feed_id, sibling_type)
        if sibling:
            rel = 'prev-archive' if sibling_type == 'previous' else 'next-archive'
            atom_feed.link(href=self.request.route_url((self.get_atom_feed_url), id=sibling),
              rel=rel)

    def init_atom_feed(self, feed_id):
        """
        Initialise an atom feed `feedgen.feed.FeedGenerator`.

        :param feed_id: feed_id
        :return: an atom feed `feedgen.feed.FeedGenerator`
        """
        atom_feed = FeedGenerator()
        atom_feed.id(id=self.request.route_url((self.get_atom_feed_url), id=feed_id))
        atom_feed.link(href=self.request.route_url((self.get_atom_feed_url), id=feed_id),
          rel='self')
        atom_feed.language('nl-BE')
        self.link_to_sibling(feed_id, 'previous', atom_feed)
        self.link_to_sibling(feed_id, 'next', atom_feed)
        return atom_feed

    def _generate_atom_feed(self, feed_id):
        """
        Return a feed like `feedgen.feed.FeedGenerator`.

        The function can be overwritten when used in other applications.

        :param feed_id: feed_id
        :return: an atom feed `feedgen.feed.FeedGenerator`
        """
        atom_feed = self.init_atom_feed(feed_id)
        atom_feed.title('Feed')
        return atom_feed