# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/yamltrak/__init__.py
# Compiled at: 2009-04-19 15:14:21
from __future__ import with_statement
import yaml
from mercurial import hg, commands as hgcommands, ui, util
from mercurial.error import RepoError
from os import path, makedirs
from time import time
import exceptions
NEW_ISSUE_TAG = 'YAMLTrak-new-issue'
SKELETON = {'title': 'A title for the issue', 
   'description': 'A detailed description of this issue.', 
   'estimate': 'A time estimate for completion', 
   'status': 'open, closed', 
   'group': 'unfiled', 
   'priority': 'high, normal, low', 
   'comment': 'The current comment on this issue.'}
SKELETON_NEW = {'title': 'A title for the issue', 
   'description': 'A detailed description of this issue.', 
   'estimate': 'A time estimate for completion'}
INDEX = {'skeleton': {'title': 'A title for the issue', 
                'description': 'A detailed description of this issue.', 
                'estimate': 'A time estimate for completion', 
                'status': 'open, closed', 
                'group': 'unfiled', 
                'priority': 'high, normal, low'}}

def issues(repositories=[], dbfolder='issues', status='open'):
    """Return the list of issues with the given statuses in dictionary form"""
    issues = {}
    for repository in repositories:
        try:
            issuedb = IssueDB(repository, dbfolder=dbfolder)
        except NoRepository:
            continue
        except NoIssueDB:
            continue

        issues[path.basename(issuedb.root)] = issuedb.issues(status)

    return issues


def issuediff(revx, revy):
    """Perform a simple one-level deep diff of a dictionary"""
    revxkeys = sorted(revx.keys())
    revykeys = sorted(revy.keys())
    x = 0
    y = 0
    added = {}
    removed = {}
    changed = {}
    while x < len(revxkeys) or y < len(revykeys):
        if x == len(revxkeys):
            added[revykeys[y]] = revy[revykeys[y]]
        elif y == len(revykeys):
            removed[revxkeys[x]] = revx[revxkeys[x]]
        elif revxkeys[x] < revykeys[y]:
            removed[revxkeys[x]] = revx[revxkeys[x]]
            x += 1
        elif revxkeys[x] > revykeys[y]:
            added[revykeys[y]] = revy[revykeys[y]]
            y += 1
        else:
            if revx[revxkeys[x]] != revy[revykeys[y]]:
                changed[revxkeys[x]] = (
                 revx[revxkeys[x]], revy[revykeys[y]])
            x += 1
            y += 1

    if not added and not removed and not changed:
        return False
    return (
     added, removed, changed)


def edit_issue(repository=None, dbfolder='issues', issue=None, id=None):
    """Modify the copy of the issue on disk, both in it's file, and the index."""
    try:
        issuedb = IssueDB(repository, dbfolder=dbfolder)
    except NoRepository:
        return
    except NoIssueDB:
        return

    return issuedb.edit(issue=issue, id=id)


def issue(repository=None, dbfolder='issues', id=None, detail=True):
    try:
        issuedb = IssueDB(repository, dbfolder=dbfolder)
    except NoRepository:
        return
    except NoIssueDB:
        return

    return issuedb.issue(id, detail=detail)


def relatedissues(repository=None, dbfolder='issues', filename=None, ids=None):
    try:
        issuedb = IssueDB(repository, dbfolder=dbfolder)
    except NoRepository:
        return []
    except NoIssueDB:
        return []

    return issuedb.related([filename], ids=ids)


def _hex_node(node_binary):
    """Convert a binary node string into a 40-digit hex string"""
    return ('').join(('%0.2x' % ord(letter) for letter in node_binary))


def new(repository, issue, dbfolder='issues', status='open'):
    """Add a new issue to the database"""
    try:
        issuedb = IssueDB(repository, dbfolder=dbfolder)
    except NoRepository:
        return
    except NoIssueDB:
        return

    return issuedb.new(issue=issue, status=status)


def dbinit(repository, dbfolder='issues'):
    try:
        issuedb = IssueDB(repository, dbfolder=dbfolder, dbinit=True)
    except NoRepository:
        return False
    except NoIssueDB:
        return False

    return True


def close(repository, id, dbfolder='issues'):
    """Sets the status of the issue on disk to close, both in it's file, and the index."""
    try:
        issuedb = IssueDB(repository, dbfolder=dbfolder)
    except NoRepository:
        return
    except NoIssueDB:
        return

    return issuedb.close(id)


def purge(repository, issueid, dbfolder='issues', status=['open']):
    try:
        issuedb = IssueDB(repository, dbfolder=dbfolder)
    except NoRepository:
        return
    except NoIssueDB:
        return

    return issuedb.purge(id)


def _group_estimate(issues, groupvalue, groupfield='group', groupdefault='unfiled', statuses=['open']):
    hours = 0
    minutes = 0
    for (issueid, issue) in issues.iteritems():
        if issue.get(groupfield, groupdefault) != groupvalue:
            continue
        valid_status = False
        for status in statuses:
            if status in issue.get('status', '').lower():
                valid_status = True
                break

        if not valid_status:
            continue
        estimate = issue.get('estimate', '')
        try:
            (timeamount, timescale) = estimate.split()[:2]
            timescale = timescale.lower().rstrip('s')
            if timescale == 'minute':
                minutes += int(timeamount)
            elif timescale == 'hour':
                hours += int(timeamount)
            elif timescale == 'day':
                hours += 8 * int(timeamount)
            elif timescale == 'week':
                hours += 40 * int(timeamount)
            else:
                continue
        except ValueError:
            continue
        except IndexError:
            continue
        except AttributeError:
            continue

    return hours + minutes // 60


def burndown(repository, groupvalue, dbfolder='issues'):
    try:
        issuedb = IssueDB(repository, dbfolder=dbfolder)
    except NoRepository:
        return []
    except NoIssueDB:
        return []

    checkpoints = issuedb.burndown(groupvalue, 'group', 'unfiled')
    return [ [timestamp * 1000, estimate] for (timestamp, estimate) in checkpoints ]


class NoRepository(Exception):
    """Exception raised when the folder given isn't inside a DVCS."""

    def __init__(self, repository):
        self.repository = repository

    def __str__(self):
        return 'No repository found at: %s' % self.repository


class NoIssueDB(Exception):
    """    Exception raised when the repository given doesn't contain an issue
    database.
    """

    def __init__(self, repository):
        self.repository = repository

    def __str__(self):
        return 'No issue database found in: %s' % self.repository


class IssueDB(object):
    """    An object that represents an issue database.  This provides a simpler means
    of accessing the YAMLTrak API than constantly passing in all of the
    parameters. In addition, it caches some of the work performed so that
    multiple operations run faster.
    """

    def __init__(self, folder, dbfolder='issues', indexfile='issues.yaml', dbinit=False):
        self.dbfolder = dbfolder
        self.__indexfile = indexfile
        self.__skeletonfile = 'skeleton'
        self.__skeleton_newfile = 'skeleton_new'
        self._skeleton = None
        self._skeleton_new = None
        self.ui = ui.ui()
        self.repo = self.__find_repo(folder)
        self.root = self.repo.root
        if not path.exists(self._indexfile) or not path.exists(self._skeletonfile):
            if dbinit and self._dbinit():
                return
            raise NoIssueDB(self.root)
        if not path.exists(self._skeleton_newfile):
            self.__skeleton_newfile = 'newticket'
        if not path.exists(self._skeleton_newfile):
            if dbinit:
                self.__skeleton_newfile = 'skeleton_new'
                if self._dbinit():
                    return
            raise NoIssueDB(self.root)
        return

    def __find_repo(self, folder):
        checkrepo = folder
        while checkrepo:
            if path.exists(path.join(checkrepo, '.hg')):
                try:
                    return hg.repository(self.ui, checkrepo)
                except (RepoError, util.Abort):
                    raise NoRepository(folder)

            (root, tail) = path.split(folder)
            if root == checkrepo:
                raise NoRepository(folder)
            checkrepo = root

    def _dbinit(self):
        """        Internal method for initializing the database.  It's not much use on
        the outside, since you can't get an IssueDB object with an
        uninitialized DB.
        """
        try:
            makedirs(path.join(self.root, self.dbfolder))
        except OSError:
            pass

        with open(self._skeletonfile, 'w') as (skeletonfile):
            skeletonfile.write(yaml.dump(SKELETON, default_flow_style=False))
        with open(self._skeleton_newfile, 'w') as (skeletonfile):
            skeletonfile.write(yaml.dump(SKELETON_NEW, default_flow_style=False))
        with open(self._indexfile, 'w') as (skeletonfile):
            skeletonfile.write(yaml.dump(INDEX, default_flow_style=False))
        hgcommands.add(self.ui, self.repo, self._skeletonfile)
        hgcommands.add(self.ui, self.repo, self._skeleton_newfile)
        hgcommands.add(self.ui, self.repo, self._indexfile)
        return True

    @property
    def _indexfile(self):
        """Helper that returns the full path of the issues index file."""
        return path.join(self.root, self.dbfolder, self.__indexfile)

    @property
    def _skeletonfile(self):
        """Helper that returns the full path of the issues skeleton file."""
        return path.join(self.root, self.dbfolder, self.__skeletonfile)

    @property
    def _skeleton_newfile(self):
        """Helper that returns the full path of the issues new skeleton file."""
        return path.join(self.root, self.dbfolder, self.__skeleton_newfile)

    def related(self, filenames=None, ids=None, detail=False, status='open'):
        """        Find the list of issue ids, among the ones that are provided, that are
        linked by changeset the the filenames provided.  If no filenames are
        provided, than this will choose the list of modified and uncommitted
        files.  If no ids are provided, this will pull the current list of
        issues with the status provided, which defaults to 'open'.
        """
        issues = []
        statuses = self.repo.status()
        (modified, added) = statuses[:2]
        uncommitted = modified + added
        if not filenames:
            filenames = modified
        if self._indexfile in filenames:
            filenames.remove(self._indexfile)
        allissues = self.issues(status=status)
        if not ids:
            ids = [ id for (id, issue) in allissues.iteritems() ]
        for id in ids:
            if path.join(self.dbfolder, id) in uncommitted:
                issues.append(id)
                continue
            try:
                filectxt = self.repo['tip'][path.join(self.dbfolder, id)]
            except LookupError:
                continue

            filerevid = filectxt.filerev()
            filectxt = filectxt.filectx(filerevid)
            try:
                while True:
                    for filename in filenames:
                        if filename in filectxt.files():
                            issues.append(id)
                            raise StopIteration

                    filerevid = filectxt.filerev() - 1
                    if filerevid < 0:
                        break
                    filectxt = filectxt.filectx(filerevid)

            except StopIteration:
                pass

        if detail:
            return dict(((id, allissues[id]) for id in issues))
        return issues

    def issues(self, status='open'):
        """        Return a list of issues in the database with the given status.
        """
        issuedb = {}
        try:
            with open(self._indexfile) as (indexfile):
                issuedb = dict((issue for issue in yaml.load(indexfile.read()).iteritems() if issue[0] != 'skeleton' if status in issue[1].get('status', '').lower()))
        except IOError:
            return issuedb

        for issue in issuedb.itervalues():
            try:
                timescale = issue['estimate'].split()[1].rstrip('s')
                if timescale.lower() == 'hour' or timescale.lower() == 'minute':
                    scale = 'short'
                elif timescale.lower() == 'day':
                    scale = 'medium'
                else:
                    scale = 'long'
            except IndexError:
                scale = 'unplanned'
            except AttributeError:
                scale = 'unplanned'

            try:
                priority = issue['priority'].lower()
                if 'high' in priority:
                    priority = 'high'
                elif 'normal' in priority:
                    priority = 'normal'
                elif 'low' in priority:
                    priority = 'low'
                else:
                    priority = 'high'
            except KeyError:
                priority = 'high'
            except IndexError:
                priority = 'high'
            except AttributeError:
                priority = 'high'

            issue['estimate'] = {'scale': scale, 'text': issue.get('estimate') is None and '' or issue['estimate']}
            issue['priority'] = priority

        return issuedb

    def issue(self, id, detail=True):
        """        Return detailed information about the issue requested.  If detail is
        set to True, then return a issue history as well, including changesets,
        associating files, the committing user, changeset node, and date.
        """
        issue = None
        try:
            with open(path.join(self.root, self.dbfolder, id)) as (issuefile):
                issue = [{'data': yaml.safe_load(issuefile.read())}]
            if not detail:
                return issue
            try:
                filectxt = self.repo['tip'][path.join(self.dbfolder, id)]
            except LookupError:
                return issue

            filerevid = filectxt.filerev()
            filectxt = filectxt.filectx(filerevid)
            oldrev = issue[0]['data']
            while True:
                try:
                    newrev = yaml.safe_load(filectxt.data())
                except yaml.loader.ScannerError:
                    filerevid = filectxt.filerev() - 1
                    if filerevid < 0:
                        break
                    filectxt = filectxt.filectx(filerevid)
                    continue

                issue[(-1)]['diff'] = issuediff(newrev, oldrev)
                issue.append({'data': newrev, 'user': filectxt.user(), 
                   'date': util.datestr(filectxt.date()), 
                   'files': filectxt.files(), 
                   'node': _hex_node(filectxt.node())})
                filerevid = filectxt.filerev() - 1
                if filerevid < 0:
                    break
                filectxt = filectxt.filectx(filerevid)
                oldrev = newrev

        except IOError:
            return

        return issue

    @property
    def skeleton(self):
        """        Return the issue database skeleton, with a list of fields and default
        values.
        """
        if self._skeleton:
            return self._skeleton
        self._skeleton = self.issue(self.__skeletonfile, detail=False)
        if self._skeleton:
            self._skeleton = self._skeleton[0]['data']
        return self._skeleton

    @property
    def skeleton_new(self):
        """        Return the issue database new issue skeleton, with a list of fields and
        default values.
        """
        if self._skeleton_new:
            return self._skeleton_new
        self._skeleton_new = self.issue(self.__skeleton_newfile, detail=False)
        if self._skeleton_new:
            self._skeleton_new = self._skeleton_new[0]['data']
        return self._skeleton_new

    def new(self, issue, status='open'):
        """        Add a new issue to the issue database.  Returns an issueid if
        successful.  All fields are filtered by those in the new issue
        skeleton.
        """
        newissue = {}
        for (field, default) in self.skeleton_new.iteritems():
            newissue[field] = issue.get(field, default)

        if 'status' not in newissue:
            newissue['status'] = status
        if 'comment' not in newissue:
            newissue['comment'] = 'Opening issue'
        hgcommands.tag(self.ui, self.repo, NEW_ISSUE_TAG, force=True, message='ISSUEPREP: %s' % newissue.get('title', 'No issue title'))
        context = self.repo['tip']
        issueid = _hex_node(context.node())
        try:
            with open(path.join(self.root, self.dbfolder, issueid), 'w') as (issuefile):
                issuefile.write(yaml.safe_dump(newissue, default_flow_style=False))
            hgcommands.add(self.ui, self.repo, path.join(self.root, self.dbfolder, issueid))
        except IOError:
            return false

        return self.edit(id=issueid, issue={}) and issueid

    def edit(self, id=None, issue=None):
        """        Save the issue with the given id.  The issue must already exist in the
        database.  Because we already filter using the skeleton, you can don't
        have to worry that any unwanted fields will show up.
        """
        if issue is None or not id:
            return
        oldissue = self.issue(id=id, detail=False)[0]['data']
        saveissue = {}
        for (field, default) in self.skeleton.iteritems():
            saveissue[field] = issue.get(field, oldissue.get(field, default))
            if saveissue[field] is None:
                saveissue[field] = ''

        try:
            with open(path.join(self.root, self.dbfolder, id), 'w') as (issuefile):
                issuefile.write(yaml.safe_dump(saveissue, default_flow_style=False))
        except IOError:
            return false

        return self._update_index(id, saveissue)

    def _update_index(self, id, issue):
        """        Take the given issue and update the index file, filtering based on the
        index skeleton. This should only be called with the full issue data,
        not just changed values, to ensure that we have a fully up to date
        index if the skeleton changes.
        """
        try:
            with open(self._indexfile, 'r') as (indexfile):
                index = yaml.load(indexfile.read())
        except IOError:
            return false

        if issue is None:
            del index[id]
        else:
            indexissue = {}
            for field in index['skeleton']:
                if field in issue:
                    indexissue[field] = issue[field]

            index[id] = indexissue
        with open(self._indexfile, 'w') as (indexfile):
            indexfile.write(yaml.safe_dump(index, default_flow_style=False))
        return True

    def close(self, id, comment=None):
        """        Set the status on the given issue to closed.  This is just a
        convenience method.
        """
        if comment is not None:
            return self.edit(issue={'status': 'closed', 'comment': comment}, id=id)
        return self.edit(issue={'status': 'closed'}, id=id)

    def purge(self, id):
        """        Purge an issue from the database.  This schedules the issue file for
        removal from the repository, and removes any info from the index.
        """
        if not id:
            return
        hgcommands.remove(self.ui, self.repo, path.join(self.root, self.dbfolder, id, force=True))
        return self._update_index(id, None)

    def burndown(self, groupvalue, groupfield='group', groupdefault='unfiled'):
        """        Return issue completing status for the given grouping.  This will
        return a list of datestamps, and the amount of work left to do at each
        timestamp for the lifetime of the group.
        """
        checkpoints = []
        try:
            with open(self._indexfile) as (indexfile):
                issues = yaml.load(indexfile.read())
        except IOError:
            return checkpoints

        found = False
        estimate = _group_estimate(issues, groupvalue, groupfield, groupdefault)
        if estimate > 0:
            found = True
        checkpoints.append([time(), estimate])
        try:
            filectxt = self.repo['tip'][path.join(self.dbfolder, 'issues.yaml')]
        except LookupError:
            return checkpoints

        filerevid = filectxt.filerev()
        filectxt = filectxt.filectx(filerevid)
        while True:
            try:
                issues = yaml.safe_load(filectxt.data())
            except yaml.loader.ScannerError:
                filerevid = filectxt.filerev() - 1
                if filerevid < 0:
                    break
                filectxt = filectxt.filectx(filerevid)
                continue

            estimate = _group_estimate(issues, groupvalue, groupfield, groupdefault)
            if estimate > 0:
                found = True
            elif found:
                return checkpoints
            checkpoints.append([filectxt.date()[0], estimate])
            filerevid = filectxt.filerev() - 1
            if filerevid < 0:
                break
            filectxt = filectxt.filectx(filerevid)

        return checkpoints