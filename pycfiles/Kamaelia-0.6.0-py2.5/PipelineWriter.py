# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Compose/PipelineWriter.py
# Compiled at: 2008-10-19 12:19:52
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class PipelineWriter(component):
    """Writes a Kamaelia pipeline based on instructions received.

    Accepts:
        ("PIPELINE", [pipelineelements])
            pipelineelements = dictionary containing:
                name : name of class/factory function
                module : module containing it
                instantiation : string of the arguments to be passed
                    (the bit that goes inside the brackets)

    Emits:
        Strings of python source code
        followed by 'None' to terminate
    """

    def main(self):
        done = False
        while not done:
            while self.dataReady('inbox'):
                data = self.recv('inbox')
                if data[0].upper() == 'PIPELINE':
                    for output in PipelineWriter.generatePipeline(data[1]):
                        self.send(output, 'outbox')

                    self.send(None, 'outbox')

            while self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    done = True
                self.send(shutdownMicroprocess(self), 'signal')

            if not done:
                self.pause()
            yield 1

        return

    def generatePipeline(pipeline):
        yield '#!/usr/bin/env python\n\n'
        if len(pipeline):
            imports = {'Kamaelia.Chassis.Pipeline': ['Pipeline']}
            for component in pipeline:
                classname = component['name']
                modulename = component['module']
                imports.setdefault(modulename, [])
                if classname not in imports[modulename]:
                    imports[modulename].append(classname)

            for module in imports:
                yield 'from ' + module + ' import '
                prefix = ''
                for classname in imports[module]:
                    yield prefix + classname
                    prefix = ', '

                yield '\n'

            yield '\n'
            indent = 'Pipeline( '
            for component in pipeline:
                yield indent + component['name'] + '( ' + component['instantiation'] + ' ),\n'
                indent = ' ' * len(indent)

            yield '        ).run()\n'
        else:
            yield '# no pipeline!\n'

    generatePipeline = staticmethod(generatePipeline)