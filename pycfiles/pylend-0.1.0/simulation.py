# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/model/simulation.py
# Compiled at: 2016-03-18 06:01:10
__doc__ = '\nSimulation specification classes.\n\n@author: Gautham Ganapathy\n@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)\n@contact: gautham@lisphacker.org\n'
from lems.base.base import LEMSBase
from lems.base.errors import ModelError
from lems.base.map import Map

class Run(LEMSBase):
    """
    Stores the description of an object to be run according to an independent
    variable (usually time).
    """

    def __init__(self, component, variable, increment, total):
        """
        Constructor.

        See instance variable documentation for information on parameters.
        """
        self.component = component
        self.variable = variable
        self.increment = increment
        self.total = total

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Run component="{0}" variable="{1}" increment="{2}" total="{3}"/>').format(self.component, self.variable, self.increment, self.total)


class Record(LEMSBase):
    """
    Stores the parameters of a <Record> statement.
    """

    def __init__(self, quantity, scale=None, color=None, id=None):
        """
        Constructor.

        See instance variable documentation for information on parameters.
        """
        self.id = ''
        self.quantity = quantity
        self.scale = scale
        self.color = color
        self.id = id

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<Record quantity="{0}" scale="{1}" color="{2}" id="{3}"/>').format(self.quantity, self.scale, self.color, self.id)


class EventRecord(LEMSBase):
    """
    Stores the parameters of an <EventRecord> statement.
    """

    def __init__(self, quantity, eventPort):
        """
        Constructor.

        See instance variable documentation for information on parameters.
        """
        self.id = ''
        self.quantity = quantity
        self.eventPort = eventPort

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<EventRecord quantity="{0}" eventPort="{1}"/>').format(self.quantity, self.eventPort)


class DataOutput(LEMSBase):
    """
    Generic data output specification class.
    """

    def __init__(self):
        """
        Constuctor.
        """
        pass


class DataDisplay(DataOutput):
    """
    Stores specification for a data display.
    """

    def __init__(self, title, data_region):
        """
        Constuctor.

        See instance variable documentation for information on parameters.
        """
        DataOutput.__init__(self)
        self.title = title
        self.data_region = data_region
        self.time_scale = 1

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<DataDisplay title="{0}" dataRegion="{1}"/>').format(self.title, self.data_region)


class DataWriter(DataOutput):
    """
    Stores specification for a data writer.
    """

    def __init__(self, path, file_name):
        """
        Constuctor.

        See instance variable documentation for information on parameters.
        """
        DataOutput.__init__(self)
        self.path = path
        self.file_name = file_name

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<DataWriter path="{0}" fileName="{1}"/>').format(self.path, self.file_name)

    def __str__(self):
        return ('DataWriter, path: {0}, fileName: {1}').format(self.path, self.file_name)


class EventWriter(DataOutput):
    """
    Stores specification for an event writer.
    """

    def __init__(self, path, file_name, format):
        """
        Constuctor.

        See instance variable documentation for information on parameters.
        """
        DataOutput.__init__(self)
        self.path = path
        self.file_name = file_name
        self.format = format

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        return ('<EventWriter path="{0}" fileName="{1}" format="{2}"/>').format(self.path, self.file_name, self.format)

    def __str__(self):
        return ('EventWriter, path: {0}, fileName: {1}, format: {2}').format(self.path, self.file_name, self.format)


class Simulation(LEMSBase):
    """
    Stores the simulation-related attributes of a component-type.
    """

    def __init__(self):
        """
        Constructor.
        """
        self.runs = Map()
        self.records = Map()
        self.event_records = Map()
        self.data_displays = Map()
        self.data_writers = Map()
        self.event_writers = Map()

    def add_run(self, run):
        """
        Adds a runnable target component definition to the list of runnable
        components stored in this context.

        @param run: Run specification
        @type run: lems.model.simulation.Run
        """
        self.runs[run.component] = run

    def add_record(self, record):
        """
        Adds a record object to the list of record objects in this dynamics
        regime.

        @param record: Record object to be added.
        @type record: lems.model.simulation.Record
        """
        self.records[record.quantity] = record

    def add_event_record(self, event_record):
        """
        Adds an eventrecord object to the list of event_record objects in this dynamics
        regime.

        @param event_record: EventRecord object to be added.
        @type event_record: lems.model.simulation.EventRecord
        """
        self.event_records[event_record.quantity] = event_record

    def add_data_display(self, data_display):
        """
        Adds a data display to this simulation section.

        @param data_display: Data display to be added.
        @type data_display: lems.model.simulation.DataDisplay
        """
        self.data_displays[data_display.title] = data_display

    def add_data_writer(self, data_writer):
        """
        Adds a data writer to this simulation section.

        @param data_writer: Data writer to be added.
        @type data_writer: lems.model.simulation.DataWriter
        """
        self.data_writers[data_writer.path] = data_writer

    def add_event_writer(self, event_writer):
        """
        Adds an event writer to this simulation section.

        @param event_writer: event writer to be added.
        @type event_writer: lems.model.simulation.EventWriter
        """
        self.event_writers[event_writer.path] = event_writer

    def add(self, child):
        """
        Adds a typed child object to the simulation spec.

        @param child: Child object to be added.
        """
        if isinstance(child, Run):
            self.add_run(child)
        elif isinstance(child, Record):
            self.add_record(child)
        elif isinstance(child, EventRecord):
            self.add_event_record(child)
        elif isinstance(child, DataDisplay):
            self.add_data_display(child)
        elif isinstance(child, DataWriter):
            self.add_data_writer(child)
        elif isinstance(child, EventWriter):
            self.add_event_writer(child)
        else:
            raise ModelError('Unsupported child element')

    def toxml(self):
        """
        Exports this object into a LEMS XML object
        """
        chxmlstr = ''
        for run in self.runs:
            chxmlstr += run.toxml()

        for record in self.records:
            chxmlstr += record.toxml()

        for event_record in self.event_records:
            chxmlstr += event_record.toxml()

        for data_display in self.data_displays:
            chxmlstr += data_display.toxml()

        for data_writer in self.data_writers:
            chxmlstr += data_writer.toxml()

        for event_writer in self.event_writers:
            chxmlstr += event_writer.toxml()

        if chxmlstr:
            xmlstr = '<Simulation>' + chxmlstr + '</Simulation>'
        else:
            xmlstr = ''
        return xmlstr