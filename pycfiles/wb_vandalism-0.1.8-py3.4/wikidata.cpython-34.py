# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wb_vandalism/feature_lists/wikidata.py
# Compiled at: 2015-12-19 13:27:28
# Size of source mod 2**32: 6094 bytes
from revscoring.features import user
from revscoring.features.modifiers import not_, log
from ..features import diff, revision

class properties:
    __doc__ = '\n    Mapping of english descriptions to property identifiers\n    '
    IMAGE = 'P18'
    SEX_OR_GENDER = 'P21'
    COUNTRY_OF_CITIZENSHIP = 'P27'
    INSTANCE_OF = 'P31'
    MEMBER_OF_SPORTS_TEAM = 'P54'
    SIGNATURE = 'P109'
    COMMONS_CATEGORY = 'P373'
    DATE_OF_BIRTH = 'P569'
    DATE_OF_DEATH = 'P570'
    OFFICIAL_WEBSITE = 'P856'


class items:
    __doc__ = '\n    Mapping of english descriptions to item idenifiers\n    '
    HUMAN = 'Q5'


is_client_delete = revision.comment_matches('^\\/\\* clientsitelink\\-remove\\:', name='revision.is_client_delete')
is_client_move = revision.comment_matches('^\\/\\* clientsitelink\\-update\\:', name='revision.is_client_move')
is_merge_into = revision.comment_matches('^\\/\\* wbmergeitems\\-to\\:', name='revision.is_merge_into')
is_merge_from = revision.comment_matches('^\\/\\* wbmergeitems\\-from\\:', name='revision.is_merge_from')
is_revert = revision.comment_matches('^Reverted edits by \\[\\[Special\\:Contributions', name='revision.is_revert')
is_rollback = revision.comment_matches('^Undid revision ', name='revision.is_rollback')
is_restore = revision.comment_matches('^Restored revision ', name='revision.is_restore')
is_item_creation = revision.comment_matches('^\\/\\* (wbsetentity|wbeditentity-create\\:0\\|) \\*\\/', name='revision.is_item_creation')
sex_or_gender_changed = diff.property_changed(properties.SEX_OR_GENDER, name='diff.sex_or_gender_changed')
country_of_citizenship_changed = diff.property_changed(properties.COUNTRY_OF_CITIZENSHIP, name='diff.country_of_citizenship_changed')
member_of_sports_team_changed = diff.property_changed(properties.MEMBER_OF_SPORTS_TEAM, name='diff.member_of_sports_team_changed')
date_of_birth_changed = diff.property_changed(properties.DATE_OF_BIRTH, name='diff.date_of_birth_changed')
image_changed = diff.property_changed(properties.IMAGE, name='diff.image_changed')
signature_changed = diff.property_changed(properties.SIGNATURE, name='diff.signature_changed')
commons_category_changed = diff.property_changed(properties.COMMONS_CATEGORY, name='diff.commons_category_changed')
official_website_changed = diff.property_changed(properties.OFFICIAL_WEBSITE, name='diff.official_website_changed')
is_human = revision.has_property_value(properties.INSTANCE_OF, items.HUMAN, name='revision.is_human')
has_birthday = revision.has_property(properties.DATE_OF_BIRTH, name='revision.has_birthday')
dead = revision.has_property(properties.DATE_OF_BIRTH, name='revision.dead')
is_blp = has_birthday.and_(not_(dead))
reverted = [
 log(user.age + 1),
 diff.number_added_sitelinks,
 diff.number_removed_sitelinks,
 diff.number_changed_sitelinks,
 diff.number_added_labels,
 diff.number_removed_labels,
 diff.number_changed_labels,
 diff.number_added_descriptions,
 diff.number_removed_descriptions,
 diff.number_changed_descriptions,
 diff.number_added_aliases,
 diff.number_removed_aliases,
 diff.number_added_claims,
 diff.number_removed_claims,
 diff.number_changed_claims,
 diff.number_changed_identifiers,
 diff.en_label_touched,
 diff.number_added_sources,
 diff.number_removed_sources,
 diff.number_added_qualifiers,
 diff.number_removed_qualifiers,
 diff.number_added_badges,
 diff.number_removed_badges,
 diff.proportion_of_qid_added,
 diff.proportion_of_language_added,
 diff.proportion_of_links_added,
 is_client_move,
 is_client_delete,
 is_merge_into,
 is_merge_from,
 is_revert,
 is_rollback,
 is_restore,
 is_item_creation,
 sex_or_gender_changed,
 country_of_citizenship_changed,
 member_of_sports_team_changed,
 date_of_birth_changed,
 image_changed,
 signature_changed,
 commons_category_changed,
 official_website_changed,
 log(revision.number_claims + 1),
 log(revision.number_aliases + 1),
 log(revision.number_sources + 1),
 log(revision.number_qualifiers + 1),
 log(revision.number_badges + 1),
 log(revision.number_labels + 1),
 log(revision.number_sitelinks + 1),
 log(revision.number_descriptions + 1),
 is_human,
 is_blp,
 user.is_bot,
 user.is_anon]