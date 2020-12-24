# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sdb/db/sequence.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 8223 bytes
from boto.exception import SDBResponseError
from boto.compat import six

class SequenceGenerator(object):
    __doc__ = 'Generic Sequence Generator object, this takes a single\n    string as the "sequence" and uses that to figure out\n    what the next value in a string is. For example\n    if you give "ABC" and pass in "A" it will give you "B",\n    and if you give it "C" it will give you "AA".\n\n    If you set "rollover" to True in the above example, passing\n    in "C" would give you "A" again.\n\n    The Sequence string can be a string or any iterable\n    that has the "index" function and is indexable.\n    '
    __name__ = 'SequenceGenerator'

    def __init__(self, sequence_string, rollover=False):
        """Create a new SequenceGenerator using the sequence_string
        as how to generate the next item.

        :param sequence_string: The string or list that explains
        how to generate the next item in the sequence
        :type sequence_string: str,iterable

        :param rollover: Rollover instead of incrementing when
        we hit the end of the sequence
        :type rollover: bool
        """
        self.sequence_string = sequence_string
        self.sequence_length = len(sequence_string[0])
        self.rollover = rollover
        self.last_item = sequence_string[(-1)]
        self.__name__ = "%s('%s')" % (self.__class__.__name__, sequence_string)

    def __call__(self, val, last=None):
        """Get the next value in the sequence"""
        if val is None or len(val) < self.sequence_length:
            return self.sequence_string[0]
        last_value = val[-self.sequence_length:]
        if not self.rollover and last_value == self.last_item:
            val = '%s%s' % (self(val[:-self.sequence_length]), self._inc(last_value))
        else:
            val = '%s%s' % (val[:-self.sequence_length], self._inc(last_value))
        return val

    def _inc(self, val):
        """Increment a single value"""
        assert len(val) == self.sequence_length
        return self.sequence_string[((self.sequence_string.index(val) + 1) % len(self.sequence_string))]


def increment_by_one(cv=None, lv=None):
    if cv is None:
        return 0
    return cv + 1


def double(cv=None, lv=None):
    if cv is None:
        return 1
    return cv * 2


def fib(cv=1, lv=0):
    """The fibonacci sequence, this incrementer uses the
    last value"""
    if cv is None:
        cv = 1
    if lv is None:
        lv = 0
    return cv + lv


increment_string = SequenceGenerator('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

class Sequence(object):
    __doc__ = 'A simple Sequence using the new SDB "Consistent" features\n    Based largly off of the "Counter" example from mitch garnaat:\n    http://bitbucket.org/mitch/stupidbototricks/src/tip/counter.py'

    def __init__(self, id=None, domain_name=None, fnc=increment_by_one, init_val=None):
        """Create a new Sequence, using an optional function to
        increment to the next number, by default we just increment by one.
        Every parameter here is optional, if you don't specify any options
        then you'll get a new SequenceGenerator with a random ID stored in the
        default domain that increments by one and uses the default botoweb
        environment

        :param id: Optional ID (name) for this counter
        :type id: str

        :param domain_name: Optional domain name to use, by default we get this out of the
            environment configuration
        :type domain_name:str

        :param fnc: Optional function to use for the incrementation, by default we just increment by one
            There are several functions defined in this module.
            Your function must accept "None" to get the initial value
        :type fnc: function, str

        :param init_val: Initial value, by default this is the first element in your sequence,
            but you can pass in any value, even a string if you pass in a function that uses
            strings instead of ints to increment
        """
        self._db = None
        self._value = None
        self.last_value = None
        self.domain_name = domain_name
        self.id = id
        if init_val is None:
            init_val = fnc(init_val)
        if self.id is None:
            import uuid
            self.id = str(uuid.uuid4())
        self.item_type = type(fnc(None))
        self.timestamp = None
        if isinstance(fnc, six.string_types):
            from boto.utils import find_class
            fnc = find_class(fnc)
        self.fnc = fnc
        if not self.val:
            self.val = init_val

    def set(self, val):
        """Set the value"""
        import time
        now = time.time()
        expected_value = []
        new_val = {}
        new_val['timestamp'] = now
        if self._value is not None:
            new_val['last_value'] = self._value
            expected_value = ['current_value', str(self._value)]
        new_val['current_value'] = val
        try:
            self.db.put_attributes(self.id, new_val, expected_value=expected_value)
            self.timestamp = new_val['timestamp']
        except SDBResponseError as e:
            if e.status == 409:
                raise ValueError('Sequence out of sync')
            else:
                raise

    def get(self):
        """Get the value"""
        val = self.db.get_attributes(self.id, consistent_read=True)
        if val:
            if 'timestamp' in val:
                self.timestamp = val['timestamp']
            if 'current_value' in val:
                self._value = self.item_type(val['current_value'])
            if 'last_value' in val:
                if val['last_value'] is not None:
                    self.last_value = self.item_type(val['last_value'])
        return self._value

    val = property(get, set)

    def __repr__(self):
        return "%s('%s', '%s', '%s.%s', '%s')" % (
         self.__class__.__name__,
         self.id,
         self.domain_name,
         self.fnc.__module__, self.fnc.__name__,
         self.val)

    def _connect(self):
        """Connect to our domain"""
        if not self._db:
            import boto
            sdb = boto.connect_sdb()
            if not self.domain_name:
                self.domain_name = boto.config.get('DB', 'sequence_db', boto.config.get('DB', 'db_name', 'default'))
            try:
                self._db = sdb.get_domain(self.domain_name)
            except SDBResponseError as e:
                if e.status == 400:
                    self._db = sdb.create_domain(self.domain_name)
                else:
                    raise

        return self._db

    db = property(_connect)

    def next(self):
        self.val = self.fnc(self.val, self.last_value)
        return self.val

    def delete(self):
        """Remove this sequence"""
        self.db.delete_attributes(self.id)