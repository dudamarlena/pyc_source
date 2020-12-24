# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jc01/miniconda2/envs/psychopyenv/lib/python2.7/site-packages/expcontrol/base.py
# Compiled at: 2016-05-14 10:14:13
"""base expcontrol functionality."""
import datetime, functools, numpy
from . import event

def addcustomdict(funhand):
    """
    Decorator for save functionality (currently in Experiment class).
    """

    @functools.wraps(funhand)
    def wrapper(*args, **kwargs):
        if 'customdict' in kwargs and kwargs['customdict']:
            args = list(args)
            args[1] = args[1].copy()
            for extrafield, extraval in kwargs['customdict'].iteritems():
                args[1][extrafield] = extraval

        return funhand(*args, **kwargs)

    return wrapper


class Controller(object):
    """
    Control experiment timing, stimulus delivery and response collection.
    """

    def __init__(self, window=None, response=None, clock=None, eyetracker=None):
        """
        Initialise a controller instance. For example inputs, see
        expcontrol.psychopydep.window, KeyboardResponse and clock."""
        self.window = window
        self.response = response
        self.clock = clock
        self.eyetracker = eyetracker

    def __call__(self):
        """
        Check for responses and flip the screen. If this is called often
        enough you will achieve sync with the screen refresh (assuming that
        your window method holds until the refresh)."""
        frametime = self.window()
        response, resptime = self.response()
        return (response, resptime, frametime)


class Experiment(object):
    """
    Class for running a set of trials in some experiment."""

    def __init__(self, conditions=[], preevent=None, postevent=None, subject=None, context=None):
        """
        Initialise an Experiment instance.

        Keyword arguments:
        conditions -- dict or list of Event-derived instances (including
            EventSeq).
        preevent -- An event-derived instance that is called before the
            main trial sequence with an endtime of numpy.inf. This instance
            should practically always be initialised with
            skiponresponse=True.
        postevent -- An event-derived instance that is called after the
            main trial sequence. Otherwise similar to preevent above.
        subject -- str for log file. Prompted if undefined.
        context -- str for log file. Prompted if undefined.
        """
        self.conditions = conditions
        self.preevent = preevent
        self.postevent = postevent
        if not subject:
            subject = raw_input('subject: ')
        self.subject = subject
        if not context:
            context = raw_input('context: ')
        self.context = context
        self.session = numpy.datetime64(datetime.datetime.now())

    def __call__(self, controller, conditionkeys, seqclass=event.EventSeqAbsTime):
        """
        Run a sequence of trials of the experiment, and return panda
        dataframes corresponding to the main trial sequence and the output
        of any pre/post events.

        Arguments:
        controller -- a Controller instance
        conditionkeys -- a list of keys or indices into self.conditions,
            which defines the sequence of conditions over the run.
        seqclass -- class to use for creating the trial sequence. Use
            EventSeqRelTime if absolute timing is not possible (e.g.,
            self-timed events, synching to pulses).
        """
        sequence = seqclass([ self.conditions[key] for key in conditionkeys ], name=None)
        preevlog = None
        if self.preevent:
            preevlog, preresplog = self.preevent(controller, numpy.inf)
            preevlog['subject'] = self.subject
            preevlog['session'] = self.session
            preevlog['context'] = self.context
        controller.clock.start()
        eventlog, resplog = sequence(controller)
        postevlog = None
        if self.postevent:
            postevlog, postresplog = self.postevent(controller, numpy.inf)
            postevlog['subject'] = self.subject
            postevlog['session'] = self.session
            postevlog['context'] = self.context
        eventlog['subject'] = self.subject
        eventlog['session'] = self.session
        eventlog['context'] = self.context
        return (eventlog, resplog, preevlog, preresplog, postevlog, postresplog)

    @addcustomdict
    def to_sql(self, res, path, customdict=None):
        """
        Save data to SQL database with self.context as key. If self.context
        exists, we append.
        """
        import sqlalchemy
        engine = sqlalchemy.create_engine('sqlite:///' + path)
        res.to_sql(self.context, engine, if_exists='append')

    @addcustomdict
    def to_hdf(self, res, path, customdict=None):
        """
        Save data to HDF database with self.context as key. If the self.context
        field already exists, we append.
        """
        res.to_hdf(path, self.context, append=True)