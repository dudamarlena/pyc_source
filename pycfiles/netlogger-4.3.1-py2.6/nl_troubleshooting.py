# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/pegasus/nl_troubleshooting.py
# Compiled at: 2009-12-08 17:43:30
""" A set of functions to extract troubleshooting information about Pegasus 
jobs from a database."""
from netlogger.analysis.loader import *

class directory:

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return self.path

    def asXML(self):
        return '<path' > +self.path + '</path>'


class pegasusFile:

    def __init__(self, path='', contents=''):
        self.path = path
        if contents == '':
            self.contents = self.getContentsFromDisk()
        else:
            self.contents = contents

    def __repr__(self):
        return self.path

    def asXML(self):
        return '<path' > +self.path + '</path>'

    def getContents(self):
        return self.contents

    def getContentsFromDisk():
        try:
            self.contents = file(self.path).read()
        except:
            self.contents = ''


class task:

    def __init__(self, run, taskid=0, taskclass='', workflow='', description='', transform='', status=0, duration=0.0):
        self.run = run
        self.taskid = taskid
        self.taskclass = taskclass
        self.description = description
        self.transform = transform
        self.status = status
        self.duration = duration
        self.parents = []
        self.children = []
        self.fillInValues()

    def fillInValues(self):
        curs = getConnection(self.run)
        curs.execute('select name, value from ident where e_id = %d' % self.taskid)
        res = curs.fetchall()
        for item in res:
            if item[0] == 'workflow':
                self.workflow = item[1]
            if item[0] == 'comp':
                self.description = item[1]

        curs.execute('select name, value from attr where e_id = %d' % self.taskid)
        res = curs.fetchall()
        for item in res:
            if item[0] == 'status':
                self.status = item[1]
            if item[0] == 'type':
                self.transform = item[1]
            if item[0] == 'duration':
                self.duration = item[1]

    def getParents(self):
        c = getConnection(self.run)
        c.execute("select event.id from event join ident where event.name = 'condor.dag.edge' and ident.value = '%s' and event.id = ident.e_id and ident.name = 'comp.child';" % self.description)
        ids = [ res[0] for res in c.fetchall() ]
        tl = []
        for i in ids:
            c.execute("select value from ident where e_id = %s and name = 'comp.parent'" % i)
            res = c.fetchall()
            desc = res[0][0]
            c.execute("select event.id from event join ident where event.name = 'pegasus.invocation' and ident.name = 'comp' and ident.value = '%s' and event.id = ident.e_id;" % desc)
            eventid = c.fetchall()[0]
            tl.append(task(self.run, taskid=eventid, description=desc))

        return tl

    def getChildren(self):
        c = getConnection(self.run)
        c.execute("select event.id from event join ident where event.name = 'condor.dag.edge' and ident.value = '%s' and event.id = ident.e_id and ident.name = 'comp.parent';" % self.description)
        ids = [ res[0] for res in c.fetchall() ]
        tl = []
        for i in ids:
            c.execute("select value from ident where e_id = %s and name = 'comp.child'" % i)
            res = c.fetchall()
            desc = res[0]
            c.execute("select event.id from event join ident where event.name = 'pegasus.invocation' and ident.name = 'comp' and ident.value = '%s' and event.id = ident.e_id;" % desc)
            eventid = c.fetchall()[0]
            tl.append(task(self.run, taskid=eventid, description=desc))

        return tl


def getFailedTasks(run):
    curs = getConnection(run)
    curs.execute("select e_id from attr where name='status' and attr.value != 0")
    tl = curs.fetchall()
    tasks = [ task(run, item[0]) for item in tl ]
    return tasks


class mapping:

    def __init__(self, jobid, xform='', jobclass=''):
        self.jobid = jobid
        self.xform = xform
        self.jobclass = jobclass
        self.tasks = []


def getMappings(run):
    curs = getConnection(run)
    curs.execute("select id from event where name = 'pegasus.job.map'")
    res = curs.fetchall()
    eids = [ item[0] for item in res ]
    mappings = []
    for eid in eids:
        curs.execute('select * from ident where e_id = %s' % eid)
        res = curs.fetchall()
        for r in res:
            if r[2] == 'job':
                job = r[3]
            if r[2] == 'task':
                task = r[3]

        if filter(lambda x: x.jobid == job, mappings):
            m = filter(lambda x: x.jobid == job, mappings)[0]
            m.tasks.append(task)
        else:
            m = mapping(job)
            m.tasks = [task]
            curs.execute('select * from attr where e_id = %s' % eid)
            res = curs.fetchall()
            for r in res:
                if r[2] == 'task.class':
                    m.jobclass = r[3]
                if r[2] == 'task.xform':
                    m.xform = r[3]

            mappings.append(m)

    return mappings


class job:

    def __init__(self, jobName, workflow, status='SUCCESS', site='local', localPath='', remoteSite='', remotePath='', jobScript=None, sterr=None, inputFiles=[], outputFiles=[], condorJobs=[], parents=[], children=[], buildRelationships=False):
        self.jobName = jobName
        if status:
            self.status = status
        else:
            self.status = self.getStatus()
        self.site = site
        self.localPath = directory(localPath)
        self.remoteSite = remoteSite
        self.remotePath = directory(remotePath)
        if jobScript:
            self.jobScript = pegasusFile(jobScript)
        else:
            self.jobScript = jobScript
        if sterr:
            self.sterr = pegasusFile(sterr)
        else:
            self.sterr = sterr
        self.inputFiles = [ pegasusFile(f) for f in inputFiles ]
        self.outputFiles = [ pegasusFile(f) for f in outputFiles ]
        self.condorJobs = [ pegasusFile(f) for f in condorJobs ]
        if parents == [] and buildRelationships:
            self.parents = self.findParents()
        else:
            self.parents = parents
        if children == [] and buildRelationships:
            self.children = self.findChildren()
        else:
            self.children = children

    def __repr__(self):
        return self.jobName

    def info(self):
        return 'jobName: %s \n Status: %s \n Local Site: %s \n Local Path: %s \n Remote Site: %s \n Remote Path: %s \n Job Script %s \n Standard Error: %s \n Input Files; %s \n Output Files: %s \n Condor Jobs %s \n Parents: %s \n Children: %s \n' % (self.jobName, self.status, self.site, self.localPath, self.remoteSite, self.remotePath, self.jobScript, self.sterr, self.inputFiles, self.outputFiles, self.condorJobs, self.parents, self.children)

    def asXML(self):
        xml = '<job>'
        xml += '<jobName>' + self.jobName + '</jobName>'
        xml += '<status>' + self.status + '<status>'
        xml += '<localSite>' + self.site + '</localSite>'
        xml += '<localPath>' + self.localPath.asXML() + '</localPath>'
        xml += '<remoteSite>' + self.remoteSite + '</remoteSite>'
        xml += '<remotePath>' + self.remotePath.asXML() + '</remotePath>'
        xml = '<jobScript>' + self.jobScript.asXML() + '</jobScript>'
        xml += '<localSite>' + self.site + '</localSite>'
        xml += '<standardError>' + self.sterr.asXML() + '</standardError>'
        xml += '<inputFiles>'
        for f in self.inputFiles:
            xml += f.asXML()

        xml += '</inputFiles>'
        xml += '<outputFiles>'
        for f in self.outputFiles:
            xml += f.asXML()

        xml += '</outputFiles>'
        xml += '<condorJobs>'
        for c in self.condorJobs:
            xml += c.asXML()

        xml += '</condorJobs>'
        xml += '<parents>'
        for p in parents:
            xml += '<jobName>' + p + '</jobName>'

        xml += '</parents>'
        xml += '<children>'
        for c in children:
            xml += '<jobName>' + c + '</jobName>'

        xml += '</children>'
        xml += '</job>'
        return xml

    def getStatus(self):
        c = getConnection(workflow)
        q = "select attr.value from attr join ident where attr.id = ident.e_id and ident.name = 'comp' and ident.value = '%s' and attr.name = 'status';" % self.jobName
        c.execute(q)
        res = c.fetchone()
        status = res[0]
        return status

    def getParents(self):
        qArray = [
         'drop table if exists parentids',
         'create temporary table parentids (e_id integer not null, name varchar(50) not null);',
         "insert into parentids select e_id, value from ident where name = 'comp.child' and value = " + self.jobName,
         "select ident.value from ident join parentids where parentids.e_id = ident.e_id and ident.name = 'comp.parent';"]
        c = getConnection(self.dbname)
        [ c.execute(q) for q in qArray ]
        res = c.fetchall()
        return [ host[0] for host in res ]

    def getChildren(self):
        qArray = [
         'drop table if exists childids',
         'create temporary table childids (e_id integer not null, name varchar(50) not null);',
         "insert into childids select e_id, value from ident where name = 'comp.parent' and value = " + self.jobName,
         "select ident.value from ident join childids where childids.e_id = ident.e_id and ident.name = 'comp.child';"]
        c = getConnection(self.dbname)
        [ c.execute(q) for q in qArray ]
        res = c.fetchall()
        return [ host[0] for host in res ]


def getConnection(dbname):
    factory = DBFactory(mysql)
    conn = factory.new('localhost', conn_kw={'database': dbname})
    return conn.cursor()


def getTimings(curs, partitions):
    statements = [
     '-- STAGES table\n drop table if exists stages;',
     'create table stages (id integer, name char(40), wflow_id char(36), time double, dur double, startend tinyint(2), dup integer);',
     "-- Add all stages except pegasus invocations -- \n insert into stages (id, name, wflow_id, time, dur, startend, dup) select event.id, event.name, right(ident.value, 36), event.time, 0.0, event.startend, 0 from event join ident on event.id = ident.e_id join ident as pid on event.id = pid.e_id where ident.name = 'comp' and event.name != 'pegasus.invocation';",
     '-- nota bene: Make sure there is an index on attr(e_id) \n -- Add an index on wflow_id \n  create index ww on stages(wflow_id);',
     "-- Part 1 of augmenting stages table with values for 'dup' column \n -- Done early because the pegasus invocations arent needed to calculate duplicates (and slow it down). \n -- where there are duplicate submits for the same workflow id. \n  -- (1) Create temporary table [but not with that keyword because we need to do a self-join] to hold duplicates \n drop table if exists temp1;",
     'create table temp1 ( id integer, wflow_id char(36), time double);',
     "-- (2) Populate the table \n  insert into temp1(id, wflow_id, time)  select s1.id, s1.wflow_id, s1.time from stages s1  join stages s2 on s1.wflow_id = s2.wflow_id and s1.id != s2.id where s1.name = 'pegasus.jobstate.submit' and s2.name='pegasus.jobstate.submit' group by s1.id;",
     '-- (3) Create 2nd temporary table to hold time range for each duplicate \n drop table if exists temp2;',
     'create table temp2 (wflow_id char(36), start double, end double, n integer auto_increment primary key);',
     '-- (4) Populate 2nd temp table with the results of joining the first table with itself so that we have the begin and end time for each duplicate (numbered with a global duplicate number; local would be better) \n insert into temp2 (wflow_id, start, end) select a.wflow_id, max(a.time) as start, b.time as end  from temp1 as a join temp1 as b on a.wflow_id = b.wflow_id and a.time < b.time group by a.time order by a.time;',
     '-- (4b) Add a row for the last duplicate (end time = Jan 1, 2034) \n insert into temp2 (wflow_id, start, end) select a.wflow_id, max(a.time) as start, 2019715200 from temp1 a group by wflow_id;',
     "-- Add pegasus invocations to stages \n insert into stages (id, name, wflow_id, time, dur, startend, dup) select event.id, event.name, right(ident.value, 36), event.time, attr.value + 0.0, event.startend, 0 from event join ident on event.id = ident.e_id join ident as pid on event.id = pid.e_id join attr on event.id = attr.e_id where ident.name = 'comp' and event.name = 'pegasus.invocation' and attr.name = 'duration';",
     "-- (5) Update 'dup' value in stages for all workflows matching an identifier in temp2 \n update stages s set dup = (select n from temp2 where s.wflow_id = temp2.wflow_id  and s.time >= temp2.start and s.time < temp2.end ) where exists (select null from temp2 where s.wflow_id = temp2.wflow_id);",
     '-- JOB table \n  drop table if exists job;',
     'create table job (id integer auto_increment primary key, wflow_id char(36) not null, submit double not null, exec double, ks_begin double, ks_end double, term double, ps_end double, dup integer not null);',
     "-- Create one row per submit workflow/dup combination \n insert into job (wflow_id, submit, exec, ks_begin, ks_end, term, ps_end, dup) select s.wflow_id, s.time, 0, 0, 0, 0, 0, s.dup from stages s where s.name = 'pegasus.jobstate.submit';",
     "-- Fill in each column with an update \n  update job set exec = (select time from stages s where s.name = 'pegasus.jobstate.execute' and s.wflow_id = job.wflow_id and s.dup = job.dup);",
     "update job set ks_begin = (select min(time) from stages s where s.name = 'pegasus.invocation' and s.wflow_id = job.wflow_id and s.dup = job.dup);",
     "update job set ks_end = (select max(time) from stages s where s.name = 'pegasus.invocation' and s.wflow_id = job.wflow_id and s.dup = job.dup);",
     "update job set term = (select time from stages s where s.name = 'pegasus.jobstate.job_terminated' and s.wflow_id = job.wflow_id and s.dup = job.dup);",
     "update job set ps_end = (select time from stages s where s.name = 'pegasus.jobstate.postscript' and s.startend = 1 and s.wflow_id = job.wflow_id and s.dup = job.dup);"]
    for partition in partitions:
        for q in statements:
            if '%s' in q:
                if type(partition) == type(0):
                    p = 'PID%s' % partition
                else:
                    p = partition
                q = q % p
            print q
            curs.execute(q)


def getTimeElapsedFromJobTable(curs, jobName, asXML=False):
    q = 'select submit, ps_end from job where wflow_id = %s' % jobName
    curs.execute(q)
    res = curs.fetchall()


def getJobsByType(curs):
    curs.execute("select * from attr where  name = 'type' or name = 'duration'")
    res = curs.fetchall()
    r1 = {}
    for item in res:
        if item[1] in r1:
            r1[item[1]].append(item)
        else:
            r1[item[1]] = [
             item]

    jobhash = {}
    jobs = [ (item[0][1], item[0][3], item[1][3]) for item in r1.values() ]
    for job in jobs:
        if job[2] in jobhash:
            jobhash[job[2]].append(job[1])
        else:
            jobhash[job[2]] = [
             job[1]]

    return jobhash


def getAllJobs(curs, workflow):
    curs.execute('select distinct value from ident where name="comp"')
    res = curs.fetchall()
    jobnames = [ j[0] for j in res ]
    jobs = [ job(n, workflow) for n in jobnames ]
    return jobs


def getTimesForJob(curs, job):
    curs.execute("select e_id from ident where name = 'comp' and value = '%s'" % job)
    eids = [ e[0] for e in curs.fetchall() ]
    times = []
    for e in eids:
        curs.execute("select value from attr where e_id = %s and name = 'duration'" % e)
        times.append([ s[0] for s in curs.fetchall() ])

    return times