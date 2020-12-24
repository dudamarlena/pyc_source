# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/usufy/lib/processing.py
# Compiled at: 2014-12-26 04:33:02
import urllib2, os, time
from multiprocessing import Process, Queue, Pool
import i3visiotools.logger, usufy.lib.config_usufy as config, i3visiotools.benchmark as benchmark, i3visiotools.export as export_mod, i3visiotools.browser as browser, i3visiotools.general as general, i3visiotools.logger as logger, logging

def fuzzUsufy(fDomains=None, fFuzzStruct=None):
    """ 
                Method to guess the usufy path against a list of domains or subdomains.
                
                :param fDomains:        a list to strings containing the domains and (optionally) a nick.
                :param fFuzzStruct:     a list to strings containing the transforms to be performed.
                
                :return:        Dictionary of {domain: url}.
        """
    logger = logging.getLogger('usufy')
    if fFuzzStruct == None:
        fuzzingStructures = [
         'http://<USERNAME>.<DOMAIN>',
         'http://<USERNAME>.<DOMAIN>/user/',
         'http://<DOMAIN>/<USERNAME>',
         'http://<DOMAIN>/user/<USERNAME>',
         'http://<DOMAIN>/users/<USERNAME>',
         'http://<DOMAIN>/en/users/<USERNAME>',
         'http://<DOMAIN>/profil/<USERNAME>',
         'http://<DOMAIN>/profile/<USERNAME>',
         'http://<DOMAIN>/members/<USERNAME>',
         'http://<DOMAIN>/channel/<USERNAME>',
         'http://<DOMAIN>/u/<USERNAME>',
         'http://<DOMAIN>/home/<USERNAME>',
         'http://<DOMAIN>/people/<USERNAME>',
         'http://<DOMAIN>/usr/<USERNAME>',
         'http://<DOMAIN>/~<USERNAME>',
         'http://<DOMAIN>/user-<USERNAME>',
         'http://<DOMAIN>/causes/author/<USERNAME>',
         'http://<DOMAIN>/profile/page/<USERNAME>',
         'http://<DOMAIN>/component/comprofiler/userprofiler/<USERNAME>',
         'http://<DOMAIN>/social/usuarios/<USERNAME>',
         'http://<DOMAIN>/mi-espacio/<USERNAME>',
         'http://<DOMAIN>/forum/profile.php?mode=viewprofile&u=<USERNAME>',
         'http://<DOMAIN>/index.php?action=profile;user=<USERNAME>',
         'http://<DOMAIN>/member.php?username=<USERNAME>',
         'http://<DOMAIN>/members/?username=<USERNAME>',
         'http://<DOMAIN>/forum/member.php?username=<USERNAME>',
         'http://<DOMAIN>/member.php?username=<USERNAME>',
         'http://<DOMAIN>/rapidforum/index.php?action=profile;user=<USERNAME>']
    else:
        try:
            fuzzingStructures = fFuzzStruct.read().splitlines()
        except:
            logger.error('Usufy could NOT open the following file: ' + fFuzzStruct)

        res = {}
        lines = fDomains.read().splitlines()
        for l in lines:
            domain = l.split('\t')[0]
            logger.info('Performing tests for' + domain + '...')
            nick = l.split('\t')[1]
            possibleURL = []
            for struct in fuzzingStructures:
                urlToTry = struct.replace('<DOMAIN>', domain)
                test = urlToTry.replace('<USERNAME>', nick.lower())
                logger.debug('Processing ' + test + '...')
                i3Browser = browser.Browser()
                try:
                    html = i3Browser.recoverURL(test)
                    if nick in html:
                        possibleURL.append(test)
                except:
                    logger.error('An error took place when downloading the webpage...')

            res[domain] = possibleURL

    return res


def getPageWrapper(p, nick, rutaDescarga, avoidProcessing=True, avoidDownload=True, outQueue=None):
    """ 
                Method that wraps the call to the getUserPage.

                List of parameters that the method receives:
                :param p:               platform where the information is stored.
                :param nick:            nick to be searched.
                :param rutaDescarga:    local file where saving the obtained information.
                :param avoidProcessing:boolean var that defines whether the profiles will NOT be processed (stored in this version).
                :param avoidDownload: boolean var that defines whether the profiles will NOT be downloaded (stored in this version).
                :param outQueue:        Queue where the information will be stored.
                :param maltego:         parameter to tell usufy.py that he has been invoked by Malego.

           :return: 
                        None if a queue is provided. Note that the values will be stored in the outQueue or a dictionary is returned.
        """
    logger = logging.getLogger('usufy')
    logger.debug('\tLooking for profiles in ' + str(p) + '...')
    res = p.getUserPage(nick, rutaDescarga, avoidProcessing=avoidProcessing, avoidDownload=avoidDownload)
    if res != None:
        if outQueue != None:
            outQueue.put(res)
        else:
            return res
    else:
        logger.debug('\t' + str(p) + ' - User profile not found...')
    return


def processNickList(nicks, platforms=None, rutaDescarga='./', avoidProcessing=True, avoidDownload=True, nThreads=12, maltego=False, verbosity=1, logFolder='./logs'):
    """ 
                Method that receives as a parameter a series of nicks and verifies whether those nicks have a profile associated in different social networks.

                List of parameters that the method receives:
                :param nicks:           list of nicks to process.
                :param platforms:       list of <Platform> objects to be processed. 
                :param rutaDescarga:    local file where saving the obtained information.
                :param avoidProcessing: boolean var that defines whether the profiles will NOT be processed.
                :param avoidDownload: boolean var that defines whether the profiles will NOT be downloaded (stored in this version).
                :param maltego:         parameter to tell usufy.py that he has been invoked by Malego.
                :param verbosity:       the level of verbosity to be used.
                :param logFolder:       the path to the log folder.
                
                :return:
                        Returns a dictionary where the key is the nick and the value another dictionary where the keys are the social networks and te value is the corresponding URL.
        """
    i3visiotools.logger.setupLogger(loggerName='usufy', verbosity=verbosity, logFolder=logFolder)
    logger = logging.getLogger('usufy')
    if platforms == None:
        platforms = config.getPlatforms()
    res = {}
    for nick in nicks:
        logger.info("Looking for '" + nick + "' in " + str(len(platforms)) + ' different platforms:\n' + str([ str(plat) for plat in platforms ]))
        if nThreads <= 0 or nThreads > len(platforms):
            nThreads = len(platforms)
        args = []
        for plat in platforms:
            args.append((plat, nick, rutaDescarga, avoidProcessing, avoidDownload))

        logger.info('Launching ' + str(nThreads) + ' different threads...')
        pool = Pool(nThreads)
        poolResults = pool.map(multi_run_wrapper, args)
        pool.close()
        profiles = []
        for r in poolResults:
            if r != None:
                profiles.append(r)

        res[nick] = profiles

    return res


def multi_run_wrapper(args):
    """ 
                Wrapper for being able to launch all the threads of getPageWrapper. 
                :param args: We receive the parameters for getPageWrapper as a tuple.
        """
    return getPageWrapper(*args)


def usufy_main(args):
    """ 
                Main function. This function is created in this way so as to let other applications make use of the full configuration capabilities of the application. 
        """
    i3visiotools.logger.setupLogger(loggerName='usufy', verbosity=args.verbose, logFolder=args.logfolder)
    logger = logging.getLogger('usufy')
    logger.info('usufy-launcher.py Copyright (C) F. Brezo and Y. Rubio (i3visio) 2014\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it under certain conditions.\nFor details, run:\n\tpython usufy-launcher.py --license')
    logger.info('Starting usufy-launcher.py...')
    if args.license:
        logger.info('Looking for the license...')
        try:
            with open('COPYING', 'r') as (iF):
                contenido = iF.read().splitlines()
                for linea in contenido:
                    print linea

        except Exception:
            logger.error('ERROR: there has been an error when opening the COPYING file.\n\tThe file contains the terms of the GPLv3 under which this software is distributed.\n\tIn case of doubts, verify the integrity of the files or contact contacto@i3visio.com.')

    elif args.fuzz:
        logger.info('Performing the fuzzing tasks...')
        res = fuzzUsufy(args.fuzz, args.fuzz_config)
        logger.info('Recovered platforms:\n' + str(res))
    else:
        logger.debug('Recovering the list of platforms to be processed...')
        listPlatforms = config.getPlatforms(sites=args.platforms, tags=args.tags, fileCreds=args.credentials)
        logger.debug('Platforms recovered.')
        if args.info:
            if args.info == 'list_platforms':
                infoPlatforms = 'Listing the platforms:\n'
                for p in listPlatforms:
                    infoPlatforms += '\t\t' + (str(p) + ': ').ljust(16, ' ') + str(p.tags) + '\n'

                logger.info(infoPlatforms)
                return infoPlatforms
            if args.info == 'list_tags':
                logger.info('Listing the tags:')
                tags = {}
                for p in listPlatforms:
                    for t in p.tags:
                        if t not in tags.keys():
                            tags[t] = 1
                        else:
                            tags[t] += 1

                infoTags = 'List of tags:\n'
                for t in tags.keys():
                    infoTags += '\t\t' + (t + ': ').ljust(16, ' ') + str(tags[t]) + '  time(s)\n'

                logger.info(infoTags)
                return infoTags
        else:
            if args.benchmark:
                logger.warning('The benchmark mode may last some minutes as it will be performing similar queries to the ones performed by the program in production. ')
                logger.info('Launching the benchmarking tests...')
                platforms = config.getPlatforms()
                res = benchmark.doBenchmark(platforms)
                strTimes = ''
                for e in sorted(res.keys()):
                    strTimes += str(e) + '\t' + str(res[e]) + '\n'

                logger.info(strTimes)
                return strTimes
            else:
                nicks = []
                logger.debug('Recovering nicknames to be processed...')
                if args.nicks:
                    for n in args.nicks:
                        if 'properties.i3visio' not in n:
                            nicks.append(n)

                else:
                    try:
                        nicks = args.list.read().splitlines()
                    except:
                        logger.error('ERROR: there has been an error when opening the file that stores the nicks.\tPlease, check the existence of this file.')

                if args.squatting:
                    logger.debug('Making basic transformations on the provided nicknames...')
                    nicks = profilesquatting.getNewNicks(nicks, logName='usufy', modes=args.squatting, nonValidChars=args.nonvalid)
                    logger.info('Obtained nicks:\n' + str(nicks))
                    logger.debug('Profilesquatting nicknames recovered.')
                    if args.info == 'list_users':
                        strNicks = ''
                        for n in nicks:
                            strNicks += n + '\n'

                        logger.info('Generated nicks:\n----------------\n' + strNicks)
                        logger.info('Creating output files as requested.')
                        if not os.path.exists(args.output_folder):
                            logger.warning("The output folder '" + args.output_folder + "' does not exist. The system will try to create it.")
                            os.makedirs(args.output_folder)
                        strTime = general.getCurrentStrDatetime()
                        logger.info('Writing generated nicks to a text file.')
                        with open(os.path.join(args.output_folder, 'nicks_' + strTime + '.txt'), 'w') as (oF):
                            oF.write(strNicks)
                        return nicks
                if args.output_folder != None:
                    logger.debug('Preparing the output folder...')
                    if not os.path.exists(args.output_folder):
                        logger.warning("The output folder '" + args.output_folder + "' does not exist. The system will try to create it.")
                        os.makedirs(args.output_folder)
                    res = processNickList(nicks, listPlatforms, args.output_folder, avoidProcessing=args.avoid_processing, avoidDownload=args.avoid_download, nThreads=args.threads, verbosity=args.verbose, logFolder=args.logfolder)
                else:
                    res = processNickList(nicks, listPlatforms, nThreads=args.threads, verbosity=args.verbose, logFolder=args.logfolder)
                logger.info('Listing the results obtained...')
                strResults = '\t'
                for nick in res.keys():
                    for r in res[nick]:
                        nick = r['value']
                        results = "Results for '" + nick + "':\n"
                        for profile in r['attributes']:
                            url = profile['value']
                            for details in profile['attributes']:
                                if details['type'] == 'i3visio.platform':
                                    platform = details['value']

                            strResults += (str(platform) + ':').ljust(16, ' ') + ' ' + str(url) + '\n\t\t'

                    logger.info(strResults)
                    if args.extension:
                        logger.info('Creating output files as requested.')
                        if not args.output_folder:
                            args.output_folder = './'
                        elif not os.path.exists(args.output_folder):
                            logger.warning("The output folder '" + args.output_folder + "' does not exist. The system will try to create it.")
                            os.makedirs(args.output_folder)
                        strTime = general.getCurrentStrDatetime()
                        if 'json' in args.extension:
                            logger.info('Writing results to json file.')
                            with open(os.path.join(args.output_folder, 'results_' + nick + '_' + strTime + '.json'), 'w') as (oF):
                                oF.write(general.dictToJson(res) + '\n')
                        if 'maltego' in args.extension:
                            logger.info('Writing results to maltego file.')
                            with open(os.path.join(args.output_folder, 'results_' + nick + '_' + strTime + '.maltego'), 'w') as (oF):
                                profiles = []
                                for element in res[nick]:
                                    profiles += element['attributes']

                                oF.write(general.listToMaltego(profiles) + '\n')
                    if args.maltego:
                        profiles = []
                        for element in res[nick]:
                            profiles += element['attributes']

                        general.listToMaltego(profiles)

                return res

    return