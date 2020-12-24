# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange_django/models.py
# Compiled at: 2011-05-12 16:13:31
import datetime
try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.db import models

class DBHash(models.Model):
    """
    DBHash represents first level item in multihash, e.g. hash with its own
    items, that may be accessed by key as item of multihash object.
    """
    dbname = models.CharField(help_text='Name of multihash database.', max_length=100, db_index=True)
    key = models.CharField(help_text='Hash key.', max_length=100, db_index=True)
    mtime = models.DateTimeField(help_text='Hash modification time.', auto_now_add=True)

    class Meta:
        unique_together = (('dbname', 'key'), )

    def __unicode__(self):
        return '%s:%s' % (self.dbname, self.key)

    def __len__(self):
        return self.items.all().count()

    def __getitem__(self, key):
        try:
            return pickle.loads(str(self.items.get(key=key).value))
        except DBHashItem.DoesNotExist:
            raise KeyError(key)

    def __setitem__(self, key):
        raise RuntimeError('Hash is read only')

    def __iter__(self):
        for item in self.items.all():
            yield item.key

    def __contains__(self, item):
        return self.items.filter(key=item).count() > 0

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def clear_items(self):
        self.items.all().delete()
        self.mtime = datetime.datetime.now()

    def update_items(self, newhash):
        if isinstance(newhash, dict):
            newhash = newhash.items()
        for key, value in newhash:
            try:
                record = self.items.get(key=key)
                record.value = pickle.dumps(value)
            except DBHashItem.DoesNotExist:
                record = self.items.create(key=key, value=pickle.dumps(value))

            record.save()

        self.mtime = datetime.datetime.now()

    def set_items(self, newhash):
        if isinstance(newhash, dict):
            newhash = newhash.items()
        newhash = [ (key, pickle.dumps(value)) for key, value in newhash ]
        newhash.sort()
        oldhash = [ (x.key, x.value) for x in self.items.all() ]
        oldhash.sort()
        i = 0
        while i < max(len(newhash), len(oldhash)):
            if i < len(newhash):
                nkey, nval = newhash[i]
            else:
                nkey = nval = None
                kdiff = 1
            if i < len(oldhash):
                okey, oval = oldhash[i]
            else:
                okey = oval = None
                kdiff = -1
            if nkey and okey:
                kdiff = cmp(nkey, okey)
            if kdiff == 0:
                if nval != oval:
                    item = self.items.get(key=okey)
                    item.value = nval
                    item.save()
                i += 1
            elif kdiff < 0:
                item = self.items.create(key=nkey, value=nval)
                item.save()
                oldhash.insert(i, (nkey, nval))
                i += 1
            elif kdiff > 0:
                self.items.filter(key=okey).delete()
                del oldhash[i]

        self.mtime = datetime.datetime.now()
        return

    def delete_items(self, keys):
        for k in keys:
            self.items.filter(key=k).delete()

        self.mtime = datetime.datetime.now()


class DBHashItem(models.Model):
    hash = models.ForeignKey(DBHash, db_index=True, related_name='items')
    key = models.CharField(max_length=1000, db_index=True)
    value = models.TextField()

    class Meta:
        unique_together = (('hash', 'key'), )

    def __unicode__(self):
        return self.key