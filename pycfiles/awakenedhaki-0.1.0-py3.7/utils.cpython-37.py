# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/crossrefapiclient/utils.py
# Compiled at: 2020-02-20 17:53:49
# Size of source mod 2**32: 6086 bytes
import logging
from urllib.parse import quote_plus
from functools import wraps
VALIDATORS = {'query':[
  'query',
  'container_title',
  'author',
  'editor',
  'chair',
  'translator',
  'contributor',
  'bibliographic',
  'affiliation'], 
 'sort':[
  'score',
  'relevance',
  'updated',
  'deposited',
  'indexed',
  'published',
  'published-print',
  'published-online',
  'issued',
  'is-referenced-by-count',
  'reference-count'], 
 'order':[
  'asc', 'desc'], 
 'members->filter':[
  'has_public_references',
  'reference_visibility',
  'backfile_doi_count',
  'current_doi_count'], 
 'funders->filter':[
  'location'], 
 'workers->filter':[
  'has_funder',
  'funder',
  'lcoation',
  'prefix',
  'member',
  'from_index_date',
  'until_index_date',
  'from_deposit_date',
  'until_deposit_date',
  'from_update_date',
  'until_update_date',
  'from_created_date',
  'until_created_date',
  'from_pub_date',
  'until_pub_date',
  'from_online_pub_date',
  'until_online_pub_date',
  'from_print_pub_date',
  'until_print_pub_date',
  'from_posted_date',
  'until_posted_date',
  'from_accepted_date',
  'until_accepted_date',
  'has_license',
  'lincense.url',
  'license.version',
  'license.delay',
  'has_full_text',
  'full_text.version',
  'full_text.type',
  'full_text.application',
  'has_references',
  'reference_visibility',
  'has_archive',
  'archive',
  'has_orcid',
  'has_authenticated_orcid',
  'orcid',
  'issn',
  'isbn',
  'type',
  'directory',
  'doi',
  'updates',
  'is_update',
  'has_update_policy',
  'container_title',
  'category_name',
  'type',
  'type_name',
  'award.number',
  'award.funder',
  'assertion',
  'has_assertion',
  'alternative_id',
  'article_number',
  'has_abstract',
  'has_clinical_trial_number',
  'content_domain',
  'has_content_domain',
  'has_domain_restriction',
  'has_relation',
  'relation.type',
  'relation.object',
  'relation.object_type']}

def validate(attribute=None):
    """
    Verifies user defined parameters are compliant with CrossRef.

    Arguments
    ---------
    attribute : str (optional; default is None)
        Attribute for which a value must be retrieved from class of wrapped
        method. Required do to differences in keywords depending on Resource.

    Exceptions
    ----------
    ValueError
        If a user defined parameter is not within validation list.
    """

    def inner(func):

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            validator = _select_validator(self, func, attribute)
            parameters = {}
            for key, value in kwargs.items():
                if key not in validator:
                    raise ValueError(f"Invalid {func.__name__} field.")
                parameters[_fix_parameter_name(key)] = quote_plus(value)
            else:
                return func(self, *args, **parameters)

        return wrapper

    return inner


def _select_validator(obj, func, attribute):
    """
    Select appropriate validation list for a given function and attribute.

    Arguments
    ---------
    obj : Object
        A python object
    func : Function
        A python function
    attribute : str
        Name of an attribute of obj.

    Returns
    -------
    A list of strings of CrossRef compliant parameters.
    """
    if attribute is not None:
        attribute = attribute.format(vars(obj))
        field = f"{attribute}->{func.__name__}"
    else:
        field = func.__name__
    validator = VALIDATORS[field]
    if field == 'sort':
        validator.extend(VALIDATORS['order'])
    return validator


def prefix_query(func):
    """
    Prefixes query parameters with "query.".
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        queries = {}
        for key, value in kwargs.copy().items():
            queries[f"query.{key}"] = value

        return func(*args, **queries)

    return wrapper


def _fix_parameter_name(field):
    """
    Fixes user defined parameter names to comply with CrossRef.
    """
    return field.replace('_', '-')


def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(stream_format)
    logger.addHandler(stream_handler)
    file_handler = logging.FileHandler('file.log')
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    return logger


def _filter_builder(**kwargs):
    """
    Formats filters into a string of comma separated parameters.
    """
    field = [f"{filter_name}:{quote_plus(value)}" for filter_name, value in kwargs.items()]
    return ','.join(field)