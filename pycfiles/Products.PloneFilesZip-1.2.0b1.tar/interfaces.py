# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneBooking\interfaces.py
# Compiled at: 2008-11-19 15:29:18
__doc__ = '\n    PloneBooking: Interfaces\n'
__version__ = '$Revision: 1.5 $'
__author__ = ''
__docformat__ = 'restructuredtext'
from zope.interface import Interface

class IBooking(Interface):
    """ This interface proposes methods to access to Booked Objects, and get the
        booking period.
    """
    __module__ = __name__

    def getBookedObject(self, UID):
        """
        Parameters
            UID -> UID of attachment
            
        Return a Bookable object
        """
        pass

    def getBookedObjectRefs(self):
        """
        Return all booked objects referenced in Booking.
        """
        pass

    def getBookedObjectUIDs(self):
        """
        Return all Booked Objects uids referenced in Booking.
        """
        pass

    def isBookingObject(self, UID):
        """
        Parameters
            UID -> UID of bookable object
        
        Return true if the booking books the object with the given UID.
        """
        pass

    def isBookingObjects(self, uids_list):
        """
        Parameters
            uids_list -> uids_list of bookable object
        
        Return true if the booking books one of the object (from uid's list).
        """
        pass

    def hasBookedObject(self, UID, start_date, end_date):
        """
        Parameters
            UID -> uid of object
            start_date -> Date of booking's start
            end_date -> Date of booking's end
            
        Return true there are booked object during the given period.
        """
        pass

    def hasBookedObjects(self, uids_list, start_date, end_date):
        """
        Parameters 
            uids_list -> list of uids to test
            start_date -> Date of booking's start
            end_date -> Date of booking's end
        """
        pass


class IBookingCenter(Interface):
    """ This interface proposes methods to access contains of a Booking Center.
    """
    __module__ = __name__

    def getBookingCenter(self):
        """
        Return the Booking center itself
        """
        pass

    def getBookings(self, sort=''):
        """
        Return all Bookings contained in the BookingCenter.
        """
        pass

    def getBookingContainer(self):
        """
        Return the booking container.
        """
        pass

    def getBookableObjectContainer(self):
        """
        Return the bookable object container.
        """
        pass

    def getBookedObjects(self):
        """
        Return all booked object in container
        """
        pass


class IBookableObject(Interface):
    """ This interface proposes methods to know if an object is booked.
    """
    __module__ = __name__

    def isBooked(self):
        """
        """
        pass


class IBookingExporter(Interface):
    """
        Utility methods to format and manipulate exports fields
    """
    __module__ = __name__