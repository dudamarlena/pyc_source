# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/bprc/stepprocessor.py
# Compiled at: 2016-08-20 13:14:45
# Size of source mod 2**32: 15085 bytes
__doc__ = '\nThis module implements the logic to process a step in a recipe\n'
import sys, os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import logging, json, requests, re
from functools import partial
from bprc.recipe import Body
from bprc.utils import vlog
from bprc.utils import errlog
from bprc.utils import verboseprint
from bprc.utils import httpstatuscodes
from bprc.utils import php_sub_pattern
from bprc.utils import var_sub_pattern
from bprc.utils import file_sub_pattern
from urllib.parse import urlencode
import bprc.cli
from bprc.outputprocessor import OutputProcessor
from bprc._version import __version__

class BodyEncoder(json.JSONEncoder):
    """BodyEncoder"""

    def default(self, body):
        logging.debug('inside JSON BodyEncoder.default()')
        if isinstance(body, Body):
            return body._body


class StepProcessor:
    """StepProcessor"""

    def __init__(self, *, recipe, stepid, variables):
        """Instantiates the Step Processor Object"""
        self.recipe = recipe
        self.stepid = stepid
        self.variables = variables

    def prepare(self):
        """prepares the step by substituting php-like constructs or variables in the step subtree of the passed recipe"""
        vlog('Step parser initialised for step ' + str(self.stepid))
        from bprc.utils import _insert_file_param
        from bprc.utils import _insert_php_param
        from bprc.utils import _insert_var

        def executeSubstition(*, re, substitfunc, inputstring, recipe, variables):
            """executes the appropriate substitution type, given a:
            - regex pattern
            - substitution function
            - input text
            - the recipe object
            - the variables object
            """
            vlog('Commencing ' + str(inputstring) + ' substitution with ' + substitfunc.__name__)
            substituted_text, n = re.subn(partial(substitfunc, recipe=recipe, variables=variables), str(inputstring))
            vlog('Made -------------' + str(n) + ' substitutions resulting in ' + substituted_text)
            return substituted_text

        parts = [
         self.recipe.steps[self.stepid].name,
         self.recipe.steps[self.stepid].URL,
         self.recipe.steps[self.stepid].request.querystring,
         self.recipe.steps[self.stepid].request.body,
         self.recipe.steps[self.stepid].request.headers]
        subREs = [
         var_sub_pattern, php_sub_pattern, file_sub_pattern]
        subfuncs = [_insert_var, _insert_php_param, _insert_file_param]
        partlist = []
        for part in parts:
            for subRE, subfunc in zip(subREs, subfuncs):
                if isinstance(part, str):
                    part = executeSubstition(re=subRE, substitfunc=subfunc, inputstring=part, recipe=self.recipe, variables=self.variables)
                elif hasattr(part, '__getitem__'):
                    for key in part:
                        part[key] = executeSubstition(re=subRE, substitfunc=subfunc, inputstring=part[key], recipe=self.recipe, variables=self.variables)

            partlist.append(part)

        self.recipe.steps[self.stepid].name = partlist[0]
        self.recipe.steps[self.stepid].URL = partlist[1]
        self.recipe.steps[self.stepid].request.querystring = partlist[2]
        self.recipe.steps[self.stepid].request.body = partlist[3]
        self.recipe.steps[self.stepid].request.headers = partlist[4]
        return self.recipe.steps[self.stepid]

    def call(self):
        """calls the URL specified in the current step"""
        name = self.recipe.steps[self.stepid].name
        httpmethod = self.recipe.steps[self.stepid].httpmethod
        url = self.recipe.steps[self.stepid].URL
        options = self.recipe.steps[self.stepid].options
        from urllib.parse import urlparse
        parse_object = urlparse(url)
        if parse_object.hostname is None:
            try:
                raise ValueError("Couldn't find hostname in URL")
            except ValueError as e:
                errlog('Bad URL. Aborting...', e)

        if parse_object.scheme != 'http' and parse_object.scheme != 'https':
            try:
                raise ValueError("Couldn't find http(s) scheme in URL")
            except ValueError as e:
                errlog('Bad URL. Aborting...', e)

            try:
                vlog('Host: = ' + self.recipe.steps[self.stepid].request.headers['Host'])
            except KeyError as ke:
                vlog('No Host header set, using host part of URL: ' + parse_object.hostname)
                self.recipe.steps[self.stepid].request.headers['Host'] = parse_object.hostname

            try:
                vlog('User-agent = ' + self.recipe.steps[self.stepid].request.headers['User-agent'])
            except KeyError as ke:
                vlog('No User-agent header set, defaulting to bprc/' + __version__)
                self.recipe.steps[self.stepid].request.headers['User-agent'] = 'bprc/' + __version__

            self.recipe.steps[self.stepid].request.headers['Accept'] = 'application/json'
            extra_options = list(set(options.keys()) - set(['request.retries', 'request.body_format']))
            if len(extra_options) > 0:
                vlog('Unrecognised options detected... Ingoring ' + str(extra_options))
            if 'request.body_format' in options:
                if options['request.body_format'] == 'form':
                    bodyformat = 'form'
                    self.recipe.steps[self.stepid].request.headers['Content-type'] = 'application/x-www-form-urlencoded'
                else:
                    bodyformat = 'json'
                    self.recipe.steps[self.stepid].request.headers['Content-type'] = 'application/json'
            else:
                bodyformat = 'json'
                self.recipe.steps[self.stepid].request.headers['Content-type'] = 'application/json'
            if 'request.retries' in options:
                try:
                    retries = int(options['request.retries'])
                except ValueError as e:
                    errlog("Bad type passed on 'request.retries' option", e)

            else:
                retries = 3
            querystring = self.recipe.steps[self.stepid].request.querystring
            requestheaders = self.recipe.steps[self.stepid].request.headers
            requestbody = self.recipe.steps[self.stepid].request.body
            responsecode = self.recipe.steps[self.stepid].response.code
            responseheaders = self.recipe.steps[self.stepid].response.headers
            responsebody = self.recipe.steps[self.stepid].response.body
            vlog('About to make HTTP request for step ' + str(self.stepid) + ' ' + str(self.recipe.steps[self.stepid].name))
            vlog(httpmethod.upper() + ' ' + self.recipe.steps[self.stepid].URL)
            try:
                if bodyformat == 'json':
                    r = requests.Request(httpmethod.lower(), url, params=querystring, headers=requestheaders, data=json.dumps(requestbody, cls=BodyEncoder))
                else:
                    r = requests.Request(httpmethod.lower(), url, params=querystring, headers=requestheaders, data=requestbody._body)
                prepared = r.prepare()
                logging.debug('Req body' + prepared.body)
                s = requests.Session()
                a = requests.adapters.HTTPAdapter(max_retries=retries)
                b = requests.adapters.HTTPAdapter(max_retries=retries)
                s.mount('http://', a)
                s.mount('https://', b)
                logging.debug('Retries set to ' + str(retries))
                logging.debug('Verify parameter == ' + str(not bprc.cli.args.ignoressl))
                resp = s.send(prepared, verify=not bprc.cli.args.ignoressl)
            except requests.exceptions.SSLError as ssle:
                errlog('Could not verify SSL certificate. Try the --ignore-ssl option', ssle)
            except requests.exceptions.ConnectionError as httpe:
                errlog('Could not open HTTP connection. Network problem or bad URL?', httpe)
            except AttributeError as ae:
                errlog('Problem with URL or HTTP method', ae)

            self.recipe.steps[self.stepid].request.headers = resp.request.headers
            self.recipe.steps[self.stepid].response.code = resp.status_code
            vlog('Received HTTP response code: ' + str(self.recipe.steps[self.stepid].response.code))
            vlog('Code prefix ' + str(resp.status_code)[:1])
            if str(resp.status_code)[:1] == '4' or str(resp.status_code)[:1] == '5':
                msg = 'Received an HTTP error code...' + str(resp.status_code)
                logging.error(msg)
                verboseprint(msg)
                if bprc.cli.args.skiphttperrors:
                    pass
        else:
            try:
                resp.raise_for_status()
            except Exception as e:
                if bprc.cli.args.debug:
                    print('Response body: ' + resp.text)
                errlog('Got error HTTP response and --skip-http-errors not passed. Aborting', e)

        self.recipe.steps[self.stepid].response.headers = resp.headers
        self.recipe.steps[self.stepid].response.httpversion = resp.raw.version
        self.recipe.steps[self.stepid].response.encoding = resp.encoding
        self.recipe.steps[self.stepid].response.statusmsg = httpstatuscodes[str(resp.status_code)]
        if resp.status_code == 204 or resp.status_code == 205:
            response_content_type = ''
        else:
            try:
                response_content_type = resp.headers['Content-type'].split(';')[0]
            except KeyError as ke:
                errlog('Server sent content without content-type header. Cannot parse. Aborting...', ke)

            logging.debug(resp.text)
            logging.debug('Content-type:' + response_content_type)
            logging.debug('Encoding:' + str(resp.encoding))
            logging.debug('Text:' + resp.text)
            if response_content_type.lower() == 'application/json' or response_content_type == '':
                vlog('JSON/empty response expected. Received Content-type: ' + response_content_type)
                try:
                    vlog('Attempting to parse JSON response body...')
                    if response_content_type == '':
                        vlog('Response had no body... Proceeding...')
                        self.recipe.steps[self.stepid].response.body = None
                    else:
                        self.recipe.steps[self.stepid].response.body = json.loads(resp.text)
                except Exception as e:
                    errlog('Failed to parse JSON response. Aborting', e)

                vlog('JSON parsed ok.')
            else:
                errlog('Response body is not JSON! Content-type: ' + response_content_type + '. Aborting', Exception('Non-JSON response not supported'))
        return prepared

    def generateOutput(self, req):
        """imvokes the output processor to write the output"""
        output = OutputProcessor(step=self.recipe.steps[self.stepid], id=self.stepid, req=req)
        output.writeOutput(writeformat=bprc.cli.args.outputformat, writefile=bprc.cli.args.outputfile, req=req)