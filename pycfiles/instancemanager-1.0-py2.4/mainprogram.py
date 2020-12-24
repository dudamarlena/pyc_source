# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/instancemanager/mainprogram.py
# Compiled at: 2007-12-17 05:32:50
"""Manager of development zope instances
"""
import actions, config, configuration, utils, logging, sys, os, os.path
from optparse import OptionParser
log = logging.getLogger('main')
__version__ = '1.0-svn'

def getProjects():
    userDir = os.path.expanduser('~')
    configDir = os.path.join(userDir, config.CONFIGDIR)
    results = [ p.replace('.py', '') for p in os.listdir(configDir) if p.endswith('.py') if p not in ['__init__.py', 'userdefaults.py'] if not p.startswith(config.SECRET_PREFIX) if not p.startswith(config.STUB_PREFIX) ]
    return results


def usage():
    """Return the usage message.
    """
    res = []
    res.append('Usage: instancemanager [options] [multi-action] <project>')
    res.append("multi-action: default ones are 'fresh' and 'soft'.")
    res.append('project: the name of the project, available projects are:')
    userDir = os.path.expanduser('~')
    configDir = os.path.join(userDir, config.CONFIGDIR)
    if os.path.exists(configDir):
        projects = getProjects()
        for project in projects:
            res.append('    %s' % project)

        res.append('    You can use ALL to perform the action ' + 'for all projects.')
    else:
        conf = configuration.Configuration()
        res.append('    You can look at userdefaults.py to change')
        res.append('    instancemanager to your local config.')
        res.append('    Or run instancemanager again with <project> and <action>.')
    return ('\n').join(res)


parser = OptionParser(usage(), version=__version__)
parser.add_option('--verbose', '-v', help='Show all logging messages.', action='store_true', default=False)
parser.add_option('--quiet', '-q', help='Only show error messages.', action='store_true', default=False)
parser.add_option('--manifest', '-m', help='Print Manifest of installed Products and collisions', action='store_true', default=False)
actions.addOptions(parser)

def parseArguments():
    """Parse the arguments, exit on error.
    """
    (options, args) = parser.parse_args()
    projects = getProjects()
    projects.append('ALL')
    project = None
    multiAction = None
    if len(args) == 0:
        log.debug('No loose arguments are passed.')
    if len(args) > 0:
        firstArgument = args[0]
        if firstArgument in projects:
            project = firstArgument
        elif options.bootstrap:
            project = firstArgument
            log.debug('Bootstrapping, so taking the first argument as projectname: %s.', project)
    if len(args) > 1:
        secondArgument = args[1]
        if project:
            multiAction = secondArgument
        elif secondArgument in projects:
            project = secondArgument
            multiAction = firstArgument
    if options.verbose:
        loglevel = logging.DEBUG
    elif options.quiet:
        loglevel = logging.ERROR
    else:
        loglevel = logging.INFO
    if not project and options.bootstrap is not None:
        try:
            project = options.bootstrap.split('/')[(-1)][:-3]
            log.debug('Extracted project name out of bootstrap filename: %s.', project)
        except:
            log.error('Could not get project name out of bootstrap option.')

    if not project:
        log.error('Missing project.')
        parser.print_help()
        sys.exit(1)
    log.debug('Arguments have been read: project=%s, multiAction=%s.', project, multiAction)
    log.debug('Options: %r.', options)
    return (options, project, multiAction, loglevel)


def performActionOnProject(projectConfig, options):
    Actions = actions.getActions()
    for Action in Actions:
        destination = parser.get_option(Action.option).dest
        if getattr(options, destination):
            action = Action(configuration=projectConfig)
            action.run(options=options)


def handleMultiAction(projectConfig, multiActionName):
    """Perform the options specified in the multiAction.

    A multi-action is a list of options you'd normally pass (in turn)
    to instancemanager.
    """
    multiActions = projectConfig.configData['multi_actions']
    multiAction = multiActions.get(multiActionName, None)
    if not multiAction:
        log.error('No multi-action of this name found: %s.\nAvailable multi-actions for this project: %s.\nNote that the invocation of instancemanager has changed lately.\n', multiActionName, multiActions.keys())
        parser.print_help()
        return
    for line in multiAction:
        arguments = line.split(' ')
        log.debug('Extracting arguments from line %r.', line)
        copiedArguments = []
        insideDoubleQuotes = False
        inQuotes = []
        for argument in arguments:
            log.debug('Argument part: %r.', argument)
            if insideDoubleQuotes:
                if argument.endswith('"'):
                    inQuotes.append(argument[:-1])
                    joined = (' ').join(inQuotes)
                    copiedArguments.append(joined)
                    insideDoubleQuotes = False
                else:
                    inQuotes.append(argument)
            elif argument.startswith('"'):
                inQuotes = [
                 argument[1:]]
                insideDoubleQuotes = True
                log.debug('Start of stuff inside double quotes: %r', inQuotes)
            else:
                copiedArguments.append(argument)

        arguments = copiedArguments
        log.debug('Remaining arguments: %r.', arguments)
        (options, args) = parser.parse_args(arguments)
        performActionOnProject(projectConfig, options)

    return


def main():
    utils.initLog()
    (options, project, multiAction, loglevel) = parseArguments()
    utils.addConsoleLogging(loglevel)
    if project == 'ALL':
        log.info('Performing action on all projects.')
        projects = getProjects()
        for project in projects:
            log.info('Project: %s', project)
            projectConfig = configuration.Configuration(project)
            performActionOnProject(projectConfig, options)
            if multiAction:
                handleMultiAction(projectConfig, multiAction)

    else:
        log.info('Project: %s', project)
        if options.bootstrap:
            projectConfig = configuration.BootstrapConfiguration(project, bootstrap=options.bootstrap)
        projectConfig = configuration.Configuration(project)
    performActionOnProject(projectConfig, options)
    if multiAction:
        handleMultiAction(projectConfig, multiAction)


if __name__ == '__main__':
    main()