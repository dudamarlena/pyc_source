# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/entify/lib/processing.py
# Compiled at: 2015-01-05 07:52:52
import logging, requests, os
from os import listdir
from os.path import isfile, join, isdir
import i3visiotools.logger, i3visiotools.general as general, entify.lib.config_entify as config

def getEntitiesByRegexp(data=None, listRegexp=None, verbosity=1, logFolder='./logs'):
    """ 
                Method to obtain entities by Regexp.

                :param data:    text where the entities will be looked for.
                :param listRegexp:      list of selected regular expressions to be looked for. If None was provided, all the available will be chosen instead.
                :param verbosity:       Verbosity level.
                :param logFolder:       Folder to store the logs.
                
                :return:        a list of the available objects containing the expressions found in the provided data.
                [
                  {
                        "attributes": [],
                        "type": "i3visio.email",
                        "value": "foo@bar.com"
                  },
                  {
                        "attributes": [],
                        "type": "i3visio.email",
                        "value": "bar@foo.com"
                  }
                ]
        """
    i3visiotools.logger.setupLogger(loggerName='entify', verbosity=verbosity, logFolder=logFolder)
    logger = logging.getLogger('entify')
    if listRegexp == None:
        listRegexp = config.getAllRegexp()
    foundExpr = []
    for r in listRegexp:
        foundExpr += r.findExp(data)

    return foundExpr


def scanFolderForRegexp(folder=None, listRegexp=None, recursive=False, verbosity=1, logFolder='./logs'):
    """ 
                [Optionally] recursive method to scan the files in a given folder.

                :param folder:  the folder to be scanned.
                :param listRegexp:      listRegexp is an array of <RegexpObject>.
                :param recursive:       when True, it performs a recursive search on the subfolders.
        
                :return:        a list of the available objects containing the expressions found in the provided data.
                [
                  {
                        "attributes": [],
                        "type": "i3visio.email",
                        "value": "foo@bar.com"
                  },
                  {
                        "attributes": [],
                        "type": "i3visio.email",
                        "value": "bar@foo.com"
                  }
                ]
        """
    i3visiotools.logger.setupLogger(loggerName='entify', verbosity=verbosity, logFolder=logFolder)
    logger = logging.getLogger('entify')
    logger.info('Scanning the folder: ' + folder)
    results = {}
    onlyfiles = [ f for f in listdir(folder) if isfile(join(folder, f)) ]
    for f in onlyfiles:
        filePath = join(folder, f)
        logger.debug('Looking for regular expressions in: ' + filePath)
        with open(filePath, 'r') as (tempF):
            foundExpr = getEntitiesByRegexp(data=tempF.read(), listRegexp=listRegexp)
            logger.debug('Updating the ' + str(len(foundExpr)) + ' results found on: ' + filePath)
            results[filePath] = foundExpr

    if recursive:
        onlyfolders = [ f for f in listdir(folder) if isdir(join(folder, f)) ]
        for f in onlyfolders:
            folderPath = join(folder, f)
            logger.debug('Looking for additional in the folder: ' + folderPath)
            results.update(scanFolderForRegexp(folder=folderPath, listRegexp=listRegexp, recursive=recursive))

    return results


def scanResource(uri=None, listRegexp=None, verbosity=1, logFolder='./logs'):
    """ 
                [Optionally] recursive method to scan the files in a given folder.

                :param uri:     the URI to be scanned.
                :param listRegexp:      listRegexp is an array of <RegexpObject>.

                :return:        a dictionary where the key is the name of the file.
        """
    i3visiotools.logger.setupLogger(loggerName='entify', verbosity=verbosity, logFolder=logFolder)
    logger = logging.getLogger('entify')
    results = {}
    logger.debug('Looking for regular expressions in: ' + uri)
    import urllib2
    foundExpr = getEntitiesByRegexp(data=urllib2.urlopen(uri).read(), listRegexp=listRegexp)
    logger.debug('Updating the ' + str(len(foundExpr)) + ' results found on: ' + uri)
    results[uri] = foundExpr
    return results


def entify_main(args):
    """ 
                Main function. This function is created in this way so as to let other applications make use of the full configuration capabilities of the application. 
        """
    i3visiotools.logger.setupLogger(loggerName='entify', verbosity=args.verbose, logFolder=args.logfolder)
    logger = logging.getLogger('entify')
    logger.info('entify-launcher.py Copyright (C) F. Brezo and Y. Rubio (i3visio) 2014\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it under certain conditions.\nFor details, run:\n\tpython entify-launcher.py --license')
    logger.info('Selecting the regular expressions to be analysed...')
    listRegexp = []
    if args.regexp:
        listRegexp = config.getRegexpsByName(args.regexp)
    elif args.new_regexp:
        for i, r in enumerate(args.new_regexp):
            list.Regexp.append(RegexpObject(name='NewRegexp' + str(i), reg_exp=args.new_regexp))

    if not args.web:
        results = scanFolderForRegexp(folder=args.input_folder, listRegexp=listRegexp, recursive=args.recursive, verbosity=args.verbose, logFolder=args.logfolder)
    else:
        results = scanResource(uri=args.web, listRegexp=listRegexp, verbosity=args.verbose, logFolder=args.logfolder)
    logger.info('Printing the results:\n' + general.dictToJson(results))
    if args.output_folder:
        logger.info('Preparing the output folder...')
        if not os.path.exists(args.output_folder):
            logger.warning("The output folder '" + args.output_folder + "' does not exist. The system will try to create it.")
            os.makedirs(args.output_folder)
        logger.info('Storing the results...')
        if 'json' in args.extension:
            with open(os.path.join(args.output_folder, 'results.json'), 'w') as (oF):
                oF.write(general.dictToJson(results))