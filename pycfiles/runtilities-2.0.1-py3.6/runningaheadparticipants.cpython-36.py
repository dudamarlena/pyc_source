# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\running\runningaheadparticipants.py
# Compiled at: 2020-02-26 14:46:23
# Size of source mod 2**32: 6167 bytes
import csv

class RunningAheadParticipant:
    __doc__ = '\n    Represents single RunningAHEAD registration\n\n    :param registration: registration record from RunningAHEAD export file\n    '
    filehdr = 'Registration Date,Event Category,Status,Bib,Last Name,First Name,Middle Name,Gender,Age,DOB,Email,Street 1,Street 2,City,State,ZIP Code,Country'.split(',')
    participantattr = 'registrationdate,category,status,bib,lname,fname,mname,gender,age,dob,email,street1,street2,city,state,zip,country'.split(',')
    participantxlate = dict(list(zip(filehdr, participantattr)))
    reprattr = 'fname,lname,dob,registrationdate'.split(',')

    def __init__(self, registration):
        for key in self.filehdr:
            if key in self.participantxlate:
                setattr(self, self.participantxlate[key], registration[key])

    def __repr__(self):
        reprval = '{}('.format(self.__class__)
        for attr in self.reprattr:
            if not attr[0:2] == '__':
                if attr == 'fields':
                    pass
                else:
                    reprval += '{}={},'.format(attr, getattr(self, attr))

        reprval = reprval[:-1]
        reprval += ')'
        return reprval


class RunningAheadParticipants:
    __doc__ = '\n    Collect participant data from RunningAHEAD event registration export\n    file.\n\n    Provide access functions to gain access to these registration records.\n\n    :param participantfile: participant filename, filehandle or string of file records\n    :param overlapfile: debug file to test for overlaps between records\n    '

    def __init__(self, participantfile, overlapfile=None):
        openedhere = False
        if isinstance(participantfile, str):
            participantfileh = open(participantfile, 'r', newline='')
            openedhere = True
        else:
            if isinstance(participantfile, file):
                participantfileh = participantfile
            else:
                if isinstance(participantfile, list):
                    participantfileh = participantfile
                else:
                    raise unsupportedFileType
        INCSV = csv.DictReader(participantfileh)
        self.registrations = {}
        for registration in INCSV:
            thisparticipant = RunningAheadParticipant(registration)
            lname = thisparticipant.lname
            fname = thisparticipant.fname
            dob = thisparticipant.dob
            thisrec = {'lname':lname, 
             'fname':fname,  'dob':dob,  'fullrec':registration,  'RunningAheadParticipant':thisparticipant}
            thisname = (thisparticipant.lname, thisparticipant.fname, thisparticipant.dob)
            self.registrations[thisname] = thisrec

    def allregistrations_iter(self):
        """
        generator function that yields full record for each registrations
        """
        for thisregistration in self.registrations:
            yield self.registrations[thisregistration]['RunningAheadParticipant']

    def activeregistrations_iter(self):
        """
        generator function that yields full record for each registrations
        """
        for thisregistration in self.registrations:
            if self.registrations[thisregistration]['RunningAheadParticipant'].status == 'Registered':
                yield self.registrations[thisregistration]['RunningAheadParticipant']