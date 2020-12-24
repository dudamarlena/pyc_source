# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/test/schema/schema_001.py
# Compiled at: 2007-03-21 14:34:39
"""Test schema."""
from schevo.schema import *
schevo.schema.prep(locals())
from schevo import error
from schevo.test import raises

class AlphaAlpha(E.Entity):
    """Referred to by other classes, and can also optionally refer to
    self."""
    __module__ = __name__
    beta = f.integer()
    alpha_alpha = f.entity('AlphaAlpha', required=False)
    _key(beta)
    _hidden = True

    def __unicode__(self):
        return 'beta %i' % self.beta


class AlphaBravo(E.Entity):
    """Has a reference to an AlphaAlpha, such that when that
    AlphaAlpha is deleted, this AlphaBravo will also be deleted."""
    __module__ = __name__
    alpha_alpha = f.entity('AlphaAlpha', on_delete=CASCADE)


class AlphaCharlie(E.Entity):
    """Has a reference to an AlphaAlpha, such that when that
    AlphaAlpha is deleted, the operation will fail because the
    deletion of this AlphaCharlie is restricted."""
    __module__ = __name__
    alpha_alpha = f.entity('AlphaAlpha', on_delete=RESTRICT)


class AlphaDelta(E.Entity):
    """Has a reference to an AlphaAlpha, such that when that
    AlphaAlpha is deleted, this field on this AlphaDelta will be set
    to UNASSIGNED."""
    __module__ = __name__
    alpha_alpha = f.entity('AlphaAlpha', on_delete=UNASSIGN, required=False)


class AlphaEcho(E.Entity):
    """Has a reference to an AlphaAlpha or an AlphaBravo, such that
    when a referenced AlphaAlpha is deleted, this field on this
    AlphaEcho will be set to UNASSIGNED, and when a referenced
    AlphaBravo is deleted, this AlphaEcho will also be deleted."""
    __module__ = __name__
    alpha_or_bravo = f.entity(('AlphaAlpha', UNASSIGN), (
     'AlphaBravo', CASCADE), required=False)


class Bravo(E.Entity):
    """Contains one of every class of field possible."""
    __module__ = __name__
    hashed_value = f.hashedValue(required=False)
    string = f.string(required=False)
    memo = f.memo(required=False)
    password = f.password(required=False)
    path = f.path(required=False)
    unicode = f.unicode(required=False)
    blob = f.blob(required=False)
    image = f.image(required=False)
    integer = f.integer(required=False)
    float = f.float(required=False)
    money = f.money(required=False)
    date = f.date(required=False)
    datetime = f.datetime(required=False)
    boolean = f.boolean(required=False)
    entity = f.entity('Bravo', required=False)


class Charlie(E.Entity):
    """Fields have default values for create transactions."""
    __module__ = __name__
    beta = f.string(default='foo')
    gamma = f.integer(default=lambda : 42)
    _sample_unittest = [
     ('bar', 12), (DEFAULT, 12), ('bar', DEFAULT), (DEFAULT, DEFAULT)]


class DeltaAlpha(E.Entity):
    """A plain extent that has a default query like any other."""
    __module__ = __name__
    string = f.string(required=False)
    integer = f.integer(required=False)
    float = f.float(required=False)
    entity = f.entity('DeltaAlpha', required=False)


class DeltaBravo(E.Entity):
    """An extent that has its default query hidden."""
    __module__ = __name__
    string = f.string(required=False)
    _hide('q_by_example')


class DeltaCharlie(E.Entity):
    """An extent that has a custom query."""
    __module__ = __name__
    hashed_value = f.hashedValue()

    @extentmethod
    def q_hashes(extent, **kw):
        return E.DeltaCharlie._Hashes(extent, **kw)

    class _Hashes(Q.Param):
        __module__ = __name__
        compare_with = f.string()

        def __call__(self):
            extent = self._on
            compare_with = self.compare_with
            return schevo.query.results((dc for dc in extent if dc.f.hashed_value.compare(compare_with)))


class EchoAlpha(E.Entity):
    """A plain extent that has a default view like any other."""
    __module__ = __name__
    unicode = f.unicode(required=False)
    integer = f.integer(required=False)
    float = f.float(required=False)
    _sample_unittest = [
     ('unicode', 5, 2.2), ('yoonicode', 6, 3.3)]


class EchoBravo(E.Entity):
    """An extent that has its default view hidden."""
    __module__ = __name__
    unicode = f.unicode(required=False)
    _hide('v_default')
    _sample_unittest = [
     ('string', ), ('strang', )]


class EchoCharlie(E.Entity):
    """An extent that has an overridden default view."""
    __module__ = __name__
    single = f.integer()

    @with_label('Custom View')
    def v_custom(self):
        return self._CustomView(self)

    class _CustomView(V.View):
        __module__ = __name__
        _label = 'Custom View'

        def _setup(self, entity):
            self.f.double = f.integer()
            self.double = entity.single * 2
            self.f.single_text = f.unicode()
            self.single_text = unicode(entity.single)

    class _DefaultView(V.View):
        __module__ = __name__

        def _setup(self, entity):
            self.f.double = f.integer()
            self.double = self.single * 2

    _sample_unittest = [
     (1, ), (2, )]


class FoxtrotAlpha(E.Entity):
    """Used for testing ``links`` and ``count``."""
    __module__ = __name__
    beta = f.integer()
    foxtrot_bravo = f.entity('FoxtrotBravo', required=False)
    foxtrot_any = f.entity('FoxtrotAlpha', 'FoxtrotBravo', 'FoxtrotCharlie', required=False)
    _key(beta)
    _sample_unittest = [
     (
      1, DEFAULT, DEFAULT), (2, DEFAULT, ('FoxtrotAlpha', (1, ))), (3, (1, ), DEFAULT), (4, (1, ), ('FoxtrotBravo', (1, ))), (5, DEFAULT, ('FoxtrotCharlie', (2, )))]


class FoxtrotBravo(E.Entity):
    __module__ = __name__
    gamma = f.integer()
    foxtrot_charlie = f.entity('FoxtrotCharlie', required=False)
    _key(gamma)
    _sample_unittest = [
     (
      1, DEFAULT), (2, (1, )), (3, DEFAULT), (4, (2, )), (5, (2, ))]


class FoxtrotCharlie(E.Entity):
    __module__ = __name__
    epsilon = f.integer()
    _key(epsilon)
    _sample_unittest = [
     (1, ), (2, ), (3, ), (4, ), (5, )]


class FoxtrotDelta(E.Entity):
    __module__ = __name__
    zeta = f.integer()
    foxtrot_bravo = f.entity('FoxtrotBravo', required=False)
    _key(zeta)
    _sample_unittest = [
     (
      1, (1, )), (2, DEFAULT), (3, DEFAULT), (4, DEFAULT), (5, DEFAULT)]


class _GolfAlphaBase(E.Entity):
    __module__ = __name__
    beta = f.unicode()
    _key(beta)


class GolfAlpha(E._GolfAlphaBase):
    __module__ = __name__
    gamma = f.integer()
    _key(gamma, 'beta')


class Hotel(E.Entity):
    __module__ = __name__

    @extentmethod
    def x_return_extent(extent):
        return extent


class Avatar(E.Entity):
    __module__ = __name__
    realm = f.entity('Realm')
    user = f.entity('User')
    name = f.unicode()
    _key(user, realm, name)

    def __unicode__(self):
        return '%s (%s in %s)' % (self.name, self.user, self.realm)


class Batch_Job(E.Entity):
    __module__ = __name__
    name = f.unicode()
    priority = f.integer(label='Pri.')
    _key(name)
    _key(priority)

    @extentmethod
    def t_multiple_keys_create(extent):
        return T.Multiple_Keys_Create()

    @extentmethod
    def t_multiple_keys_update(extent):
        return T.Multiple_Keys_Update()

    def __unicode__(self):
        return '%s :: %i' % (self.name, self.priority)


class Realm(E.Entity):
    __module__ = __name__
    name = f.unicode()
    _key(name)

    class _Create(T.Create):
        __module__ = __name__

        def _undo(self):
            return


class User(E.Entity):
    __module__ = __name__
    name = f.unicode()
    age = f.integer(required=False)
    _key(name)
    _index(age)
    _index(age, name)
    _index(name, age)

    @extentmethod
    def t_create_foo_and_bar(extent):
        return T.Create_Foo_And_Bar()

    @extentmethod
    def t_create_name_only(extent):
        tx = E.User._Create()
        del tx.f.age
        return tx

    @extentmethod
    def t_trigger_key_collision(extent):
        return T.Trigger_Key_Collision()


class Multiple_Keys_Create(T.Transaction):
    __module__ = __name__

    def _execute(self, db):
        Batch_Job = db.Batch_Job
        tx = Batch_Job.t.create(name='foo', priority=1)
        result = db.execute(tx)
        tx = Batch_Job.t.create(name='bar', priority=1)
        raises(error.KeyCollision, db.execute, tx)
        tx = Batch_Job.t.create(name='foo', priority=2)
        raises(error.KeyCollision, db.execute, tx)
        tx = Batch_Job.t.create(name='bar', priority=2)
        result = db.execute(tx)


class Multiple_Keys_Update(T.Transaction):
    __module__ = __name__

    def _execute(self, db):
        Batch_Job = db.Batch_Job
        tx = Batch_Job.t.create(name='foo', priority=1)
        result_foo = db.execute(tx)
        tx = Batch_Job.t.create(name='bar', priority=2)
        result_bar = db.execute(tx)
        tx = result_bar.t.update(name='foo', priority=3)
        raises(error.KeyCollision, db.execute, tx)
        tx = result_bar.t.update(name='baz', priority=1)
        raises(error.KeyCollision, db.execute, tx)
        tx = Batch_Job.t.create(name='baz', priority=3)
        result = db.execute(tx)


class Create_Foo_And_Bar(T.Transaction):
    __module__ = __name__

    def _execute(self, db):
        User = db.User
        tx = User.t.create(name='foo')
        db.execute(tx)
        tx = User.t.create(name='bar')
        db.execute(tx)


class Trigger_Key_Collision(T.Transaction):
    __module__ = __name__

    def _execute(self, db):
        User = db.User
        tx = User.t.create(name='foo')
        db.execute(tx)
        tx = User.t.create(name='foo')
        db.execute(tx)


class Subtransactions(T.Transaction):
    """The top-level transaction of a series of subtransactions.

    The sequence of execution is as follows:

    - create user 1
    - subtransaction as list
      - create user 2
      - create user 3
    - subtransaction as list -> handled failure
      - create user 4
      - update user 2
      - delete user 3
      - create user -> unhandled failure
    - subtransaction 1 as instance
      - create user 5
      - create user 6
    - subtransaction 2 as instance -> handled failure
      - create user 7
      - update user 5
      - delete user 6
      - create user -> unhandled failure
    - subtransaction 3 as instance
      - sub-subtransaction as list
        - create user 8
        - create user 9
      - sub-subtransaction as list -> handled failure
        - create user 10
        - update user 8
        - delete user 9
        - create user -> unhandled failure
    - subtransaction 4 as instance -> handled failure
      - sub-subtransaction as list
        - create user 11
        - update user 2
        - delete user 3
      - sub-subtransaction as list -> unhandled failure
        - create user 12
        - create user -> unhandled failure
    - create user 13

    The result is that eight users with the following OIDs should
    exist in the User extent, all with revision 0: 1, 2, 3, 5, 6, 8,
    9, 13
    """
    __module__ = __name__

    def _execute(self, db):
        User = db.User
        txc1 = User.t.create(name='1')
        db.execute(txc1)
        assert len(User) == 1
        txc2 = User.t.create(name='2')
        txc3 = User.t.create(name='3')
        (user2, user3) = db.execute(txc2, txc3)
        assert len(User) == 3
        txc4 = User.t.create(name='4')
        txu2 = user2.t.update(name='2b')
        txd3 = user3.t.delete()
        txcfail = User.t.create(name='1')
        raises(error.KeyCollision, db.execute, txc4, txu2, txd3, txcfail)
        assert len(User) == 3
        txs1 = T.Subtransaction1()
        db.execute(txs1)
        txs2 = T.Subtransaction2()
        raises(error.KeyCollision, db.execute, txs2)
        txs3 = T.Subtransaction3()
        db.execute(txs3)
        txs4 = T.Subtransaction4()
        raises(error.KeyCollision, db.execute, txs4)
        txc13 = User.t.create(name='13')
        db.execute(txc13)


def t_subtransactions():
    return T.Subtransactions()


class Subtransaction1(T.Transaction):
    __module__ = __name__

    def _execute(self, db):
        User = db.User
        txc5 = User.t.create(name='5')
        db.execute(txc5)
        txc6 = User.t.create(name='6')
        db.execute(txc6)


class Subtransaction2(T.Transaction):
    __module__ = __name__

    def _execute(self, db):
        User = db.User
        txc7 = User.t.create(name='7')
        db.execute(txc7)
        txu5 = User[5].t.update(name='5b')
        db.execute(txu5)
        txd6 = User[6].t.delete()
        db.execute(txd6)
        txcfail = User.t.create(name='1')
        db.execute(txcfail)


class Subtransaction3(T.Transaction):
    __module__ = __name__

    def _execute(self, db):
        User = db.User
        txc8 = User.t.create(name='8')
        txc9 = User.t.create(name='9')
        (user8, user9) = db.execute(txc8, txc9)
        txc10 = User.t.create(name='10')
        txu8 = user8.t.update(name='8b')
        txd9 = user9.t.delete()
        txcfail = User.t.create(name='1')
        raises(error.KeyCollision, db.execute, txc10, txu8, txd9, txcfail)


class Subtransaction4(T.Transaction):
    __module__ = __name__

    def _execute(self, db):
        User = db.User
        txc11 = User.t.create(name='11')
        txu2 = User[2].t.update(name='2b')
        txd3 = User[3].t.delete()
        db.execute(txc11, txu2, txd3)
        txc12 = User.t.create(name='12')
        txcfail = User.t.create(name='1')
        db.execute(txc12, txcfail)


class Everything(E.Entity):
    """A bit of everything from Schevo fields."""
    __module__ = __name__
    string_field = f.string(required=False)
    integer_field = f.integer(required=False)
    float_field = f.float(required=False)
    money_field = f.money(required=False)
    date_field = f.date(required=False)
    datetime_field = f.datetime(required=False)
    boolean_field = f.boolean(required=False)
    entity_field = f.entity('Everything', required=False)


class Folder(E.Entity):
    """Folder that could have a parent."""
    __module__ = __name__
    name = f.unicode(error_message='Please enter the name of the folder.')
    parent = f.entity('Folder', required=False)
    _key(name, parent)

    def __unicode__(self):
        name = self.name
        parent = self.parent
        while parent and parent != self:
            name = parent.name + '/' + name
            parent = parent.parent

        return name


class Account(E.Entity):
    """Bank account."""
    __module__ = __name__
    owner = f.entity('Person')
    name = f.unicode()
    balance = f.money()
    overdraft_protection = f.boolean(default=False)
    suspended = f.boolean(default=False)
    _key(owner, name)

    def t_suspend(self):
        """Suspend this account."""
        tx = T.Suspend()
        tx.account = self
        tx.f.account.readonly = True
        return tx

    @with_label('Transfer Funds From This Account')
    def t_transfer(self):
        """Transfer funds from this account."""
        tx = T.Transfer()
        tx.from_account = self
        tx.f.from_account.readonly = True
        tx._label = 'Transfer Funds From %s' % self
        return tx

    _sample_unittest = [
     (
      ('Fred Flintstone', ), 'Personal', 204.52, False, False), (('Fred Flintstone', ), 'Business', 29142.75, True, False), (('Betty Rubble', ), 'Family', 291.0, False, True), (('Betty Rubble', ), 'Savings', 2816.5, False, False)]


class Gender(E.Entity):
    """Gender of a person."""
    __module__ = __name__
    code = f.unicode()
    name = f.unicode()

    @f.integer()
    def count(self):
        return self.sys.count('Person', 'gender')

    _key(code)
    _key(name)


class Person(E.Entity):
    """Bank account owner."""
    __module__ = __name__
    name = f.unicode()
    gender = f.entity('Gender', required=False)
    _key(name)
    _plural = 'People'
    _sample_unittest = [
     (
      'Fred Flintstone', UNASSIGNED), ('Betty Rubble', UNASSIGNED)]


class Suspend(T.Transaction):
    """Suspend an account."""
    __module__ = __name__
    account = f.entity('Account')

    def _execute(self, db):
        tx = self.account.t.update(suspended=True)
        db.execute(tx)


class Transfer(T.Transaction):
    """Transfer money from one account to another."""
    __module__ = __name__
    from_account = f.entity('Account')
    to_account = f.entity('Account')
    amount = f.money(min_value=0.0)

    def _execute(self, db):
        from_account = self.from_account
        to_account = self.to_account
        amount = self.amount
        has_overdraft_protection = from_account.overdraft_protection
        new_balance = from_account.balance - amount
        if from_account.suspended or to_account.suspended:
            raise Exception('An account is suspended.')
        if not has_overdraft_protection and new_balance < 0.0:
            raise Exception('Insufficient funds.')
        tx_withdraw = from_account.t.update()
        tx_withdraw.balance -= amount
        tx_deposit = to_account.t.update()
        tx_deposit.balance += amount
        db.execute(tx_withdraw, tx_deposit)


class Cog(E.Entity):
    """A cog with sprockets."""
    __module__ = __name__
    name = f.unicode()
    _key(name)

    class _Create(T.Create):
        """A cog is usually created with five sprockets."""
        __module__ = __name__

        def _execute(self, db):
            cog = T.Create._execute(self, db)
            sprockets = db.extent('Sprocket')
            try:
                for x in xrange(5):
                    db.execute(sprockets.t.create(cog=cog))

            except:
                pass

            return cog


class Sprocket(E.Entity):
    """A sprocket for a cog."""
    __module__ = __name__
    cog = f.entity('Cog')

    class _Create(T.Create):
        """A sprocket is only created if the cog's name is not
        'Spacely'."""
        __module__ = __name__

        def _execute(self, db):
            sprocket = T.Create._execute(self, db)
            if sprocket.cog.name == 'Spacely':
                raise Exception('Antitrust error.')
            return sprocket


class LoopSegment(E.Entity):
    """A loop segment must always have a 'next' field.

    If it is UNASSIGNED during a create operation, then the segment
    itself will be the value.
    """
    __module__ = __name__
    next = f.entity('LoopSegment')
    _key(next)
    _hide('t_create', 't_update')
    _hide('t_update')

    class _CreateLoop(T.Transaction):
        """Create a loop of multiple segments.  Result of execution is
        the first segment made."""
        __module__ = __name__
        count = f.integer()

        def _execute(self, db):
            db.LoopSegment.relax_index('next')
            segments = []
            for x in xrange(self.count):
                tx = db.LoopSegment.t.create()
                segments.append(db.execute(tx, strict=False))

            for x in xrange(self.count - 1):
                this = segments[x]
                next = segments[(x + 1)]
                tx = this.t.update()
                tx.next = next
                db.execute(tx)

            this = segments[(-1)]
            next = segments[0]
            tx = this.t.update()
            tx.next = next
            db.execute(tx)
            db.LoopSegment.enforce_index('next')
            return segments[0]

    @extentmethod
    def t_create_loop(extent):
        return E.LoopSegment._CreateLoop()

    class _DirtyCreateLoop(T.Transaction):
        """Create a loop of multiple segments.  Intentionally fails."""
        __module__ = __name__
        count = f.integer()

        def _execute(self, db):
            db.LoopSegment.relax_index('next')
            segments = []
            for x in xrange(self.count):
                tx = db.LoopSegment.t.create()
                segments.append(db.execute(tx, strict=False))

            try:
                db.LoopSegment.enforce_index('next')
            except error.KeyCollision:
                raise
            else:
                raise Exception('Key collision not detected!')

    @extentmethod
    def t_dirty_create_loop(extent):
        return E.LoopSegment._DirtyCreateLoop()


class Event(E.Entity):
    """An event must have a unique date and datetime, but none are
    required."""
    __module__ = __name__
    date = f.date(required=False)
    datetime = f.datetime(required=False)
    _key(date)
    _key(datetime)


class ProblemGender(E.Entity):
    """Gender of a person, with a problematic _Create transaction."""
    __module__ = __name__
    code = f.unicode()
    name = f.unicode()

    @f.integer()
    def count(self):
        return self.sys.count('Person', 'gender')

    _key(code)
    _key(name)

    class _Create(T.Create):
        __module__ = __name__
        count = f.unicode()
        foo = f.integer()

    class _Update(T.Update):
        __module__ = __name__
        count = f.unicode()
        foo = f.integer()