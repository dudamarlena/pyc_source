# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/parente/projects/nbviewer/nbviewer/providers/__init__.py
# Compiled at: 2016-10-24 14:40:21
# Size of source mod 2**32: 2016 bytes
default_providers = ['nbviewer.providers.{}'.format(prov) for prov in ['url', 'github', 'gist']]
default_rewrites = ['nbviewer.providers.{}'.format(prov) for prov in ['gist', 'github', 'dropbox', 'url']]

def provider_handlers(providers):
    """Load tornado URL handlers from an ordered list of dotted-notation modules
       which contain a `default_handlers` function

       `default_handlers` should accept a list of handlers and returns an
       augmented list of handlers: this allows the addition of, for
       example, custom URLs which should be intercepted before being
       handed to the basic `url` handler
    """
    return _load_provider_feature('default_handlers', providers)


def provider_uri_rewrites(providers):
    """Load (regex, template) tuples from an ordered list of dotted-notation
       modules which contain a `uri_rewrites` function

       `uri_rewrites` should accept a list of rewrites and returns an
       augmented list of rewrites: this allows the addition of, for
       example, the greedy behavior of the `gist` and `github` providers
    """
    return _load_provider_feature('uri_rewrites', providers)


def _load_provider_feature(feature, providers):
    """Load the named feature from an ordered list of dotted-notation modules
       which each implements the feature.

       The feature will be passed a list of feature implementations and must
       return that list, suitably modified.
    """
    features = []
    for provider in providers:
        mod = __import__(provider, fromlist=[feature])
        features = getattr(mod, feature)(features)

    return features