# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/mysql/tests/test_datastore_mysql.py
# Compiled at: 2010-12-12 04:36:57
"""Unit tests for the Datastore MySQL stub."""
from google.appengine.api import apiproxy_stub
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import datastore
from google.appengine.api import datastore_admin
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
from google.appengine.api import taskqueue
from google.appengine.api import users
from google.appengine.datastore import datastore_index
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.runtime import apiproxy_errors
import datetime, os, time, typhoonae.mysql.datastore_mysql_stub, unittest

class TaskQueueServiceStubMock(apiproxy_stub.APIProxyStub):
    """Task queue service stub for testing purposes."""

    def __init__(self, service_name='taskqueue', root_path=None):
        super(TaskQueueServiceStubMock, self).__init__(service_name)

    def _Dynamic_Add(self, request, response):
        pass

    def _Dynamic_BulkAdd(self, request, response):
        response.add_taskresult()


class DatastoreMySQLTestCaseBase(unittest.TestCase):
    """Base class for testing the TyphoonAE Datastore MySQL API proxy stub."""

    def setUp(self):
        """Sets up test environment and regisers stub."""
        os.environ['APPLICATION_ID'] = 'test'
        os.environ['AUTH_DOMAIN'] = 'mydomain.local'
        os.environ['USER_EMAIL'] = 'tester@mydomain.local'
        os.environ['USER_IS_ADMIN'] = '1'
        index_yaml = open(os.path.join(os.path.dirname(__file__), 'index.yaml'), 'r')
        try:
            self.indices = datastore_index.IndexDefinitionsToProtos('test', datastore_index.ParseIndexDefinitions(index_yaml).indexes)
        except TypeError:
            self.indices = []

        index_yaml.close()
        apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
        database_info = {'host': '127.0.0.1', 
           'user': 'root', 
           'passwd': '', 
           'db': 'testdb'}
        datastore = typhoonae.mysql.datastore_mysql_stub.DatastoreMySQLStub('test', database_info)
        try:
            apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', datastore)
        except apiproxy_errors.ApplicationError, e:
            raise RuntimeError('These tests require a running MySQL server (%s)' % e)

        self.stub = apiproxy_stub_map.apiproxy.GetStub('datastore_v3')
        apiproxy_stub_map.apiproxy.RegisterStub('taskqueue', TaskQueueServiceStubMock())

    def tearDown(self):
        """Clears all data."""
        self.stub.Clear()


class DatastoreMySQLTestCase(DatastoreMySQLTestCaseBase):
    """Testing the TyphoonAE Datastore MySQL API proxy stub."""

    def testStub(self):
        """Tests whether our stub is registered."""
        self.assertNotEqual(None, self.stub)
        return

    def testPutGetDelete(self):
        """Puts/gets/deletes entities into/from the datastore."""

        class Author(db.Model):
            name = db.StringProperty()

        class Book(db.Model):
            title = db.StringProperty()

        a = Author(name='Mark Twain', key_name='marktwain')
        a.put()
        b = Book(parent=a, title='The Adventures Of Tom Sawyer')
        b.put()
        key = b.key()
        del a
        del b
        book = datastore.Get(key)
        self.assertEqual("{u'title': u'The Adventures Of Tom Sawyer'}", str(book))
        author = datastore.Get(book.parent())
        self.assertEqual("{u'name': u'Mark Twain'}", str(author))
        del book
        datastore.Delete(key)
        self.assertRaises(datastore_errors.EntityNotFoundError, datastore.Get, key)
        del author
        mark_twain = Author.get_by_key_name('marktwain')
        self.assertEqual('Author', mark_twain.kind())
        self.assertEqual('Mark Twain', mark_twain.name)
        mark_twain.delete()

    def testGetPutMultiTypes(self):
        """Sets and Gets models with different entity groups."""

        class Author(db.Model):
            name = db.StringProperty()

        class Book(db.Model):
            title = db.StringProperty()

        a = Author(name='Mark Twain', key_name='marktwain')
        b = Book(title='The Adventures Of Tom Sawyer')
        keys = db.put([a, b])
        self.assertEqual(2, len(keys))
        items = db.get(keys)
        self.assertEqual(2, len(items))
        db.delete(keys)

    def testExpando(self):
        """Test the Expando superclass."""

        class Song(db.Expando):
            title = db.StringProperty()

        crazy = Song(title='Crazy like a diamond', author='Lucy Sky', publish_date='yesterday', rating=5.0)
        oboken = Song(title='The man from Hoboken', author=[
         'Anthony', 'Lou'], publish_date=datetime.datetime(1977, 5, 3))
        crazy.last_minute_note = db.Text('Get a train to the station.')
        crazy.put()
        oboken.put()
        self.assertEqual('The man from Hoboken', Song.all().filter('author =', 'Anthony').get().title)
        self.assertEqual('The man from Hoboken', Song.all().filter('publish_date >', datetime.datetime(1970, 1, 1)).get().title)

    def testPolymodel(self):
        """Tests Polymodels."""

        class Contact(polymodel.PolyModel):
            phone_number = db.PhoneNumberProperty()
            address = db.PostalAddressProperty()

        class Person(Contact):
            first_name = db.StringProperty()
            last_name = db.StringProperty()
            mobile_number = db.PhoneNumberProperty()

        class Company(Contact):
            name = db.StringProperty()
            fax_number = db.PhoneNumberProperty()

        p = Person(phone_number='1-206-555-9234', address='123 First Ave., Seattle, WA, 98101', first_name='Alfred', last_name='Smith', mobile_number='1-206-555-0117')
        c = Company(phone_number='1-503-555-9123', address='P.O. Box 98765, Salem, OR, 97301', name='Data Solutions, LLC', fax_number='1-503-555-6622')
        p.put()
        c.put()
        self.assertEqual(set([ e.phone_number for e in [p, c] ]), set([ e.phone_number for e in list(Contact.all()) ]))
        self.assertEqual(set([p.phone_number]), set([ e.phone_number for e in list(Person.all()) ]))

    def testGetEntitiesByNameAndID(self):
        """Tries to retrieve entities by name or numeric id."""

        class Book(db.Model):
            title = db.StringProperty()

        Book(title="The Hitchhiker's Guide to the Galaxy").put()
        book = Book.get_by_id(1)
        self.assertEqual("The Hitchhiker's Guide to the Galaxy", book.title)
        Book(key_name='solong', title='So Long, and Thanks for All the Fish').put()
        book = Book.get_by_key_name('solong')
        self.assertEqual('So Long, and Thanks for All the Fish', book.title)

    def testTransaction(self):
        """Executes multiple operations in one transaction."""

        class Author(db.Model):
            name = db.StringProperty()

        class Book(db.Model):
            title = db.StringProperty()

        marktwain = Author(name='Mark Twain', key_name='marktwain').put()

        def tx():
            assert db.get(marktwain).name == 'Mark Twain'
            b = Book(parent=marktwain, title='The Adventures Of Tom Sawyer')
            b.put()
            c = Book(parent=marktwain, title="The Hitchhiker's Guide to the Galaxy")
            c.put()
            c.delete()

        db.run_in_transaction(tx)
        self.assertEqual(1, Author.all().count())
        self.assertEqual(1, Book.all().count())
        marktwain = Author.get_by_key_name('marktwain')

        def query_tx():
            query = db.Query()
            query.filter('__key__ = ', marktwain.key())
            author = query.get()

        self.assertRaises(datastore_errors.BadRequestError, db.run_in_transaction, query_tx)

    def testTransactionRollback(self):
        """Performs a transaction rollback."""

        class Author(db.Model):
            name = db.StringProperty()

        class Book(db.Model):
            title = db.StringProperty()

        marktwain = Author(name='Mark Twain', key_name='marktwain').put()

        def tx():
            assert db.get(marktwain).name == 'Mark Twain'
            b = Book(parent=marktwain, title='The Adventures Of Tom Sawyer')
            b.put()
            raise db.Rollback()

        db.run_in_transaction(tx)
        self.assertEqual(1, Author.all().count())
        self.assertEqual(0, Book.all().count())

    def testKindlessAncestorQueries(self):
        """Perform kindless queries for entities with a given ancestor."""

        class Author(db.Model):
            name = db.StringProperty()

        class Book(db.Model):
            title = db.StringProperty()

        author = Author(name='Mark Twain', key_name='marktwain').put()
        book = Book(parent=author, title='The Adventures Of Tom Sawyer').put()
        query = db.Query()
        query.ancestor(author)
        query.filter('__key__ = ', book)
        self.assertEqual(book, query.get().key())
        book = query.get()
        book.delete()
        self.assertEqual(0, query.count())

    def testRunQuery(self):
        """Runs some simple queries."""

        class Employee(db.Model):
            first_name = db.StringProperty(required=True)
            last_name = db.StringProperty(required=True)
            manager = db.SelfReferenceProperty()

        manager = Employee(first_name='John', last_name='Dowe')
        manager.put()
        employee = Employee(first_name='John', last_name='Appleseed', manager=manager.key())
        employee.put()
        query = Employee.all()
        self.assertEqual(set(['John Dowe', 'John Appleseed']), set([ '%s %s' % (e.first_name, e.last_name) for e in query.run()
                                                                   ]))
        manager.first_name = 'Clara'
        manager.put()
        query = Employee.all()
        self.assertEqual(set(['Clara Dowe', 'John Appleseed']), set([ '%s %s' % (e.first_name, e.last_name) for e in query.run()
                                                                    ]))
        query = Employee.all()
        self.assertEqual('Dowe', query.get().last_name)
        self.assertEqual('Dowe', query.fetch(1)[0].last_name)
        employee.delete()
        manager.delete()
        query = Employee.all()
        self.assertEqual([], list(query.run()))

    def testCount(self):
        """Counts query results."""

        class Balloon(db.Model):
            color = db.StringProperty()

        Balloon(color='Red').put()
        self.assertEqual(1, Balloon.all().count())
        Balloon(color='Blue').put()
        self.assertEqual(2, Balloon.all().count())

    def testQueryWithFilter(self):
        """Tries queries with filters."""

        class SomeKind(db.Model):
            value = db.StringProperty()

        foo = SomeKind(value='foo')
        foo.put()
        bar = SomeKind(value='bar')
        bar.put()

        class Artifact(db.Model):
            description = db.StringProperty(required=True)
            age = db.IntegerProperty()

        vase = Artifact(description='Mycenaean stirrup vase', age=3300)
        vase.put()
        helmet = Artifact(description='Spartan full size helmet', age=2400)
        helmet.put()
        unknown = Artifact(description='Some unknown artifact')
        unknown.put()
        query = Artifact.all().filter('age =', 2400)
        self.assertEqual([
         'Spartan full size helmet'], [ artifact.description for artifact in query.run() ])
        query = db.GqlQuery('SELECT * FROM Artifact WHERE age = :1', 3300)
        self.assertEqual([
         'Mycenaean stirrup vase'], [ artifact.description for artifact in query.run() ])
        query = Artifact.all().filter('age IN', [2400, 3300])
        self.assertEqual(set(['Spartan full size helmet', 'Mycenaean stirrup vase']), set([ artifact.description for artifact in query.run() ]))
        vase.delete()
        query = Artifact.all().filter('age IN', [2400])
        self.assertEqual([
         'Spartan full size helmet'], [ artifact.description for artifact in query.run() ])
        helmet.age = 2300
        helmet.put()
        query = Artifact.all().filter('age =', 2300)
        self.assertEqual([2300], [ artifact.age for artifact in query.run() ])
        query = Artifact.all()
        self.assertEqual(set([2300, None]), set([ artifact.age for artifact in query.run() ]))
        return

    def testQueryForKeysOnly(self):
        """Queries for entity keys instead of full entities."""

        class Asset(db.Model):
            name = db.StringProperty(required=True)
            price = db.FloatProperty(required=True)

        lamp = Asset(name='Bedside Lamp', price=10.45)
        lamp.put()
        towel = Asset(name='Large Towel', price=3.5)
        towel.put()
        query = Asset.all(keys_only=True)
        app_id = os.environ['APPLICATION_ID']
        self.assertEqual(set([
         datastore_types.Key.from_path('Asset', 1, _app=app_id),
         datastore_types.Key.from_path('Asset', 2, _app=app_id)]), set(query.run()))

    def testQueryWithOrder(self):
        """Tests queries with sorting."""

        class Planet(db.Model):
            name = db.StringProperty()
            moon_count = db.IntegerProperty()
            distance = db.FloatProperty()

        earth = Planet(name='Earth', distance=93.0, moon_count=1)
        earth.put()
        saturn = Planet(name='Saturn', distance=886.7, moon_count=18)
        saturn.put()
        venus = Planet(name='Venus', distance=67.2, moon_count=0)
        venus.put()
        mars = Planet(name='Mars', distance=141.6, moon_count=2)
        mars.put()
        mercury = Planet(name='Mercury', distance=36.0, moon_count=0)
        mercury.put()
        query = Planet.all().filter('moon_count <', 10).order('moon_count').order('-name').order('distance')
        self.assertEqual([
         'Venus', 'Mercury', 'Earth', 'Mars'], [ planet.name for planet in query.run() ])
        query = Planet.all().filter('distance >', 100.0).order('-distance')
        self.assertEqual([
         'Saturn', 'Mars'], [ planet.name for planet in query.run() ])
        query = Planet.all().filter('distance <=', 93.0).order('distance')
        self.assertEqual([
         'Mercury', 'Venus', 'Earth'], [ planet.name for planet in query.run() ])
        query = Planet.all().filter('distance >', 80.0).filter('distance <', 150.0).order('distance')
        self.assertEqual([
         'Earth', 'Mars'], [ planet.name for planet in query.run() ])
        query = Planet.all().filter('distance >=', 93.0).order('distance')
        self.assertEqual([
         'Earth', 'Mars', 'Saturn'], [ planet.name for planet in query.run() ])
        query = Planet.all().filter('distance ==', 93.0)
        self.assertEqual([
         'Earth'], [ planet.name for planet in query.run() ])

    def testQueriesWithMultipleFiltersAndOrders(self):
        """Tests queries with multiple filters and orders."""

        class Artist(db.Model):
            name = db.StringProperty()

        class Album(db.Model):
            title = db.StringProperty()

        class Song(db.Model):
            artist = db.ReferenceProperty(Artist)
            album = db.ReferenceProperty(Album)
            duration = db.StringProperty()
            genre = db.CategoryProperty()
            title = db.StringProperty()

        beatles = Artist(name='The Beatles')
        beatles.put()
        abbeyroad = Album(title='Abbey Road')
        abbeyroad.put()
        herecomesthesun = Song(artist=beatles.key(), album=abbeyroad.key(), duration='3:06', genre=db.Category('Pop'), title='Here Comes The Sun')
        herecomesthesun.put()
        query = Song.all().filter('artist =', beatles).filter('album =', abbeyroad)
        self.assertEqual('Here Comes The Sun', query.get().title)
        cometogether = Song(artist=beatles.key(), album=abbeyroad.key(), duration='4:21', genre=db.Category('Pop'), title='Come Together')
        cometogether.put()
        something = Song(artist=beatles.key(), album=abbeyroad.key(), duration='3:03', genre=db.Category('Pop'), title='Something')
        something.put()
        because1 = Song(key_name='because', artist=beatles.key(), album=abbeyroad.key(), duration='2:46', genre=db.Category('Pop'), title='Because')
        because1.put()
        because2 = Song(artist=beatles.key(), album=abbeyroad.key(), duration='2:46', genre=db.Category('Pop'), title='Because')
        because2.put()
        query = Song.all().filter('artist =', beatles).filter('album =', abbeyroad).order('title')
        self.assertEqual([
         'Because', 'Because', 'Come Together', 'Here Comes The Sun',
         'Something'], [ song.title for song in query.run() ])
        query = Song.all().filter('title !=', 'Because').order('title')
        self.assertEqual([
         'Come Together', 'Here Comes The Sun', 'Something'], [ song.title for song in query.run() ])
        query = Song.all().filter('title >', 'Come').order('title')
        self.assertEqual([
         'Come Together', 'Here Comes The Sun', 'Something'], [ song.title for song in query.run() ])
        something.delete()
        query = Song.all().filter('title >', 'Come').order('title')
        self.assertEqual([
         'Come Together', 'Here Comes The Sun'], [ song.title for song in query.run() ])

    def testUnicode(self):
        """Tests unicode."""

        class Employee(db.Model):
            first_name = db.StringProperty(required=True)
            last_name = db.StringProperty(required=True)

        employee = Employee(first_name='Björn', last_name='Müller')
        employee.put()
        query = Employee.all(keys_only=True).filter('first_name =', 'Björn')
        app_id = os.environ['APPLICATION_ID']
        self.assertEqual(datastore_types.Key.from_path('Employee', 1, _app=app_id), query.get())

    def testUnicodeKeyName(self):
        """Sets and Gets models with unicode key names."""

        class Author(db.Model):
            name = db.StringProperty()

        Author(name='Jesús Cebrián', key_name='jesúscebrián').put()
        a = Author.get_by_key_name('jesúscebrián')
        self.assertEqual('Author', a.kind())
        self.assertEqual('Jesús Cebrián', a.name)
        a.delete()
        del a

    def testListProperties(self):
        """Tests list properties."""

        class Numbers(db.Model):
            values = db.ListProperty(int)

        Numbers(values=[0, 1, 2, 3]).put()
        Numbers(values=[4, 5, 6, 7]).put()
        query = Numbers.all().filter('values =', 0)
        self.assertEqual([0, 1, 2, 3], query.get().values)
        query = db.GqlQuery('SELECT * FROM Numbers WHERE values > :1 AND values < :2', 4, 7)
        self.assertEqual([4, 5, 6, 7], query.get().values)

        class Issue(db.Model):
            reviewers = db.ListProperty(db.Email)

        me = db.Email('me@somewhere.net')
        you = db.Email('you@home.net')
        issue = Issue(reviewers=[me, you])
        issue.put()
        query = db.GqlQuery('SELECT * FROM Issue WHERE reviewers = :1', db.Email('me@somewhere.net'))
        self.assertEqual(1, query.count())
        query = db.GqlQuery('SELECT * FROM Issue WHERE reviewers = :1', 'me@somewhere.net')
        self.assertEqual(1, query.count())
        query = db.GqlQuery('SELECT * FROM Issue WHERE reviewers = :1', db.Email('foo@bar.net'))
        self.assertEqual(0, query.count())

    def testStringListProperties(self):
        """Tests string list properties."""

        class Pizza(db.Model):
            topping = db.StringListProperty()

        Pizza(topping=['tomatoe', 'cheese']).put()
        Pizza(topping=['tomatoe', 'cheese', 'salami']).put()
        Pizza(topping=['tomatoe', 'cheese', 'prosciutto']).put()
        query = Pizza.all(keys_only=True).filter('topping =', 'salami')
        self.assertEqual(1, query.count())
        query = Pizza.all(keys_only=True).filter('topping =', 'cheese')
        self.assertEqual(3, query.count())
        query = Pizza.all().filter('topping IN', ['salami', 'prosciutto'])
        self.assertEqual(2, query.count())
        key = datastore_types.Key.from_path('Pizza', 1)
        query = db.GqlQuery('SELECT * FROM Pizza WHERE __key__ IN :1', [key])
        pizza = query.get()
        self.assertEqual(['tomatoe', 'cheese'], pizza.topping)
        pizza.delete()
        query = db.GqlQuery('SELECT * FROM Pizza WHERE __key__ IN :1', [key])
        self.assertEqual(0, query.count())

    def testVariousPropertiyTypes(self):
        """Tests various property types."""

        class Note(db.Model):
            timestamp = db.DateTimeProperty(auto_now=True)
            description = db.StringProperty()
            author_email = db.EmailProperty()
            location = db.GeoPtProperty()
            user = db.UserProperty()

        Note(description='My first note.', author_email='me@inter.net', location='52.518,13.408', user=users.get_current_user()).put()
        query = db.GqlQuery('SELECT * FROM Note ORDER BY timestamp DESC')
        self.assertEqual(1, query.count())
        query = db.GqlQuery('SELECT * FROM Note WHERE timestamp <= :1', datetime.datetime.now())
        self.assertEqual(1, query.count())
        note = query.get()
        self.assertEqual('My first note.', note.description)
        self.assertEqual(db.Email('me@inter.net'), note.author_email)
        self.assertEqual('me@inter.net', note.author_email)
        self.assertEqual(datastore_types.GeoPt(52.518, 13.408), note.location)
        self.assertEqual('52.518,13.408', note.location)
        del note
        query = Note.all().filter('location =', datastore_types.GeoPt(52.518, 13.408))
        self.assertEqual(1, query.count())
        query = Note.all().filter('location =', db.GeoPt('52.518,13.408'))
        self.assertEqual(1, query.count())

    def testDerivedProperty(self):
        """Query by derived property."""

        class LowerCaseProperty(db.Property):
            """A convenience class for generating lower-cased fields."""

            def __init__(self, property, *args, **kwargs):
                """Constructor.
 
                Args:
                    property: The property to lower-case.
                """
                super(LowerCaseProperty, self).__init__(*args, **kwargs)
                self.property = property

            def __get__(self, model_instance, model_class):
                return self.property.__get__(model_instance, model_class).lower()

            def __set__(self, model_instance, value):
                raise db.DerivedPropertyError('Cannot assign to a DerivedProperty')

        class TestModel(db.Model):
            contents = db.StringProperty(required=True)
            lowered_contents = LowerCaseProperty(contents)

        TestModel(contents='Foo Bar').put()
        query = db.GqlQuery('SELECT * FROM TestModel WHERE lowered_contents = :1', 'foo bar')
        self.assertEqual('Foo Bar', query.get().contents)

    def testQueriesWithOffsetAndLimit(self):
        """Retrieves a limited number of results."""

        class MyModel(db.Model):
            data = db.StringProperty()
            number = db.IntegerProperty()

        for i in range(100):
            MyModel(data='Random data.', number=i).put()

        query = MyModel.all().filter('data =', 'Random data.').filter('number >=', 10).filter('number <', 20).order('-number')
        self.assertEqual([
         19, 18], [ e.number for e in query.fetch(2) ])
        self.assertEqual([
         14, 13, 12], [ e.number for e in query.fetch(3, offset=5) ])
        self.assertEqual([
         18, 17], [ e.number for e in query.fetch(2, offset=1) ])
        self.assertEqual([], [ e.number for e in query.fetch(2, offset=10) ])

    def testAllocateIds(self):
        """Tests allocation of id ranges."""

        class EmptyModel(db.Model):
            pass

        for i in xrange(0, 1000):
            key = EmptyModel().put()

        query = db.GqlQuery('SELECT * FROM EmptyModel')
        self.assertEqual(1000, query.count())
        (start, end) = db.allocate_ids(key, 2000)
        self.assertEqual(start, 1001)
        self.assertEqual(end, 3000)

    def testCursors(self):
        """Tests the cursor API."""

        class Number(db.Model):
            unit = db.StringProperty(choices=set(['cm', 'm']))
            value = db.IntegerProperty()

        for i in xrange(0, 2000):
            if i % 2:
                unit = 'm'
            else:
                unit = 'cm'
            Number(unit=unit, value=i).put()

        query = Number.all()
        a = query.fetch(500)
        self.assertEqual(0, a[0].value)
        self.assertEqual(499, a[(-1)].value)
        b = query.fetch(500, offset=500)
        self.assertEqual(500, b[0].value)
        self.assertEqual(999, b[(-1)].value)
        cursor = query.cursor()
        query.with_cursor(cursor)
        c = query.fetch(200)
        self.assertEqual(1000, c[0].value)
        self.assertEqual(1199, c[(-1)].value)
        query.with_cursor(query.cursor())
        d = query.fetch(500)
        self.assertEqual(1200, d[0].value)
        self.assertEqual(1699, d[(-1)].value)
        query.with_cursor(query.cursor())
        self.assertEqual(1700, query.get().value)
        query = Number.all().filter('value >', 500).filter('value <=', 1000)
        e = query.fetch(100)
        query.with_cursor(query.cursor())
        e = query.fetch(50)
        self.assertEqual(601, e[0].value)
        self.assertEqual(650, e[(-1)].value)
        query = Number.all().filter('unit =', 'cm').order('-value')
        f = query.fetch(5)
        self.assertEqual([
         1998, 1996, 1994, 1992, 1990], [ n.value for n in f ])
        query.with_cursor(query.cursor())
        f = query.fetch(5)
        self.assertEqual([
         1988, 1986, 1984, 1982, 1980], [ n.value for n in f ])
        query.with_cursor(query.cursor())
        f = query.fetch(6)
        self.assertEqual([
         1978, 1976, 1974, 1972, 1970, 1968], [ n.value for n in f ])

    def testGetSchema(self):
        """Infers an app's schema from the entities in the datastore."""

        class Foo(db.Model):
            foobar = db.IntegerProperty(default=42)

        Foo().put()
        entity_pbs = datastore_admin.GetSchema()
        entity = datastore.Entity.FromPb(entity_pbs.pop())
        self.assertEqual('Foo', entity.key().kind())

    def testTransactionalTasks(self):
        """Tests tasks within transactions."""

        def my_transaction():
            taskqueue.add(url='/path/to/my/worker', transactional=True)

        db.run_in_transaction(my_transaction)

    def testIndices(self):
        """Creates, updates and deletes an index."""
        from google.appengine.api.datastore_admin import CreateIndex, UpdateIndex, DeleteIndex
        self.assertEqual(1, CreateIndex(self.indices[0]))
        UpdateIndex(self.indices[0])
        DeleteIndex(self.indices[0])