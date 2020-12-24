# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: gitenberg/metadata/marc.py
# Compiled at: 2016-03-08 12:03:43
"""
This takes a MARCXML filename as an argument and converts it into
MARC records for the unglued pandata (in .xml and .mrc formats).

"""
import pymarc, logging
from datetime import datetime
from StringIO import StringIO
import licenses
from .utils import marc_rels, inverse_marc_rels, plural, reverse_name
main_entries = [
 'aut', 'edt', 'trl', 'ill']

def stub(pandata):
    record = pymarc.Record(force_utf8=True)
    now = datetime.now()
    record.add_ordered_field(pymarc.Field(tag='001', data='stb' + now.strftime('%y%m%d%H%M%S')))
    add_stuff(record)
    new_field_value = now.strftime('%y%m%d') + 's'
    publication_date = pandata.gutenberg_issued
    if publication_date and len(publication_date) > 3:
        new_field_value += publication_date[0:4]
    else:
        new_field_value += '||||'
    new_field_value += '||||xx |||||o|||||||||||eng||'
    record.add_ordered_field(pymarc.Field(tag='008', data=new_field_value))
    identifiers = pandata.identifiers
    isbn = identifiers.get('isbn', None)
    if isbn:
        record.add_ordered_field(pymarc.Field(tag='020', indicators=[
         ' ', ' '], subfields=[
         'a', isbn]))
    related = identifiers.get('isbns_related', [])
    for isbn in related:
        record.add_ordered_field(pymarc.Field(tag='020', indicators=[
         ' ', ' '], subfields=[
         'a', isbn + ' (related)']))

    oclc = identifiers.get('oclc', None)
    if oclc:
        record.add_ordered_field(pymarc.Field(tag='035', indicators=[
         ' ', ' '], subfields=[
         'a', '(OCoLC)' + str(oclc)]))
    creators = []
    for marc_type in main_entries:
        creator = pandata.creator.get(marc_rels.get(marc_type), None)
        if creator:
            creators.append((marc_type, creator))
        else:
            creator = pandata.creator.get(marc_rels.get(plural(marc_type)), [])
            for each_creator in creator:
                creators.append((marc_type, each_creator))

    if creators:
        marc_code, creator = creators[0]
        sortname = creator.get('agent_sortname', '')
        if not sortname:
            sortname = reverse_name(creator.get('agent_name', ''))
        record.add_ordered_field(pymarc.Field(tag='100', indicators=[
         '1', ' '], subfields=[
         'a', sortname,
         '4', marc_code]))
    if pandata.language:
        is_translation = '1' if pandata.translators else '0'
        record.add_ordered_field(pymarc.Field(tag='041', indicators=[
         is_translation, 'iso639-1'], subfields=[
         'a', pandata.language]))
    contributors = creators[1:] if creators else []
    for contributor_type in pandata.contributor.keys():
        contributor = pandata.contributor[contributor_type]
        marc_code = inverse_marc_rels.get(contributor_type, 'unk')
        if contributor_type in marc_rels.values():
            contributors.append((marc_code, contributor))
        else:
            for each_contributor in contributor:
                contributors.append((marc_code, each_contributor))

    for marc_code, contributor in contributors:
        sortname = contributor.get('agent_sortname', '')
        if not sortname:
            sortname = reverse_name(contributor.get('agent_name', ''))
        record.add_ordered_field(pymarc.Field(tag='700', indicators=[
         '1', ' '], subfields=[
         'a', sortname,
         'e', marc_rels[marc_code].replace('_', ' ') + '.',
         '4', marc_code]))

    record.add_ordered_field(pymarc.Field(tag='245', indicators=[
     '1', '0'], subfields=[
     'a', pandata.title,
     'a', '[electronic resource]']))
    if pandata.publisher:
        field260 = pymarc.Field(tag='260', indicators=[
         ' ', ' '], subfields=[
         'b', pandata.publisher])
        if publication_date:
            field260.add_subfield('c', unicode(publication_date))
        record.add_ordered_field(field260)
    if pandata.description:
        field520 = pymarc.Field(tag='520', indicators=[
         ' ', ' '], subfields=[
         'a', pandata.description])
        record.add_ordered_field(field520)
    if pandata.subjects:
        for subject in pandata.subjects:
            if isinstance(subject, tuple):
                authority, heading = subject
            elif isinstance(subject, str):
                authority, heading = '', subject
            else:
                continue
            if authority == 'lcsh':
                subjectfield = pymarc.Field(tag='650', indicators=['0', '0'])
                subjectfield.add_subfield('a', heading)
            elif authority == 'lcc':
                subjectfield = pymarc.Field(tag='050', indicators=['0', '0'])
                subjectfield.add_subfield('a', heading)
            elif authority == '':
                subjectfield = pymarc.Field(tag='653', indicators=['0', '0'])
                subjectfield.add_subfield('a', heading)
            else:
                subjectfield = None
            if subjectfield:
                record.add_ordered_field(subjectfield)

    add_license(record, pandata)
    return record


def add_license(record, pandata):
    if pandata.rights:
        record.add_ordered_field(pymarc.Field(tag='536', indicators=[
         ' ', ' '], subfields=[
         'a', pandata.funding_info]))
        field540 = pymarc.Field(tag='540', indicators=[
         ' ', ' '], subfields=[
         'a', dict(licenses.CHOICES).get(pandata.rights, pandata.rights)])
        rights_url = pandata.rights_url if pandata.rights_url else dict(licenses.GRANTS).get(pandata.rights, None)
        if rights_url:
            field540.add_subfield('u', rights_url)
        record.add_ordered_field(field540)
    return


def add_stuff(record):
    record.add_ordered_field(pymarc.Field(tag='003', data='GITenberg'))
    datestamp = datetime.now().strftime('%Y%m%d%H%M%S') + '.0'
    record.add_ordered_field(pymarc.Field(tag='005', data=datestamp))
    record.add_ordered_field(pymarc.Field(tag='006', data='m     o  d        '))
    record.add_ordered_field(pymarc.Field(tag='007', data='cr'))