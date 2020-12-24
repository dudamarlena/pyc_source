# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Base/Utilities.py
# Compiled at: 2019-11-03 18:09:03
import re, os, sys, time, dill, errno, pprint, hashlib, logging, inspect, textwrap, datetime, dpath.util, coloredlogs
from lxml import etree
from funcy import decorator
from pygments import highlight
from shutil import copy, rmtree
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer, XmlLexer, get_lexer_by_name
from jinja2 import Environment, FileSystemLoader, Template, TemplateSyntaxError, TemplateAssertionError, TemplateError
reload(sys)
sys.setdefaultencoding('utf-8')

def printSource(text, language, parameters=None, style='monokai'):
    if parameters is not None and parameters['globals']['noColours']:
        print text
    else:
        print highlight(text, get_lexer_by_name(language), Terminal256Formatter(style=Terminal256Formatter().style))
    return


def printCode(code, parameters=None, style='monokai'):
    if not isinstance(code, list):
        code = [
         code]
    for element in code:
        if isinstance(element, etree._Element):
            if parameters is not None and parameters['globals']['noColours']:
                print etree.tostring(element, pretty_print=True)
            else:
                print highlight(etree.tostring(element, pretty_print=True), XmlLexer(), Terminal256Formatter(style=Terminal256Formatter(style=style).style))

    if all([ isinstance(element, etree._ElementStringResult) for element in code ]):
        print code
    return


def printParameters(elements, parameters=None, style='monokai'):
    if parameters is not None and parameters['globals']['noColours']:
        pprint.pprint(elements)
    else:
        print highlight(pprint.pformat(elements), PythonLexer(), Terminal256Formatter(style=Terminal256Formatter(style=style).style))
    return


def printVariable(x):
    frame = inspect.currentframe().f_back
    s = inspect.getframeinfo(frame).code_context[0]
    r = re.search('\\((.*)\\)', s).group(1)
    print ('{} = {}').format(r, x)


def logErrors(errors, parameters):
    if isinstance(errors, list):
        for error in errors:
            logging.error(error)
            parameters['errors'].append(error)

    else:
        logging.error(errors)
        parameters['errors'].append(errors)


def fileLineNumberToLine(filename, line_number):
    with open(filename) as (file):
        line = [ next(file) for x in xrange(line_number) ][(-1)]
    return line


def textLineNumberToLine(text, line_number):
    return text.split('\n')[(line_number - 1)]


def positionToLineColumn(position, text):
    lines = str(text).split('\n')
    counter = 0
    line_number = 1
    column_number = 0
    for line in lines:
        new_counter = counter + len(line)
        if new_counter > position:
            column_number = position - counter
            break
        else:
            counter += len(line) + 1
            line_number += 1

    return (
     line_number, column_number, line)


def errorMessage(error_type, reason, line='', filename='', line_number=0, column_number=0):
    line_text = '\n' + line.strip('\n') + '\n' + (' ' * column_number + '^') + '\n' if line is not '' else ''
    file_text = ' in file:\n"' + filename + '"\n' if filename is not '' else ''
    line_number_text = ' at line ' + str(line_number) if line_number > 0 else ''
    column_number_text = ' column ' + str(column_number) if column_number > 0 else ''
    return line_text + error_type + ' error' + file_text + line_number_text + column_number_text + ': ' + color.BOLD + reason + color.END


def formatJinjaErrorMessage(exception, filename=''):
    if isinstance(exception, TemplateSyntaxError):
        line = fileLineNumberToLine(exception.filename, exception.lineno)
        return errorMessage('Output template syntax', exception.message, line=line, line_number=exception.lineno, filename=exception.filename)
    else:
        if isinstance(exception, TemplateAssertionError):
            line = fileLineNumberToLine(exception.filename, exception.lineno)
            return errorMessage('Output template assertion', exception.message, line=line, line_number=exception.lineno, filename=exception.filename)
        return errorMessage('Unexpected output template', exception.message, filename=filename)


def formatParsleyErrorMessage(exception):
    line_number, column_number, line = positionToLineColumn(exception.position, exception.input)
    return errorMessage('Input syntax parsing', exception.formatReason(), line_number=line_number, column_number=column_number, line=line)


def formatOSErrorMessage(exception):
    return errorMessage('File system', exception.strerror)


def formatLxmlErrorMessage(exception, text=''):
    errors = []
    for error in exception.error_log:
        if text is not '':
            line = textLineNumberToLine(text, error.line)
        else:
            line = ''
        errors.append('\n' + errorMessage('XML parsing', error.message, line=line, line_number=error.line, column_number=error.column))

    return errors


def formatSemanticTypeErrorMessage(code_text, parameters, position, error, reason):
    line_number, column_number, line = positionToLineColumn(int(position), code_text)
    parameters['errors'].append(error + reason)
    return errorMessage(error, reason, line_number=line_number, column_number=column_number, line=line)


def errorOptionalArgumentTypes(code, parameters, optional_names, optional_types):
    message = 'Incorrect types for optional parameters. '
    for name, types in zip(optional_names, optional_types):
        if not parameters['language'][code.tag]['definition']['optional'][name]['test'](types):
            message += 'The type of the optional parameter "' + name + '" should be "' + parameters['language'][code.tag]['definition']['optional'][name]['documentation'] + '" instead of "' + types + '"\n'

    logging.error(formatSemanticTypeErrorMessage(parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))


def errorOptionalArgumentNotDefined(code, parameters, optional_names):
    message = ''
    keys = parameters['language'][code.tag]['definition']['optional'].keys()
    for x in set(optional_names) - set(keys):
        message += 'The optional parameter "' + x + '" is not defined.\n'

    message += 'The list of defined optional parameters is: ' + str(keys)
    logging.error(formatSemanticTypeErrorMessage(parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))


def errorArgumentTypes(code, parameters, argument_types):
    message = 'Incorrect argument types for function "' + code.tag + '". The expected argument types are:\n   '
    message += code.tag + '( ' + parameters['language'][code.tag]['definition']['arguments']['documentation'] + ' )\n'
    message += '\nInstead received:\n   ' + code.tag + '( ' + (',').join(argument_types) + ' )\n'
    logging.error(formatSemanticTypeErrorMessage(parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))


def errorLanguageDefinition(code, parameters):
    message = 'Language element "' + code.tag + '" ill defined. Please check definition.'
    logging.error(formatSemanticTypeErrorMessage(parameters['text'], parameters, getTextMinimumPositionXML(code), 'Type', message))


@decorator
def log_all_calls(function):
    print 'function name: ' + function._func.__name__ + ' arguments: ' + str(function._args)
    return function()


@decorator
def name_all_calls(function):
    print 'function name:' + function._func.__name__
    return function()


@decorator
def time_all_calls(function):
    start = time.time()
    sys.stdout.write('<<<')
    sys.stdout.flush()
    result = function()
    print 'function name: ' + function._func.__name__ + 'execution time: ' + str(time.time() - start) + ' seconds>>>'
    return result


@decorator
def cache_in_disk(function):
    cache_path = '/.rol/cache/'
    name = __name__ + '.' + function._func.__name__
    path = os.path.expanduser('~') + cache_path + name + '.cache'
    if os.path.isfile(path):
        return dill.load(open(path, 'rb'))
    else:
        data = function()
        createFolder(os.path.expanduser('~') + cache_path)
        dill.dump(data, open(path, 'wb'))
        return data


global_function_cache = {}

def cache_function(function):

    def wrapper(*arguments, **options):
        global global_function_cache
        hash = hashlib.md5(function.__name__ + str(arguments) + str(options)).hexdigest()
        if hash not in global_function_cache.keys():
            result = function(*arguments, **options)
            global_function_cache[hash] = result
        else:
            result = global_function_cache[hash]
        return result

    return wrapper


coloredlogs.install(fmt='%(levelname)s: %(message)s', level='WARN')

def setLoggerLevel(level):
    coloredlogs.install(fmt='%(levelname)s: %(message)s', level=level.upper())


class color:
    PURPLE = '\x1b[95m'
    CYAN = '\x1b[96m'
    DARKCYAN = '\x1b[36m'
    BLUE = '\x1b[94m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    RED = '\x1b[91m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'
    END = '\x1b[0m'


def incrementCompilerStep(parameters, group, name):
    parameters['developer']['stepCounter'] = parameters['developer']['stepCounter'] + 1
    parameters['developer']['stepGroup'] = group
    parameters['developer']['stepName'] = name
    logging.info('Step [' + str(parameters['developer']['stepCounter']) + ']: ' + group + ' - ' + name)
    return parameters


def progressMessage(parameters):
    parameters['developer']['progressPercentage'] = parameters['developer']['progressPercentage'] + 1
    progress_percentage = parameters['developer']['progressPercentage']
    progress_total = parameters['developer']['progressTotal']
    progress_bar = parameters['developer']['progressBar']
    sys.stdout.write(('\r[{:04.1f}%] {} {}                         ').format(progress_percentage * 100 / progress_total, '\\|/-'[(progress_bar % 4)], parameters['developer']['stepGroup'] + ', ' + parameters['developer']['stepName']))
    sys.stdout.flush()


def progressSpin(parameters):
    parameters['developer']['progressBar'] = parameters['developer']['progressBar'] + 1
    progress_percentage = parameters['developer']['progressPercentage']
    progress_total = parameters['developer']['progressTotal']
    progress_bar = parameters['developer']['progressBar']
    sys.stdout.write(('\r[{:04.1f}%] {}').format(progress_percentage * 100 / progress_total, '\\|/-'[(progress_bar % 4)]))
    sys.stdout.flush()


def progressDone(parameters):
    final_time = time.time() - parameters['developer']['progressStartTime']
    sys.stdout.write(('\r[{:04.1f}%] {}                         \n').format(100, ('Done in {}.').format(time.strftime('%Hh %Mm %Ss', time.gmtime(final_time)))))
    sys.stdout.flush()


def checkQueryNamespaces(text):
    """Looks for namespace references in the query text and add them explicitely to xpath"""
    namespaces = {'namespaces': {}}
    name = re.split('([a-zA-Z0-9]+):[a-zA-Z0-9]+', text)
    if name is not None:
        namespaces['namespaces'] = {value:value for value in name[1::2]}
    return (
     text, namespaces)


def showDeveloperInformation(code, parameters):
    if parameters['developer']['progress']:
        progressMessage(parameters)
    if parameters['developer']['step'] == parameters['developer']['stepCounter']:
        if parameters['developer']['code'] and code is not None:
            printCode(code, parameters)
        if parameters['developer']['parameters']:
            printParameters(parameters, parameters)
        if parameters['developer']['codePath'] is not '' and code is not None:
            try:
                query, namespaces = checkQueryNamespaces(parameters['developer']['codePath'])
                printCode(code.xpath(query, **namespaces), parameters)
            except:
                logging.warning("The path'" + parameters['developer']['codePath'] + "' is not present in the code")

        if parameters['developer']['parametersPath'] is not '':
            try:
                for element in paths(parameters, parameters['developer']['parametersPath']):
                    printParameters(element, parameters)

            except:
                logging.warning("The path'" + parameters['developer']['parametersPath'] + "' is not defined in the internal parameters.")

        if parameters['developer']['stop']:
            sys.exit(0)
    return


def importModule(z, a, b, c):
    return __import__(z + '.' + a + '.' + b, globals(), locals(), ensureList(c))


def removeCache(cache_path='/.rol/cache'):
    logging.debug('Removing caching...')
    path = os.path.expanduser('~') + cache_path
    if os.path.isdir(path):
        rmtree(path)


def myPluginPath(parameters):
    return parameters['manifesto'][parameters['developer']['stepGroup']][parameters['developer']['stepName']]['path']


def myOutputPath(parameters):
    if parameters['developer']['stepName'] in parameters['globals']['deployOutputs'].keys():
        return parameters['globals']['deployOutputs'][parameters['developer']['stepName']]
    else:
        return parameters['globals']['deploy']


def getPackageOutputParents(parameters, package):
    if 'parent' in parameters['manifesto']['Outputs'][package].keys():
        return [package] + getPackageOutputParents(parameters, parameters['manifesto']['Outputs'][package]['parent'])
    else:
        return [
         package]


def isKeyDefined(key, d):
    if isinstance(d, dict):
        return key in d.keys()
    else:
        return False


def isDefined(dictionary, element):
    return len(dpath.util.values(dictionary, element)) > 0


def getDictValue(key, d):
    if isKeyDefined(key, d):
        return d[key]
    else:
        return
        return


def mergeDictionaries(a, b):
    dpath.util.merge(b, a)
    return b


def flatDictionary(d, s='-', list=None, name=''):
    if list is None:
        list = {}
    for key, value in d.iteritems():
        if isinstance(value, dict):
            list.update(flatDictionary(value, s, list, name + s + key))
        else:
            list[name + s + key] = value

    return list


def unflatDictionary(l, s='-'):
    dictionary = {}
    for key, value in l.iteritems():
        dpath.util.new(dictionary, key.replace(s, '/'), value)

    return dictionary


def path(dictionary, dictionary_path):
    return dpath.util.get(dictionary, dictionary_path)


def paths(dictionary, dictionary_path):
    return dpath.util.values(dictionary, dictionary_path)


def textWrapBox(text):
    return ('\\n').join(textwrap.wrap(text, int(13.9231 - 0.0769231 * len(text) + 0.846154 * len(text.split(' ')))))


def replaceLast(string, source, destination):
    return source.join(string.split(source)[0:-1]) + destination + string.split(source)[(-1)]


def replaceFirst(string, source, destination):
    return string.replace(source, destination, 1)


def lowerNoSpace(s):
    return s.replace(' ', '').lower()


def lowerSpaceToDash(s):
    return s.replace(' ', '-').lower()


def underscore(text):
    return text.replace('/', '_').replace(' ', '_').replace('.', '_').lower()


def dashes(text):
    return text.replace('/', '-').replace(' ', '-').replace('.', '-').replace('_', '-').lower()


def underscoreFullCaps(text):
    return text.replace('/', '_').replace(' ', '_').replace('.', '_').upper()


def fullCaps(text):
    return text.replace('/', '').replace(' ', '').replace('.', '').replace('_', '').upper()


def smartTitle(s):
    return (' ').join(w[0].upper() + w[1:] for w in s.split())


def camelCase(text):
    return smartTitle(text.replace('/', ' ').replace('.', ' ').replace('_', ' ')).replace(' ', '')


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def camelCaseToUnderscore(name):
    s1 = first_cap_re.sub('\\1_\\2', name)
    return all_cap_re.sub('\\1_\\2', s1).lower()


def unCamelCase(name):
    s1 = first_cap_re.sub('\\1 \\2', name)
    return all_cap_re.sub('\\1 \\2', s1).lower()


def initials(text):
    return ('').join(c for c in smartTitle(text) if c.isupper())


def mergeManyOrdered(list_of_lists):
    """Non-optimized generalization of mergeOrdered"""
    return reduce(mergeOrdered, list_of_lists)


def mergeOrdered(a, b):
    """Merges two lists, while keeping the order of the elements and trying to find
  minimum number of repetitions. E.g.:
  a = [0,1,3,8,9]
  b = [1,2,4,5,8,9]
  mergeOrdered(a, b) -> [0, 1, 2, 4, 5, 3, 8, 9]
  """
    c = []
    while len(a) > 0 and len(b) > 0:
        if a[0] == b[0]:
            c.append(a.pop(0))
            b.pop(0)
        elif a[0] in b and b[0] not in a:
            c.append(b.pop(0))
        elif a[0] not in b and b[0] in a:
            c.append(a.pop(0))
        elif len(a) > len(b):
            c.append(a.pop(0))
        else:
            c.append(b.pop(0))

    return c + a + b


def ensureList(a):
    if isinstance(a, list):
        return a
    else:
        return [
         a]


def unique(a):
    return list(set(a))


def sortListCodeByAttribute(list, attribute):
    return sorted(list, key=lambda x: x.attrib[attribute])


def findFileType(extension='py', path='.', followlinks=True):
    for entry in ensureList(path):
        for root, dirs, files in os.walk(entry, followlinks=followlinks):
            for eachfile in files:
                fileName, fileExtension = os.path.splitext(eachfile)
                if fileExtension.lower() == '.' + extension:
                    yield root + '/' + eachfile


def findFileName(name, path='.', followlinks=True):
    for entry in ensureList(path):
        for root, dirs, files in os.walk(entry, followlinks=followlinks):
            for eachfile in files:
                if os.path.basename(eachfile) == name:
                    yield root + '/' + eachfile


def createFolder(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def createFolderForFile(filename):
    createFolder(os.path.dirname(filename))


def copyWithPermissions(source, destination):
    permissions = os.stat(source)
    copy(source, destination)
    os.chmod(destination, permissions.st_mode)


def getNonexistantPath(fname_path):
    """
    Get the path to a filename which does not exist by incrementing path.

    Examples
    --------
    >>> get_nonexistant_path('/etc/issue')
    '/etc/issue-1'
    >>> get_nonexistant_path('whatever/1337bla.py')
    'whatever/1337bla.py'
    """
    if not os.path.exists(fname_path):
        return fname_path
    filename, file_extension = os.path.splitext(fname_path)
    i = 1
    new_fname = ('{}-{}{}').format(filename, i, file_extension)
    while os.path.exists(new_fname):
        i += 1
        new_fname = ('{}-{}{}').format(filename, i, file_extension)

    return new_fname


def xml(tag, content, position=0):
    """creates XML text for entry"""
    text = ('').join(content) if isinstance(content, list) else content
    return '<' + tag + ' p="' + str(position) + '" >' + text + '</' + tag + '>'


def xmlAttributes(tag, content, position=0, attributes={}):
    """creates XML text for entry with attributes"""
    attributes_text = (' ').join([ key + '="' + str(value) + '"' for key, value in attributes.iteritems() ])
    text = ('').join(content) if isinstance(content, list) else content
    return '<' + tag + ' p="' + str(position) + '" ' + attributes_text + '>' + text + '</' + tag + '>'


def xmlFunction(parameters, tag, content, position=0):
    """creates XML for functions"""
    if tag in parameters['language'].keys():
        return xml(tag, content, position)
    else:
        return xmlAttributes('function', content, position, attributes={'name': tag})


def xmlFunctionDefinition(parameters, name, arguments, returns, content, position=0):
    parameters['symbols']['functions'].append(name)
    arguments_text = xml('function_arguments', arguments, position) if isinstance(arguments, basestring) else ''
    returns_text = xml('function_returns', returns, position) if isinstance(returns, basestring) else ''
    content_text = xml('function_content', content, position) if isinstance(content, basestring) else ''
    return xmlAttributes('function_definition', arguments_text + returns_text + content_text, position, attributes={'name': name})


def xmlVariable(parameters, name, position=0):
    """creates XML for variables"""
    if name in parameters['language'].keys():
        return xmlFunction(parameters, name, '', position)
    else:
        if name in parameters['symbols']['functions']:
            return xmlAttributes('function_pointer', '', position, attributes={'name': name})
        parameters['symbols']['variables'].append(name)
        return xmlAttributes('variable', '', position, attributes={'name': name})


def xmlMiniLanguage(parameters, key, text, position):
    """Calls a different parser to process inline mini languages"""
    try:
        parameters['parsing']['position'] = position
        code, parameters = importModule(parameters['manifesto']['Inputs'][key]['type'], 'Inputs', key, 'Parse').Parse.parse(text, parameters)
        result = etree.tostring(code)
        return result
    except:
        logging.error('Failed to parse mini-language ' + key)


def children(xml):
    return xml.getchildren()


def parent(xml):
    return xml.getparent()


def xpath(xml, path, namespaces={}):
    result = xml.xpath(path, namespaces=namespaces)
    if isinstance(result, list):
        return result[0]
    else:
        return result


def xpaths(xml, path, namespaces={}):
    return xml.xpath(path, namespaces=namespaces)


def text(xml):
    if xml.text is None:
        return ''
    else:
        return xml.text
        return


def tag(xml):
    return xml.tag


def attributes(xml):
    return xml.attrib


def attribute(xml, name):
    try:
        if isinstance(xml, list):
            if len(xml) > 0:
                xml = xml[0]
            else:
                return ''
        if name in xml.attrib.keys():
            return xml.attrib[name]
        return ''
    except:
        return ''


def allAttribute(xml_list, name):
    if isinstance(xml_list, list):
        return map(lambda xml: attribute(xml, name), xml_list)
    else:
        return attribute(xml_list, name)


def option(xml, name, debug=''):
    try:
        return optionalArguments(xml)[name]
    except:
        return

    return


def optionalArguments(xml):
    return {a.attrib['name']:a for a in xml.xpath('option')}


def getTextMinimumPositionXML(xml):
    minimum = xml.attrib['p'] if 'p' in xml.attrib else sys.maxint
    childrens_minimum = [ getTextMinimumPositionXML(x) for x in xml.getchildren() ]
    if childrens_minimum == []:
        return minimum
    else:
        return min(min(childrens_minimum), minimum)


def getFirstParent(code, parent_name):
    try:
        if code.getparent().tag == parent_name:
            return code.getparent()
        else:
            return getFirstParent(code.getparent(), parent_name)

    except:
        return

    return


def todaysDate(format):
    today = datetime.date.today()
    return today.strftime(format)


def fillDefaultsInOptionalArguments(code, parameters):
    """Fill in defaults in optional arguments in case they are not explicitely defined."""
    try:
        for element in code.xpath('*[not(self::option)]'):
            __, parameters = fillDefaultsInOptionalArguments(element, parameters)

        if len(dpath.util.values(parameters['language'][code.tag], 'definition/optional')) > 0:
            optional_names = code.xpath('option/@name')
            missing_parameters = list(set(parameters['language'][code.tag]['definition']['optional'].keys()) - set(optional_names))
            for parameter in missing_parameters:
                optional_argument_tag = etree.Element('option')
                optional_argument_tag.attrib['name'] = parameter
                value_tag = etree.Element(parameters['language'][code.tag]['definition']['optional'][parameter]['tag'])
                if parameters['language'][code.tag]['definition']['optional'][parameter]['default'] is not None:
                    value_tag.text = str(parameters['language'][code.tag]['definition']['optional'][parameter]['default'])
                    optional_argument_tag.append(value_tag)
                code.append(optional_argument_tag)

        for element in code.xpath('option'):
            for child in element.getchildren():
                __, parameters = fillDefaultsInOptionalArguments(child, parameters)

    except:
        pass

    return (
     code, parameters)


default_template_engine_filters = {'todaysDate': todaysDate, 'dpath': path, 
   'xpath': xpath, 
   'dpaths': paths, 
   'xpaths': xpaths, 
   'isDefined': isDefined, 
   'ensureList': ensureList, 
   'text': text, 
   'tag': tag, 
   'attributes': attributes, 
   'attribute': attribute, 
   'option': option, 
   'optionalArguments': optionalArguments, 
   'initials': initials, 
   'underscore': underscore, 
   'fullCaps': fullCaps, 
   'camelCase': camelCase, 
   'underscoreFullCaps': underscoreFullCaps}

def templateEngine(code, parameters, filepatterns, templates_path, deploy_path, filters=default_template_engine_filters):
    files_to_process = []
    files_to_copy = []
    try:
        for root, dirs, files in os.walk(templates_path, followlinks=True):
            for file in files:
                if file.endswith('.template'):
                    files_to_process.append(os.path.join(root, file))
                else:
                    files_to_copy.append(os.path.join(root, file))

        new_files = [ x.replace(templates_path, deploy_path).replace('.template', '') for x in files_to_process
                    ]
        new_copy_files = [ x.replace(templates_path, deploy_path) for x in files_to_copy
                         ]
        for key, value in filepatterns.iteritems():
            for i in range(len(new_files)):
                new_files[i] = new_files[i].replace('_' + key + '_', value)

            for i in range(len(new_copy_files)):
                new_copy_files[i] = new_copy_files[i].replace('_' + key + '_', value)

        env = Environment(loader=FileSystemLoader('/'))
        for key, value in filters.iteritems():
            env.filters[key] = value

        for i in range(0, len(files_to_process)):
            try:
                template_body = env.get_template(files_to_process[i])
                text_body = template_body.render(code=code, parameters=parameters)
            except TemplateError as e:
                logErrors(formatJinjaErrorMessage(e, filename=files_to_process[i]), parameters)
                return False

            createFolderForFile(new_files[i])
            new_package_file = open(new_files[i], 'w')
            new_package_file.write(text_body)
            new_package_file.close()
            logging.debug('Wrote file ' + new_files[i] + '...')

        for i in range(0, len(files_to_copy)):
            createFolderForFile(new_copy_files[i])
            copy(files_to_copy[i], new_copy_files[i])
            logging.debug('Copied file ' + new_copy_files[i] + '...')

    except OSError as e:
        logErrors(formatOSErrorMessage(e), parameters)
        return False

    return True


def ExtractLanguageDefinitions(language, type, module):
    return {key:value[type][module] for key, value in dpath.util.search(language, '/*/' + type + '/' + module + '/*').iteritems()}


def CreateBracketGrammar(definitions):
    bracket = dpath.util.search(definitions, '/*/bracket')
    text = '\n# Bracket operators\n'
    for key, value in bracket.iteritems():
        text += key + " = ( '" + value['bracket']['open'] + "' wws " + value['bracket']['arguments'] + ":a wws '" + value['bracket']['close'] + "' -> xml('" + key + "',a,self.input.position)\n      | '" + value['bracket']['open'] + "' wws '" + value['bracket']['close'] + "' -> xml('" + key + "','',self.input.position)\n      )\n"

    return (text, bracket.keys())


def CreateGenericGrammar(definitions):
    generic = dpath.util.search(definitions, '/*/generic')
    text = '\n# Generic operators\n'
    for key, value in generic.iteritems():
        text += key + "Generic = '" + ('').join([ x + "' wws values:" + chr(97 + y) + " wws '" for x, y in zip(value['generic'], range(len(value['generic']))) ][:-1]) + value['generic'][(-1)] + "' -> xml('" + key + "'," + ('+').join([ chr(97 + x) for x in range(len(value['generic']) - 1) ]) + ',self.input.position)\n'

    return (text, [ x + 'Generic' for x in generic.keys() ])


def CreatePreInPostFixGrammar(definitions):
    infix = dpath.util.search(definitions, '/*/infix')
    prefix = dpath.util.search(definitions, '/*/prefix')
    postfix = dpath.util.search(definitions, '/*/postfix')
    alternatives = dpath.util.search(definitions, '/*/alternatives')
    orders = list(set(dpath.util.values(definitions, '/*/*/order')))
    orders.sort()
    previousOrder = dict(zip(orders + ['max'], ['min'] + orders))
    text = ''
    text += '\n# function names alternatives\n'
    for key, value in alternatives.iteritems():
        text += key + " = ( '" + (' | ').join(value['alternatives']) + "' | '" + key + "' ) -> '" + key + "'\n"

    if len(alternatives.keys()) > 0:
        text += 'functionName = ( ' + (' | ').join(alternatives.keys()) + ' | objectName )\n'
    else:
        text += 'functionName = objectName\n'
    text += '\n# Infix operators\n'
    for key, value in infix.iteritems():
        flat = 'flat' in value['infix'] and value['infix']['flat'] is True
        text += key + ' = P' + str(value['infix']['order']) + ':a '
        if flat:
            text += '( wws '
        else:
            text += 'wws '
        if isinstance(value['infix']['key'], list):
            text += "( '" + ("' | '").join(value['infix']['key']) + "' )"
        else:
            text += "'" + value['infix']['key'] + "'"
        text += ' wws P' + str(value['infix']['order'])
        if flat:
            text += ")+:b -> xml('" + key + "',[a]+b,self.input.position)\n"
        else:
            text += ":b -> xml('" + key + "',a+b,self.input.position)\n"

    text += '\n# Prefix operators\n'
    for key, value in prefix.iteritems():
        text += key + ' = '
        if isinstance(value['prefix']['key'], list):
            text += "( '" + ("' | '").join(value['prefix']['key']) + "' )"
        else:
            text += "'" + value['prefix']['key'] + "'"
        text += ' wws P' + str(value['prefix']['order']) + ":a -> xml('" + key + "',a)\n"

    text += '\n# Postfix operators\n'
    for key, value in postfix.iteritems():
        text += key + ' = P' + str(value['postfix']['order']) + ':a wws '
        if isinstance(value['postfix']['key'], list):
            text += "( '" + ("' | '").join(value['postfix']['key']) + "' )"
        else:
            text += "'" + value['postfix']['key'] + "'"
        text += " -> xml('" + key + "',a)\n"

    text += '\n# Precedence order operators\n'
    for order in orders:
        keys = dpath.util.search(definitions, '*/*/order', afilter=lambda x: x == order)
        text += 'P' + str(previousOrder[order]) + ' = ( ' + (' | ').join(keys.keys()) + ' | P' + str(order) + ' )\n'

    if len(orders) > 0:
        return (text, orders[(-1)])
    else:
        return (
         text, 'min')