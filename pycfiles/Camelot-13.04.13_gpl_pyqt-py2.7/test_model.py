# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_model.py
# Compiled at: 2013-04-11 17:47:52
import datetime, os
from sqlalchemy import orm
from sqlalchemy import schema, types
from camelot.admin.entity_admin import EntityAdmin
from camelot.core.orm import Session
from camelot.core.sql import metadata
from camelot.core.conf import settings
from camelot.model import party
from camelot.test import ModelThreadTestCase
from camelot.test.action import MockModelContext
from .test_orm import TestMetaData

class ExampleModelCase(ModelThreadTestCase):
    """
    Test case that makes sure the example tables are available in
    the Camelot metadata
    """

    def setUp(self):
        super(ExampleModelCase, self).setUp()
        from camelot.model import authentication, batch_job, fixture, party, i18n, memento
        self.engine = settings.ENGINE()
        metadata.bind = self.engine
        metadata.create_all()
        self.session = Session()
        self.session.expunge_all()

    def tearDown(self):
        metadata.drop_all()
        self.session.expunge_all()


class ModelCase(ExampleModelCase):
    """Test the build in camelot model"""

    def test_memento(self):
        from camelot.model import memento
        from camelot.model.authentication import get_current_authentication
        m = memento.Memento(primary_key=1, model='TestCase', authentication=get_current_authentication(), memento_type=1, previous_attributes={'name': 'memento'})
        self.assertTrue(m.previous)

    def test_i18n(self):
        from camelot.model.i18n import Translation, ExportAsPO
        session = Session()
        session.execute(Translation.__table__.delete())
        self.assertEqual(Translation.translate('bucket', 'nl_BE'), None)
        Translation.translate_or_register('bucket', 'nl_BE')
        Translation.translate_or_register('bucket', 'nl_BE')
        self.assertEqual(Translation.translate('bucket', 'nl_BE'), 'bucket')
        self.assertEqual(Translation.translate('', 'nl_BE'), '')
        self.assertEqual(Translation.translate_or_register('', 'nl_BE'), '')
        Translation._cache.clear()
        translation = Translation(language='nl_BE', source='bucket', value='emmer', uid=1)
        orm.object_session(translation).flush()
        self.assertEqual(Translation.translate('bucket', 'nl_BE'), 'emmer')
        export_action = ExportAsPO()
        model_context = MockModelContext()
        model_context.obj = translation
        try:
            generator = export_action.model_run(model_context)
            file_step = generator.next()
            generator.send(['/tmp/test.po'])
        except StopIteration:
            pass

        return

    def test_batch_job_example(self):
        from camelot.model.batch_job import BatchJob, BatchJobType
        synchronize = BatchJobType.get_or_create('Synchronize')
        with BatchJob.create(synchronize) as (batch_job):
            batch_job.add_strings_to_message(['Synchronize part A',
             'Synchronize part B'])
            batch_job.add_strings_to_message(['Done'], color='green')

    def test_batch_job(self):
        from camelot.model.batch_job import BatchJob, BatchJobType
        batch_job_type = BatchJobType.get_or_create('Synchronize')
        self.assertTrue(unicode(batch_job_type))
        batch_job = BatchJob.create(batch_job_type)
        self.assertTrue(orm.object_session(batch_job))
        self.assertFalse(batch_job.is_canceled())
        batch_job.change_status('canceled')
        self.assertTrue(batch_job.is_canceled())
        with batch_job:
            batch_job.add_strings_to_message(['Doing something'])
            batch_job.add_strings_to_message(['Done'], color='green')
        self.assertEqual(batch_job.current_status, 'success')
        batch_job = BatchJob.create(batch_job_type)
        with batch_job:
            batch_job.add_strings_to_message(['Doing something'])
            raise Exception('Something went wrong')
        self.assertEqual(batch_job.current_status, 'errors')

    def test_current_authentication(self):
        from camelot.model.authentication import get_current_authentication
        authentication = get_current_authentication()
        orm.object_session(authentication).expire_all()
        orm.object_session(authentication).expunge_all()
        authentication = get_current_authentication()
        self.assertTrue(authentication.username)
        self.assertTrue(unicode(authentication))

    def test_authentication_group(self):
        from camelot.model import authentication
        authentication.roles.extend([(1, 'administrator'),
         (2, 'movie_editor')])
        authentication.update_last_login(initial_group_name='Admin', initial_group_roles=[
         'administrator'])
        auth = authentication.get_current_authentication()
        self.assertTrue(auth.has_role('administrator'))
        self.assertFalse(auth.has_role('movie_editor'))


class PartyCase(ExampleModelCase):
    """Test the build in party - address - contact mechanism model"""

    def setUp(self):
        super(PartyCase, self).setUp()
        from camelot.admin.application_admin import ApplicationAdmin
        self.session = Session()
        self.app_admin = ApplicationAdmin()
        self.person_admin = self.app_admin.get_related_admin(party.Person)
        self.organization_admin = self.app_admin.get_related_admin(party.Organization)

    def tearDown(self):
        self.session.expunge_all()

    def test_party(self):
        p = party.Party()
        self.assertFalse(p.name)

    def test_geographic_boundary(self):
        belgium = party.Country.get_or_create(code='BE', name='Belgium')
        self.assertTrue(unicode(belgium))
        city = party.City.get_or_create(country=belgium, code='1000', name='Brussels')
        return city

    def test_address(self):
        city = self.test_geographic_boundary()
        address = party.Address.get_or_create(street1='Avenue Louise', street2=None, city=city)
        self.assertTrue(unicode(address))
        return address

    def test_party_address(self):
        city = self.test_geographic_boundary()
        org = party.Organization(name='PSF')
        party_address = party.PartyAddress(party=org)
        party_address.street1 = 'Avenue Louise 5'
        party_address.street2 = 'Boite 4'
        party_address.city = city
        party_address_admin = party.AddressAdmin(self.app_admin, party.PartyAddress)
        self.assertTrue(party_address.address in party_address_admin.get_compounding_objects(party_address))
        self.assertTrue(party_address.address in self.session.new)
        org_admin = self.app_admin.get_related_admin(party.Organization)
        org_validator = org_admin.get_validator()
        self.assertTrue(party_address in org_admin.get_compounding_objects(org))
        org_admin.flush(org)
        self.assertFalse(party_address.address in self.session.new)
        party_address_admin.refresh(party_address)
        self.assertEqual(party_address.street1, 'Avenue Louise 5')
        self.assertEqual(party_address.street2, 'Boite 4')
        self.assertEqual(party_address.city, city)
        self.assertEqual(org.street1, 'Avenue Louise 5')
        self.assertEqual(org.street2, 'Boite 4')
        self.assertEqual(org.city, city)
        self.assertTrue(unicode(party_address))
        query = self.session.query(party.PartyAddress)
        self.assertTrue(query.filter(party.PartyAddress.street1 == 'Avenue Louise 5').first())
        self.assertTrue(query.filter(party.PartyAddress.street2 == 'Boite 4').first())
        depending_objects = list(party_address_admin.get_depending_objects(party_address))
        self.assertTrue(org in depending_objects)
        address = party_address.address
        address_admin = self.app_admin.get_related_admin(party.Address)
        depending_objects = list(address_admin.get_depending_objects(address))
        self.assertTrue(party_address in depending_objects)
        self.assertTrue(org in depending_objects)
        org.street1 = 'Rue Belliard 1'
        org.street2 = 'Second floor'
        org.city = None
        org_admin.expunge(org)
        self.session.flush()
        org = party.Organization(name='PSF')
        org.street1 = 'Rue Belliard 1'
        org.street2 = 'Second floor'
        org.city = city
        org_admin.flush(org)
        self.assertEqual(len(org.addresses), 1)
        self.assertEqual(org.street1, 'Rue Belliard 1')
        self.assertEqual(org.street2, 'Second floor')
        self.assertEqual(org.city, city)
        self.assertFalse(org_validator.validate_object(org))
        org.city = None
        self.assertTrue(org_validator.validate_object(org))
        org_admin.refresh(org)
        self.assertFalse(org_validator.validate_object(org))
        org.street1 = None
        org.street2 = None
        org.city = None
        self.assertFalse(org_validator.validate_object(org))
        org = party.Organization(name='PSF')
        org.street1 = 'Rue Belliard 1'
        for address in org.addresses:
            self.assertTrue(address in self.session.new)

        org.street1 = None
        self.assertTrue(address not in self.session)
        self.assertEqual(len(org.addresses), 0)
        return

    def test_person(self):
        person = party.Person(first_name='Robin', last_name='The brave')
        self.assertEqual(person.email, None)
        self.assertEqual(person.phone, None)
        self.assertEqual(person.fax, None)
        self.assertEqual(person.street1, None)
        self.assertEqual(person.street2, None)
        self.assertEqual(person.city, None)
        self.person_admin.flush(person)
        person2 = party.Person(first_name='Robin')
        self.assertFalse(person2.note)
        person2.last_name = 'The brave'
        self.assertTrue(person2.note)
        return person

    def test_contact_mechanism(self):
        contact_mechanism = party.ContactMechanism(mechanism=('email', 'info@test.be'))
        self.assertTrue(unicode(contact_mechanism))

    def test_person_contact_mechanism(self):
        person = party.Person(first_name='Robin', last_name='The brave')
        self.person_admin.flush(person)
        self.assertEqual(person.email, None)
        mechanism_1 = ('email', 'robin@test.org')
        person.email = mechanism_1
        self.person_admin.set_defaults(person)
        self.assertTrue(person.contact_mechanisms[0].from_date)
        self.person_admin.flush(person)
        self.assertEqual(person.email, mechanism_1)
        mechanism_2 = ('email', 'robin@test.com')
        person.email = mechanism_2
        self.person_admin.flush(person)
        self.assertEqual(person.email, mechanism_2)
        person.email = ('email', '')
        self.assertEqual(person.email, None)
        self.person_admin.flush(person)
        self.assertEqual(person.email, None)
        admin = party.PartyContactMechanismAdmin(self.app_admin, party.PartyContactMechanism)
        contact_mechanism = party.ContactMechanism(mechanism=mechanism_1)
        party_contact_mechanism = party.PartyContactMechanism(party=person, contact_mechanism=contact_mechanism)
        admin.flush(party_contact_mechanism)
        admin.refresh(party_contact_mechanism)
        list(admin.get_depending_objects(party_contact_mechanism))
        contact_mechanism_admin = self.app_admin.get_related_admin(party.ContactMechanism)
        depending_objects = list(contact_mechanism_admin.get_depending_objects(contact_mechanism))
        self.assertTrue(person in depending_objects)
        self.assertTrue(party_contact_mechanism in depending_objects)
        depending_objects = list(admin.get_depending_objects(party_contact_mechanism))
        self.assertTrue(person in depending_objects)
        self.person_admin.delete(person)
        return

    def test_organization(self):
        org = party.Organization(name='PSF')
        org.email = ('email', 'info@python.org')
        org.phone = ('phone', '1234')
        org.fax = ('fax', '4567')
        self.organization_admin.flush(org)
        self.assertTrue(unicode(org))
        self.assertEqual(org.number_of_shares_issued, 0)
        query = orm.object_session(org).query(party.Organization)
        self.assertTrue(query.filter(party.Organization.email == ('email', 'info@python.org')).first())
        self.assertTrue(query.filter(party.Organization.phone == ('phone', '1234')).first())
        self.assertTrue(query.filter(party.Organization.fax == ('fax', '4567')).first())
        return org

    def test_party_relationship(self):
        person = self.test_person()
        org = self.test_organization()
        employee = party.EmployerEmployee(established_from=org, established_to=person)
        self.assertTrue(unicode(employee))

    def test_party_contact_mechanism(self):
        person = self.test_person()
        party_contact_mechanism = party.PartyContactMechanism(party=person)
        party_contact_mechanism.mechanism = ('email', 'info@test.be')
        party_contact_mechanism.mechanism = ('email', 'info2@test.be')
        self.assertTrue(party_contact_mechanism in self.session.new)
        self.assertTrue(party_contact_mechanism.contact_mechanism in self.session.new)
        self.person_admin.flush(person)
        self.assertFalse(party_contact_mechanism in self.session.new)
        self.assertFalse(party_contact_mechanism.contact_mechanism in self.session.new)
        self.assertTrue(unicode(party_contact_mechanism))
        query = self.session.query(party.PartyContactMechanism)
        self.assertTrue(query.filter(party.PartyContactMechanism.mechanism == ('email',
                                                                               'info2@test.be')).first())
        party_contact_mechanism_admin = self.app_admin.get_related_admin(party.PartyContactMechanism)
        compounding_objects = list(party_contact_mechanism_admin.get_compounding_objects(party_contact_mechanism))
        self.assertTrue(party_contact_mechanism.contact_mechanism in compounding_objects)
        party_contact_mechanism_validator = party_contact_mechanism_admin.get_validator()
        self.assertFalse(party_contact_mechanism_validator.validate_object(party_contact_mechanism))
        party_contact_mechanism.contact_mechanism.mechanism = None
        self.assertTrue(party_contact_mechanism_validator.validate_object(party_contact_mechanism))
        party_admin = self.app_admin.get_related_admin(party.Person)
        party_validator = party_admin.get_validator()
        self.assertTrue(party_validator.validate_object(person))
        return

    def test_party_category(self):
        org = self.test_organization()
        category = party.PartyCategory(name='Imortant')
        category.parties.append(org)
        self.session.flush()
        self.assertTrue(list(category.get_contact_mechanisms('email')))
        self.assertTrue(unicode(category))


class FixtureCase(ExampleModelCase):
    """Test the build in camelot model for fixtures"""

    def test_fixture(self):
        from camelot.model.party import Person
        from camelot.model.fixture import Fixture
        session = Session()
        self.assertEqual(Fixture.find_fixture_key(Person, -1), None)
        p1 = Person()
        self.assertEqual(Fixture.find_fixture_key_and_class(p1), (None, None))
        session.expunge(p1)
        p2 = Fixture.insert_or_update_fixture(Person, 'test', {'first_name': 'Peter', 'last_name': 'Principle'}, fixture_class='test')
        self.assertEqual(Fixture.find_fixture_key(Person, p2.id), 'test')
        self.assertEqual(Fixture.find_fixture_key_and_class(p2), ('test', 'test'))
        self.assertEqual(Fixture.find_fixture_keys_and_classes(Person)[p2.id], ('test',
                                                                                'test'))
        session.delete(p2)
        session.flush()
        p3 = Fixture.insert_or_update_fixture(Person, 'test', {'first_name': 'Peter', 'last_name': 'Principle'}, fixture_class='test')
        self.assertNotEqual(p2, p3)
        Fixture.remove_all_fixtures(Person)
        return

    def test_fixture_version(self):
        from camelot.model.party import Person
        from camelot.model.fixture import FixtureVersion
        session = self.session
        self.assertEqual(FixtureVersion.get_current_version('unexisting'), 0)
        FixtureVersion.set_current_version('demo_data', 0)
        session.flush()
        self.assertEqual(FixtureVersion.get_current_version('demo_data'), 0)
        example_file = os.path.join(os.path.dirname(__file__), '..', 'camelot_example', 'import_example.csv')
        person_count_before_import = Person.query.count()
        import csv
        if FixtureVersion.get_current_version('demo_data') == 0:
            reader = csv.reader(open(example_file))
            for line in reader:
                Person(first_name=line[0], last_name=line[1])

            FixtureVersion.set_current_version('demo_data', 1)
            session.flush()
        self.assertTrue(Person.query.count() > person_count_before_import)
        self.assertEqual(FixtureVersion.get_current_version('demo_data'), 1)


class CustomizationCase(ExampleModelCase):

    def test_add_field(self):
        metadata.drop_all()
        session = Session()
        party.Person.language = schema.Column(types.Unicode(30))
        metadata.create_all()
        p = party.Person(first_name='Peter', last_name='Principle', language='English')
        session.flush()


class StatusCase(TestMetaData):

    def test_status_type(self):
        Entity, session = self.Entity, self.session
        from camelot.model import type_and_status

        class Invoice(Entity, type_and_status.StatusMixin):
            book_date = schema.Column(types.Date(), nullable=False)
            status = type_and_status.Status()

        self.create_all()
        self.assertTrue(issubclass(Invoice._status_type, type_and_status.StatusType))
        self.assertTrue(issubclass(Invoice._status_history, type_and_status.StatusHistory))
        draft = Invoice._status_type(code='DRAFT')
        ready = Invoice._status_type(code='READY')
        session.flush()
        self.assertTrue(unicode(ready))
        invoice = Invoice(book_date=datetime.date.today())
        self.assertEqual(invoice.current_status, None)
        invoice.change_status(draft, status_from_date=datetime.date.today())
        self.assertEqual(invoice.current_status, draft)
        self.assertEqual(invoice.get_status_from_date(draft), datetime.date.today())
        self.assertTrue(len(invoice.status))
        for history in invoice.status:
            self.assertTrue(unicode(history))

        return

    def test_status_enumeration(self):
        Entity, session = self.Entity, self.session
        from camelot.model import type_and_status

        class Invoice(Entity, type_and_status.StatusMixin):
            book_date = schema.Column(types.Date(), nullable=False)
            status = type_and_status.Status(enumeration=[(1, 'DRAFT'),
             (2, 'READY')])

            class Admin(EntityAdmin):
                list_display = [
                 'book_date', 'current_status']
                list_actions = [type_and_status.ChangeStatus('DRAFT'),
                 type_and_status.ChangeStatus('READY')]
                form_actions = list_actions

        self.create_all()
        self.assertTrue(issubclass(Invoice._status_history, type_and_status.StatusHistory))
        invoice = Invoice(book_date=datetime.date.today())
        self.assertEqual(invoice.current_status, None)
        invoice.change_status('DRAFT', status_from_date=datetime.date.today())
        self.assertEqual(invoice.current_status, 'DRAFT')
        self.assertEqual(invoice.get_status_from_date('DRAFT'), datetime.date.today())
        draft_invoices = Invoice.query.filter(Invoice.current_status == 'DRAFT').count()
        ready_invoices = Invoice.query.filter(Invoice.current_status == 'READY').count()
        self.assertEqual(draft_invoices, 1)
        self.assertEqual(ready_invoices, 0)
        ready_action = Invoice.Admin.list_actions[(-1)]
        model_context = MockModelContext()
        model_context.obj = invoice
        list(ready_action.model_run(model_context))
        self.assertTrue(invoice.current_status, 'READY')
        return