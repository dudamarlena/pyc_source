# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/cromulent/extract.py
# Compiled at: 2019-12-02 16:46:42
import re, warnings
from collections import namedtuple
from cromulent import model, vocab
CURRENCY_MAPPING = {'österreichische schilling': 'at shillings', 
   'florins': 'de florins', 
   'fl': 'de florins', 
   'fl.': 'de florins', 
   'pounds': 'gb pounds', 
   'livres': 'fr livres', 
   'guineas': 'gb guineas', 
   'reichsmark': 'de reichsmarks'}
NEXT_FINER_DIMENSION_UNIT = {'inches': None, 
   'feet': 'inches', 
   'cm': None, 
   'fr_feet': 'fr_inches', 
   'fr_inches': 'ligne'}
NUMBER_PATTERN = '((?:\\d+\\s+\\d+/\\d+)|(?:\\d+/\\d+)|(?:\\d+(?:[.,]\\d+)?))'
UNIT_PATTERN = '(\'|"|d(?:[.]?|uymen)|pouc[e.]s?|in(?:ch(?:es)?|[.]?)|pieds?|v[.]?|voeten|f(?:eet|oot|t[.]?)|cm|lignes?|linges?)'
DIMENSION_PATTERN = '(%s\\s*(?:%s)?)' % (NUMBER_PATTERN, UNIT_PATTERN)
DIMENSION_RE = re.compile('\\s*%s' % (DIMENSION_PATTERN,))
SIMPLE_WIDTH_HEIGHT_PATTERN = '(?:\\s*((?<!\\w)[wh]|width|height))?'
SIMPLE_DIMENSIONS_PATTERN_X1 = '(?P<d1>(?:%s\\s*)+)(?P<d1w>%s)' % (
 DIMENSION_PATTERN, SIMPLE_WIDTH_HEIGHT_PATTERN)
SIMPLE_DIMENSIONS_RE_X1 = re.compile(SIMPLE_DIMENSIONS_PATTERN_X1)
SIMPLE_DIMENSIONS_PATTERN_X2a = '(?P<d1>(?:%s\\s*)+)(?P<d1w>%s)(?:,)?\\s*(x|by)(?P<d2>(?:\\s*%s)+)(?P<d2w>%s)' % (
 DIMENSION_PATTERN,
 SIMPLE_WIDTH_HEIGHT_PATTERN,
 DIMENSION_PATTERN,
 SIMPLE_WIDTH_HEIGHT_PATTERN)
SIMPLE_DIMENSIONS_PATTERN_X2b = '(?P<d1w>%s)\\s*(?P<d1>(?:%s\\s*)+)*(?:(?:,)?\\s*(x|by)|,\\s*)(?P<d2w>%s)\\s*(?P<d2>(?:\\s*%s)+)' % (
 SIMPLE_WIDTH_HEIGHT_PATTERN,
 DIMENSION_PATTERN,
 SIMPLE_WIDTH_HEIGHT_PATTERN,
 DIMENSION_PATTERN)
SIMPLE_DIMENSIONS_RE_X2a = re.compile(SIMPLE_DIMENSIONS_PATTERN_X2a)
SIMPLE_DIMENSIONS_RE_X2b = re.compile(SIMPLE_DIMENSIONS_PATTERN_X2b)
FRENCH_DIMENSIONS_PATTERN = '[Hh](?:(?:aut(?:eur|[.])?)|[.])\\s*(?P<d1>(?:%s\\s*)+),? [Ll](?:(?:arge?(?:ur|[.])?)|[.])\\s*(?P<d2>(?:%s\\s*)+)' % (
 DIMENSION_PATTERN, DIMENSION_PATTERN)
FRENCH_DIMENSIONS_RE = re.compile(FRENCH_DIMENSIONS_PATTERN)
DUTCH_DIMENSIONS_PATTERN = '(?P<d1w>[Hh]oogh?[.]?|[Bb]reedt?) (?P<d1>(?:%s\\s*)+), (?P<d2w>[Hh]oogh?[.]?|[Bb]reedt?) (?P<d2>(?:%s\\s*)+)' % (
 DIMENSION_PATTERN, DIMENSION_PATTERN)
DUTCH_DIMENSIONS_RE = re.compile(DUTCH_DIMENSIONS_PATTERN)
Dimension = namedtuple('Dimension', [
 'value',
 'unit',
 'which'])

def _canonical_value(value):
    try:
        value = value.replace(',', '.')
        parts = value.split(None, 1)
        if len(parts) > 1 and '/' in parts[1]:
            intpart = int(parts[0])
            numer, denom = map(int, parts[1].split('/', 1))
            fracpart = float(numer) / denom
            value = str(intpart + fracpart)
        else:
            if len(parts) == 1 and '/' in parts[0]:
                intpart = 0
                numer, denom = map(int, parts[0].split('/', 1))
                fracpart = float(numer) / denom
                value = str(intpart + fracpart)
            if value.startswith('.'):
                value = '0' + value
            try:
                return int(value)
            except ValueError:
                return float(value)

    except:
        pass

    return


def _canonical_unit(value):
    inches = {
     'duymen', 'd.', 'd', '"'}
    feet = {'pieds', 'pied', 'feet', 'foot', 'voeten', 'v.', 'v', "'"}
    fr_inches = {'pouces', 'pouce', 'pouc.'}
    fr_feet = {'pieds', 'pied'}
    if value is None:
        return
    else:
        value = value.lower()
        if value in fr_inches:
            return 'fr_inches'
        if value in fr_feet:
            return 'fr_feet'
        if 'ligne' in value or 'linge' in value:
            return 'ligne'
        if 'in' in value or value in inches:
            return 'inches'
        if 'ft' in value or value in feet:
            return 'feet'
        if 'cm' in value:
            return 'cm'
        return


def _canonical_which(value):
    if not value:
        return
    else:
        value = value.strip().lower()
        if value.startswith('w'):
            return 'width'
        if value.startswith('h'):
            return 'height'
        warnings.warn('*** Unknown which dimension: %s' % (value,))
        return


def parse_simple_dimensions(value, which=None):
    """
        Parse the supplied string for dimensions (value + unit), and return a list of
        `Dimension`s, optionally setting the `which` property to the supplied value.

        Examples:

        1 cm
        2ft
        5 pieds
        """
    if value is None:
        return
    else:
        value = value.strip()
        dims = []
        last_unit = None
        for match in re.finditer(DIMENSION_RE, value):
            matched_value = _canonical_value(match.group(2))
            if not matched_value:
                warnings.warn('*** failed to canonicalize dimension value: %s' % (match.group(2),))
                return
            unit_value = match.group(3)
            matched_unit = _canonical_unit(unit_value)
            if matched_unit is None:
                matched_unit = NEXT_FINER_DIMENSION_UNIT.get(last_unit)
            if unit_value and not matched_unit:
                warnings.warn('*** not a recognized unit: %s' % (unit_value,))
            which = _canonical_which(which)
            dim = Dimension(value=matched_value, unit=matched_unit, which=which)
            last_unit = matched_unit
            dims.append(dim)

        if not dims:
            return
        return dims


def normalized_dimension_object(dimensions, source=None):
    """
        Normalizes the given `dimensions`, or returns `None` is normalization fails.

        Returns a tuple of the normalized data, and a label which preserves the original
        set of dimensions.

        For example, the input:

                [
                        Dimension(value=10, unit='feet', which=None),
                        Dimension(value=3, unit='inches', which=None),
                ]

        results in the output:

                (
                        Dimension(value=123.0, unit='inches', which=None),
                        "10 feet, 3 inches"
                )
        """
    normalized = normalize_dimension(dimensions, source=source)
    if not normalized:
        return
    else:
        labels = []
        for dim in dimensions:
            if dim.unit == 'inches':
                units = ('inch', 'inches')
            elif dim.unit == 'feet':
                units = ('foot', 'feet')
            elif dim.unit == 'fr_feet':
                units = ('French foot', 'French feet')
            elif dim.unit == 'fr_inches':
                units = ('French inch', 'French inches')
            elif dim.unit == 'cm':
                units = ('cm', 'cm')
            elif dim.unit == 'ligne':
                units = ('ligne', 'lignes')
            elif dim.unit is None:
                units = ('', '')
            else:
                warnings.warn('*** unrecognized unit: {dim.unit}')
                return
            unit = units[0] if float(dim.value) == 1.0 else units[1]
            if unit:
                label = '%s %s' % (dim.value, unit)
            else:
                label = str(dim.value)
            labels.append(label)

        label = (', ').join(labels)
        return (
         normalized, label)


def normalize_dimension(dimensions, source=None):
    """
        Given a list of `Dimension`s, normalize them into a single Dimension (e.g. values in
        both feet and inches become a single dimension of inches).

        If the values cannot be sensibly combined (e.g. inches + centimeters), returns `None`.
        """
    unknown = 0
    inches = 0
    fr_inches = 0
    centimeters = 0
    used_unknown = False
    used_inches = False
    used_fr_inches = False
    used_centimeters = False
    which = None
    for dim in dimensions:
        which = dim.which
        if dim.unit == 'inches':
            inches += dim.value
            used_inches = True
        elif dim.unit == 'feet':
            inches += 12 * dim.value
            used_inches = True
        elif dim.unit == 'cm':
            centimeters += dim.value
            used_centimeters = True
        elif dim.unit == 'fr_feet':
            fr_inches += 12.0 * dim.value
            used_fr_inches = True
        elif dim.unit == 'fr_inches':
            fr_inches += dim.value
            used_fr_inches = True
        elif dim.unit == 'ligne':
            fr_inches += dim.value / 12.0
            used_fr_inches = True
        elif dim.unit is None:
            unknown += dim.value
            used_unknown = True
        else:
            warnings.warn('*** unrecognized unit: %s' % (dim.unit,))
            return

    used_systems = 0
    for used in (used_inches, used_fr_inches, used_centimeters, used_unknown):
        if used:
            used_systems += 1

    if used_systems != 1:
        if source:
            warnings.warn('*** dimension used a mix of metric, imperial, and/or unknown: %r; source is %r' % (
             dimensions, source))
        else:
            warnings.warn('*** dimension used a mix of metric, imperial, and/or unknown: %r' % (
             dimensions,))
        return
    if fr_inches:
        return Dimension(value=fr_inches, unit='fr_inches', which=which)
    else:
        if inches:
            return Dimension(value=inches, unit='inches', which=which)
        if centimeters:
            return Dimension(value=centimeters, unit='cm', which=which)
        return Dimension(value=unknown, unit=None, which=which)


def extract_physical_dimensions(dimstr):
    dimensions = dimensions_cleaner(dimstr)
    if dimensions:
        for orig_d in dimensions:
            dimdata = normalized_dimension_object(orig_d, source=dimstr)
            if dimdata:
                dimension, label = dimdata
                if dimension.which == 'height':
                    dim = vocab.Height(ident='')
                elif dimension.which == 'width':
                    dim = vocab.Width(ident='')
                else:
                    dim = vocab.PhysicalDimension(ident='')
                dim.value = dimension.value
                dim.identified_by = model.Name(ident='', content=label)
                unit = vocab.instances.get(dimension.unit)
                if unit:
                    dim.unit = unit
                yield dim


def dimensions_cleaner(value):
    """
        Attempt to parse a set of dimensions from the given string.

        Returns a tuple of `pipeline.util.Dimension` objects if parsing succeeds,
        None otherwise.
        """
    if value is None:
        return
    else:
        cleaners = [
         simple_dimensions_cleaner_x2,
         french_dimensions_cleaner_x2,
         dutch_dimensions_cleaner_x2,
         simple_dimensions_cleaner_x1]
        for cleaner in cleaners:
            dimension = cleaner(value)
            if dimension:
                return dimension

        return


def french_dimensions_cleaner_x2(value):
    """Attempt to parse 2 dimensions from a French-formatted string."""
    match = FRENCH_DIMENSIONS_RE.match(value)
    if match:
        groups = match.groupdict()
        dim1 = parse_simple_dimensions(groups['d1'], 'h')
        dim2 = parse_simple_dimensions(groups['d2'], 'w')
        if dim1 and dim2:
            return (dim1, dim2)
        warnings.warn('dim1: %s %s h' % (dim1, groups['d1']))
        warnings.warn('dim2: %s %s w' % (dim2, groups['d2']))
        warnings.warn('*** Failed to parse dimensions: %s' % (value,))
    return


def dutch_dimensions_cleaner_x2(value):
    """Attempt to parse 2 dimensions from a Dutch-formatted string."""
    match = DUTCH_DIMENSIONS_RE.match(value)
    if match:
        groups = match.groupdict()
        height = 'h'
        width = 'w'
        if 'breed' in groups['d1w'].lower():
            height, width = width, height
        dim1 = parse_simple_dimensions(groups['d1'], height)
        dim2 = parse_simple_dimensions(groups['d2'], width)
        if dim1 and dim2:
            return (dim1, dim2)
        warnings.warn('dim1: %s %s h' % (dim1, groups['d1']))
        warnings.warn('dim2: %s %s w' % (dim2, groups['d2']))
        warnings.warn('*** Failed to parse dimensions: %s' % (value,))
    return


def simple_dimensions_cleaner_x1(value):
    """Attempt to parse 1 dimension from a string."""
    match = SIMPLE_DIMENSIONS_RE_X1.match(value)
    if match:
        groups = match.groupdict()
        dim1 = parse_simple_dimensions(groups['d1'], groups['d1w'])
        if dim1:
            return (dim1,)
    return


def simple_dimensions_cleaner_x2(value):
    """Attempt to parse 2 dimensions from a string."""
    for pattern in (SIMPLE_DIMENSIONS_RE_X2a, SIMPLE_DIMENSIONS_RE_X2b):
        match = pattern.match(value)
        if match:
            groups = match.groupdict()
            dim1 = parse_simple_dimensions(groups['d1'], groups['d1w'])
            dim2 = parse_simple_dimensions(groups['d2'], groups['d2w'])
            if dim1 and dim2:
                return (dim1, dim2)
            warnings.warn('dim1: %s %s %s' % (dim1, groups['d1'], groups['d1w']))
            warnings.warn('dim2: %s %s %s' % (dim2, groups['d2'], groups['d2w']))
            warnings.warn('*** Failed to parse dimensions: %s' % (value,))

    return


def extract_monetary_amount(data, add_citations=False, currency_mapping=CURRENCY_MAPPING):
    """
        Returns a `MonetaryAmount`, `StartingPrice`, or `EstimatedPrice` object
        based on properties of the supplied `data` dict. If no amount or currency
        data is found in found, returns `None`.

        For `EstimatedPrice`, values will be accessed from these keys:
                - amount: `est_price_amount` or `est_price`
                - currency: `est_price_currency` or `est_price_curr`
                - note: `est_price_note` or `est_price_desc`
                - bibliographic statement: `est_price_citation`

        For `StartingPrice`, values will be accessed from these keys:
                - amount: `start_price_amount` or `start_price`
                - currency: `start_price_currency` or `start_price_curr`
                - note: `start_price_note` or `start_price_desc`
                - bibliographic statement: `start_price_citation`

        For `MonetaryAmount` prices, values will be accessed from these keys:
                - amount: `price_amount` or `price`
                - currency: `price_currency` or `price_curr`
                - note: `price_note` or `price_desc`
                - bibliographic statement: `price_citation`
        """
    amount_type = 'Price'
    if 'price' in data or 'price_amount' in data:
        amnt = model.MonetaryAmount(ident='')
        price_amount = data.get('price_amount', data.get('price'))
        price_currency = data.get('currency', data.get('price_currency', data.get('price_curr')))
        note = data.get('price_note', data.get('price_desc'))
        cite = data.get('price_citation', data.get('citation'))
    elif 'est_price' in data or 'est_price_amount' in data:
        amnt = vocab.EstimatedPrice(ident='')
        price_amount = data.get('est_price_amount', data.get('est_price'))
        price_currency = data.get('currency', data.get('est_price_currency', data.get('est_price_curr')))
        amount_type = 'Estimated Price'
        note = data.get('est_price_note', data.get('est_price_desc'))
        cite = data.get('est_price_citation', data.get('citation'))
    elif 'start_price' in data or 'start_price_amount' in data:
        amnt = vocab.StartingPrice(ident='')
        price_amount = data.get('start_price_amount', data.get('start_price'))
        price_currency = data.get('currency', data.get('start_price_currency', data.get('start_price_curr')))
        amount_type = 'Starting Price'
        note = data.get('start_price_note', data.get('start_price_desc'))
        cite = data.get('start_price_citation', data.get('citation'))
    else:
        return
    if price_amount or price_currency:
        if cite and add_citations:
            amnt.referred_to_by = vocab.BibliographyStatement(ident='', content=cite)
        if note:
            amnt.referred_to_by = vocab.Note(ident='', content=note)
        if price_amount:
            try:
                value = price_amount
                value = value.replace('[?]', '')
                value = value.replace('?', '')
                value = value.strip()
                price_amount = float(value)
                amnt.value = price_amount
            except ValueError:
                amnt._label = price_amount
                amnt.identified_by = model.Name(ident='', content=price_amount)

        if price_currency:
            price_currency_key = price_currency
            try:
                price_currency_key = currency_mapping[price_currency_key.lower()]
            except KeyError:
                pass

            if isinstance(price_currency_key, model.BaseResource):
                amnt.currency = price_currency_key
            elif price_currency_key in vocab.instances:
                amnt.currency = vocab.instances[price_currency_key]
            else:
                warnings.warn('*** No currency instance defined for %s' % (price_currency_key,))
        if price_amount and price_currency:
            amnt._label = '%s %s' % (price_amount, price_currency)
        elif price_amount:
            amnt._label = '%s' % (price_amount,)
        return amnt
    return