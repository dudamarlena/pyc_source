# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/djubby/dispatcher.py
# Compiled at: 2010-04-21 04:21:52
import logging
from django.http import HttpResponse, HttpResponseRedirect, Http404
from configuration import Configuration
from resource import Resource
from http import Http303, get_preferred_prefix, get_preferred_output, get_mimetype, url_handler
from urllib2 import URLError

def dispatcher(request, ref=None):
    logging.debug("Dispatching request on '%s'..." % ref)
    conf = Configuration()
    if ref == None or len(ref) == 0:
        index = conf.get_value('indexResource')
        index = index.replace(conf.get_value('datasetBase'), conf.get_value('webBase'))
        logging.debug('Redirecting to the index resource...')
        return HttpResponseRedirect(index)
    else:
        try:
            (uri, prefix) = url_handler(ref)
            resource = Resource(uri)
        except ValueError, ve:
            logging.error("Error processing request for '%s': %s" % (ref, str(ve)))
            raise Http404(ve)
        except URLError, ue:
            logging.error("Error retrieving data for '%s': %s" % (ref, str(ue)))
            raise Http404(ue)

        if prefix == None:
            prefix = get_preferred_prefix(request)
            get_url = getattr(resource, 'get_%s_url' % prefix)
            url = get_url()
            logging.debug('Redirecting to the %s representation of %s: %s' % (prefix, uri, url))
            return Http303(url)
        else:
            output = get_preferred_output(request, prefix)
            func = getattr(resource, 'get_%s_%s' % (prefix, output))
            mimetype = get_mimetype(prefix, output)
            logging.debug('Returning the %s representation of %s serialized as %s' % (prefix, uri, output))
            return HttpResponse(func(), mimetype=mimetype)
    return