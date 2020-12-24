# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/data/data_managers.py
# Compiled at: 2020-03-25 06:12:47
# Size of source mod 2**32: 8089 bytes
from oe_utils.data.data_transfer_objects import ResultDTO
from oe_utils.data.models import Wijziging

class DataManager(object):
    __doc__ = 'A datamanager base class.'

    @staticmethod
    def process_ranged_query(query, result_range):
        """
        Create a query with limit and offset.

        :param query: the query to be processed
        :param result_range: :class: 'oe_utils.range_parser.Range'
        :return: :class:`oe_utils.data.data_transfer_objects.ResultDTO`
        """
        total = query.count()
        if result_range is not None:
            data = query.offset(result_range.start).limit(result_range.get_page_size()).all()
        else:
            data = query.all()
        return ResultDTO(data, total)

    @staticmethod
    def ordered_result_list(query, model_type, sortlist):
        for sorttuple in sortlist:
            if hasattr(model_type, sorttuple[0]):
                attr = getattr(model_type, sorttuple[0])
                query = query.order_by(attr.asc()) if sorttuple[1] == 'asc' else query.order_by(attr.desc())

        return query

    def __init__(self, session, cls):
        """
        Create a datamanager for a specific model class.

        :param session: a db session
        :param cls: the class of the objects to manage
        :return:
        """
        if not session.autoflush:
            raise ValueError('Session autoflush must be True.')
        self.session = session
        self.cls = cls

    def get_one(self, object_id):
        """
        Retrieve an object by its object_id, raises when not found.

        :param object_id: the objects id.
        :return: the requested object
        :raises: :class: NoResultFound when the object could not be found
        """
        return self.session.query(self.cls).filter_by(id=object_id).one()

    def get_one_for_update(self, object_id):
        """
        Retrieve an object by its object_id and locks the row.

        Does a select for update on the row,
        results in row level lock for the duration of the transaction

        :param object_id: the objects id.
        :return: the requested object
        :raises: :class: NoResultFound when the object could not be found
        """
        return self.session.query(self.cls).with_for_update().filter_by(id=object_id).one()

    def get(self, object_id, cls=None):
        """
        Retrieve an object by its object_id or None when not found.

        :param: object_id: the objects id.
        :param: cls: the objects class,
        if None use the default class from the datamanager
        :return: the requested object or None if not found
        """
        cls = self.cls if cls is None else cls
        return self.session.query(cls).get(object_id)

    def get_for_update(self, object_id, cls=None):
        """
        Retrieve an object by its object_id and locks the row.

        Does a select for update on the row,
        results in row level lock for the duration of the transaction

        :param: object_id: the objects id.
        :param: cls: the objects class,
        if None use the default class from the datamanager
        :return: the requested object or None if not found
        """
        cls = self.cls if cls is None else cls
        return self.session.query(cls).with_for_update().get(object_id)

    def delete(self, object_id):
        """
        Delete an object by its id.

        :param object_id: the objects id.
        :return: the deleted object
        :raises: :class: NoResultFound when the object could not be found
        """
        obj = self.session.query(self.cls).filter_by(id=object_id).one()
        self.session.delete(obj)
        return obj

    def save(self, obj):
        """
        Save an object.

        :param obj: the object
        :return: the saved object
        """
        if obj not in self.session:
            self.session.add(obj)
        else:
            obj = self.session.merge(obj)
        self.session.flush()
        self.session.refresh(obj)
        return obj


class FeedArchiveNotFound(Exception):
    pass


class AtomFeedManager(object):
    __doc__ = 'A data manager for feeds.'

    def __init__(self, session, feed_entries_per_page, feedentry_model):
        """
        Create an atom feed manager.

        :param session: a db session
        :param feed_repository: a repository to store the archived feeds
        """
        self.session = session
        self.feedentry_model = feedentry_model
        self._current_feed = None
        self.feed_entries_per_page = feed_entries_per_page

    def _get_max_min(self):
        return self.session.execute('\n            SELECT max(feed_id), min(feed_id) FROM (\n            SELECT (row_number () OVER (ORDER BY id) -1) / {per_page} AS "feed_id"\n            FROM feedentries\n            ) AS "feed_ids" '.format(per_page=(self.feed_entries_per_page))).fetchall()[0]

    @property
    def current_feed_id(self):
        max, min = self._get_max_min()
        if self._current_feed is None:
            self._current_feed = max
        return self._current_feed

    def get_sibling_id(self, feed_id, sibling_type):
        """
        Get a previous/next sibling from a feed.

        :param feed_id: id of the feed
        :param sibling_type: sibling type ('previous', 'next')
        :return: the sibling
        """
        max, min = self._get_max_min()
        if sibling_type == 'previous':
            if feed_id - 1 >= min:
                return feed_id - 1
            else:
                return
        else:
            if sibling_type == 'next':
                if feed_id + 1 <= max:
                    return feed_id + 1
                else:
                    return
            else:
                raise Exception('Unhandled sibling relation type')

    def save_object(self, obj):
        """
        Save an object to the db.

        :param obj: the object to save
        :return: the saved object
        """
        self.session.add(obj)
        self.session.flush()
        return obj

    def get_atom_feed_entry(self, feedentry_id):
        """
        Get a specific feed entry.

        :param feedentry_id: id of the feed entry to retrieve
        :return: the feed entry
        """
        return self.session.query(self.feedentry_model).filter(self.feedentry_model.id == feedentry_id).one()

    def get_feed_entries_where_feed_id(self, feed_id):
        """
        Get all entries linked to a feed_id.

        :return: feed entries of one feed_id (page)
        """
        return self.session.execute('\n            SELECT * FROM (\n            SELECT *, (row_number () over (order by id) -1) / {per_page} as "feed_id"\n            FROM feedentries order by id\n            ) f\n            WHERE feed_id = {feed_id} '.format(per_page=(self.feed_entries_per_page),
          feed_id=feed_id)).fetchall()

    def get_all_entries(self):
        """
        Get all entries with generated feed_id column.

        :return: all entries with feed_id column
        """
        return self.session.execute('\n            SELECT *, (row_number () over (order by id) -1) / {per_page} as "feed_id"\n            FROM feedentries\n            ORDER by id '.format(per_page=(self.feed_entries_per_page))).fetchall()


class AuditManager(DataManager):
    __doc__ = 'A data manager for audit revisions.'

    def __init__(self, session):
        super(AuditManager, self).__init__(session, Wijziging)
        self.session = session

    @staticmethod
    def create_revision():
        """
        Create a new revision object.

        :return: new revision object
        """
        return Wijziging()