# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/db/sql/lookup.py
# Compiled at: 2019-08-05 00:35:42
from sqlalchemy import func
from .model import session, get_model, put_multi, ForeignKey, String, Integer, ModelBase

class CTRefCount(ModelBase):
    target = ForeignKey()
    reference = String()
    count = Integer(default=0)

    def mydata(self):
        return {'target': self.target.urlsafe(), 
           'reference': self.reference, 
           'count': self.count}

    def inc(self, amount=1):
        self.count += amount

    def dec(self, amount=1):
        self.count -= amount

    def refresh(self):
        fname, fkey = self.reference.split('.')
        fmod = get_model(fname)
        self.count = fmod.query(getattr(fmod, fkey) == self.target).count()


def ref_counter(target, reference, session=session):
    return CTRefCount.query(CTRefCount.target == target, CTRefCount.reference == reference, session=session).get() or CTRefCount(target=target, reference=reference)


def inc_counter(target, reference, amount=1, session=session):
    rc = ref_counter(target, reference, session)
    rc.inc(amount)
    return rc


def dec_counter(target, reference, amount=1, session=session):
    rc = ref_counter(target, reference, session)
    rc.dec(amount)
    return rc


def refresh_counter(target, reference, session=session):
    rc = ref_counter(target, reference, session)
    rc.refresh()
    return rc


def refcount_subq(reference, session=session):
    if reference.count('.') == 2:
        rp = reference.split('.')
        t1 = get_model(rp[1])
        t2 = get_model(rp[2])
        tlink = getattr(t1, rp[2])
        return session.query(CTRefCount.target, CTRefCount.count, tlink).filter(CTRefCount.reference == ('.').join(rp[:2])).join(t1, CTRefCount.target == t1.key).join(t2, t2.key == tlink).group_by(tlink).with_entities(t2.key.label('target'), func.sum(CTRefCount.count).label('count')).subquery()
    return session.query(CTRefCount.target, CTRefCount.count).filter(CTRefCount.reference == reference).subquery()