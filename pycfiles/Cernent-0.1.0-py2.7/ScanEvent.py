# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ScanEvent/ScanEvent.py
# Compiled at: 2012-04-26 15:24:51
"""
.. module:: ScanEvent
   :platform: Unix
   :synopsis: Key Module in the Cernent framework.  Scan Events are configured by the user
            and loaded by the daemon.  When the daemon looks for what scans should be ran,
            it searches the scan event directory, located at: /opt/cernent/ScanEvents and
            loads all .se files which are the saved scan event files.  Each one of these
            is a representation of the who, when, where, and what of scans.  The daemon
            runs a scan as the specified user: 'who', at the specified schedule 'when',
            at the specified target: 'where' and contains the email information of 
            the type of reports: 'what', that will be sent out to the respective parties.
            
            Each Scan Event contains all the information for scheduling a scan, signing
            in to the scanner, what type of scan will be run, and who will recieve the
            reports.  The daemon will use all this information when running a scan and
            sending out via-email the reports.
            

.. moduleauthor:: Brian_K, Daniel, Chris, and Brian_D
"""
import os, logging
from datetime import datetime
import MarkerFileIO, itertools
logger = logging.getLogger('ScanEvent')

class ScanEvent():
    """
    A serializable class that contains the user specified attributes of a scan and its reporting
    by the Cernent daemon.
    """
    BASE_PATH = globals()['__file__'].rpartition(os.sep)[0]
    RELATIVE_PATH = '/opt/cernent/ScanEvents/'
    DELIMITER = '|'
    DELIMITER_TARGETS = ','
    DELIMITER_EMAIL = '^'
    EXTENSION = '.se'

    def __init__(self):
        self.emailItems = []
        self.name = ''
        self.policy = ''
        self.scannerName = ''
        self.scansToKeep = 2
        self.schedule = getDefaultSchedule()
        self.targets = ''
        self.timeToWait = 10
        self.uuid = ''
        self.startNotif = None
        self.endNotif = None
        return

    def setEmailItems(self, itemList):
        """
        Sets the email items to a list of EmailItem instances.
        """
        if itemList != None:
            self.emailItems = itemList
        return True

    def getEmailItems(self):
        """
        Returns the list of email items.
        """
        return self.emailItems

    def setName(self, name):
        """
        Sets the name of this ScanEvent to the given String containing the name.
        """
        self.name = ('_').join(name.split())
        if self.name:
            return True
        return False

    def getName(self):
        """
        Returns the name of this ScanEvent, this should be the same as the file it was saved under.
        """
        return self.name

    def setPolicy(self, policy):
        """
        Sets the policy of this ScanEvent to the given String containing the policy name.
        """
        if not policy:
            return False
        self.policy = policy
        return True

    def getPolicy(self):
        """
        Returns the policy name to be used for this ScanEvent.
        """
        return self.policy

    def setSchedule(self, sched):
        """
        A dictionary where the keys are: strings 
        and the values are also strings.
        """
        self.schedule = sched
        return True

    def getSchedule_GUI(self):
        return self.schedule

    def getSchedule(self):
        """
        Returns a Schedule object as defined so that you can tell if this Scan even object should be scanned
        with now or not.
        """
        c = self.schedule.copy()
        if 'dwm' in c:
            c.pop('dwm')
        return c

    def setTargets(self, targets):
        """
        Sets the targets - which hosts are scanned.  This is a String containing a comma delimited list
        of hosts.
        """
        self.targets = targets
        return self.validateTargets(self.targets)

    def validateTargets(self, text):
        if not text:
            return True
        tokens = flatten([ x.split(',') for x in text.split() ])
        for t in tokens:
            if not t:
                continue
            parts = t.split('/')
            if len(parts) == 0:
                return False
            ret = self._validateIP(parts[0])
            if len(parts) == 2:
                ret = ret and self._validateCidr(parts[1])
            if not ret:
                return ret

        return True

    def _validateIP(self, ip):
        parts = ip.split('.')
        if len(parts) is not 4:
            return False
        for p in parts:
            try:
                if not int(p) < 256 or not int(p) > -1:
                    return False
            except:
                return False

        return True

    def _validateCidr(self, c):
        try:
            if not int(c) < 33 or not int(c) > 0:
                return False
        except:
            return False

        return True

    def getTargets(self):
        """
        Returns the list of targets to be scanned, a String containing a comma
        delimited lits of hosts.
        """
        return self.targets

    def setTimeToWait(self, time):
        """
        Sets the time to wait, which is the time between result download attempts in minutes. (Int)
        """
        self.timeToWait = time
        return True

    def getTimeToWait(self):
        """
        Returns the time to wait, which is the time between result download attempts in seconds. (Int)
        """
        return self.timeToWait

    def setUUID(self, uuid):
        """
        Sets the UUID of the scan that is initated on the nessus server.  This is an String.
        """
        self.uuid = uuid

    def getUUID(self):
        """
        Once a scan on the nessus server is initaited, it will return a unique UUID to identify the
        scan.  This method returns the UUID, if previously set.
        """
        return self.uuid

    def setScansToKeep(self, x):
        """
        Sets the number of scans to keep on disk
        """
        self.scansToKeep = x
        return True

    def getScansToKeep(self):
        """
        Returns the number of scans to keep on disk
        """
        return self.scansToKeep

    def setScannerName(self, scanner):
        """
        Sets the name of the Scanner to use for this SE
        """
        self.scannerName = scanner
        return True

    def getScannerName(self):
        """
        Returns the name of the Scanner to use for this SE
        """
        return self.scannerName

    def setStartNotif(self, slist):
        """
        Sets the list of email addressed to notify when this scan event starts.
        list should be a list of valid email addresses (comma delimited string).
        """
        if not slist:
            return True
        ls = slist.replace(' ', '').split(',')
        if self._validateEmailList(ls):
            self.startNotif = ls
            return True

    def _validateEmailList(self, slist):
        emails = slist
        for email in emails:
            if not self._validEmail(email):
                return False

        return True

    def _validEmail(self, email):
        parts = email.split('@')
        if len(parts) is not 2:
            return False
        if len(parts[1].split('.')) < 2:
            return False
        return True

    def getStartNotif(self):
        """
        Returns the list of email addresses (strings) that are the recipients of
        a notification as to when this scan event starts.
        """
        return self.startNotif

    def setEndNotif(self, elist):
        """
        Sets the list of email addressed to notify when this scan event end.
        list should be a list of valid email addresses (strings).
        """
        if not elist:
            return True
        ls = elist.replace(' ', '').split(',')
        if self._validateEmailList(ls):
            self.endNotif = ls
            return True

    def getEndNotif(self):
        """
        Returns the list of email addresses (strings) that are the recipients of
        a notification as to when this scan event ends.
        """
        return self.endNotif

    def isComplete(self):
        """
        Tests to see if this ScanEvent has been completely filled out.
        Returns "True" if everything important is a valid, or "False" if
        something is missing.
        """
        if not self.emailItems:
            return False
        else:
            if self.name is '' or self.name == None:
                return False
            if self.policy is '' or self.policy == None:
                return False
            if self.scannerName is '' or self.scannerName == None:
                return False
            if self.schedule == None:
                return False
            if not self.targets or self.targets is '' or len(self.targets) is 1:
                return False
            return True

    def isValid(self):
        """
        Returns whether or not this ScanEvent is Valid.
        """
        ret = True
        ret = ret and self.isComplete()
        ret = ret and self._validateIP(self.getTargets())
        ret = ret and self._validateEmailList(self.getStartNotif())
        ret = ret and self._validateEmailList(self.getEndNotif())
        return ret

    def getProblems(self):
        """
        Returns a list of strings naming each item that is missing in order for
        this ScanEvent's isComplete method to return "True".
        """
        problems = []
        if not self.emailItems:
            problems.append('No Email Items')
        if self.name is '' or self.name == None:
            problems.append('No Name')
        if self.policy is '' or self.policy == None:
            problems.append('No Policy')
        if self.scannerName is '' or self.scannerName == None:
            problems.append('No Server')
        if self.schedule == None:
            problems.append('No Schedule')
        if not self.targets or self.targets is '' or len(self.targets) is 1:
            problems.append('No Targets')
        return problems


def flatten(lists):
    """
    Flattens a list of lists.  Only shallow.
    """
    return list(itertools.chain.from_iterable(lists))


def getPathToSaves():
    """
    No longer configurabe, this is the mandatory final installation path directory.
    """
    return '/opt/cernent/ScanEvents/'


def loadScanEvent(filename):
    """
    Creates a ScanEvent instance from the data held within the file specified by filename.
    This filename should be just the name of the file itself, and not an absolute path.  For example,
    "myScan.se" is all that is required, but "/nfs/user/bkraus/cerno/.../myScan.se" is also acceptable.
    Having the .se at the end is required.
    """
    path = filename
    if not os.path.isabs(filename):
        path = ScanEvent.RELATIVE_PATH + os.sep + filename
    f = open(path, 'r')
    tokens = f.read().rstrip().split(ScanEvent.DELIMITER)
    f.close()
    scan = ScanEvent()
    __loadData(tokens, scan)
    return scan


def __loadData(tokens, scan):
    """
        Called by loadScanEvent, given the scan event tokens split by the delimiter, this helper method
        takes those tokens and loads them into the class instance.
    """

    def tokenDebugMsg(i):
        logger.debug('Token[%d]: %s %s' % (i, type(tokens[i]), str(tokens[i])))

    emailItems = tokens[0]
    tokenDebugMsg(0)
    if emailItems == '' or emailItems == 'None':
        val = None
    else:
        val = fromString(emailItems)
    scan.setEmailItems(val)
    scan.setName(tokens[1])
    tokenDebugMsg(1)
    policy = tokens[2]
    tokenDebugMsg(2)
    if policy == '' or policy == 'None':
        val = None
    else:
        val = policy
    scan.setPolicy(val)
    scan.setScannerName(tokens[3])
    tokenDebugMsg(3)
    stk = tokens[4]
    tokenDebugMsg(4)
    if stk == '' or stk == 'None':
        val = 0
    else:
        val = int(stk)
    scan.setScansToKeep(val)
    sched = tokens[5]
    tokenDebugMsg(5)
    val = None
    if sched == '':
        val = getDefaultSchedule()
    else:
        val = eval(sched)
    scan.setSchedule(val)
    tokenDebugMsg(6)
    scan.setTargets(tokens[6])
    val = tokens[7]
    tokenDebugMsg(7)
    if val:
        snotif = val
    else:
        snotif = None
    scan.setStartNotif(snotif)
    val = tokens[8]
    tokenDebugMsg(8)
    if val:
        enotif = val
    else:
        enotif = None
    scan.setEndNotif(enotif)
    return


def saveScanEvent(scanEvent, location):
    """
    Saves the given ScanEvent instance into a file specified by location.  If location
    is an absolute path, then it the ScanEvent instance will be saved there.  If it is not, then
    it will be a relative path from the local scanEvents folder.  The path contained in location
    is expected to have the file name with it, thus not being a path to just a directory.
    """
    if not location.endswith(ScanEvent.EXTENSION):
        location = location + ScanEvent.EXTENSION
    savePath = location
    if not os.path.isabs(location):
        savePath = ScanEvent.RELATIVE_PATH + os.sep + location
    f = open(savePath, 'w')
    f.write(__getString(scanEvent))
    f.close()
    MarkerFileIO.addSE(scanEvent.getName())


def getScanEventList():
    """
    Instanciates and returns all scan events in the scan event directory.
    """
    scanEventPaths = getScanEventPaths()
    scanEventObjects = []
    for path in scanEventPaths:
        nextScnEvent = loadScanEvent(path)
        scanEventObjects.append(nextScnEvent)

    return scanEventObjects


def getScanEventPaths():
    """
    Returns a list of the saved ScanEvent files in the local directory.
    """
    return [ x for x in os.listdir(ScanEvent.RELATIVE_PATH) if x.endswith(ScanEvent.EXTENSION) ]


def __getString(scanEvent):
    """
    Given the scan event, this method serializes the object into a pipe-deliminated string that
    is exact contents of a .se file.
    """
    strings = []
    emailItems = scanEvent.getEmailItems()
    emailString = ''
    if emailItems:
        emailString = toString(emailItems)
    strings.append(emailString)
    name = scanEvent.getName()
    if not name:
        name = ''
    strings.append(name)
    policy = scanEvent.getPolicy()
    if not policy:
        policy = ''
    strings.append(policy)
    scannerName = scanEvent.getScannerName()
    if not scannerName:
        scannerName = ''
    strings.append(scannerName)
    strings.append(str(scanEvent.getScansToKeep()))
    sched = scanEvent.getSchedule_GUI()
    if not sched:
        sched = getDefaultSchedule()
    strings.append(str(sched))
    targets = scanEvent.getTargets()
    if not targets:
        targets = ''
    strings.append(targets)
    snotif = scanEvent.getStartNotif()
    if not snotif:
        snotif = [
         '']
    strings.append(ScanEvent.DELIMITER_TARGETS.join(snotif))
    enotif = scanEvent.getEndNotif()
    if not enotif:
        enotif = [
         '']
    strings.append(ScanEvent.DELIMITER_TARGETS.join(enotif))
    return ScanEvent.DELIMITER.join(strings) + '\n'


def getDefaultSchedule():
    sched = {}
    sched['start_date'] = datetime.today().strftime('%Y-%m-%d')
    sched['dwm'] = 'Weekly'
    sched['hour'] = datetime.today().strftime('%H')
    sched['minute'] = datetime.today().strftime('%M')
    sched['day_of_week'] = ''
    return sched


class EmailItem():
    """
    A wrapper class that contains the information for the reporting emails that will 
    be sent out after a sucessful scan. 
    """
    NAME = 0
    TOADDRESSES = 1
    SUBJECT = 2
    BODY = 3
    REPORTLIST = 4

    def __init__(self, parameters):
        """
        Creates a new Email Item using an array of input parameters. 
        
        Args:
        
            parameters: An array of input parameters for the email item. 
        
        """
        self.contents = parameters

    def getName(self):
        """
        """
        return self.contents[EmailItem.NAME]

    def getToAddress(self):
        """
        """
        return self.contents[EmailItem.TOADDRESSES].split(',')

    def getSubject(self):
        """
        """
        return self.contents[EmailItem.SUBJECT]

    def getBody(self):
        """
        """
        return self.contents[EmailItem.BODY]

    def getReportList(self):
        """
        """
        return self.contents[EmailItem.REPORTLIST]

    def toString(self):
        """
        """
        return sanitizeForward(ScanEvent.DELIMITER_EMAIL, 'car', str(self.contents))

    def getContents(self):
        """
        """
        return self.contents

    def isValid(self):
        """
        This method ensures that the instanciated EmailItem will not 
        cause the java-equivalent of a null-pointer exception, and
        also ensures that the member values are 'sane'.
        """
        try:
            self.contents[EmailItem.BODY]
            self.contents[EmailItem.NAME]
            self.contents[EmailItem.REPORTLIST]
            self.contents[EmailItem.SUBJECT]
            self.contents[EmailItem.TOADDRESSES]
        except NameError:
            return False

        if not type(self.BODY) == type('Foo'):
            return False
        name = self.contents[EmailItem.NAME]
        if not type(name) == type('Foo'):
            return False
        if self.contents[EmailItem.NAME] == '':
            return False
        return True


def fromString(string):
    """
    This takes a string however formatted and returns a
    list of email items loaded from the string.
    
    Args: 
    
        string: A string version of an email item list.  
    
    """
    emailItems = []
    if string == '':
        return emailItems
    string.lstrip()
    for item in string.split(ScanEvent.DELIMITER_EMAIL):
        emailItems.append(EmailItem(eval(sanitizeBackward(ScanEvent.DELIMITER_EMAIL, 'car', item))))

    return emailItems


def toString(emailItemList):
    """
    This takes a list of email items and converts them into a string that cannot contain the character "|".
    The formatting of this string must match that used by fromString(string).
    
    Args: 
    
        emailItemList: A list of EmailItems to be turned into a string. 
    
    """
    string = ''
    first = True
    for emailItem in emailItemList:
        if first:
            string = string + emailItem.toString()
            first = False
        else:
            string = string + ScanEvent.DELIMITER_EMAIL + emailItem.toString()

    return string


def sanitizeForward(charDilimiterToBeReplaced, strNameOfChar, strToBeForwardEncoded):
    """
    This function takes user inputs and encodes the given delimiter so it does not
    affect later parsing.
    
    charDilimiterToBeReplaced is the character that will be removed from the string
       which came from user input.
    
    strNameOfChar is the name of character, it is a unique string that will be used
        for replacement, and should not contain any other delimiters.
        
    strToBeForwardEncoded is the user input that is having any possible delimiters
        coded.
    """
    output = strToBeForwardEncoded
    output = output.replace(strNameOfChar, '(' + strNameOfChar + ')')
    output = output.replace(charDilimiterToBeReplaced, '_' + strNameOfChar + '_')
    return output


def sanitizeBackward(charDilimiterReplaced, strNameOfChar, strToBeBackwardDecoded):
    """
    This is for undoing the encoding that was performed on user input.  This will put
    any delimiters back as well as any other mutations that were needed
    """
    output = strToBeBackwardDecoded
    output = str.replace(output, '_' + strNameOfChar + '_', charDilimiterReplaced)
    output = str.replace(output, '(' + strNameOfChar + ')', strNameOfChar)
    return output