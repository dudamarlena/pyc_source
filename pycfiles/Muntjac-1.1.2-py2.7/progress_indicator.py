# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/progress_indicator.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a component that shows user state of a process."""
from muntjac.data.util.object_property import ObjectProperty
from muntjac.ui.abstract_field import AbstractField
from muntjac.data import property as prop

class ProgressIndicator(AbstractField, prop.IValueChangeListener, prop.IProperty, prop.IViewer):
    """C{ProgressIndicator} is component that shows user state of
    a process (like long computing or file upload)

    C{ProgressIndicator} has two mainmodes. One for indeterminate processes
    and other (default) for processes which progress can be measured.

    May view an other property that indicates progress 0...1

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    CLIENT_WIDGET = None
    CONTENT_TEXT = 0
    CONTENT_PREFORMATTED = 1

    def __init__(self, *args):
        """Creates an a new ProgressIndicator.

        @param args: tuple of the form
            - ()
            - (value)
            - (contentSource)
        """
        super(ProgressIndicator, self).__init__()
        self._indeterminate = False
        self._dataSource = None
        self._pollingInterval = 1000
        nargs = len(args)
        if nargs == 0:
            self.setPropertyDataSource(ObjectProperty(0.0, float))
        elif nargs == 1:
            if isinstance(args[0], prop.IProperty):
                contentSource, = args
                self.setPropertyDataSource(contentSource)
            else:
                value, = args
                self.setPropertyDataSource(ObjectProperty(value, float))
        else:
            raise ValueError, 'too many arguments'
        return

    def setReadOnly(self, readOnly):
        """Sets the component to read-only. Readonly is not used in
        ProgressIndicator.

        @param readOnly:
                   True to enable read-only mode, False to disable it.
        """
        if self._dataSource is None:
            raise ValueError, 'datasource must be set'
        self._dataSource.setReadOnly(readOnly)
        return

    def isReadOnly(self):
        """Is the component read-only ? Readonly is not used in
        ProgressIndicator - this returns allways false.

        @return: True if the component is in read only mode.
        """
        if self._dataSource is None:
            raise ValueError, 'datasource must be set'
        return self._dataSource.isReadOnly()

    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the Paint Event.
        @raise PaintException:
                    if the Paint Operation fails.
        """
        target.addAttribute('indeterminate', self._indeterminate)
        target.addAttribute('pollinginterval', self._pollingInterval)
        target.addAttribute('state', str(self.getValue()))

    def getValue(self):
        """Gets the value of the ProgressIndicator. Value of the
        ProgressIndicator is a float between 0 and 1.

        @return: the Value of the ProgressIndicator.
        @see: L{AbstractField.getValue}
        """
        if self._dataSource is None:
            raise ValueError, 'datasource must be set'
        return self._dataSource.getValue()

    def setValue(self, newValue, repaintIsNotNeeded=None):
        """Sets the value of the ProgressIndicator. Value of the
        ProgressIndicator is the float between 0 and 1.

        @param newValue: the new value of the ProgressIndicator.
        @see: L{AbstractField.setValue}
        """
        if repaintIsNotNeeded is None:
            if self._dataSource is None:
                raise ValueError, 'datasource must be set'
            self._dataSource.setValue(newValue)
        else:
            super(ProgressIndicator, self).setValue(newValue, repaintIsNotNeeded)
        return

    def __str__(self):
        """@see: L{AbstractField.__str__}"""
        if self._dataSource is None:
            raise ValueError, 'datasource must be set'
        return str(self._dataSource)

    def getType(self):
        """@see: L{AbstractField.getType}"""
        if self._dataSource is None:
            raise ValueError, 'datasource must be set'
        return self._dataSource.getType()

    def getPropertyDataSource(self):
        """Gets the viewing data-source property.

        @return: the datasource.
        @see: L{AbstractField.getPropertyDataSource}
        """
        return self._dataSource

    def setPropertyDataSource(self, newDataSource):
        """Sets the property as data-source for viewing.

        @param newDataSource:
                   the new data source.
        @see: L{AbstractField.setPropertyDataSource}
        """
        if self._dataSource is not None and issubclass(self._dataSource.__class__, prop.IValueChangeNotifier):
            self._dataSource.removeListener(self, prop.IValueChangeListener)
        self._dataSource = newDataSource
        if self._dataSource is not None and issubclass(self._dataSource.__class__, prop.IValueChangeNotifier):
            self._dataSource.addListener(self, prop.IValueChangeListener)
        return

    def getContentMode(self):
        """Gets the mode of ProgressIndicator.

        @return: true if in indeterminate mode.
        """
        return self._indeterminate

    def setIndeterminate(self, newValue):
        """Sets wheter or not the ProgressIndicator is indeterminate.

        @param newValue:
                   true to set to indeterminate mode.
        """
        self._indeterminate = newValue
        self.requestRepaint()

    def isIndeterminate(self):
        """Gets whether or not the ProgressIndicator is indeterminate.

        @return: true to set to indeterminate mode.
        """
        return self._indeterminate

    def setPollingInterval(self, newValue):
        """Sets the interval that component checks for progress.

        @param newValue:
                   the interval in milliseconds.
        """
        self._pollingInterval = newValue
        self.requestRepaint()

    def getPollingInterval(self):
        """Gets the interval that component checks for progress.

        @return: the interval in milliseconds.
        """
        return self._pollingInterval