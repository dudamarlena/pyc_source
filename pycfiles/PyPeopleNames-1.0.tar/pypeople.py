# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/pypeople/pypeople.py
# Compiled at: 2013-01-07 15:41:50
from __future__ import unicode_literals, print_function, with_statement, absolute_import
import subprocess, glob, optparse, sys, os, json, vobject, re, errno
__version_info__ = [
 0, 6, 2, 4]
__version__ = b'0.6.2,4'
VERSION = b'0.6.2,4'
if __version__ != VERSION and VERSION != (b'.').join([ str(x) for x in __version_info__ ]):
    raise Exception(b'Version is screwed up')
_g_config = None

def is_valid_config_json(rawData):
    return True


def has_config_file(configFilename=None):
    """ quick check for config file existing. """
    file = configFilename if configFilename else b'~/.pypeople'
    return os.path.isfile(os.path.expanduser(file))


def dict_from_vcard(vcard):
    """ loads a dictionary with *select* vcard info. NOTE: this does not
    load *all* vcard data, since that can be a bit batshit complex. It only
    loads some key values. Keep the origional vcard around to merge values back 
    into it, or you *will lose data* esp for complex or edge-case data"""
    retDict = {}
    rekeyings = (
     ('fullname', 'fn'), ('name', 'n'), ('address', 'adr'))
    contents = vcard.contents
    for key in contents.keys():
        if len(contents[key]) == 0:
            raise Exception(b'emtpy vcard key %s' % key)
        if len(contents[key]) > 1:
            import pdb
            pdb.set_trace()
            print(b'WARNING: More than one entry for vcard key %s' % key)
        vCardObj = contents[key][0]
        unpackedData = None
        if type(vCardObj.value) == type(b'str'):
            unpackedData = vCardObj.value
        elif type(vCardObj.value) == vobject.vcard.Name:
            unpackedData = {}
            unpackedData[b'given'] = vCardObj.value.given
            unpackedData[b'family'] = vCardObj.value.family
            unpackedData[b'additional'] = vCardObj.value.additional
            unpackedData[b'prefix'] = vCardObj.value.prefix
            unpackedData[b'suffix'] = vCardObj.value.suffix
        elif type(vCardObj.value) is vobject.vcard.Address:
            unpackedData = {}
            a = vCardObj.value
            unpackedData[b'street'] = a.street
            unpackedData[b'city'] = a.city
            unpackedData[b'region'] = a.region
            unpackedData[b'code'] = a.code
            unpackedData[b'country'] = a.country
        elif type(vCardObj.value) is list:
            unpackedData = vCardObj.value
        else:
            print(b'ohhhh! new datatype. We need to investigate!')
            import pdb
            pdb.set_trace()
        if unpackedData == None:
            import pdb
            pdb.set_trace()
            raise Exception(b'We do not know how to unpack key %s' % key)
        outKey = key
        newkeys, oldkeys = zip(*rekeyings)
        if key in oldkeys:
            idx = oldkeys.index(key)
            outKey = newkeys[idx]
        retDict[outKey] = unpackedData

    print(b'TODO: extend this to other key values')
    return retDict


def shitty_cc_parse(addrLine):
    """Parses out countrycode from addressline
    @returns tuple of (reminingAddr, countrycode)"""
    shitty_cc = b'(?P<cc>[a-zA-Z]{2,5})'
    shitty_break = b'\\s*?[.,]?\\s*$'
    se = re.compile(shitty_cc + b'$')
    cc = b'US'
    if se:
        grp = se.search(addrLine)
        if grp:
            cc = grp.groupdict()[b'cc']
            rest = addrLine[:grp.start()]
            grp2 = re.search(shitty_break, rest)
            if grp2:
                rest = rest[:grp2.start()]
            return (rest, cc)
    return (
     addrLine, cc)


def shitty_zip_parse(addrLine):
    """Parse out countrycode from addressline
    @returns tuple of (reminingAddr, countrycode)"""
    shitty_zip = b'(?P<zip>\\d{5})'
    shitty_break = b'\\s*?[.,]?\\s*$'
    se = re.compile(shitty_zip + b'$')
    zip = b''
    if se:
        grp = se.search(addrLine)
        if grp:
            zip = grp.groupdict()[b'zip']
            rest = addrLine[:grp.start()]
            grp2 = re.search(shitty_break, rest)
            if grp2:
                rest = rest[:grp2.start()]
            return (rest, zip)
    return (
     addrLine, zip)


def shitty_citystate_parse(addrLine):
    """ parse out city/state data from addr
    @return tuple of (rest, city, state) """
    shitty_state = b'(?P<state>\\w[.,]?\\w[.,]?)'
    shitty_city = b'(?P<city>\\w+[.-]?\\s*?\\w*?)'
    shitty_break = b'\\s*?[.,]?\\s*$'
    se = re.compile(shitty_city + b'\\s+' + shitty_state + b'$')
    state = b''
    if se:
        grp = se.search(addrLine)
        if grp:
            state = grp.groupdict()[b'state']
            city = grp.groupdict()[b'city']
            rest = addrLine[:grp.start()]
            grp2 = re.search(shitty_break, rest)
            if grp2:
                rest = rest[:grp2.start()]
            return (rest, city, state)
    return (
     addrLine, b'', b'')


def shitty_addr_parser(addrLine):
    """shitty address parser. Assumes US always"""
    shitty_state = b'(P<st>\\w[.,]?{2}|\\w{3,6})'
    shitty_break = b'\\s*,?\\s+'
    shitty_city = b'(P<city>\\w+)'
    final_zip = None
    addrLeft = addrLine
    ma = re.compile(shitty_zip + b'$')
    grp = ma.search(addrLeft)
    if grp:
        final_zip = grp.groupdict[b'cc']
        addrLeft = addrLeft[:grp.span()[1]]
    else:
        final_zip = b''
    ma = re.compile(shitty_state)
    return


def shitty_addr_parser(addrLine):
    """shitty address parser. Assumes US always"""
    shitty_state = b'(P<st>\\w[.,]?{2}|\\w{3,6})'
    shitty_break = b'\\s*,?\\s+'
    shitty_city = b'(P<city>\\w+)'
    final_zip = None
    addrLeft = addrLine
    ma = re.compile(shitty_zip + b'$')
    grp = ma.search(addrLeft)
    if grp:
        final_zip = grp.groupdict[b'cc']
        addrLeft = addrLeft[:grp.span()[1]]
    else:
        final_zip = b''
    ma = re.compile(shitty_state)
    return


def vcard_merge_in_dict(dict, vCard):
    """ merges a well-specified dictionary of data into the passed v-card"""
    rfinal_fn = b'fail'
    final_given = None
    final_family = None
    final_other = b'fail_firstname'
    final_nick = b'fail_nick'
    if b'nick' in dict.keys():
        final_nick = dict[b'nick']
    if b'fullname' in dict.keys():
        final_fn = dict[b'fullname']
    if b'name' in dict.keys():
        final_family = dict[b'name'][b'family']
        final_given = dict[b'name'][b'given']
    elif b'nick' in dict.keys():
        final_fn = b'nick'
    else:
        import pdb
        pdb.set_trace()
        raise Exception(b'Total Name Failure')
    contents = vCard.contents()
    if b'fn' not in contents.keys():
        vCard.add(b'fn')
    vCard.fn.value = final_fn
    if b'n' not in contents.keys():
        vCard.add(b'n')
    vNameObj = vobject.vcard.Name(final_nick)
    if final_given is not None and final_family is not None:
        vNameObj = vobject.vcard.Name(family=final_family, given=final_given)
        vCard.n.value = vNameObj
    if b'address' in dict.keys():
        addr_dict = dict[b'address']
        if addr_dict != {}:
            if b'adr' not in contents.keys():
                vCard.add(b'adr')
            vAddrObj = vobject.vcard.Address(addr_dict[b'street'], addr_dict[b'city'], addr_dict[b'region'], addr_dict[b'code'], addr_dict[b'country'])
            vCard.adr.value = vAddrObj
    if b'email' in dict.keys():
        if b'email' not in contents.keys():
            vCard.add(b'email')
        vCard.email.value = dict[b'email']
    if b'org' in dict.keys():
        if b'org' not in contents.keys():
            vCard.add(b'org')
        vCard.org.value = dict[b'org']
    return


def get_config():
    """ load config, assuming it exists. If no config, sets
    some basic values into the global config object """
    global _g_config
    if _g_config != None:
        return _g_config
    else:
        cfg_file = b'~/.pypeople'
        if not has_config_file(cfg_file):
            _g_config = {}
            _g_config[b'vcard_dir'] = os.getcwd()
            _g_config[b'cfg_file'] = None
            _g_config[b'cfg_version'] = __version_info__
            return _g_config
        cfg_full = os.path.expanduser(cfg_file)
        with open(cfg_full, b'rb') as (fh):
            rawdata = fh.read()
            data = json.loads(rawdata)
            if is_valid_config_json(data):
                _g_config = data
                return _g_config
        print(b'unspecified load config error')
        return


def __help(cmd, paramLine):
    """Print a help menu for the user"""
    print(b'help (aka %s) called with %s' % (cmd, paramLine))
    print(b'pypeople: Command line tool for vcard management, with git backend')
    print(b'Version: ' + __version__)
    print(b'Available Commands:')
    for cmd in availSubCmds.keys():
        helptxt = availSubCmds[cmd].__doc__ if availSubCmds[cmd].__doc__ else b'Undocumented'
        print(b'\t' + str(cmd) + b':\t ' + helptxt)


def vcard_dir_init(cmd, paramLine):
    """Create/Update a config file. 'init <dir_of_vfc> [remote repo]' """
    print(b'init (aka %s) called with %s' % (cmd, paramLine))
    dir, remote = (None, None)
    if len(paramLine) == 0:
        print(vcard_dir_init.__doc__)
        print(b'initalize in dir, pulling from remote_repo as needed ')
        return False
    else:
        if len(paramLine) > 0:
            dir = paramLine[0]
        if len(paramLine) > 1:
            remote = paramLine[1]
        if len(paramLine) > 2:
            print(b'too many params for init!')
            return False
        config = get_config()
        import os
        config[b'vcard_dir'] = os.path.abspath(os.path.expanduser(dir))
        config[b'cfg_file'] = os.path.abspath(os.path.expanduser(b'~/.pypeople'))
        config[b'cfg_version'] = __version_info__
        config[b'remote'] = None
        if remote != None:
            config[b'remote'] = remote
        with open(config[b'cfg_file'], b'w+') as (fh):
            raw = json.dumps(config, indent=2)
            fh.write(raw)
            print(b'written')
        if not os.path.isdir(config[b'vcard_dir']):
            mkdir_p(config[b'vcard_dir'])
            print(b'making new dir for contacts at %s' % config[b'vcard_dir'])
            if b'remote' in config.keys():
                if not os.path.isdir(config[b'remote']):
                    print(b'settings vcard dir %s to track git remote %s' % (
                     config[b'vcard_dir'], config[b'remote']))
                    cmd2 = [b'git', b'clone', config[b'remote'], config[b'vcard_dir']]
                    subprocess.call(cmd2)
                else:
                    print(b'cannot git init an existing dir yet. Sorry :( ')
                    print(b'directory %s already exists' % config[b'remote'])
                    return False
        return


def cd_vcard_dir():
    """ changes our cwd to the vcard dir, 
    @returns cwd from entry, to be restored later """
    cwd = os.getcwd()
    config = get_config()
    os.chdir(config[b'vcard_dir'])
    return cwd


def vcard_dir_sync(cmd, paramLine):
    """ sync our vcard file to our remote repo (if one exists) """
    if len(paramLine) == 0:
        print(vcard_dir_sync.__doc__)
    if len(paramLine) >= 1:
        print(b'sync param %s not understood' % paramLine)
    config = get_config()
    if b'remote' in config.keys() and config[b'remote'] != None:
        oldcwd = cd_vcard_dir()
        cmd = [b'git', b'pull']
        files = glob.glob(config[b'vcard_dir'] + b'/*.vcf')
        cmd = [b'git', b'add']
        cmd.extend(files)
        subprocess.call(cmd)
        import datetime
        dtString = str(datetime.datetime.now())
        cmd = [b'git', b'commit', b'--message="pypeople v%s autocommit on %s"' % (__version__, dtString)]
        subprocess.call(cmd)
        cmd = ('git', 'push', 'origin', 'master')
        subprocess.call(cmd)
        os.chdir(oldcwd)
        return True
    else:
        return


def mkdir_p(path):
    """ a quick and dirty mkdir -p in python"""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise exc


def vcard_list(cmd, paramLine):
    """list : Lists all vCards in vcard folder, take a regex someday"""
    config = get_config()
    files = glob.glob(config[b'vcard_dir'] + b'/*.vcf')
    nicks = [ fname[len(config[b'vcard_dir']) + 1:-4] for fname in files ]
    print((b',\t').join(nicks))


def whois(cmd, paramLine):
    """whois <nick> display info on a single exact nick """
    nick = None
    if len(paramLine) == 0:
        print(whois.__doc__)
        return False
    else:
        if len(paramLine) > 0:
            nick = paramLine[0]
        if len(paramLine) > 1:
            print(b'too many params')
            raise Exception(b'too many params')
        config = get_config()
        nick_fn = nick + b'.vcf'
        nick_fn = os.path.join(config[b'vcard_dir'], nick_fn)
        if not os.path.isfile(nick_fn):
            print(b'ERROR: old nickname %s does not exist at %s' % (
             nick, nick_fn))
            return True
        allVcards = get_all_vcard_elements(nick_fn)
        if len(allVcards) == 0:
            raise Exception(b'No vcards in nick file !' % nick_fn)
        if len(allVcards) > 1:
            raise Exception(b'Multiple Vcards in one file. We are too stupid to hadle this!')
        vCard = allVcards[0]
        infoDict = dict_from_vcard(vCard)
        for k in infoDict.keys():
            if type(infoDict[k]) is dict:
                print(k + b'::')
                for subk in infoDict[k]:
                    print(b'\t' + subk + b':' + str(infoDict[k][subk]))

            else:
                print(k + b':' + infoDict[k])

        return


def vcard_rm(cmd, paramLine):
    """rm <nick> delete a vcard file """
    oldnick = None
    if len(paramLine) == 0:
        print(rm.__doc__)
        return False
    else:
        if len(paramLine) > 0:
            oldnick = paramLine[0]
        if len(paramLine) > 1:
            print(b'too many params')
            raise Exception(b'too many params')
        config = get_config()
        oldnick_fn = oldnick + b'.vcf'
        oldnick_fn = os.path.join(config[b'vcard_dir'], oldnick_fn)
        if not os.path.isfile(oldnick_fn):
            print(b'ERROR: old nickname %s does not exist at %s' % (
             oldnick, oldnick_fn))
            return True
        cmd = [
         b'rm', oldnick_fn]
        os.system((b' ').join(cmd))
        return True


def getvcard(vcard_fn):
    """ takes a caononical filename, returns a vcard object
    @returns vcard for that filename, or None on error"""
    get_config()
    vCard = None
    with open(vcard_fn, b'rb') as (fh):
        rawdata = fh.read()
        vCard = vobject.readOne(rawdata)
    return vCard


def get_all_vcard_elements(vcard_fn):
    """Loads and returns  a list of all vcard elements in the specified file.
    @returns a list of all VCARD entries in the specified file. Empty list of no vcard in file
    """
    vCardList = []
    with open(vcard_fn, b'rb') as (fh):
        rawdata = fh.read()
        for obj in vobject.readComponents(rawdata):
            if obj.name == b'VCARD':
                vCardList.append(obj)

    return vCardList


def vcard_mv(cmd, paramLine):
    """mv <oldnick> <newnick>: move a vcard to a new nickname """
    oldnick = newnick = None
    if len(paramLine) == 0:
        print(mv.__doc__)
        return False
    else:
        if len(paramLine) > 0:
            oldnick = paramLine[0]
        if len(paramLine) > 1:
            newnick = paramLine[1]
        if len(paramLine) > 2:
            print(b'too many params')
            raise Exception(b'too many params')
        config = get_config()
        newnick_fn = newnick + b'.vcf'
        oldnick_fn = oldnick + b'.vcf'
        oldnick_fn = os.path.join(config[b'vcard_dir'], oldnick_fn)
        newnick_fn = os.path.join(config[b'vcard_dir'], newnick_fn)
        if not os.path.isfile(oldnick_fn):
            print(b'ERROR: old nickname %s does not exist at %s' % (
             oldnick, oldnick_fn))
        if os.path.isfile(newnick_fn):
            print(b'ERROR: new nickname %s exists for a previous vcard at %s' % (
             newnick, newnick_fn))
            raise Exception(b'colliding nicknames')
        cmd = [
         b'mv', oldnick_fn, newnick_fn]
        os.system((b' ').join(cmd))
        print(b'oldnick at %s moved to newnick at %s' % (oldnick_fn, newnick_fn))
        return


def undefined(cmd, paramLine):
    """Lazy programmer has not written this function"""
    print(b'undefined %s called with %s' % (cmd, paramLine))


def add_org(cmd, paramLine):
    """org <nick> <org> add org to an existing vcard"""
    config = get_config()
    nick, org = (None, None)
    if len(paramLine) == 0:
        print(add_org.__doc__)
    if len(paramLine) >= 1:
        nick = paramLine[0]
    if len(paramLine) >= 2:
        org = paramLine[1]
    if len(paramLine) >= 3:
        print(b'only <nick> <org_addr> understood :(')
    vcard_fn = nick + b'.vcf'
    vcard_fn = os.path.join(config[b'vcard_dir'], vcard_fn)
    vCard = getvcard(vcard_fn)
    infoDict = dict_from_vcard(vCard)
    infoDict[b'org'] = [
     org]
    vcard_merge_in_dict(infoDict, vCard)
    rawdata = vCard.serialize()
    with open(vcard_fn, b'w+') as (fh):
        fh.write(rawdata)
    return True


def add_email(cmd, paramLine):
    """email <nick> <email> add email to an existing vcard"""
    config = get_config()
    nick, email = (None, None)
    if len(paramLine) == 0:
        print(add_email.__doc__)
    if len(paramLine) >= 1:
        nick = paramLine[0]
    if len(paramLine) >= 2:
        email = paramLine[1]
    if len(paramLine) >= 3:
        print(b'only <nick> <email_addr> understood :(')
    vcard_fn = nick + b'.vcf'
    vcard_fn = os.path.join(config[b'vcard_dir'], vcard_fn)
    vCard = getvcard(vcard_fn)
    infoDict = dict_from_vcard(vCard)
    infoDict[b'email'] = email
    vcard_merge_in_dict(dict, vCard)
    rawdata = vCard.serialize()
    with open(vcard_fn, b'w+') as (fh):
        fh.write(rawdata)
    return


def add_addr(cmd, paramLine):
    """addr <nick> <addr_chunk> : add meatspace address to contact"""
    config = get_config()
    nick = None
    if len(paramLine) == 0:
        print(add_addr.__doc__)
    if len(paramLine) >= 1:
        nick = paramLine[0]
    if len(paramLine) >= 2:
        addr_list = paramLine[1:]
    vcard_fn = nick + b'.vcf'
    vcard_fn = os.path.join(config[b'vcard_dir'], vcard_fn)
    vCard = getvcard(vcard_fn)
    infoDict = dict_from_vcard(vCard)
    addr = (b' ').join(addr_list)
    rest, country = shitty_cc_parse(addr)
    rest2, zip = shitty_zip_parse(rest)
    rest3, city, state = shitty_citystate_parse(rest2)
    street = rest3
    addrDict = {b'street': street, b'city': city, b'region': state, b'code': zip, 
       b'country': country}
    if b'address' in infoDict.keys():
        print(b'has address: %s replacing' % str(infoDict[b'address']))
    infoDict[b'address'] = addrDict
    newVCard = vobject.vCard()
    vcard_from_dict(dict, newVCard)
    rawdata = newVCard.serialize()
    with open(vcard_fn, b'w+') as (fh):
        fh.write(rawdata)
    return True


def add_contact(cmd, paramLine):
    """add <nick> ["full name"] [email], [phone]"""
    config = get_config()
    nick = None
    if len(paramLine) == 0:
        print(add_contact.__doc__)
    if len(paramLine) >= 1:
        nick = paramLine[0]
        fulname = nick
    if len(paramLine) >= 2:
        fullname = paramLine[1]
    else:
        print(b'cant handle those params ' + str(paramLine))
    vcard_fn = nick + b'.vcf'
    vcard_fn = os.path.join(config[b'vcard_dir'], vcard_fn)
    info = {}
    info[b'nick'] = nick
    info[b'fullname'] = fullname
    if len(fullname.split(b' ')) > 1:
        subname = fullname.split()
        info[b'name'] = {b'family': subname[0], b'given': subname[1]}
    if os.path.isfile(vcard_fn):
        print(b'file exists for %s, at %s please move or rename it' % (
         nick, vcard_fn))
        return False
    else:
        vcard = vobject.vCard()
        if os.path.isfile(vcard_fn):
            vcard = loadcraphere
        else:
            vcard = vcard_from_dict(info)
        rawdata = vcard.serialize()
        with open(vcard_fn, b'w+') as (fh):
            fh.write(rawdata)
        return


if __name__ == b'__main__':
    caller = None
    subCmd = b'help'
    cmdRest = []
    if len(sys.argv) > 0:
        caller = sys.argv[0]
    if len(sys.argv) > 1:
        subCmd = sys.argv[1]
    if len(sys.argv) > 2:
        cmdRest = sys.argv[2:]
    availSubCmds = {b'list': vcard_list, 
       b'init': vcard_dir_init, 
       b'add': add_contact, 
       b'addr': add_addr, 
       b'rm': vcard_rm, 
       b'mv': vcard_mv, 
       b'name': undefined, 
       b'whois': whois, 
       b'rename': undefined, 
       b'email': add_email, 
       b'bday': undefined, 
       b'org': add_org, 
       b'help': __help, 
       b'sync': vcard_dir_sync}
    if subCmd in availSubCmds.keys():
        if availSubCmds[subCmd] != None:
            func = availSubCmds[subCmd]
            result = func(subCmd, cmdRest)
    else:
        print(b"command '%s' not found. try 'help' to list commands" % subCmd)