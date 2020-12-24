# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIGPC4\Desktop\atamsPackage\build\lib\atams\schedulevalidity.py
# Compiled at: 2018-09-26 06:54:46
"""
---------------------------------------------------

        File name: schedulevalidity.py

---------------------------------------------------
        Description:   Validates schedule file
                                   Returns error if BeamID is not matched or no satellites found
                                   
---------------------------------------------------     
        Package     : atams
        Version     : 0.1
        Language    : Python
        Authors         : 

Revision History:

Version         Created                         Modification
-----------------------------------------------------------------

"""
from structures import *
import time, xml.etree.ElementTree as ET, os

def getkey(elem):
    return elem.get('PrePassTime')


def ScheduleValidity(ScheduleFilepath, Beam, EpochTime, new_sch):
    iSatelliteCount = 0
    strAction = ''
    try:
        if new_sch:
            ScheduleFilepath = os.path.join(ScheduleFilepath, 'new_schedule')
        else:
            ScheduleFilepath = os.path.join(ScheduleFilepath, 'schedule')
        tree = ET.parse(ScheduleFilepath)
    except:
        Output = 'Invalid schedule file'
        Valid = False
        return [Valid, Output, strAction, 0, 0, 0]

    root = tree.getroot()
    if root.tag == 'Schedule':
        StrPeriod = root.attrib['Period']
        period = StrPeriod.split(':')
        hours = int(period[0])
        mins = int(period[1])
        secs = int(period[2].split('.')[0])
        iPeriod = hours * 3600 + mins * 60 + secs
        strAction = root.attrib['Action']
        pattern = '%m/%d/%Y %H:%M:%S'
        strBeam, strRegion, strHandoverTime, strPrePassTime, strStartTime, strEndTime = ([], [], [], [], [], [])
        dwHandovertime, dwPrepassTime, dwStartTime, dwEndTime = ([], [], [], [])
        strSatelliteID = []
        try:
            for node in tree.iter('Track'):
                for element in node.iter('Handover'):
                    strBeam.append(element.attrib.get('Beam'))
                    strRegion.append(element.attrib.get('Region'))
                    strHandoverTime.append(element.attrib.get('Time'))
                    dwHandovertime.append(int(time.mktime(time.strptime(strHandoverTime[iSatelliteCount], pattern))))
                    if strBeam[iSatelliteCount] == Beam:
                        strPrePassTime.append(node.attrib.get('PrePassTime'))
                        dwPrepassTime.append(int(time.mktime(time.strptime(strPrePassTime[iSatelliteCount], pattern))))
                        strStartTime.append(node.attrib.get('StartTime'))
                        dwStartTime.append(int(time.mktime(time.strptime(strStartTime[iSatelliteCount], pattern))))
                        strEndTime.append(node.attrib.get('EndTime'))
                        dwEndTime.append(int(time.mktime(time.strptime(strEndTime[iSatelliteCount], pattern))))
                        strSatelliteID.append(node.attrib.get('Satellite'))
                        iSatelliteCount = iSatelliteCount + 1
                        Valid = True
                    else:
                        Output = 'Beam Id is not Matched'
                        Valid = False

        except:
            Output = 'No tracks found'
            Valid = False
            return [Valid, Output, strAction, 0, 0, 0]

    else:
        Output = 'schedule tag not found'
        Valid = False
        return [Valid, Output, strAction, 0, 0, 0]
    if iSatelliteCount < 2:
        Output = 'schedule file has no satellites for the Beam %s' % Beam
        Valid = False
        return [
         Valid, Output, strAction, 0, 0, 0]
    else:
        dwPrepassTime.sort()
        dwHandovertime.sort()
        dwStartTime.sort()
        dwEndTime.sort()
        Output = 'schedule file validated; %d Satellites Found' % iSatelliteCount
        Valid = True
        return [Valid, Output, strAction, dwStartTime[0], dwHandovertime[0], dwEndTime[1]]