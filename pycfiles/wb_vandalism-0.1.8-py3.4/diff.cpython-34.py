# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wb_vandalism/features/diff.py
# Compiled at: 2015-11-17 10:14:47
# Size of source mod 2**32: 13363 bytes
import re
from Levenshtein import ratio
from revscoring.features import Feature
from ..datasources import diff, parent_revision, revision
current_item = revision.item
past_item = parent_revision.item

class property_changed(Feature):
    __doc__ = "\n    Returns True if a property has changed.\n\n    :Parameters:\n        property : `str`\n            The property name\n        name : `str`\n            A name to associate with the feature.  If not set, the feature's\n            name will be 'property_changed(<property>)'\n    "

    def __init__(self, property, name=None):
        self.property = property
        if name is None:
            name = 'property_changed({0})'.format(repr(property))
        super().__init__(name, self._process, returns=bool, depends_on=[
         diff.changed_claims])

    def _process(self, changed_claims):
        return self.property in [claims[0].id for claims in changed_claims]


def process_no_added_sitelinks(sitelinks_differ):
    return len(sitelinks_differ.added())


number_added_sitelinks = Feature('number_added_sitelinks', process_no_added_sitelinks, returns=int, depends_on=[
 diff.sitelinks_differ])

def process_no_removed_sitelinks(sitelinks_differ):
    return len(sitelinks_differ.removed())


number_removed_sitelinks = Feature('number_removed_sitelinks', process_no_removed_sitelinks, returns=int, depends_on=[
 diff.sitelinks_differ])

def process_no_changed_sitelinks(sitelinks_differ):
    return len(sitelinks_differ.changed())


number_changed_sitelinks = Feature('number_changed_sitelinks', process_no_changed_sitelinks, returns=int, depends_on=[
 diff.sitelinks_differ])

def process_no_added_labels(labels_differ):
    return len(labels_differ.added())


number_added_labels = Feature('number_added_labels', process_no_added_labels, returns=int, depends_on=[
 diff.labels_differ])

def process_no_removed_labels(labels_differ):
    return len(labels_differ.removed())


number_removed_labels = Feature('number_removed_labels', process_no_removed_labels, returns=int, depends_on=[
 diff.labels_differ])

def process_no_changed_labels(labels_differ):
    return len(labels_differ.changed())


number_changed_labels = Feature('number_changed_labels', process_no_changed_labels, returns=int, depends_on=[
 diff.labels_differ])

def process_no_added_descriptions(descriptions_differ):
    return len(descriptions_differ.added())


number_added_descriptions = Feature('number_added_descriptions', process_no_added_descriptions, returns=int, depends_on=[
 diff.descriptions_differ])

def process_no_removed_descriptions(descriptions_differ):
    return len(descriptions_differ.removed())


number_removed_descriptions = Feature('number_removed_descriptions', process_no_removed_descriptions, returns=int, depends_on=[diff.descriptions_differ])

def process_no_changed_descriptions(descriptions_differ):
    return len(descriptions_differ.changed())


number_changed_descriptions = Feature('number_changed_descriptions', process_no_changed_descriptions, returns=int, depends_on=[diff.descriptions_differ])

def process_no_added_aliases(aliases_differ, current_item, past_item):
    no_added = 0
    for lang in aliases_differ.added():
        no_added += len(current_item.aliases[lang])

    for lang in aliases_differ.changed():
        for alias in current_item.aliases[lang]:
            if alias not in past_item.aliases[lang]:
                no_added += 1
                continue

    return no_added


number_added_aliases = Feature('number_added_aliases', process_no_added_aliases, returns=int, depends_on=[
 diff.aliases_differ, current_item, past_item])

def process_no_removed_aliases(aliases_differ, current_item, past_item):
    no_removed = 0
    for lang in aliases_differ.removed():
        no_removed += len(past_item.aliases[lang])

    for lang in aliases_differ.changed():
        for alias in past_item.aliases[lang]:
            if alias not in current_item.aliases[lang]:
                no_removed += 1
                continue

    return no_removed


number_removed_aliases = Feature('number_removed_aliases', process_no_removed_aliases, returns=int, depends_on=[
 diff.aliases_differ, current_item, past_item])

def process_no_added_claims(added_claims):
    return len(added_claims)


number_added_claims = Feature('number_added_claims', process_no_added_claims, returns=int, depends_on=[
 diff.added_claims])

def process_no_removed_claims(removed_claims):
    return len(removed_claims)


number_removed_claims = Feature('number_removed_claims', process_no_removed_claims, returns=int, depends_on=[
 diff.removed_claims])

def process_no_changed_claims(changed_claims):
    return len(changed_claims)


number_changed_claims = Feature('number_changed_claims', process_no_changed_claims, returns=int, depends_on=[
 diff.changed_claims])

def process_no_changed_identifiers(changed_claims):
    counter = 0
    for old, new in changed_claims:
        if isinstance(old.target, str):
            counter += 1
            continue

    return counter


number_changed_identifiers = Feature('number_changed_identifiers', process_no_changed_identifiers, returns=int, depends_on=[
 diff.changed_claims])

def process_en_label_touched(labels_differ):
    return 'en' in labels_differ.changed()


en_label_touched = Feature('en_label_touched', process_en_label_touched, returns=bool, depends_on=[
 diff.labels_differ])

def process_no_added_sources(added_sources):
    return len(added_sources)


number_added_sources = Feature('number_added_sources', process_no_added_sources, returns=int, depends_on=[
 diff.added_sources])

def process_no_removed_sources(removed_sources):
    return len(removed_sources)


number_removed_sources = Feature('number_removed_sources', process_no_removed_sources, returns=int, depends_on=[
 diff.removed_sources])

def process_no_added_qualifiers(added_qualifiers):
    return len(added_qualifiers)


number_added_qualifiers = Feature('number_added_qualifiers', process_no_added_qualifiers, returns=int, depends_on=[
 diff.added_qualifiers])

def process_no_removed_qualifiers(removed_qualifiers):
    return len(removed_qualifiers)


number_removed_qualifiers = Feature('number_removed_qualifiers', process_no_removed_qualifiers, returns=int, depends_on=[
 diff.removed_qualifiers])

def process_no_added_badges(badges_differ, current_item, past_item):
    no_added = 0
    for lang in badges_differ.added():
        no_added += len(current_item.badges[lang])

    for lang in badges_differ.changed():
        for badge in current_item.badges[lang]:
            if badge not in past_item.badges[lang]:
                no_added += 1
                continue

    return no_added


number_added_badges = Feature('number_added_badges', process_no_added_badges, returns=int, depends_on=[
 diff.badges_differ, current_item, past_item])

def process_no_removed_badges(badges_differ, current_item, past_item):
    no_removed = 0
    for lang in badges_differ.removed():
        no_removed += len(past_item.badges[lang])

    for lang in badges_differ.changed():
        for badge in past_item.badges[lang]:
            if badge not in current_item.badges[lang]:
                no_removed += 1
                continue

    return no_removed


number_removed_badges = Feature('number_removed_badges', process_no_removed_badges, returns=int, depends_on=[
 diff.badges_differ, current_item, past_item])

def process_mean_distance_desc(parent, current, differ):
    changed = differ.changed()
    if not changed:
        return 0.0
    distance = 0
    for lang in changed:
        distance += 1 - ratio(current.descriptions[lang], parent.descriptions[lang])

    return distance / len(changed)


mean_distance_descriptions = Feature('mean_distance_descriptions', process_mean_distance_desc, returns=float, depends_on=[
 past_item, current_item, diff.descriptions_differ])

def process_mean_distance_labels(parent, current, differ):
    changed = differ.changed()
    if not changed:
        return 0.0
    distance = 0
    for lang in changed:
        distance += 1 - ratio(current.labels[lang], parent.labels[lang])

    return distance / len(changed)


mean_distance_labels = Feature('mean_distance_labels', process_mean_distance_labels, returns=float, depends_on=[
 current_item, past_item, diff.labels_differ])

def process_proportion_of_qid_added(current_item, past_item):
    past_item_doc = past_item.toJSON() if past_item is not None else {}
    re_qid = re.compile('Q\\d{1,8}')
    current_item_qids = len(re.findall(re_qid, str(current_item.toJSON())))
    past_item_qids = len(re.findall(re_qid, str(past_item_doc)))
    return float(current_item_qids - past_item_qids) / float(current_item_qids + 1)


proportion_of_qid_added = Feature('proportion_of_qid_added', process_proportion_of_qid_added, returns=float, depends_on=[
 current_item, past_item])
LANGUAGE_REGEXES = '(a(frikaa?ns|lbanian?|lemanha|ng(lais|ol)|ra?b(e?|[ei]c|ian?|isc?h)|rmenian?|ssamese|azeri|z[eə]rba(ijani?|ycan(ca)?|yjan)|нглийский)|b(ahasa( (indonesia|jawa|malaysia|melayu))?|angla|as(k|qu)e|[aeo]ng[ao]?li|elarusian?|okmål|osanski|ra[sz]il(ian?)?|ritish( kannada)?|ulgarian?)|c(ebuano|hina|hinese( simplified)?|zech|roat([eo]|ian?)|atal[aà]n?|рпски|antonese)|[cč](esky|e[sš]tina)|d(an(isc?h|sk)|e?uts?ch)|e(esti|ll[hi]nika|ng(els|le(ski|za)|lisc?h)|spa(g?[nñ]h?i?ol|nisc?h)|speranto|stonian|usk[ae]ra)|f(ilipino|innish|ran[cç](ais|e|ez[ao])|ren[cs]h|arsi|rancese)|g(al(ego|ician)|uja?rati|ree(ce|k)|eorgian|erman[ay]?|ilaki)|h(ayeren|ebrew|indi|rvatski|ungar(y|ian))|i(celandic|ndian?|ndonesian?|ngl[eê]se?|ngilizce|tali(ano?|en(isch)?))|ja(pan(ese)?|vanese)|k(a(nn?ada|zakh)|hmer|o(rean?|sova)|urd[iî])|l(at(in[ao]?|vi(an?|e[sš]u))|ietuvi[uų]|ithuanian?)|m(a[ck]edon(ian?|ski)|agyar|alay(alam?|sian?)?|altese|andarin|arathi|elayu|ontenegro|ongol(ian?)|yanmar)|n(e(d|th)erlands?|epali|orw(ay|egian)|orsk( bokm[aå]l)?|ynorsk)|o(landese|dia)|p(ashto|ersi?an?|ol(n?isc?h|ski)|or?tugu?[eê]se?(( d[eo])? brasil(eiro)?| ?\\(brasil\\))?|unjabi)|r(om[aâi]ni?[aă]n?|um(ano|änisch)|ussi([ao]n?|sch))|s(anskrit|erbian|imple english|inha?la|lov(ak(ian?)?|enš?[cč]ina|en(e|ij?an?)|uomi)|erbisch|pagnolo?|panisc?h|rbeska|rpski|venska|c?wedisc?h|hqip)|t(a(galog|mil)|elugu|hai(land)?|i[eế]ng vi[eệ]t|[uü]rk([cç]e|isc?h|iş|ey))|u(rdu|zbek)|v(alencia(no?)?|ietnamese)|welsh|(англиис|[kк]алмыкс|[kк]азахс|немец|[pр]усс|[yу]збекс|татарс)кий( язык)??|עברית|[kкқ](аза[кқ]ша|ыргызча|ирилл)|українськ(а|ою)|б(еларуская|ългарски( език)?)|ελλ[ηι]νικ(ά|α)|ქართული|हिन्दी|ไทย|[mм]онгол(иа)?|([cс]рп|[mм]акедон)ски|العربية|日本語|한국(말|어)|\u200cहिनद़ि|বাংলা|ਪੰਜਾਬੀ|मराठी|ಕನ್ನಡ|اُردُو|தமிழ்|తెలుగు|ગુજરાતી|فارسی|پارسی|മലയാളം|پښتو|မြန်မာဘာသာ|中文(简体|繁體)?|中文（(简体?|繁體)）|简体|繁體)'
LANGUAGE_RE = re.compile(LANGUAGE_REGEXES)

def process_proportion_of_language_added(current_item, past_item):
    past_item_doc = past_item.toJSON() if past_item is not None else {}
    current_item_res = len(re.findall(LANGUAGE_RE, str(current_item.toJSON())))
    past_item_res = len(re.findall(LANGUAGE_RE, str(past_item_doc)))
    return float(current_item_res - past_item_res) / float(current_item_res + 1)


proportion_of_language_added = Feature('proportion_of_language_added', process_proportion_of_language_added, returns=float, depends_on=[current_item, past_item])

def process_proportion_of_links_added(current_item, past_item):
    past_item_doc = past_item.toJSON() if past_item is not None else {}
    re_qid = re.compile('https?\\://|wwww\\.')
    current_item_res = len(re.findall(re_qid, str(current_item.toJSON())))
    past_item_res = len(re.findall(re_qid, str(past_item_doc)))
    return float(current_item_res - past_item_res) / float(current_item_res + 1)


proportion_of_links_added = Feature('proportion_of_links_added', process_proportion_of_links_added, returns=float, depends_on=[current_item, past_item])