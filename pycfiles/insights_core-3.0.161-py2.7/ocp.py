# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/ocp.py
# Compiled at: 2019-12-13 11:35:35
"""
Top level OpenShift 4 component
===============================
The :py:func:`conf` component recognizes insights-operator and must-gather
archives.
"""
import logging, os, yaml
from fnmatch import fnmatch
from insights.core.plugins import component
from insights.core.context import InsightsOperatorContext, MustGatherContext
from insights.core.archives import extract
from insights.parsr.query import from_dict, Result
from insights.util import content_type
log = logging.getLogger(__name__)
try:
    Loader = yaml.CSafeLoader
except:
    log.info("Couldn't find libyaml loader. Falling back to python loader.")
    Loader = yaml.SafeLoader

def _get_files(path):
    for root, dirs, names in os.walk(path):
        for name in names:
            yield os.path.join(root, name)


def _load(path):
    with open(path) as (f):
        doc = yaml.load(f, Loader=Loader)
        return from_dict(doc)


def _process(path, excludes=None):
    excludes = excludes if excludes is not None else []
    for f in _get_files(path):
        if excludes and any(fnmatch(f, e) for e in excludes):
            continue
        try:
            yield _load(f)
        except Exception:
            log.debug('Failed to load %s; skipping.', f)

    return


def analyze(paths, excludes=None):
    if not isinstance(paths, list):
        paths = [
         paths]
    results = []
    for path in paths:
        if content_type.from_file(path) == 'text/plain':
            results.append(_load(path))
        elif os.path.isdir(path):
            results.extend(_process(path, excludes))
        else:
            with extract(path) as (ex):
                results.extend(_process(ex.tmp_dir, excludes))

    return Result(children=results)


@component([InsightsOperatorContext, MustGatherContext])
def conf(io, mg):
    """
    The ``conf`` component parses all configuration in an insights-operator or
    must-gather archive and returns an object that is part of the parsr common
    data model.  It can be navigated and queried in a standard way. See the
    `tutorial`_ for details.

    .. _tutorial: https://insights-core.readthedocs.io/en/latest/notebooks/Parsr%20Query%20Tutorial.html
    """
    return analyze((io or mg).root)