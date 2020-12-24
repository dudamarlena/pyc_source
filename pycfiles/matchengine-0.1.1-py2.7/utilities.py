# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/matchengine/utilities.py
# Compiled at: 2017-02-10 11:07:01
"""Copyright 2016 Dana-Farber Cancer Institute"""
import os, sys, yaml, json, logging, datetime as dt
from pymongo import MongoClient
import oncotreenx
from matchengine.settings import months, TUMOR_TREE

def build_gquery(field, txt):
    """Builds the Mongo query from the genomic criteria"""
    neg = False
    if field.lower() == 'wildcard_protein_change':
        if txt.startswith('!'):
            neg = True
            txt = txt[1:]
        if not txt.startswith('p.'):
            txt = 'p.' + txt
        key = '$regex'
        txt = '^%s[A-Z]' % txt
    elif field.lower() == 'variant_category' and txt.lower() == 'any variation':
        txt = [
         'MUTATION', 'CNV']
        key = '$in'
    else:
        if field.lower() == 'variant_category' and txt in ('SV', '!SV'):
            return (None, None, None)
        if isinstance(txt, str) and txt.startswith('!') or isinstance(txt, unicode) and txt.startswith('!'):
            key = '$eq'
            neg = True
            if field.lower() == 'exon':
                txt = int(txt.replace('!', ''))
            else:
                txt = txt.replace('!', '')
        else:
            key = '$eq'
    return (
     key, txt, neg)


def build_cquery(c, norm_field, txt):
    """Builds the Mongo query from the clinical criteria"""
    if isinstance(txt, list):
        c[norm_field] = {}
        for i in txt:
            if i.startswith('!'):
                if '$nin' in c[norm_field]:
                    c[norm_field]['$nin'].append(i.replace('!', ''))
                else:
                    c[norm_field]['$nin'] = [
                     i.replace('!', '')]
            elif '$in' in c[norm_field]:
                c[norm_field]['$in'].append(i)
            else:
                c[norm_field]['$in'] = [
                 i]

    else:
        if txt.startswith('!'):
            key = '$ne'
            txt = txt.replace('!', '')
        else:
            key = '$eq'
        c[norm_field] = {key: txt}
    return c


def build_oncotree():
    """Builds oncotree"""
    return oncotreenx.build_oncotree(file_path=TUMOR_TREE)


def normalize_fields(mapping, field):
    """Translates yaml field name into the database field name."""
    old_keys = [ i['key_old'] for i in mapping ]
    new_keys = [ i['key_new'] for i in mapping ]
    vals = [ i['values'] for i in mapping ]
    val_map = dict(zip(new_keys, vals))
    field = field.upper()
    if field in old_keys:
        field = new_keys[old_keys.index(field)]
        return (
         field, val_map[field])
    else:
        return (
         field, val_map[field])


def normalize_values(mapping, field, val):
    """Translates yaml fields and values into database fields and values"""
    field, mapping = normalize_fields(mapping, field)
    ne = False
    map_by = val
    if isinstance(val, str) and val[0] == '!' or isinstance(val, unicode) and val[0] == '!':
        map_by = val[1:]
        ne = True
    if map_by in mapping:
        if ne:
            return (field, '!%s' % str(mapping[map_by]))
        else:
            return (
             field, mapping[map_by])

    else:
        return (
         field, val)


def samples_from_mrns(db, mrns):
    """Returns a dictionary mapping each MRN to all of its associated SAMPLE_IDs"""
    clinical = list(db.clinical.find({'DFCI_MRN': {'$in': mrns}}, {'DFCI_MRN': 1, 'SAMPLE_ID': 1}))
    mrn_map = {}
    for c in clinical:
        mrn_map[c['SAMPLE_ID']] = c['DFCI_MRN']

    return mrn_map


def search_birth_date(c):
    """Converts query to filter by birth date based on the given age"""
    txt = c['BIRTH_DATE']['$eq']
    if txt.startswith('>='):
        key = '$lte'
    else:
        if txt.startswith('<='):
            key = '$gte'
        elif txt.startswith('>'):
            key = '$lt'
        elif txt.startswith('<'):
            key = '$gt'
        else:
            raise ValueError
        idx = 1
        if txt[1] == '=':
            idx = 2
        abs_age = str(txt[idx:])
        today = dt.datetime.today()
        if '.' in abs_age:
            month, year = get_months(abs_age, today)
            query_date = today.replace(month=month, year=today.year + year)
        else:
            try:
                query_date = today.replace(year=today.year - int(abs_age))
            except ValueError:
                query_date = today + (dt.datetime(today.year + int(abs_age), 1, 1) - dt.datetime(today.year, 1, 1))

    return {key: query_date}


def get_months(abs_age, today):
    """Given a decimal, returns the number of months and number of years to subtract from today"""
    split_age = str(abs_age).split('.')
    month = split_age[1]
    month = int(float(month) * 12 / 10 ** len(month))
    if split_age[0] == '':
        year = 0
    else:
        year = int(split_age[0])
    if today.month - month <= 0:
        month = months.index(months[(-abs(today.month - month))])
        year = -(year + 1)
    return (month, year)


def add_trials(trial_path, db):
    """Adds all ymls in the "trial_path" to the db"""
    inserted_ids = 0
    for yml in os.listdir(trial_path):
        ymlpath = os.path.join(trial_path, yml)
        if yml.split('.')[(-1)] != 'yml':
            continue
        with open(ymlpath) as (f):
            t = yaml.load(f.read())
            result = db.trial.insert_one(t)
            if result.inserted_id:
                inserted_ids += 1

    return inserted_ids


def format_genomic_alteration(g, query):
    """Format the genomic alteration that matched a particular trial"""
    if g is None:
        return g
    else:
        gene = 'TRUE_HUGO_SYMBOL'
        mut = 'TRUE_PROTEIN_CHANGE'
        cnv = 'CNV_CALL'
        var = 'TRUE_VARIANT_CLASSIFICATION'
        sv = 'VARIANT_CATEGORY'
        wt = 'WILDTYPE'
        alteration = ''
        is_variant = 'gene'
        if query.keys()[0] == '$and':
            query = query['$and'][0]
        if mut in query and query[mut] is not None:
            is_variant = 'variant'
        if wt in g and g[wt] is True:
            alteration += 'wt '
        if gene in g and g[gene] is not None:
            alteration += g[gene]
        if mut in g and g[mut] is not None:
            alteration += ' %s' % g[mut]
        elif cnv in g and g[cnv] is not None:
            alteration += ' %s' % g[cnv]
        elif var in g and g[var] is not None:
            alteration += ' %s' % g[var]
        elif sv in g and g[sv] == 'SV':
            alteration += ' Structural Variation'
        return (alteration, is_variant)


def format_not_match(g):
    """Format the genomic alteration for genomic documents that matched a negative clause of a match tree"""
    alteration = ''
    is_variant = 'gene'
    gene = 'TRUE_HUGO_SYMBOL'
    mut = 'TRUE_PROTEIN_CHANGE'
    cnv = 'CNV_CALL'
    var = 'TRUE_VARIANT_CLASSIFICATION'
    sv = 'VARIANT_CATEGORY'
    if g.keys()[0] == '$and':
        g = g['$and'][0]
    if gene in g and g[gene] is not None:
        alteration = format_query(g[gene], gene=True)
    if mut in g and g[mut] is not None:
        alteration += ' %s' % format_query(g[mut])
        is_variant = 'variant'
    elif cnv in g and g[cnv] is not None:
        alteration += ' %s' % format_query(g[cnv])
    elif var in g and g[var] is not None:
        alteration += ' %s' % format_query(g[var])
    elif sv in g and g[sv][g[sv].keys()[0]] == 'SV':
        alteration += ' Structural Variation'
    if gene not in g or g[gene] is None:
        alteration = '!' + alteration[1:]
    return (alteration, is_variant)


def format_query(g, gene=False):
    """Turns the mongo query into a formatted genomic alteration"""
    alteration = ''
    key = g.keys()[0]
    if key == '$regex':
        alteration += '!%s' % g[key].replace('^', '').replace('[A-Z]', '')
    elif key == '$in':
        for item in g[key][:-1]:
            alteration += '!%s, ' % item

        alteration += '!%s' % g[key][(-1)]
    else:
        alteration += '!%s' % g[key]
    if not gene:
        alteration = alteration.replace('!', '')
    return alteration


def add_matches(trial_matches, db):
    """Add the match table to the database or update what already exists theres"""
    if trial_matches:
        db.trial_match.drop()
        db.trial_match.insert_many(trial_matches)


def get_db(uri):
    """Returns a Mongo connection"""
    if uri:
        MONGO_URI = uri
    else:
        MONGO_URI = ''
        file_path = os.getenv('SECRETS_JSON', None)
        if file_path is None:
            uri = os.getenv('MONGO_URI')
            if uri:
                MONGO_URI = uri
            else:
                logging.error('ENVAR SECRETS_JSON not set')
                sys.exit(1)
        else:
            with open(file_path) as (fin):
                vars = json.load(fin)
                for name, value in vars.iteritems():
                    if name == 'MONGO_URI':
                        MONGO_URI = value

    if not MONGO_URI:
        logging.error('MONGO_URI not set in SECRETS_JSON')
    else:
        os.environ['MONGO_URI'] = MONGO_URI
        connection = MongoClient(MONGO_URI)
        return connection['matchminer']
    return