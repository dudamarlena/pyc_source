# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/orlo/util.py
# Compiled at: 2017-04-04 09:14:06
from __future__ import print_function, unicode_literals
from flask import json
from orlo.app import app
from orlo.orm import db, Release, Package, Platform
from orlo.exceptions import InvalidUsage
from sqlalchemy.orm import exc
from six import string_types
import uuid
__author__ = b'alforbes'

def append_or_create_platforms(request_platforms):
    """
    Create the platforms if they don't exist, and return a list of Platform
    objects

    :param list request_platforms: List of strings denoting platform names
    """
    platforms = []
    for p in request_platforms:
        try:
            query = db.session.query(Platform).filter(Platform.name == p)
            platform = query.one()
        except exc.NoResultFound:
            app.logger.info((b'Creating platform {}').format(p))
            platform = Platform(p)
            db.session.add(platform)

        platforms.append(platform)

    return platforms


def create_release(request):
    """
    Create a Release object from a request
    """
    references = request.json.get(b'references', [])
    if references and type(references) is list:
        references = list_to_string(references)
    request_platforms = request.json.get(b'platforms')
    if request_platforms and type(request_platforms) is not list:
        request_platforms = [
         request_platforms]
    platforms = append_or_create_platforms(request_platforms)
    release = Release(platforms=platforms, user=request.json[b'user'], team=request.json.get(b'team'), references=references)
    return release


def create_package(release_id, request):
    """
    Create a package object for a release
    """
    return Package(release_id, request.json.get(b'name'), request.json.get(b'version'), diff_url=request.json.get(b'diff_url', None), rollback=request.json.get(b'rollback', False))


def fetch_release(release_id):
    """
    Fetch a release by ID
    """
    rq = db.session.query(Release).filter(Release.id == release_id)
    release = rq.first()
    if not release:
        raise InvalidUsage(b'Release does not exist')
    return release


def fetch_package(release_id, package_id):
    """
    Fetch a package, and validate it is part of the release
    """
    fetch_release(release_id)
    pq = db.session.query(Package).filter(Package.id == package_id)
    package = pq.first()
    if not package:
        raise InvalidUsage(b'Package does not exist')
    if str(package.release_id) != release_id:
        raise InvalidUsage(b'This package does not belong to this release')
    return package


def validate_request_json(request):
    try:
        request.json
    except Exception:
        raise InvalidUsage(b'Could not parse JSON document')

    if not request.json:
        raise InvalidUsage(b'Missing application/json header', status_code=400)


def validate_release_input(request):
    validate_request_json(request)
    if b'platforms' not in request.json:
        raise InvalidUsage(b'JSON doc missing platforms field', status_code=400)
    return True


def validate_package_input(request, release_id):
    validate_request_json(request)
    if b'name' not in request.json or b'version' not in request.json:
        raise InvalidUsage(b'Missing name / version in request body.')
    app.logger.debug((b'Package request validated, release_id {}').format(release_id))
    return True


def _validate_package_stop_input(request):
    validate_request_json(request)
    if b'success' not in request.json:
        raise InvalidUsage(b'Missing success key in JSON doc')


def list_to_string(array):
    """
    Convert a list to a string for storage in the DB

    :param array:
    :return:
    """
    if not array:
        return []
    return b'["' + (b'", "').join(array) + b'"]'


def stream_json_list(heading, iterator):
    """
    A lagging generator to stream JSON so we don't have to hold everything in
    memory

    This is a little tricky, as we need to omit the last comma to make valid
    JSON, thus we use a lagging generator, similar to
    http://stackoverflow.com/questions/1630320/

    :param heading: The title of the set, e.g. "releases"
    :param iterator: Any object with __iter__(), e.g. SQLAlchemy Query
    """
    iterator = iterator.__iter__()
    try:
        prev_release = next(iterator)
    except StopIteration:
        yield (b'{{"{}": []}}').format(heading)
        raise StopIteration

    yield (b'{{"{}": [').format(heading)
    for item in iterator:
        yield json.dumps(prev_release.to_dict()) + b', '
        prev_release = item

    yield json.dumps(prev_release.to_dict()) + b']}'
    db.session.close()


def str_to_bool(value):
    if isinstance(value, string_types):
        try:
            value = int(value)
        except ValueError:
            if value.lower() in ('t', 'true'):
                return True
            if value.lower() in ('f', 'false'):
                return False

    if isinstance(value, int):
        if value > 0:
            return True
        return False
    raise ValueError((b'Value {} can not be cast as boolean').format(value))


def is_uuid(string):
    """
    Test whether a string is a valid UUID

    :param string:
    :return:
    """
    try:
        uuid.UUID(string)
    except ValueError:
        return False

    return True