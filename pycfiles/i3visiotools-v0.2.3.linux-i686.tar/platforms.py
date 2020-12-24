# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/platforms.py
# Compiled at: 2014-12-25 08:01:31
import os, random, re
from i3visiotools.browser import Browser
from i3visiotools.credentials import Credential
import i3visiotools.general as general, entify.lib.processing, logging

class Platform():
    """ 
                <Platform> class.
        """

    def __init__(self):
        """ 
                        Constructor without parameters...
                """
        pass

    def __init__(self, pName, tags, url, notFT, forChars, sco):
        """ 
                        Constructor with parameters. This method permits the developer to instantiate dinamically Platform objects.
                """
        self.platformName = pName
        self.tags = tags
        self.NICK_WILDCARD = 'HERE_GOES_THE_NICK'
        self.url = url
        self.notFoundText = notFT
        self.forbiddenList = forChars
        self.creds = []
        self.fieldDelimiters = {}
        self.foundFields = {}

    def __str__(self):
        u""" 
                        Función para obtener el texto que se representará a la hora de imprimir el objeto.
                        
                        :return:        self.platformName
                """
        return self.platformName

    def _genURL(self, nick):
        """        
                        Private method that returns an URL for a given nick. 
                        :param nick:                    

                        :return:        string containing a URL
                """
        return self.url.replace(self.NICK_WILDCARD, nick)

    def _genURLEnum(self, id):
        """        
                        Private method that returns an URL for a given id. 
                        :param id:      is an int value.

                        :return:        string containing a URL
                """
        return self.urlEnumeration.replace('<HERE_GOES_THE_USER_ID>', str(id))

    def _getAuthenticated(self, i3Browser):
        """ 
                        Getting authenticated. This method will be overwritten.
                """
        if len(self.creds) > 0:
            c = random.choice(self.creds)
            i3Browser.setNewPassword(url, c.user, c.password)
            return False
        else:
            logger.debug('No credentials have been added and this platform needs them.')
            return False

    def _doesTheUserExist(self, html):
        """ 
                        Method that performs the verification of the existence or not of a given profile. This method may be rewrritten.
                        
                        :param html:    The html text in which the self.notFoundText
                        :return :   None if the user was not found in the html text and the html text if the user DOES exist.                   
                """
        for t in self.notFoundText:
            if t in html:
                return None

        return html

    def _getResourceFromUser(self, url):
        u""" 
                        Este método privado de la clase padre puede ser sobreescrito por cada clase hija si la verificación
                        a realizar es más compleja que la verificación estándar.

                        Valores retornados:
                                html    Si el usuario en cuestión existe en esta red social.
                                None    Si el usuario en cuestión no existe en esta red social.
                """
        logger = logging.getLogger('i3visiotools')
        logger.debug('Trying to recover the url: ' + url)
        i3Browser = Browser()
        try:
            if self.needsCredentials():
                logger.debug('Trying to get authenticated in ' + str(self) + '...')
                authenticated = self._getAuthenticated(i3Browser)
                if authenticated:
                    logger.debug('Recovering the targetted url (authenticated)...')
                    html = i3Browser.recoverURL(url)
                else:
                    logger.debug('Something happened when trying to get authenticated... ')
                    return
            else:
                logger.debug('Recovering the targetted url...')
                html = i3Browser.recoverURL(url)
        except:
            logger.debug('Something happened when trying to recover the resource... No file will be returned.')
            return

        if self._doesTheUserExist(html):
            logger.debug('The key text has NOT been found in the downloaded file. The profile DOES exist and the html is returned.')
            return html
        else:
            logger.debug('The key text has been found in the downloaded file. The profile does NOT exist.')
            return
            return

    def _isValidUser(self, nick):
        """        
                        Method to verify if a given nick is processable by the platform. The system looks for the forbidden characters in self.Forbidden list.
                        :param nick:

                        :return:        True | False
                """
        for letter in self.forbiddenList:
            if letter in nick:
                return False

        return True

    def cleanFoundFields(self):
        """ 
                        Method that cleans up the fields recovered.
                        
                        [TO-DO]
                """
        pass

    def _getUserIdList(self, platformFolder, action):
        """
                """
        listUserId = []
        if not os.path.exists(platformFolder):
            os.makedirs(platformFolder)
            listUserId = range(self.iNumber, self.fNumber + 1)
        else:
            folder = os.path.join(platformFolder, 'raw')
            if not os.path.exists(folder):
                listUserId = range(self.iNumber, self.fNumber + 1)
            elif action == 'start':
                listUserId = range(self.iNumber, self.fNumber + 1)
            elif action == 'update':
                filenames = general.getFilesFromAFolder(folder)
                for f in filenames:
                    id = f.split('_')[0]
                    listUserId.append(id)

                lastIndex = listUserId[(len(listUserId) - 1)]
                for i in range(lastIndex, lastIndex + lastIndex / 100):
                    listUserId.append(i)

        return listUserId

    def getUserPage(self, nick, outputF='./', avoidProcessing=False, avoidDownload=False):
        u""" 
                        This public method is in charge of recovering the information from the user profile.
                        
                        List of parameters used by this method:
                        :param nick:            nick to search
                        :param outputF:         will contain a valid path to the outputFolder
                        :param avoidProcessing:boolean var that defines whether the profiles will NOT be processed .
                        :param avoidDownload: boolean var that defines whether the profiles will NOT be downloaded.
                        :return:
                                url     URL del usuario en cuestión una vez que se haya confirmado su validez.
                                None    En el caso de que no se haya podido obtener una URL válida.
                """
        logger = logging.getLogger('i3visiotools')
        if self._isValidUser(nick):
            logger.debug('Generating a URL...')
            url = self._genURL(nick)
            html = self._getResourceFromUser(url)
            if html != None:
                strTime = general.getCurrentStrDatetime()
                outputPath = os.path.join(outputF, nick)
                if not os.path.exists(outputPath):
                    os.makedirs(outputPath)
                if not avoidDownload:
                    logger.info('Storing the file...')
                    rawFolder = os.path.join(outputPath, 'raw')
                    if not os.path.exists(rawFolder):
                        os.makedirs(rawFolder)
                    rawFilename = os.path.join(rawFolder, nick + '_' + str(self).lower() + '_' + strTime + '.html')
                    logger.debug('Writing file: ' + rawFilename)
                    with open(rawFilename, 'w') as (oF):
                        oF.write(html)
                    logger.debug('File saved: ' + rawFilename)
                    rawHistoryName = os.path.join(outputPath, 'history_raw.csv')
                    logger.debug('Updating history file: ' + rawHistoryName)
                    with open(rawHistoryName, 'a') as (oF):
                        oF.write(rawFilename + '\t' + general.fileToMD5(rawFilename) + '\n')
                if not avoidProcessing:
                    procFolder = os.path.join(outputPath, 'proc')
                    if not os.path.exists(procFolder):
                        os.makedirs(procFolder)
                    procFilename = os.path.join(procFolder, nick + '_' + str(self).lower() + '_' + strTime + '.json')
                    res = self.processProfile(info=html, nick=nick, url=url)
                    logger.debug('Writing file: ' + procFilename)
                    with open(procFilename, 'w') as (oF):
                        oF.write(general.dictToJson(res))
                    logger.debug('File saved: ' + procFilename)
                    procHistoryName = os.path.join(outputPath, 'history_proc.csv')
                    logger.debug('Updating history file: ' + procHistoryName)
                    with open(procHistoryName, 'a') as (oF):
                        oF.write(procFilename + '\t' + general.fileToMD5(procFilename) + '\n')
                    return res
            else:
                logger.debug('The user was NOT found.')
                return
        else:
            logger.debug((str(self) + ':').ljust(18, ' ') + "The user '" + nick + "' will not be processed in this platform.")
            return
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

    def processProfile(self, info=None, nick=None, url=None):
        """        
                        Method to process an URL depending on the functioning of the site. By default, it stores the html downloaded on a file.
                        This method might be overwritten by each and every class to perform different actions such as indexing the contents with tools like pysolr, for example.
                        
                        Example:
                        {
                                {
                                        "type": "i3visio.alias",
                                        "value": "febrezo",
                                        "atributtes": [{
                                                "type": "i3visio.url",
                                                "value": "http://twitter.com/febrezo",
                                                "atributtes": [{
                                                        "type": "i3visio.platform",
                                                        "value": "Twitter",
                                                        "atributtes": [],
                                                }, ]
                                        }, {
                                                "type": "i3visio.url",
                                                "value": "http://facebook.com/febrezo",
                                                "atributtes": [{
                                                        "type": "i3visio.platform",
                                                        "value": "Facebook",
                                                        "atributtes": [],
                                                }]
                                        }, ]
                                }, {
                                        "type": "i3visio.alias",
                                        "value": "i3visio",
                                        "atributtes": [{
                                                "type": "i3visio.url",
                                                "value": "http://twitter.com/i3visio",
                                                "atributtes": [{
                                                        "type": "i3visio.platform",
                                                        "value": "Twitter",
                                                        "atributtes": [],
                                                }, ]
                                        }, ]
                                }
                        }

                        :return:        json text to be stored on a processed file.
                """

        def escapingSpecialCharacters(aux):
            """
                        """
            return aux
            escapingValues = ['(', ')', '[', ']', '-', '\\']
            for esc in escapingValues:
                aux = aux.replace(esc, '\\' + esc)

            return aux

        def cleanSpecialChars(auxList):
            """
                        """
            final = []
            cleaningChars = [
             '\n', '\t', '\r']
            for elem in auxList:
                for c in cleaningChars:
                    elem = elem.replace(c, '')

                elem = re.sub('<.+?>', ' ', elem)
                final.append(elem)

            return final

        logger = logging.getLogger('i3visiotools')
        try:
            self.foundFields['type'] = 'i3visio.alias'
            self.foundFields['value'] = nick
            self.foundFields['attributes'] = []
            aux_att = {}
            aux_att['type'] = 'i3visio.url'
            aux_att['value'] = url
            aux_att['attributes'] = []
            aux_att_att = {}
            aux_att_att['type'] = 'i3visio.platform'
            aux_att_att['value'] = self.platformName
            aux_att_att['attributes'] = []
            aux_att['attributes'].append(aux_att_att)
            aux_att['attributes'] += entify.getEntitiesByRegexp(data=info)
            self.foundFields['attributes'].append(aux_att)
            for field in self.fieldDelimiters.keys():
                delimiters = self.fieldDelimiters[field]
                start = escapingSpecialCharacters(delimiters['start'])
                end = escapingSpecialCharacters(delimiters['end'])
                values = re.findall(start + '(.*?)' + end, info, re.DOTALL)
                if len(values) > 0:
                    self.foundFields[field] = cleanSpecialChars(values)

            self.cleanFoundFields()
            return self.foundFields
        except:
            logger.debug('Something happened when processing ' + str(self) + '... Are self.foundFields or self.fieldDelimiters defined?')
            aux = {}
            aux['type'] = 'i3visio.alias'
            aux['value'] = nick
            aux['attributes'] = []
            aux_att = {}
            aux_att['type'] = 'i3visio.url'
            aux_att['value'] = url
            aux_att['attributes'] = []
            aux_att_att = {}
            aux_att_att['type'] = 'i3visio.platform'
            aux_att_att['value'] = self.platformName
            aux_att_att['attributes'] = []
            aux_att['attributes'].append(aux_att_att)
            aux_att['attributes'] += entify.getEntitiesByRegexp(data=info)
            aux['attributes'].append(aux_att)
            return aux

    def setCredentials(self, creds):
        """ 
                        Setting Credentials
                """
        self.creds = creds

    def hasUsufy(self):
        """ 
                        Determining if the current platform is a "usufy" platform or not.
                        
                        :return:        True if it contains a self.url and False if it is not the case.
                """
        try:
            if self.url is not None:
                return True
        except:
            return False

        return


def getAllPlatformsByMode(mode=None):
    """ 
                Method that defines the whole list of <Platform> objects to be processed... Note that <Facebook> or <Twitter> objects inherit from <Platform>.
                :param mode:    The mode of the search.  The following can be chosen: ["usufy"].

                Return values:
                        Returns a list [] of <Platform> objects.
        """
    listAll = getAllPlatforms()
    listPlatformsByMode = []
    for p in listAll:
        if mode == 'usufy':
            if p.hasUsufy():
                listPlatformsByMode.append(p)

    return listPlatformsByMode


def getAllPlatformParametersByMode(mode):
    """ 
                Method that defines the whole list of available parameters.
                :param mode:    The mode of the search. The following can be chosen: ["usufy"].

                Return values:
                        Returns a list [] of strings for the platform objects.
        """
    allPlatforms = getAllPlatformsByMode(mode=mode)
    platOptions = []
    for p in allPlatforms:
        try:
            parameter = p.parameterName
        except:
            parameter = p.platformName.lower()

        if parameter not in platOptions:
            platOptions.append(parameter)

    platOptions = sorted(set(platOptions))
    platOptions.insert(0, 'all')
    return platOptions


from i3visiotools.wrappers.px500 import Px500
from i3visiotools.wrappers.adtriboo import Adtriboo
from i3visiotools.wrappers.anarchy101 import Anarchy101
from i3visiotools.wrappers.aporrealos import Aporrealos
from i3visiotools.wrappers.apsense import Apsense
from i3visiotools.wrappers.arduino import Arduino
from i3visiotools.wrappers.ariva import Ariva
from i3visiotools.wrappers.armorgames import Armorgames
from i3visiotools.wrappers.artbreak import Artbreak
from i3visiotools.wrappers.artician import Artician
from i3visiotools.wrappers.arto import Arto
from i3visiotools.wrappers.askfm import Askfm
from i3visiotools.wrappers.audiob import Audiob
from i3visiotools.wrappers.audioboo import Audioboo
from i3visiotools.wrappers.authorstream import Authorstream
from i3visiotools.wrappers.autospies import Autospies
from i3visiotools.wrappers.backyardchickens import Backyardchickens
from i3visiotools.wrappers.badoo import Badoo
from i3visiotools.wrappers.behance import Behance
from i3visiotools.wrappers.bennugd import Bennugd
from i3visiotools.wrappers.bitbucket import Bitbucket
from i3visiotools.wrappers.bitcointalk import Bitcointalk
from i3visiotools.wrappers.bitly import Bitly
from i3visiotools.wrappers.blackplanet import Blackplanet
from i3visiotools.wrappers.bladna import Bladna
from i3visiotools.wrappers.blip import Blip
from i3visiotools.wrappers.blogspot import Blogspot
from i3visiotools.wrappers.bookmarky import Bookmarky
from i3visiotools.wrappers.boonex import Boonex
from i3visiotools.wrappers.bookofmatches import Bookofmatches
from i3visiotools.wrappers.bordom import Bordom
from i3visiotools.wrappers.boxedup import Boxedup
from i3visiotools.wrappers.breakcom import Breakcom
from i3visiotools.wrappers.bucketlistly import Bucketlistly
from i3visiotools.wrappers.burbuja import Burbuja
from i3visiotools.wrappers.burdastyle import Burdastyle
from i3visiotools.wrappers.buzznet import Buzznet
from i3visiotools.wrappers.cafemom import Cafemom
from i3visiotools.wrappers.carbonmade import Carbonmade
from i3visiotools.wrappers.cardomain import Cardomain
from i3visiotools.wrappers.care2 import Care2
from i3visiotools.wrappers.castroller import Castroller
from i3visiotools.wrappers.causes import Causes
from i3visiotools.wrappers.ccsinfo import Ccsinfo
from i3visiotools.wrappers.chess import Chess
from i3visiotools.wrappers.cockos import Cockos
from i3visiotools.wrappers.connectingsingles import Connectingsingles
from i3visiotools.wrappers.couchsurfing import Couchsurfing
from i3visiotools.wrappers.dailymail import Dailymail
from i3visiotools.wrappers.dailymotion import Dailymotion
from i3visiotools.wrappers.deviantart import Deviantart
from i3visiotools.wrappers.digitalspy import Digitalspy
from i3visiotools.wrappers.disqus import Disqus
from i3visiotools.wrappers.doodle import Doodle
from i3visiotools.wrappers.douban import Douban
from i3visiotools.wrappers.dribbble import Dribbble
from i3visiotools.wrappers.drupal import Drupal
from i3visiotools.wrappers.drugbuyersforum import Drugbuyersforum
from i3visiotools.wrappers.ebay import Ebay
from i3visiotools.wrappers.echatta import Echatta
from i3visiotools.wrappers.elmundo import Elmundo
from i3visiotools.wrappers.enfemenino import Enfemenino
from i3visiotools.wrappers.epinions import Epinions
from i3visiotools.wrappers.eqe import Eqe
from i3visiotools.wrappers.ethereum import Ethereum
from i3visiotools.wrappers.etsy import Etsy
from i3visiotools.wrappers.evilzone import Evilzone
from i3visiotools.wrappers.facebook import Facebook
from i3visiotools.wrappers.fanpop import Fanpop
from i3visiotools.wrappers.fark import Fark
from i3visiotools.wrappers.favstar import Favstar
from i3visiotools.wrappers.flickr import Flickr
from i3visiotools.wrappers.flixster import Flixster
from i3visiotools.wrappers.foodspotting import Foodspotting
from i3visiotools.wrappers.forobtc import Forobtc
from i3visiotools.wrappers.forocoches import Forocoches
from i3visiotools.wrappers.forosperu import Forosperu
from i3visiotools.wrappers.foursquare import Foursquare
from i3visiotools.wrappers.freebase import Freebase
from i3visiotools.wrappers.freerepublic import Freerepublic
from i3visiotools.wrappers.friendfeed import Friendfeed
from i3visiotools.wrappers.gametracker import Gametracker
from i3visiotools.wrappers.gapyear import Gapyear
from i3visiotools.wrappers.garage4hackers import Garage4hackers
from i3visiotools.wrappers.gather import Gather
from i3visiotools.wrappers.geeksphone import Geeksphone
from i3visiotools.wrappers.genspot import Genspot
from i3visiotools.wrappers.getsatisfaction import Getsatisfaction
from i3visiotools.wrappers.github import Github
from i3visiotools.wrappers.gitorious import Gitorious
from i3visiotools.wrappers.gogobot import Gogobot
from i3visiotools.wrappers.goodreads import Goodreads
from i3visiotools.wrappers.googleplus import GooglePlus
from i3visiotools.wrappers.gsmspain import Gsmspain
from i3visiotools.wrappers.hellboundhackers import Hellboundhackers
from i3visiotools.wrappers.hi5 import Hi5
from i3visiotools.wrappers.ibosocial import Ibosocial
from i3visiotools.wrappers.identica import Identica
from i3visiotools.wrappers.imgur import Imgur
from i3visiotools.wrappers.instagram import Instagram
from i3visiotools.wrappers.instructables import Instructables
from i3visiotools.wrappers.interracialmatch import Interracialmatch
from i3visiotools.wrappers.intersect import Intersect
from i3visiotools.wrappers.intfiction import Intfiction
from i3visiotools.wrappers.islamicawakening import Islamicawakening
from i3visiotools.wrappers.issuu import Issuu
from i3visiotools.wrappers.ixgames import Ixgames
from i3visiotools.wrappers.jamiiforums import Jamiiforums
from i3visiotools.wrappers.kaboodle import Kaboodle
from i3visiotools.wrappers.kali import Kali
from i3visiotools.wrappers.karmacracy import Karmacracy
from i3visiotools.wrappers.kickstarter import Kickstarter
from i3visiotools.wrappers.kinja import Kinja
from i3visiotools.wrappers.klout import Klout
from i3visiotools.wrappers.kongregate import Kongregate
from i3visiotools.wrappers.kupika import Kupika
from i3visiotools.wrappers.lastfm import Lastfm
from i3visiotools.wrappers.linkedin import Linkedin
from i3visiotools.wrappers.livejournal import Livejournal
from i3visiotools.wrappers.looki import Looki
from i3visiotools.wrappers.marca import Marca
from i3visiotools.wrappers.matchdoctor import Matchdoctor
from i3visiotools.wrappers.mcneel import Mcneel
from i3visiotools.wrappers.mediavida import Mediavida
from i3visiotools.wrappers.medium import Medium
from i3visiotools.wrappers.meneame import Meneame
from i3visiotools.wrappers.metacafe import Metacafe
from i3visiotools.wrappers.migente import Migente
from i3visiotools.wrappers.minecraft import Minecraft
from i3visiotools.wrappers.musicasacra import Musicasacra
from i3visiotools.wrappers.myeloma import Myeloma
from i3visiotools.wrappers.myspace import Myspace
from i3visiotools.wrappers.naver import Naver
from i3visiotools.wrappers.netlog import Netlog
from i3visiotools.wrappers.netvibes import Netvibes
from i3visiotools.wrappers.occupywallst import Occupywallst
from i3visiotools.wrappers.odnoklassniki import Odnoklassniki
from i3visiotools.wrappers.openframeworks import Openframeworks
from i3visiotools.wrappers.oroom import Oroom
from i3visiotools.wrappers.pastebin import Pastebin
from i3visiotools.wrappers.pearltrees import Pearltrees
from i3visiotools.wrappers.peerbackers import Peerbackers
from i3visiotools.wrappers.photobucket import Photobucket
from i3visiotools.wrappers.pinterest import Pinterest
from i3visiotools.wrappers.pixinsight import Pixinsight
from i3visiotools.wrappers.pjrc import Pjrc
from i3visiotools.wrappers.plancast import Plancast
from i3visiotools.wrappers.pokerred import Pokerred
from i3visiotools.wrappers.pokerstrategy import Pokerstrategy
from i3visiotools.wrappers.pornhub import Pornhub
from i3visiotools.wrappers.proboards import Proboards
from i3visiotools.wrappers.pz import Pz
from i3visiotools.wrappers.qq import QQ
from i3visiotools.wrappers.quartermoonsaloon import Quartermoonsaloon
from i3visiotools.wrappers.rankia import Rankia
from i3visiotools.wrappers.rapid import Rapid
from i3visiotools.wrappers.ratemypoo import Ratemypoo
from i3visiotools.wrappers.rawtherapee import Rawtherapee
from i3visiotools.wrappers.rebelmouse import Rebelmouse
from i3visiotools.wrappers.redtube import Redtube
from i3visiotools.wrappers.relatious import Relatious
from i3visiotools.wrappers.researchgate import Researchgate
from i3visiotools.wrappers.rojadirecta import Rojadirecta
from i3visiotools.wrappers.ruby import Ruby
from i3visiotools.wrappers.scribd import Scribd
from i3visiotools.wrappers.sencha import Sencha
from i3visiotools.wrappers.skype import Skype
from i3visiotools.wrappers.slashdot import Slashdot
from i3visiotools.wrappers.slideshare import Slideshare
from i3visiotools.wrappers.smartcitizen import Smartcitizen
from i3visiotools.wrappers.sokule import Sokule
from i3visiotools.wrappers.soundcloud import Soundcloud
from i3visiotools.wrappers.sourceforge import Sourceforge
from i3visiotools.wrappers.spaniards import Spaniards
from i3visiotools.wrappers.spoj import Spoj
from i3visiotools.wrappers.spotify import Spotify
from i3visiotools.wrappers.squidoo import Squidoo
from i3visiotools.wrappers.steamcommunity import Steamcommunity
from i3visiotools.wrappers.steinberg import Steinberg
from i3visiotools.wrappers.streakgaming import Streakgaming
from i3visiotools.wrappers.stuff import Stuff
from i3visiotools.wrappers.stumbleupon import Stumbleupon
from i3visiotools.wrappers.teamtreehouse import Teamtreehouse
from i3visiotools.wrappers.techcrunch import Techcrunch
from i3visiotools.wrappers.thecarcommunity import Thecarcommunity
from i3visiotools.wrappers.theguardian import Theguardian
from i3visiotools.wrappers.thehoodup import Thehoodup
from i3visiotools.wrappers.thesims import Thesims
from i3visiotools.wrappers.thestudentroom import Thestudentroom
from i3visiotools.wrappers.tradimo import Tradimo
from i3visiotools.wrappers.travian import Travian
from i3visiotools.wrappers.tripadvisor import Tripadvisor
from i3visiotools.wrappers.tripit import Tripit
from i3visiotools.wrappers.trulia import Trulia
from i3visiotools.wrappers.tumblr import Tumblr
from i3visiotools.wrappers.tuporno import Tuporno
from i3visiotools.wrappers.tvtag import Tvtag
from i3visiotools.wrappers.twicsy import Twicsy
from i3visiotools.wrappers.twitch import Twitch
from i3visiotools.wrappers.twoplustwo import Twoplustwo
from i3visiotools.wrappers.twitpic import Twitpic
from i3visiotools.wrappers.twitter import Twitter
from i3visiotools.wrappers.ukdebate import Ukdebate
from i3visiotools.wrappers.ummahforum import Ummahforum
from i3visiotools.wrappers.unsystem import Unsystem
from i3visiotools.wrappers.ustream import Ustream
from i3visiotools.wrappers.vexforum import Vexforum
from i3visiotools.wrappers.vimeo import Vimeo
from i3visiotools.wrappers.videohelp import Videohelp
from i3visiotools.wrappers.virustotal import Virustotal
from i3visiotools.wrappers.vk import Vk
from i3visiotools.wrappers.wefollow import Wefollow
from i3visiotools.wrappers.wikipediaar import WikipediaAr
from i3visiotools.wrappers.wikipediaca import WikipediaCa
from i3visiotools.wrappers.wikipediade import WikipediaDe
from i3visiotools.wrappers.wikipediaen import WikipediaEn
from i3visiotools.wrappers.wikipediaes import WikipediaEs
from i3visiotools.wrappers.wikipediaeu import WikipediaEu
from i3visiotools.wrappers.winamp import Winamp
from i3visiotools.wrappers.wishlistr import Wishlistr
from i3visiotools.wrappers.wordpress import Wordpress
from i3visiotools.wrappers.wykop import Wykop
from i3visiotools.wrappers.xanga import Xanga
from i3visiotools.wrappers.xat import Xat
from i3visiotools.wrappers.xing import Xing
from i3visiotools.wrappers.xtube import Xtube
from i3visiotools.wrappers.youku import Youku
from i3visiotools.wrappers.youtube import Youtube
from i3visiotools.wrappers.zabbix import Zabbix
from i3visiotools.wrappers.zentyal import Zentyal

def getAllPlatforms():
    """ 
                Method that defines the whole list of <Platform> objects to be processed... Note that <Facebook> or <Twitter> objects inherit from <Platform>.

                Return values:
                        Returns a list [] of <Platform> objects.
        """
    listAll = []
    listAll.append(Adtriboo())
    listAll.append(Anarchy101())
    listAll.append(Apsense())
    listAll.append(Aporrealos())
    listAll.append(Ariva())
    listAll.append(Arduino())
    listAll.append(Armorgames())
    listAll.append(Artbreak())
    listAll.append(Artician())
    listAll.append(Arto())
    listAll.append(Askfm())
    listAll.append(Audiob())
    listAll.append(Audioboo())
    listAll.append(Authorstream())
    listAll.append(Autospies())
    listAll.append(Backyardchickens())
    listAll.append(Badoo())
    listAll.append(Behance())
    listAll.append(Bennugd())
    listAll.append(Bitbucket())
    listAll.append(Bitcointalk())
    listAll.append(Bitly())
    listAll.append(Blackplanet())
    listAll.append(Bladna())
    listAll.append(Blip())
    listAll.append(Blogspot())
    listAll.append(Bookmarky())
    listAll.append(Bookofmatches())
    listAll.append(Boonex())
    listAll.append(Bordom())
    listAll.append(Boxedup())
    listAll.append(Breakcom())
    listAll.append(Bucketlistly())
    listAll.append(Burbuja())
    listAll.append(Burdastyle())
    listAll.append(Buzznet())
    listAll.append(Cafemom())
    listAll.append(Carbonmade())
    listAll.append(Cardomain())
    listAll.append(Care2())
    listAll.append(Castroller())
    listAll.append(Causes())
    listAll.append(Ccsinfo())
    listAll.append(Chess())
    listAll.append(Cockos())
    listAll.append(Connectingsingles())
    listAll.append(Couchsurfing())
    listAll.append(Dailymail())
    listAll.append(Dailymotion())
    listAll.append(Deviantart())
    listAll.append(Digitalspy())
    listAll.append(Disqus())
    listAll.append(Doodle())
    listAll.append(Douban())
    listAll.append(Dribbble())
    listAll.append(Drugbuyersforum())
    listAll.append(Drupal())
    listAll.append(Ebay())
    listAll.append(Echatta())
    listAll.append(Elmundo())
    listAll.append(Enfemenino())
    listAll.append(Epinions())
    listAll.append(Eqe())
    listAll.append(Ethereum())
    listAll.append(Etsy())
    listAll.append(Evilzone())
    listAll.append(Facebook())
    listAll.append(Fanpop())
    listAll.append(Fark())
    listAll.append(Favstar())
    listAll.append(Flickr())
    listAll.append(Flixster())
    listAll.append(Foodspotting())
    listAll.append(Forobtc())
    listAll.append(Forocoches())
    listAll.append(Forosperu())
    listAll.append(Foursquare())
    listAll.append(Freebase())
    listAll.append(Freerepublic())
    listAll.append(Friendfeed())
    listAll.append(Gametracker())
    listAll.append(Gapyear())
    listAll.append(Garage4hackers())
    listAll.append(Gather())
    listAll.append(Geeksphone())
    listAll.append(Genspot())
    listAll.append(Getsatisfaction())
    listAll.append(Github())
    listAll.append(Gitorious())
    listAll.append(Gogobot())
    listAll.append(Goodreads())
    listAll.append(GooglePlus())
    listAll.append(Gsmspain())
    listAll.append(Hellboundhackers())
    listAll.append(Hi5())
    listAll.append(Ibosocial())
    listAll.append(Identica())
    listAll.append(Imgur())
    listAll.append(Instagram())
    listAll.append(Interracialmatch())
    listAll.append(Intersect())
    listAll.append(Intfiction())
    listAll.append(Instructables())
    listAll.append(Islamicawakening())
    listAll.append(Issuu())
    listAll.append(Ixgames())
    listAll.append(Jamiiforums())
    listAll.append(Kaboodle())
    listAll.append(Kali())
    listAll.append(Karmacracy())
    listAll.append(Kickstarter())
    listAll.append(Kinja())
    listAll.append(Klout())
    listAll.append(Kongregate())
    listAll.append(Kupika())
    listAll.append(Lastfm())
    listAll.append(Linkedin())
    listAll.append(Livejournal())
    listAll.append(Looki())
    listAll.append(Marca())
    listAll.append(Matchdoctor())
    listAll.append(Mcneel())
    listAll.append(Mediavida())
    listAll.append(Medium())
    listAll.append(Meneame())
    listAll.append(Metacafe())
    listAll.append(Migente())
    listAll.append(Minecraft())
    listAll.append(Musicasacra())
    listAll.append(Myeloma())
    listAll.append(Myspace())
    listAll.append(Naver())
    listAll.append(Netlog())
    listAll.append(Netvibes())
    listAll.append(Occupywallst())
    listAll.append(Odnoklassniki())
    listAll.append(Openframeworks())
    listAll.append(Oroom())
    listAll.append(Pastebin())
    listAll.append(Pearltrees())
    listAll.append(Peerbackers())
    listAll.append(Photobucket())
    listAll.append(Pinterest())
    listAll.append(Pixinsight())
    listAll.append(Pjrc())
    listAll.append(Plancast())
    listAll.append(Pokerred())
    listAll.append(Pokerstrategy())
    listAll.append(Pornhub())
    listAll.append(Proboards())
    listAll.append(Px500())
    listAll.append(Pz())
    listAll.append(QQ())
    listAll.append(Quartermoonsaloon())
    listAll.append(Rankia())
    listAll.append(Rapid())
    listAll.append(Ratemypoo())
    listAll.append(Rawtherapee())
    listAll.append(Rebelmouse())
    listAll.append(Redtube())
    listAll.append(Relatious())
    listAll.append(Researchgate())
    listAll.append(Rojadirecta())
    listAll.append(Ruby())
    listAll.append(Scribd())
    listAll.append(Sencha())
    listAll.append(Skype())
    listAll.append(Slashdot())
    listAll.append(Slideshare())
    listAll.append(Smartcitizen())
    listAll.append(Sokule())
    listAll.append(Soundcloud())
    listAll.append(Sourceforge())
    listAll.append(Spaniards())
    listAll.append(Spoj())
    listAll.append(Spotify())
    listAll.append(Squidoo())
    listAll.append(Steamcommunity())
    listAll.append(Steinberg())
    listAll.append(Streakgaming())
    listAll.append(Stuff())
    listAll.append(Stumbleupon())
    listAll.append(Teamtreehouse())
    listAll.append(Techcrunch())
    listAll.append(Thecarcommunity())
    listAll.append(Theguardian())
    listAll.append(Thehoodup())
    listAll.append(Thesims())
    listAll.append(Thestudentroom())
    listAll.append(Tradimo())
    listAll.append(Travian())
    listAll.append(Tripadvisor())
    listAll.append(Tripit())
    listAll.append(Trulia())
    listAll.append(Tumblr())
    listAll.append(Tuporno())
    listAll.append(Tvtag())
    listAll.append(Twicsy())
    listAll.append(Twitch())
    listAll.append(Twitpic())
    listAll.append(Twitter())
    listAll.append(Twoplustwo())
    listAll.append(Ukdebate())
    listAll.append(Ummahforum())
    listAll.append(Unsystem())
    listAll.append(Ustream())
    listAll.append(Vexforum())
    listAll.append(Videohelp())
    listAll.append(Vimeo())
    listAll.append(Virustotal())
    listAll.append(Vk())
    listAll.append(Wefollow())
    listAll.append(WikipediaAr())
    listAll.append(WikipediaCa())
    listAll.append(WikipediaDe())
    listAll.append(WikipediaEn())
    listAll.append(WikipediaEs())
    listAll.append(WikipediaEu())
    listAll.append(Winamp())
    listAll.append(Wishlistr())
    listAll.append(Wordpress())
    listAll.append(Wykop())
    listAll.append(Xanga())
    listAll.append(Xat())
    listAll.append(Xing())
    listAll.append(Xtube())
    listAll.append(Youku())
    listAll.append(Youtube())
    listAll.append(Zabbix())
    listAll.append(Zentyal())
    return listAll