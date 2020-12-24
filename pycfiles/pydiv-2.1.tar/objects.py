# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/objects.py
# Compiled at: 2016-11-27 06:27:17
__doc__ = '\nInternal Ditz objects.\n'
import os, re, yaml, hashlib, random, six
from cerberus import Validator
from datetime import datetime, timedelta
from functools import total_ordering
from .util import make_directory, check_value, to_unicode, default_name, default_email, DitzError
from .flags import STATUS, RELSTATUS, RELEASED, UNRELEASED, BUGFIX, FEATURE, TASK, DISPOSITION, UNSTARTED, TYPE, SORT, CLOSED
from .files import read_object_file, write_yaml_file, write_config
from .config import config
from . import schemas
re_start = re.compile('to in.progress')
re_stop = re.compile('(from in.progress|closed with disposition)')

class DitzObject(yaml.YAMLObject):
    """
    Base class of a Ditz object appearing in a YAML file.

    Attributes:
        ditz_tag (str): Base YAML tag prefix.
        yaml_tag (str): YAML tag written to file.
        filename (str): YAML filename to read/write.
        attributes (list): List of recognized attributes.
        defaults (list): Defaults for new attributes.
        log_events (list): List of events.
    """
    yaml_loader = yaml.SafeLoader
    ditz_tag = '!ditz.rubyforge.org,2008-03-06'
    yaml_tag = None
    filename = None
    validator = None
    attributes = []
    defaults = {}

    def write(self, dirname='.'):
        """
        Write object to its YAML file.

        Args:
            dirname (str, optional): Directory to write file into.
        """
        make_directory(dirname)
        path = os.path.join(dirname, self.filename)
        write_yaml_file(path, self)

    def event(self, username, text, comment=None, timestamp=None):
        """
        Add an event to the object's ``log_events`` list.

        Args:
            username (str): User name.
            text (str): Event description.
            comment (str, optional): User comment.
            timestamp (datetime, optional): Time of the event.
        """
        time = timestamp or datetime.now()
        text = to_unicode(text)
        comment = to_unicode(comment) or ''
        self.log_events.append([time, username, text, comment])

    def update(self):
        """
        Update the object to the latest version.

        This adds defaults for attributes added since the original set.
        It's intended to update cached objects after reading.
        """
        for attr, default in self.defaults.items():
            if not hasattr(self, attr):
                setattr(self, attr, default)

    def normalize(self):
        """
        Normalize object to a valid Ditz object.
        """
        v = self.validator
        if not v:
            return
        data = to_dict(self)
        if v.validate(data):
            data = v.normalized(data)
            set_data(self, data)
        else:
            lines = [
             'invalid format:'] + list(errorlines(v.errors))
            text = ('\n   ').join(lines)
            if self.filename:
                text = self.filename + ': ' + text
            raise DitzError(text)


class Project(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/project'
    filename = 'project.yaml'
    validator = Validator(schemas.project)
    attributes = [
     'name', 'version', 'components', 'releases']
    name = ''
    components = []
    releases = []

    def __init__(self, name, version=0.5):
        self.name = to_unicode(name)
        self.version = version
        self.components = [Component(name)]
        self.releases = []


class Release(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/release'
    validator = Validator(schemas.release)
    attributes = [
     'name', 'status', 'release_time', 'log_events']
    name = None
    release_time = None
    log_events = []

    def __init__(self, name, status=UNRELEASED, release_time=None):
        self.name = to_unicode(name)
        self.status = status
        self.release_time = release_time
        self.log_events = []
        self.set_status(status)

    def set_status(self, status):
        check_value('status', status, RELSTATUS)
        self.status = status

    @property
    def released(self):
        """Whether release has actually been released."""
        return self.status == RELEASED

    @property
    def description(self):
        if not self.released:
            tag = 'unreleased'
        else:
            tag = 'released %s' % self.release_time.strftime('%Y-%m-%d')
        return '%s (%s)' % (self.name, tag)

    def __repr__(self):
        return '<Release: %s>' % self.name


class Component(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/component'
    attributes = ['name']
    validator = Validator(schemas.component)
    name = ''

    def __init__(self, name):
        self.name = to_unicode(name)

    def __repr__(self):
        return '<Component: %s>' % self.name


@total_ordering
class Issue(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/issue'
    template = 'issue-%s.yaml'
    validator = Validator(schemas.issue)
    attributes = [
     'title', 'desc', 'type', 'component', 'release',
     'reporter', 'claimer', 'status', 'disposition',
     'creation_time', 'references', 'id', 'log_events']
    references = []
    log_events = []
    defaults = {'claimer': None}

    def __init__(self, title, desc='', type=BUGFIX, status=UNSTARTED, disposition=None, creation_time=None, reporter=''):
        self.title = to_unicode(title.strip())
        self.desc = to_unicode(desc.strip())
        self.component = None
        self.release = None
        self.claimer = None
        self.reporter = to_unicode(reporter)
        self.set_type(type)
        self.set_status(status)
        self.set_disposition(disposition)
        self.creation_time = creation_time or datetime.now()
        self.id = self.make_id()
        self.references = []
        self.log_events = []
        return

    @property
    def name(self):
        """Name of the issue.  This is the same as its title."""
        return self.title

    @property
    def longname(self):
        """Name of the issue, with (bug) or (feature) appended."""
        if self.bugfix:
            return self.title + ' (bug)'
        else:
            if self.feature:
                return self.title + ' (feature)'
            return self.title

    @property
    def closed(self):
        """Whether the issue is closed."""
        return self.status == CLOSED

    @property
    def bugfix(self):
        """Whether the issue is a bugfix."""
        return self.type == BUGFIX

    @property
    def feature(self):
        """Whether the issue is a feature."""
        return self.type == FEATURE

    @property
    def task(self):
        """Whether the issue is a task."""
        return self.type == TASK

    @property
    def filename(self):
        return self.template % self.id

    @property
    def progress_time(self):
        """Total seconds the issue's state has been in-progress."""
        total = timedelta()
        start = None
        for time, _, event, _ in self.log_events:
            if re_start.search(event):
                start = time
            elif re_stop.search(event) and start is not None:
                total += time - start
                start = None

        if start is not None:
            total += datetime.now() - start
        return total.total_seconds()

    @property
    def modified_time(self):
        """Time the issue was last modified."""
        if self.log_events:
            return self.log_events[(-1)][0]
        else:
            return self.creation_time

    def set_type(self, type):
        check_value('type', type, TYPE)
        self.type = type

    def set_status(self, status):
        check_value('status', status, STATUS)
        self.status = status

    def set_disposition(self, disposition):
        if disposition:
            check_value('disposition', disposition, DISPOSITION)
        self.disposition = disposition

    def add_reference(self, reference):
        reference = to_unicode(reference)
        self.references.append(reference)
        return len(self.references)

    def grep(self, regexp):
        for attr in ('title', 'desc', 'reporter'):
            if regexp.search(getattr(self, attr)):
                return True

        for ref in self.references:
            if regexp.search(ref):
                return True

        for event in self.log_events:
            if regexp.search(event[3]):
                return True

        return False

    def make_id(self):
        data = [
         self.creation_time, random.random(),
         self.reporter, self.title, self.desc]
        string = ('\n').join([ six.text_type(item) for item in data ])
        return hashlib.sha1(string.encode('utf-8')).hexdigest()

    def __eq__(self, other):
        if hasattr(other, 'id'):
            return self.id == other.id
        return False

    def __lt__(self, other):
        this = (
         SORT[self.status], self.modified_time)
        that = (SORT[other.status], other.modified_time)
        return this < that

    def __hash__(self):
        return int(self.id, 16)

    def __repr__(self):
        return '<Issue: %s>' % self.id


class Config(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/config'
    filename = '.ditz-config'
    attributes = ['name', 'email', 'issue_dir']

    def __init__(self, name, email, issue_dir='issues'):
        self.name = to_unicode(name)
        self.email = to_unicode(email)
        self.issue_dir = issue_dir

    @property
    def username(self):
        if self.email:
            return '%s <%s>' % (self.name, self.email)
        else:
            return self.name

    def validate(self):
        if not hasattr(self, 'issue_dir'):
            raise DitzError("'issue_dir' not defined")

    def __repr__(self):
        return '<Config: %s>' % self.name


def find_config(basedir='.', error=False, search=True):
    """
    Find Ditz configuration in (or possibly above) a base directory.

    Return the directory and corresponding Config object.
    """
    basedir = os.path.realpath(basedir)
    curdir = basedir
    issuedirs = config.get('config', 'issuedirs').split()
    while True:
        path = os.path.join(curdir, Config.filename)
        if os.path.exists(path):
            return (curdir, read_object_file(path))
        for dirname in issuedirs:
            path = os.path.join(curdir, dirname, Project.filename)
            if os.path.exists(path):
                name = default_name()
                email = default_email()
                conf = Config(name, email, dirname)
                write_config(conf)
                return (
                 curdir, conf)

        pardir = os.path.split(curdir)[0]
        if pardir == curdir or not search:
            if error:
                where = 'in or above' if search else 'in'
                raise DitzError("can't find '%s' %s '%s'" % (
                 Config.filename, where, basedir))
            else:
                return (None, None)
        curdir = pardir

    return


def to_dict(obj):
    """Convert object to a dict, recursively."""
    if hasattr(obj, '__dict__'):
        obj = {attr:to_dict(value) for attr, value in obj.__dict__.items()}
    elif isinstance(obj, list):
        obj = [ to_dict(item) for item in obj ]
    return obj


def set_data(obj, data):
    """Set object attributes from data, recursively."""
    if hasattr(obj, '__dict__'):
        for attr, value in data.items():
            subobj = getattr(obj, attr, None)
            if not subobj or not set_data(subobj, value):
                obj.__dict__[attr] = value

        return True
    if isinstance(obj, list):
        for idx, value in enumerate(data):
            subobj = obj[idx]
            if not set_data(subobj, value):
                obj[idx] = value

        return True
    return False


def errorlines(errdict, sep='.', parent=None):
    """Yield error lines from a validator error dictionary."""
    for elt, errors in sorted(errdict.items()):
        if parent:
            path = parent + sep + str(elt)
        else:
            path = str(elt)
        for value in errors:
            if isinstance(value, dict):
                for line in errorlines(value, sep, path):
                    yield line

            else:
                yield '%s: %s' % (path, value)