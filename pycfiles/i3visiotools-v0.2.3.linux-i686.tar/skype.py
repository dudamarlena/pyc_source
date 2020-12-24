# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/skype.py
# Compiled at: 2014-12-25 06:48:18
import logging, os
from platforms import Platform
import i3visiotools.general as general, Skype4Py

class Skype(Platform):
    """ 
                A <Platform> object for Skype.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Skype'
        self.tags = [
         'messaging']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.forbiddenList = []
        self._needsCredentials = True
        self.foundFields = {}

    def processProfile(self, info=None, nick=None, url=None):
        """
                """
        pairs = info.split('; ')
        for p in pairs:
            parts = p.split(':')
            if len(parts) == 2:
                self.foundFields[parts[0]] = parts[1]

        return self.foundFields

    def getUserPage(self, nick, outputF=None, avoidProcessing=True, avoidDownload=True):
        u""" 
                        This public method is in charge of recovering the information from the user profile in Skype.
                        
                        List of parameters used by this method:
                                nick:           nick to search
                                outputF:        will contain a valid path to the outputFolder
                                avoidProcessing:will define whether a further process is performed
        
                        Return values:
                                url     URL del usuario en cuestión una vez que se haya confirmado su validez.
                                None    En el caso de que no se haya podido obtener una URL válida.
                """
        try:
            logger = logging.getLogger('usufy')
            if self._isValidUser(nick):
                logger.debug('Starting Skype client...')
                logger.warning('A Skype client must be set up... Note that the program will need a valid session of Skype having been started. If you were performing too many searches, the server may block or ban your account depending on the ToS. Please run this program under your own responsibility.')
                skype = Skype4Py.Skype()
                if not skype.Client.IsRunning:
                    skype.Client.Start()
                    if not skype.Client.IsRunning:
                        logger.error('The Skype application could NOT be started...')
                        return
                skype.FriendlyName = 'Usufy with Skype4Py'
                skype.Attach()

                def new_skype_status(status):
                    if status == Skype4Py.apiAttachAvailable:
                        skype.Attach()

                skype.OnAttachmentStatus = new_skype_status
                import codecs, sys
                UTF8Writer = codecs.getwriter('utf8')
                sys.stdout = UTF8Writer(sys.stdout)
                info = None
                resultados = skype.SearchForUsers(nick)
                for user in resultados:
                    if user.Handle.lower() == nick.lower():
                        info = 'i3visio.profile:' + user.Handle + '; '
                        try:
                            info += 'i3visio.aliases:' + str(user.Aliases) + '; i3visio.fullname:' + str(user.FullName) + '; i3visio.platform:skype://' + user.Handle
                        except:
                            pass

                if info != None:
                    if not avoidProcessing:
                        logger.debug('Storing the file...')
                        strTime = general.getCurrentStrDatetime()
                        outputPath = os.path.join(outputF, nick)
                        if not os.path.exists(outputPath):
                            os.makedirs(outputPath)
                        rawFolder = os.path.join(outputPath, 'raw')
                        if not os.path.exists(rawFolder):
                            os.makedirs(rawFolder)
                        rawFilename = os.path.join(rawFolder, nick + '_' + str(self).lower() + '_' + strTime + '.html')
                        logger.debug('Writing file: ' + rawFilename)
                        with open(rawFilename, 'w') as (oF):
                            oF.write(info)
                        logger.debug('File saved: ' + rawFilename)
                        procFolder = os.path.join(outputPath, 'proc')
                        if not os.path.exists(procFolder):
                            os.makedirs(procFolder)
                        procFilename = os.path.join(procFolder, nick + '_' + str(self).lower() + '_' + strTime + '.json')
                        logger.debug('Writing file: ' + procFilename)
                        res = self.processProfile(info, nick, None)
                        with open(procFilename, 'w') as (oF):
                            oF.write(general.dictToJson(res))
                        logger.debug('File saved: ' + procFilename)
                        rawHistoryName = os.path.join(outputPath, 'history_raw.csv')
                        procHistoryName = os.path.join(outputPath, 'history_proc.csv')
                        with open(rawHistoryName, 'a') as (oF):
                            oF.write(rawFilename + '\t' + general.fileToMD5(rawFilename) + '\n')
                        with open(procHistoryName, 'a') as (oF):
                            oF.write(procFilename + '\t' + general.fileToMD5(procFilename) + '\n')
                        return res
                    else:
                        return {}

                else:
                    logger.debug((str(self) + ':').ljust(18, ' ') + "The user '" + nick + "' will not be processed in this platform.")
                    return
            else:
                return
        except:
            logger.error('A major problem occurred when trying to launch Skype. Check if this program is already opened.')

        return

    def needsCredentials(self):
        """ 
                        Returns if it needsCredentials.
                        IT captures the exception if the option does not exist. This way we do not have to recode all the platforms
                """
        try:
            return self._needsCredentials
        except:
            return False