# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\quarchQPS.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 9892 bytes
from .device import quarchDevice
from quarchpy.qps import toQpsTimeStamp
import os, time, datetime, sys, logging
current_milli_time = lambda : int(round(time.time() * 1000))
current_second_time = lambda : int(round(time.time()))

def qpsNowStr():
    return current_milli_time()


class quarchQPS(quarchDevice):

    def __init__(self, quarchDevice):
        self.quarchDevice = quarchDevice
        self.ConType = quarchDevice.ConType
        self.ConString = quarchDevice.ConString
        self.connectionObj = quarchDevice.connectionObj
        self.IP_address = quarchDevice.connectionObj.qps.host
        self.port_number = quarchDevice.connectionObj.qps.port

    def getCanStream(self):
        streamableDevices = [
         'qtl1824', 'qtl1847', 'qtl1944', 'qtl1995', 'qtl1999']
        startPos = self.ConString.index('q')
        for item in streamableDevices:
            tmp = str(self.ConString[startPos:startPos + 7])
            if tmp == str(item):
                return True

        return False

    def startStream(self, directory):
        if not self.getCanStream():
            print('This device does not support streaming.')
            return
        return quarchStream(self.quarchDevice, directory)


class quarchStream(quarchQPS):

    def __init__(self, quarchQPS, directory):
        self.connectionObj = quarchQPS.connectionObj
        self.IP_address = quarchQPS.connectionObj.qps.host
        self.port_number = quarchQPS.connectionObj.qps.port
        self.ConString = quarchQPS.ConString
        self.ConType = quarchQPS.ConType
        time.sleep(1)
        newDirectory = self.failCheck(directory)

    def failCheck(self, newDirectory):
        validResponse = False
        while validResponse == False:
            response = self.connectionObj.qps.sendCmdVerbose('$start stream ' + str(newDirectory))
            if 'Fail' in response:
                print(response + ', Please enter a new file name:')
                path = os.path.dirname(newDirectory)
                if sys.version_info.major == 3:
                    newEnd = input()
                else:
                    newEnd = raw_input()
                newDirectory = path.replace('\\\\', '\\') + newEnd
            else:
                validResponse = True

        return newDirectory

    def addAnnotation(self, title, annotationTime=0, extraText='', yPos='', titleColor='', annotationColor='', annotationType='', annotationGroup=''):
        """
                    Adds a custom annotation to stream with given parameters.

                    Parameters
                    ----------
                    title= : str
                        The title appears next to the annotation in the stream
                    extraText= : str, optional
                        The additional text that can be viewed when selecting the annotation
                    yPos : str, optional
                        The percetange of how high up the screen the annotation should appear 0 is the bottom and 100 the top
                    titleColor : str, optional
                        The color of the text next to the annotation in hex format 000000 to FFFFFF
                    annotationColor : str, optional
                        The color of the annotation marker in hex format 000000 to FFFFFF
                    annotationGroup : str, optional
                        The group the annotation belongs to
                    annotationTime : int, optional
                        The time in milliseconds after the start of the stream at which the annotation should be placed. 0 will plot the annotation live at the most recent sample

                    Returns
                    -------
                    command_response : str or None

                        The response text from QPS. "ok" if annotation successfully added
            """
        annotationString = '<'
        if annotationTime == 0:
            annotationTime = qpsNowStr()
        else:
            annotationTime = toQpsTimeStamp(annotationTime)
        if title != '':
            annotationString += '<text>' + str(title) + '</text>'
        if extraText != '':
            annotationString += '<extraText>' + str(extraText) + '</extraText>'
        if yPos != '':
            annotationString += '<yPos>' + str(yPos) + '</yPos>'
        if titleColor != '':
            annotationString += '<textColor>' + str(titleColor) + '</textColor>'
        if annotationColor != '':
            annotationString += '<color>' + str(annotationColor) + '</color>'
        if annotationGroup != '':
            annotationString += '<userType>' + str(annotationGroup) + '</userType>'
        annotationString += '>'
        annotationString = annotationString.replace('\n', '\\n')
        annotationType = annotationType.lower()
        if annotationType == '' or annotationType == 'annotation':
            annotationType = 'annotate'
        else:
            if annotationType == 'comment':
                pass
            else:
                retString = "Fail annotationType must be 'annotation' or 'comment'"
                logging.warning(retString)
                return retString
            print('Time sending to QPS:' + str(annotationTime))
            return self.connectionObj.qps.sendCmdVerbose('$' + annotationType + ' ' + str(annotationTime) + ' ' + annotationString)

    def addComment(self, title, commentTime=0, extraText='', yPos='', titleColor='', commentColor='', annotationType='', annotationGroup=''):
        if annotationType == '':
            annotationType = 'comment'
        return self.addAnnotation(title=title, annotationTime=commentTime, extraText=extraText, yPos=yPos, titleColor=titleColor, annotationColor=commentColor, annotationType=annotationType, annotationGroup=annotationGroup)

    def stats_to_CSV(self, file_name=''):
        """
        Saves the statistics grid to a csv file

                    Parameters
                    ----------
                    file-name= : str, optional
                        The absolute path of the file you would like to save the csv to. If left empty then a filename will be give.
                        Default location is the path of the executable.
                    Returns
                    -------
                    command_response : str or None

                        The response text from QPS. If successful "ok. Saving stats to : file_name" otherwise returns the exception thrown
        """
        self.connectionObj.qps.sendCmdVerbose('$stats to csv "' + file_name + '"')

    def createChannel(self, channelName, channelGroup, baseUnits, usePrefix):
        if usePrefix == False:
            usePrefix = 'no'
        if usePrefix == True:
            usePrefix = 'yes'
        return self.connectionObj.qps.sendCmdVerbose('$create channel ' + channelName + ' ' + channelGroup + ' ' + baseUnits + ' ' + usePrefix)

    def hideChannel(self, channelSpecifier):
        return self.connectionObj.qps.sendCmdVerbose('$hide channel ' + channelSpecifier)

    def showChannel(self, channelSpecifier):
        return self.connectionObj.qps.sendCmdVerbose('$show channel ' + channelSpecifier)

    def myChannels(self):
        return self.connectionObj.qps.sendCmdVerbose('$channels')

    def channels(self):
        return self.connectionObj.qps.sendCmdVerbose('$channels').splitlines()

    def stopStream(self):
        return self.connectionObj.qps.sendCmdVerbose('$stop stream')

    def hideAllDefaultChannels(self):
        self.hideChannel('3v3:voltage')
        self.hideChannel('5v:voltage')
        self.hideChannel('12v:voltage')
        self.hideChannel('3v3:current')
        self.hideChannel('5v:current')
        self.hideChannel('12v:current')
        self.hideChannel('3v3:power')
        self.hideChannel('5v:power')
        self.hideChannel('12v:power')
        self.hideChannel('tot:power')

    def addDataPoint(self, channelName, groupName, dataValue, dataPointTime=0):
        if dataPointTime == 0:
            dataPointTime = qpsNowStr()
        else:
            dataPointTime = toQpsTimeStamp(dataPointTime)
        self.connectionObj.qps.sendCmdVerbose('$log ' + channelName + ' ' + groupName + ' ' + str(dataPointTime) + ' ' + str(dataValue))