# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.3-RELEASE-amd64/egg/dtflickr/update.py
# Compiled at: 2008-12-24 15:31:33
from __future__ import with_statement
from __init__ import Flickr
import optparse, os.path
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-a', '--api-key', action='store', dest='api_key', help='Flickr API key')
    options = parser.parse_args()[0]
    if options.api_key is None:
        parser.error('-a or --api-key not specified')
    flickr = Flickr(options.api_key)
    namespaces = {}
    for method in flickr.reflection.getMethods().methods.method:
        info = flickr.reflection.getMethodInfo(method_name=method)
        (namespace, method) = str(method).split('.', 1)
        assert namespace == 'flickr'
        (namespace, method) = method.rsplit('.', 1)
        documentation = str(info.method.name).strip() + '\n\n  ' + str(info.method.description).strip()
        if len(info.arguments.argument) != 1:
            documentation += '\n\n  Arguments:'
            for argument in info.arguments.argument:
                if argument.name != 'api_key':
                    documentation += '\n\n    ' + argument.name + ' ('
                    if int(argument.optional) == 0:
                        documentation += 'Required'
                    else:
                        documentation += 'Optional'
                    documentation += ')\n      ' + str(argument)

        try:
            namespaces[namespace].append((method, documentation))
        except KeyError:
            namespaces[namespace] = [
             (
              method, documentation)]

    namespaces = namespaces.items()
    namespaces.sort()
    with open(os.path.join(os.path.dirname(__file__), '_methods.py'), 'wb') as (python):
        python.write('# DT Flickr Methods\n#\n# Douglas Thrift\n#\n# $' + 'Id$\n\nnamespaces = (\n')
        for (namespace, methods) in namespaces:
            python.write("\t('" + namespace + "', (\n")
            for (method, documentation) in methods:
                python.write("\t\t('" + method + "', " + repr(documentation) + '),\n')

            python.write('\t)),\n')

        python.write(")\n\ndef namespace(namespace):\n\treturn namespace.title().replace('.', '')\n")