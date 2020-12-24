# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/dbspecifierwizard.py
# Compiled at: 2003-09-14 19:12:38
"""(incomplete) wxPython wizard for DBSpecifier setup"""
from wxPython.wx import *
from wxPython.wizard import *
from wxoo import propertycontrol, events
from wxoo.resources import dbsetup_png
from pytable import dbdriver
from basictypes import latebind
from wxoo.debug import *
log = Log('pytable.specwiz')
log.setLevel(DEBUG)
DEFAULT_BITMAP = dbsetup_png.getBitmap()
CHOOSE_DRIVER_MESSAGE = 'The system needs to know which database driver module\nit should use to set up this database connection.  The\ncurrently-registered database drivers are displayed\nbelow.  Choose the driver which corresponds to the\ndatabase system in which your database is (to be)\nstored.\n'
CONNECTION_SETUP_MESSAGE = 'The system needs to know how to connect to the\ndatabase using your driver.  Some drivers do not\nrequire username, password, or host designations,\nin these cases (normally file-based databases) you\nshould simply specify the filename as the "data\nsource".\n'

class DBSpecifierWizard(wxWizard):
    """Wizard to specifying a database connection"""
    __module__ = __name__

    def __init__(self, parent, id=-1, title='Database Connection Wizard', bitmap=None, pos=wxDefaultPosition, value=None):
        """Initialize the specifier wizard

                bitmap -- wxBitmap to use, otherwise uses the default
                        from wxoo.resources.dbsetup_png
                value -- a dbspecifier instance to edit, or None, in
                        which case we create a new specifier.
                """
        if bitmap is None:
            bitmap = DEFAULT_BITMAP
        wxWizard.__init__(self, parent, id, title, bitmap, pos)
        if value is None:
            from pytable import dbspecifier
            value = dbspecifier.DBSpecifier()
        self.value = value
        self.first = ChooseDriverPage(self, value=self.value)
        self.second = ConnectionSetupPage(self, value=self.value)
        self.third = DatabaseSetupPage(self, value=self.value)
        self.first.SetNext(self.second)
        self.second.SetNext(self.third)
        self.third.SetPrev(self.second)
        self.second.SetPrev(self.first)
        self.FitToPage(self.first)
        return


class BasePage(wxPyWizardPage):
    """Base page for the various wizard pages"""
    __module__ = __name__
    message = ''
    next = None
    previous = None

    def __init__(self, parent, bitmap=None, resource=NULL, value=None, title='Choose Database Driver'):
        """Initialize the BasePage object"""
        wxPyWizardPage.__init__(self, parent)
        self.value = value
        self.title = title
        self.CreateControls()

    def CreateControls(self, style=0):
        """Create the controls for the Window"""
        pass

    def SetNext(self, nextWindow):
        """Set the next window in the chain of Windows"""
        log.debug('SetNext %s %s', self, nextWindow)
        self.next = nextWindow

    def SetPrev(self, previousWindow):
        """Set the previous window in the chain of Windows"""
        log.debug('SetPrev %s %s', self, previousWindow)
        self.previous = previousWindow

    def GetNext(self):
        """Retrieve the next window in the series"""
        log.debug('GetNext %s %s', self, self.next)
        return self.next

    def GetPrev(self):
        """Retrieve the previous window in the series"""
        log.debug('GetPrev %s %s', self, self.previous)
        return self.previous

    def __repr__(self):
        return '<%s@%s>' % (self.__class__.__name__, self.this)


class ChooseDriverPage(BasePage):
    """Choice of database driver"""
    __module__ = __name__
    message = CHOOSE_DRIVER_MESSAGE

    def CreateControls(self, style=0):
        """Create the controls for choosing the dbdriver"""
        sizer = wxBoxSizer(wxVERTICAL)
        title = wxStaticText(self, -1, self.title)
        title.SetFont(wxFont(18, wxSWISS, wxNORMAL, wxBOLD))
        sizer.Add(title, 0, wxALIGN_CENTRE | wxALL, 5)
        sizer.Add(wxStaticLine(self, -1), 0, wxEXPAND | wxALL, 5)
        sizer.Add(wxStaticText(self, -1, self.message))
        self.primary = propertycontrol.PropertyControl(self, value=self.value, descriptor=type(self.value).drivername, autoCommit=1, size=(100,
                                                                                                                                           50))
        sizer.Add(self.primary, 1, wxALL | wxEXPAND, 5)
        self.driverDescription = wxStaticText(self, -1, '\n\n\n\n\n\n\n\n\n\n')
        sizer.Add(self.driverDescription, 0, wxALL, 5)
        events.EVT_PROPERTYCHANGED(self, function=self.OnChoiceChanged)
        self.SetSizer(sizer)
        self.SetAutoLayout(true)
        self.OnChoiceChanged()

    def OnChoiceChanged(self, event=None):
        """Update description on property change"""
        className = self.value.drivername.value()
        if className:
            try:
                driver = latebind.bind(className)
            except Exception, err:
                log.warn('Exception importing driver %s: %s', className, err)
            else:
                if hasattr(driver, 'userDescription'):
                    self.driverDescription.SetLabel(driver.userDescription)

    def GetNext(self):
        """Get the next page in this wizard

                This will be looking to retrieve a driver-specific
                page for setting up the driver-specific specifier
                details which are the database-related, as distinct
                from user and password related.
                """
        currentValue = self.value.drivername
        className = currentValue.value()
        log.debug('Driver name: %s', className)
        try:
            driver = latebind.bind(className)
            self.value.driver = driver
            self.value.drivername = currentValue
            log.info('Resolved driver: %s', driver)
        except Exception, err:
            log.warn('Exception importing driver %s: %s', className, err)
            return self

        self.next.SetDriver(driver)
        return self.next


class DatabaseSetupPage(BasePage):
    """Setup of database-specific specifier properties

        Basically, within a particular driver, this
        page will allow you to specify the particular
        database to which to connect, and potentially how
        to perform that connection (for instance read-only).
        """
    __module__ = __name__


class ConnectionSetupPage(BasePage):
    """Setup of connection-specific specifier properties

        dsn, username and password in particular
        """
    __module__ = __name__
    message = CONNECTION_SETUP_MESSAGE

    def CreateControls(self, style=0):
        """Create the controls for choosing the dbdriver"""
        self.controls = {}
        sizer = wxBoxSizer(wxVERTICAL)
        allowedProperties = dbdriver.DBDriver.connectionProperties
        title = wxStaticText(self, -1, self.title)
        title.SetFont(wxFont(18, wxSWISS, wxNORMAL, wxBOLD))
        sizer.Add(title, 0, wxALIGN_CENTRE | wxALL, 5)
        sizer.Add(wxStaticLine(self, -1), 0, wxEXPAND | wxALL, 5)
        sizer.Add(wxStaticText(self, -1, self.message))
        for property in allowedProperties:
            if property not in ('database', 'drivername'):
                control = propertycontrol.PropertyControl(self, value=self.value, descriptor=getattr(type(self.value), property), autoCommit=1, size=(100,
                                                                                                                                                      50))
                self.controls[property] = control
                sizer.Add(control, 1, wxLEFT | wxRIGHT | wxEXPAND, 5)

        events.EVT_PROPERTYCHANGED(self, function=self.OnChoiceChanged)
        self.SetSizer(sizer)
        self.SetAutoLayout(true)
        self.OnChoiceChanged()

    def SetDriver(self, driver):
        allowed = driver.connectionProperties
        for (key, value) in self.controls.items():
            if key in allowed:
                value.Enable(True)
            else:
                value.Enable(False)

    def OnChoiceChanged(self, event=None):
        """Update description on property change"""
        pass


if __name__ == '__main__':
    from wxoo import wxcontrolcontainer

    class TestFrame(wxcontrolcontainer.HolderFrame):
        __module__ = __name__

        def OnStatusUpdate(self, event):
            """Deal with an update to status text from a child"""
            self.GetStatusBar().SetStatusText(event.message, event.typeSpecifier or 0)


    class DemoApp(wxApp):
        __module__ = __name__
        ID_wiz = wxNewId()

        def OnChange(self, event):
            print 'changed', event.object

        def OnRunWiz(self, event):
            dialog = DBSpecifierWizard(self.GetTopWindow())
            try:
                if dialog.RunWizard(dialog.first):
                    print dialog.value.__dict__
            finally:
                dialog.Destroy()
            self.GetTopWindow().Close()

        def OnInit(self):
            frame = TestFrame(NULL, -1, 'Testing')
            ID = wxNewId()
            wxButton(frame, ID, 'Run spec wizard')
            EVT_BUTTON(frame, ID, self.OnRunWiz)
            frame.CreateStatusBar()
            events.EVT_STATUSCHANGED(frame, -1, frame.OnStatusUpdate)
            frame.Show(true)
            self.SetTopWindow(frame)
            return true


    app = DemoApp(0)
    app.MainLoop()