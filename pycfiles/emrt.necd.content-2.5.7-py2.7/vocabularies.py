# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/vocabularies.py
# Compiled at: 2020-04-10 03:06:36
import itertools
from operator import itemgetter
from plone.registry.interfaces import IRegistry
from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from plone.i18n.normalizer.interfaces import IURLNormalizer
import plone.api as api
from emrt.necd.content import MessageFactory as _
from emrt.necd.content.constants import LDAP_SECTOREXP
from emrt.necd.content.constants import ROLE_LR
from emrt.necd.content.constants import ROLE_SE
from emrt.necd.content.constants import ROLE_MSA
from emrt.necd.content.constants import ROLE_MSE
from emrt.necd.content.utilities.interfaces import IGetLDAPWrapper
from emrt.necd.content.nfr_code_matching import INECDSettings
from emrt.necd.content.nfr_code_matching import nfr_codes

def get_valid_user():
    try:
        user = api.user.get_current()
    except Exception:
        return

    if user and not api.user.is_anonymous():
        return user
    else:
        return


def validate_term(prefix, groups):
    return tuple([ group for group in groups if group.startswith(prefix)
                 ])


def build_prefix(ldap_role, sector):
    return ('{}-{}-').format(ldap_role, sector)


def vocab_from_terms(*terms):
    return SimpleVocabulary([ SimpleVocabulary.createTerm(key, key, value['title']) for key, value in terms
                            ])


def check_user_for_vocab(context, user):
    user_roles = api.user.get_roles(obj=context)
    user_groups = tuple(user.getGroups())
    user_has_sectors = tuple([ group for group in user_groups if '-sector' in group
                             ])
    user_is_lr_or_manager = set(user_roles).intersection((ROLE_LR, 'Manager'))
    return not user_is_lr_or_manager and user_has_sectors


class INECDVocabularies(Interface):
    projection_pollutants = schema.Dict(title=_('Projection pollutants vocabulary'), description=_('Registers the values for pollutants in the context of a Projection ReviewFolder'), key_type=schema.TextLine(title=_('Pollutant key')), value_type=schema.TextLine(title=_('Pollutant value')))
    projection_parameter = schema.Dict(title=_('Projection parameter vocabulary'), description=_('Registers the values for parameter in the context of a Projection ReviewFolder'), key_type=schema.TextLine(title=_('Parameter key')), value_type=schema.TextLine(title=_('Parameter value')))
    activity_data = schema.Dict(title=_('Activity data'), description=_('Registers the activity data'), key_type=schema.TextLine(title=_('Activity data type')), value_type=schema.List(value_type=schema.TextLine(title=_('Activity data'))))


def mk_term(key, value):
    return SimpleVocabulary.createTerm(key, key, value)


def get_registry_interface_field_data(interface, field):
    registry = getUtility(IRegistry)
    registry_data = registry.forInterface(interface)
    return registry_data.__getattr__(field)


@implementer(IVocabularyFactory)
class MSVocabulary(object):

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('eea_member_states')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class GHGSourceCategory(object):

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('ghg_source_category')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class GHGSourceSectors(object):

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('ghg_source_sectors')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class Pollutants(object):

    def __call__(self, context):
        terms = []
        if context.type == 'inventory':
            pvoc = api.portal.get_tool('portal_vocabularies')
            voc = pvoc.getVocabularyByName('pollutants')
            if voc is not None:
                for key, value in voc.getVocabularyLines():
                    terms.append(SimpleVocabulary.createTerm(key, key, value))

        else:
            pollutants = get_registry_interface_field_data(INECDVocabularies, 'projection_pollutants')
            for key, value in pollutants.items():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class Fuel(object):

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('fuel')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class Highlight(object):

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc_name = 'highlight' if context.type == 'inventory' else 'highlight_projection'
        voc = pvoc.getVocabularyByName(voc_name)
        if voc is None:
            return SimpleVocabulary([])
        else:
            terms = [ mk_term(*pair) for pair in voc.getVocabularyLines() ]
            return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class Parameter(object):

    def __call__(self, context):
        terms = []
        if context.type == 'inventory':
            pvoc = api.portal.get_tool('portal_vocabularies')
            voc = pvoc.getVocabularyByName('parameter')
            if voc is not None:
                for key, value in voc.getVocabularyLines():
                    terms.append(SimpleVocabulary.createTerm(key, key, value))

        else:
            pollutants = get_registry_interface_field_data(INECDVocabularies, 'projection_parameter')
            for key, value in pollutants.items():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class StatusFlag(object):

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('status_flag')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class NFRCode(object):

    def __call__(self, context):
        user = get_valid_user()
        if user:
            ldap_wrapper = getUtility(IGetLDAPWrapper)(context)
            user_groups = tuple(user.getGroups())
            vocab_with_validate = check_user_for_vocab(context, user)
            if vocab_with_validate:
                return vocab_from_terms(*((term_key, term) for term_key, term in nfr_codes(context).items() if validate_term(build_prefix(ldap_wrapper(LDAP_SECTOREXP), term['ldap']), user_groups)))
        return vocab_from_terms(*nfr_codes(context).items())


@implementer(IVocabularyFactory)
class NFRCodeInventories(object):

    def __call__(self, context):
        user = get_valid_user()
        if user:
            ldap_wrapper = getUtility(IGetLDAPWrapper)(context)
            user_groups = tuple(user.getGroups())
            vocab_with_validate = check_user_for_vocab(context, user)
            registry_field = 'nfrcodeMapping_projection_inventory'
            if vocab_with_validate:
                return vocab_from_terms(*((term_key, term) for term_key, term in nfr_codes(context, field=registry_field).items() if validate_term(build_prefix(ldap_wrapper(LDAP_SECTOREXP), term['ldap']), user_groups)))
        return vocab_from_terms(*nfr_codes(context, 'nfrcodeMapping_projection_inventory').items())


@implementer(IVocabularyFactory)
class Conclusions(object):

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('conclusion_reasons')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class SectorNames(object):

    def __call__(self, context):
        sectorNames = get_registry_interface_field_data(INECDSettings, 'sectorNames')
        return SimpleVocabulary([ mk_term(sector, name) for sector, name in sorted(sectorNames.items(), key=itemgetter(0))
                                ])


@implementer(IVocabularyFactory)
class ActivityData(object):

    def __call__(self, context):
        normalizer = getUtility(IURLNormalizer).normalize
        activity_data = get_registry_interface_field_data(INECDVocabularies, 'activity_data')
        activities = sorted(set(itertools.chain(*activity_data.values())))
        terms = [ mk_term(normalizer(activity), activity) for activity in activities
                ]
        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class ActivityDataType(object):

    def __call__(self, context):
        activity_data = get_registry_interface_field_data(INECDVocabularies, 'activity_data')
        terms = []
        for activity_type in activity_data.keys():
            terms.append(SimpleVocabulary.createTerm(activity_type))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class ScenarioType(object):

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('scenario_type')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class Roles(object):

    def __call__(self, context):
        terms = list(itertools.starmap(mk_term, [
         ('Manager', 'Manager'),
         (
          ROLE_SE, 'Sector Expert'),
         (
          ROLE_LR, 'Lead Reviewer'),
         (
          ROLE_MSA, 'MS Authority'),
         (
          ROLE_MSE, 'MS Expert')]))
        return SimpleVocabulary(terms)