# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ronny/projects/django/shopdev/scripts/tools/config/configurationvalues.py
# Compiled at: 2014-01-02 10:14:35
import os, sys, yaml, shyaml, elpotrero.lib.util as elutil
_TOOLSCONFIG = 'tools.config.yaml'

def _here():
    """standard "here" helper function"""
    return os.path.dirname(os.path.realpath(__file__))


def loadyaml(configfile):
    """Helper function to pull up the config file

    returns a yaml dict
    """
    stream = file(configfile, 'r')
    return yaml.load(stream)


def _cwdprojectpath():
    pathlist = os.getcwd().split(os.path.sep)
    index = elutil.lastindex(pathlist, 'scripts')
    return os.path.sep.join(pathlist[:index])


def getformalprojectpath():
    """
    Utility function to create a project path name based on the
    values found in configuration.basic
    """
    projectname = getconfigvalue('project')
    projectdir = getconfigvalue('projdir')
    branchname = getbranch()
    return ('{0}/{1}/{2}').format(projectdir, projectname, branchname)


def getprojectpath():
    """
    Utility to get the project path based on WHERE THIS FILE IS LOCATED
    I'm finding the above formal project path method does not do what I want
    because it limits me to using only the  configuration file.

    I'd rather use the location of the installation files as a determiner
    of what the projdir is!
    """
    pathlist = _here().split(os.path.sep)
    index = elutil.lastindex(pathlist, 'scripts')
    return os.path.sep.join(pathlist[:index])


def getrootpath():
    """ Utility function to create a project path name based on the
    values found in configuration.basic
    """
    projectdirname = ('{0}.{1}').format(getconfigvalue('project'), getconfigvalue('domain'))
    fullrootpath = os.path.join(getconfigvalue('rootpath'), projectdirname)
    return fullrootpath


def getenvironmentpath():
    """ Utility function returning the full path of the environment directory
    """
    return os.path.join(getconfigvalue('environment'), ('{0}.{1}').format(getconfigvalue('project'), getbranch()))


def _cwdfilelayout():
    global _TOOLSCONFIG
    ptoolsconfig = ('{0}/{1}').format(_here(), _TOOLSCONFIG)
    filelayoutpath = loadyaml(ptoolsconfig)['filelayout']
    return os.path.join(_cwdprojectpath(), filelayoutpath)


def _cwdfullpath(confkey):
    r""" Helper function to retrieve the configuration paths
        that are defined in the filelayout conf file

        confkey refers to either configuration.branch or configuration.basic
        which should be passed in as "configuration\.branch" or
        "configuration\.basic"

        NOTE: The values retrieved using this function are appended to the
        project directory path.  So you might want to be careful with this,
        since you could ask for a totally unrelated value and get something
        that shouldn't be appended to a project path.
    """
    ydict = loadyaml(_cwdfilelayout())
    configpath = shyaml.mget(ydict, confkey)
    return os.path.join(_cwdprojectpath(), configpath)


def _cwdconfigbasic():
    return _cwdfullpath('configuration\\.basic')


def getbranch():
    """ Helper function to retrieve the name of the branch we are working on

        NOTE: There isn't any point in retrieving the config branch file, since
            all I want is the branch value
    """
    bpath = _cwdfullpath('configuration\\.branch')
    return loadyaml(bpath)['branch']


def getbranchindex():
    """Return the index of the branch key
        """
    branch = getbranch()
    branchlist = getconfigvalue('branch', isbranchdependent=False)
    if branchlist.count(branch) == 0:
        errmsg = ('branch = {0}\nbranchlist = {1}').format(branch, branchlist)
        raise ValueError("The branch value from configuration.branch doesn't appear in configuration.basic\n." + errmsg)
    return branchlist.index(branch)


def getlayoutvalue(key):
    """ Helper function to get values from the filelayout file
    """
    ydict = loadyaml(_cwdfilelayout())
    return shyaml.mget(ydict, key)


def getconfigvalue(key, isbranchdependent=True):
    r""" Helper function to get values from the configuration.basic file
        a lot of the values that I'll request will depend on what branch I
        am using.

        I internally find the relevent branch using the getbranch method
        in this class

    Keyword arguments:
        key -- the key argument used

        NOTE: shyaml.mget drills down to find the key value, for example:
            "tools.config" is assumed to be a value in dictionary form

            tools = { 'config':someval }

            but "tools\.config" would be considered a single keyname of:

            tools.config = someval
    """
    ydict = loadyaml(_cwdconfigbasic())
    value = shyaml.mget(ydict, key)
    if not isbranchdependent:
        return value
    else:
        errmsg_vals = ('\nValues are:\nbranch = {0}\nconfigurationpath = {1}\nkey requested = {2}\nextracted ymldict = {3}\n').format(getbranch(), _cwdconfigbasic(), key, ydict)
        if type(value) is list:
            bindex = getbranchindex()
            if len(value) < bindex:
                raise ValueError('The branch index is higher than the length of the list value returned by the key you requested.\nThis is probably a problem with the configuration.basic file.\nYou should check the key in it.\n' + errmsg_vals)
            return value.pop(bindex)
        return value


def getconfigkeys():
    """ Helper function to return the keys for the configuration.basic file
    """
    ydict = loadyaml(_cwdconfigbasic())
    return ydict.keys()


def getfilelayoutkeys():
    """ Helper function to return the keys for the filelayout file
    """
    ydict = loadyaml(_cwdfilelayout())
    return ydict.keys()


def getconfigurationcontext():
    r""" The purpose of this function is to create a context dictionary
    for use in a template renderer

    if you look at how keys are generated, you'll notice I replace the
    '.' with a '\.'

    e.g.  bind.zones ->  bind\.zones
    """
    context = dict()
    keys = getconfigkeys()
    for k in keys:
        context[k] = getconfigvalue(k)

    return context


def main(args):
    print getconfigurationcontext()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))