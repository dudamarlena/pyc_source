# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\suit\__init__.py
# Compiled at: 2010-12-21 14:30:09
"""SUIT Framework (Scripting Using Integrated Templates) allows developers to
define their own syntax for transforming templates by using rules.

-----------------------------
Example Usage
-----------------------------

::

    import suit
    from rulebox import templating # easy_install rulebox
    template = open('template.tpl').read()
    # Template contains "Hello, <strong>[var]username[/var]</strong>!"
    templating.var.username = 'Brandon'
    print suit.execute(templating.rules, template)
    # Result: Hello, <strong>Brandon</strong>!

Basic usage; see http://www.suitframework.com/docs/ for other uses.

-----------------------------
Caching and Logging
-----------------------------

``cache``
    dict - Saves processing time by storing the results of these functions.

``log``
    dict - Contains information on how the execute function works.

For both ``log`` and ``cache``, the `hash` key contains the actual data. The
others reference this to deal with redundant items.
"""
from hashlib import md5
try:
    import json
except ImportError:
    import simplejson as json

__all__ = [
 'cache', 'close', 'closed', 'configitems', 'defaultconfig', 'escape',
 'evalrules', 'execute', 'log', 'loghash', 'parse', 'ruleitems', 'rulesort',
 'separators', 'tokens', 'treeappend', 'walk']
__version__ = '2.0.2'
cache = {'hash': {}, 'parse': {}, 'tokens': {}}
log = {'contents': [], 'hash': {}}
separators = (',', ':')

def close(rules, append, pop, tree):
    """Handle the closing of a rule.

    ``rules``
        dict - The rules used to determine how to add the string.

    ``append``
        str - The string to add.

    ``pop``
        dict - The last item of the tree's contents.

    ``tree``
        list - The contents of the tree.

    Returns: dict - A dict with the following format format:

    `skip`
        str - The skip rule, if opened.

    `tree`
        list - The contents of the tree with the appended data.
    """
    skip = False
    rule = rules[pop['rule']]
    if 'create' not in rule:
        if append:
            pop['contents'].append(append)
        tree = treeappend((pop,), tree)
    else:
        if closed(pop):
            create = rule['create']
            append = {'contents': [], 'create': append, 
               'createrule': ('').join((
                            pop['rule'],
                            append,
                            rule['close'])), 
               'rule': create}
            if 'skip' in rules[create] and rules[create]['skip']:
                skip = create
        else:
            append = ('').join((
             pop['rule'],
             append))
        tree.append(append)
    return {'skip': skip, 'tree': tree}


def closed(node):
    """Check whether or not this item is a dict and has been closed.

    ``node``
        mixed - The item to check.

    Returns: bool - The condition.
    """
    return not isinstance(node, dict) or 'closed' in node and node['closed']


def configitems(config, items):
    """Get the specified items from the config.

    ``config``
        dict - The dict to grab from.

    ``items``
        list - The items to grab from the dict.

    Returns: dict - The dict with the specified items.
    """
    newconfig = {}
    for value in items:
        if value in config:
            newconfig[value] = config[value]

    return newconfig


def defaultconfig(config):
    """Fill a dict with the defaults for the missing items.

    ``config``
        dict - The dict to fill.

    Returns: dict - A dict with the following format:

    `escape`
        str - The escape string.

    `insensitive`
        str - Whether or not the searching should be done case insensitively.

    `log`
        bool - Whether or not the execute call should be logged.

    `mismatched`
        bool - Whether or not to parse if the closing string does not match the
        opening string.

    `unclosed`
        bool - Whether or not the SUIT should walk through the node if it was
        opened but not closed.
    """
    if config == None:
        config = {}
    if 'escape' not in config:
        config['escape'] = '\\'
    if 'insensitive' not in config:
        config['insensitive'] = True
    if 'log' not in config:
        config['log'] = True
    if 'mismatched' not in config:
        config['mismatched'] = False
    if 'unclosed' not in config:
        config['unclosed'] = False
    return config


def escape(escapestring, position, string, insensitive=True):
    """Handle escape strings for this position.

    ``escapestring``
        str - The string to check for behind this position.

    ``position``
        int - The position of the open or close string to check for.

    ``string``
        str - The full string to check in.

    ``insensitive``
        bool - Whether or not the searching should be done case insensitively.

    Returns: dict - A dict with the following format:

    `odd`
        bool - Whether or not the count of the escape strings to the left of
        this position is odd, escaping the open or close string.

    `position`
        int - The position adjusted to the change in the string.

    `string`
        str - The string omitting the necessary escape strings.
    """
    count = 0
    caseescape = escapestring
    casestring = string
    if insensitive:
        caseescape = caseescape.lower()
        casestring = casestring.lower()
    if escapestring:
        focus = position - len(escapestring)
        while focus == abs(focus) and casestring[focus:focus + len(escapestring)] == caseescape:
            count += len(escapestring)
            focus = position - count - len(escapestring)

        count = count / len(escapestring)
    odd = count % 2
    if odd:
        count += 1
    count = count / 2
    position -= len(escapestring) * count
    string = ('').join((
     string[0:position],
     string[position + len(escapestring) * count:]))
    return {'odd': odd, 
       'position': position, 
       'string': string}


def execute(rules, string, config=None):
    """Transform a string using rules. The function calls ``tokens``,
    ``parse``, and ``walk`` all in one convenient call.

    ``rules``
        dict - The rules used to transform the string.

    ``string``
        str - The string to transform.

    ``config``
        dict - Specifics on how the function should work.
        (Optional. See `defaultconfig`)

    Returns: str - The transformed string.
    """
    config = defaultconfig(config)
    pos = tokens(rules, string, config)
    tree = parse(rules, pos, string, config)
    if config['log']:
        log['contents'].append(loghash({'config': config, 
           'contents': [], 'parse': tree, 
           'rules': ruleitems(rules, ('close', 'create', 'skip')), 
           'string': string, 
           'tokens': pos}, ('config', 'parse', 'rules', 'string', 'tokens')))
    string = walk(rules, tree, config)
    if config['log'] and log['contents']:
        pop = log['contents'].pop()
        pop['walk'] = string
        pop = loghash(pop, ('walk', ))
        log['contents'] = treeappend((pop,), log['contents'])
    return string


def functions(params):
    """Run the specified functions."""
    for value in params['rules'][params['tree']['rule']]['functions']:
        params = value(params)

    return params


def loghash(entry, items):
    """Hash specific keys for logging.

    ``entry``
        dict - The dict.

    ``items``
        list - The items to hash in the dict.

    Returns: dict - The dict with the specified items hashed.
    """
    newlog = {}
    for (key, value) in list(entry.items()):
        if key in items:
            dumped = json.dumps(value, separators=separators)
            hashkey = md5(dumped).hexdigest()
            log['hash'][hashkey] = dumped
            value = hashkey
        newlog[key] = value

    return newlog


def parse(rules, pos, string, config=None):
    """Generate the tree from the tokens and string. The tree will show how the
    string has been broken up and how to transform it.

    ``rules``
        dict - The rules used to break up the string.

    ``pos``
        dict - A list of the positions of the various open and close strings.

    ``string``
        str - The string to break up.

    ``config``
        dict - Specifics on how the function should work.
        (Optional. See `defaultconfig`)

    Returns: dict -

    ::

        {
            'closed': True # Shown if this node has been closed.
            'contents':
            [
                'string',
                {
                    'closed': True
                    'contents': [...],
                    'create': ' condition="var"', # The contents of the create
                    # rule if applicable.
                    'createrule': '[if condition="var"]', # The whole create
                    # rule statement if applicable.
                    'rule': '[if]' # The type of rule
                },
                ...
            ] # This node's branches.
        }
    """
    config = defaultconfig(config)
    cachekey = md5(json.dumps((
     ruleitems(rules, ('close', 'create', 'skip')),
     pos,
     string,
     configitems(config, ('escape', 'insensitive', 'mismatched'))), separators=separators)).hexdigest()
    if cachekey in cache['parse']:
        return json.loads(cache['hash'][cache['parse'][cachekey]])
    flat = set([])
    last = 0
    skip = False
    skipoffset = 0
    temp = string
    tree = []
    for value in pos:
        position = value['bounds']['start'] + len(string) - len(temp)
        escapeinfo = escape(config['escape'], position, string, config['insensitive'])
        escaping = not skip or 'skipescape' in rules[skip] and rules[skip]['skipescape']
        flatopen = value['type'] == 'flat' and value['string'] not in flat
        if value['type'] == 'open' or flatopen:
            rule = rules[value['string']]
            if not skip:
                position = escapeinfo['position']
                string = escapeinfo['string']
                if not escapeinfo['odd']:
                    append = string[last:position]
                    last = position + len(value['string'])
                    tree = treeappend((append,), tree)
                    tree.append({'contents': [], 'rule': value['string']})
                    if 'skip' in rule and rule['skip']:
                        skip = value['string']
                    flat.add(value['string'])
            else:
                skipclose = [
                 rule['close']]
                if 'create' in rule:
                    skipclose.append(rules[rule['create']]['close'])
                if rules[skip]['close'] in skipclose:
                    if escaping:
                        position = escapeinfo['position']
                        string = escapeinfo['string']
                    if not escapeinfo['odd']:
                        skipoffset += 1
        elif not skip or value['string'] == rules[skip]['close']:
            if escaping:
                position = escapeinfo['position']
                string = escapeinfo['string']
            if escapeinfo['odd'] or skipoffset:
                skipoffset -= 1
            elif tree:
                if not closed(tree[(len(tree) - 1)]):
                    skip = False
                    pop = tree.pop()
                    if rules[pop['rule']]['close'] == value['string'] or config['mismatched']:
                        pop['closed'] = True
                        result = close(rules, string[last:position], pop, tree)
                        skip = result['skip']
                        tree = result['tree']
                        flat.discard(value['string'])
                        last = position + len(value['string'])
                    else:
                        rulestring = pop['rule']
                        if 'createrule' in pop:
                            rulestring = pop['createrule']
                        tree = treeappend([
                         rulestring] + pop['contents'], tree)

    append = string[last:]
    while tree and not closed(tree[(len(tree) - 1)]):
        pop = tree.pop()
        tree = close(rules, append, pop, tree)['tree']
        append = tree.pop()

    if append:
        tree.append(append)
    tree = {'closed': True, 'contents': tree}
    dumped = json.dumps(tree, separators=separators)
    hashkey = md5(dumped).hexdigest()
    cache['hash'][hashkey] = dumped
    cache['parse'][cachekey] = hashkey
    return tree


def ruleitems(rules, items):
    """Get the specified items from the rules.

    ``rules``
        dict - The dict to grab from.

    ``items``
        list - The items to grab from the dict.

    Returns: dict - The dict with the specified items.
    """
    newrules = {}
    for (key, value) in list(rules.items()):
        newrules[key] = {}
        for value2 in items:
            if value2 in value:
                newrules[key][value2] = value[value2]

    return newrules


def rulesort(a, b):
    """Sort by priority, and if it is equal, sort by the size of the
    string."""
    if 'priority' in a and 'priority' not in b:
        return -1
    if 'priority' in b and 'priority' not in a:
        return 1
    if 'priority' in a and 'priority' in b:
        if a['priority'] > b['priority']:
            return -1
        if b['priority'] > a['priority']:
            return 1
    return len(b['string']) - len(a['string'])


def tokens(rules, string, config=None):
    """Generate the tokens from the string. Tokens contain the different open
    and close strings and their positions.

        ``rules``
            dict - The rules containing the strings to search for.

        ``string``
            str - The string to find the strings in.

        ``config``
            dict - Specifics on how the function should work.
            (Optional. See `defaultconfig`)

        Returns: dict - A list of dicts with the following format:

        `bounds`
            dict - A dict with the following format:
                `start`
                    int - Where the string starts.

                `end`
                    int - Where the string ends.

        `string`
            str - The located string.

        `type`
            str - The type, options being open, close, or flat.
    """
    config = defaultconfig(config)
    cachekey = md5(json.dumps((
     ruleitems(rules, ('close', )),
     string,
     configitems(config, ('insensitive', ))), separators=separators)).hexdigest()
    if cachekey in cache['tokens']:
        return json.loads(cache['hash'][cache['tokens'][cachekey]])
    pos = []
    repeated = set({})
    strings = []
    for (key, value) in list(rules.items()):
        if 'close' in value:
            item = {}
            if 'priority' in value:
                item['priority'] = value['priority']
            stringtype = 'flat'
            if key != value['close']:
                stringtype = 'open'
                item['string'] = value['close']
                item['type'] = 'close'
                strings.append(item.copy())
            item['string'] = key
            item['type'] = stringtype
            strings.append(item)

    strings.sort(cmp=rulesort)
    if config['insensitive']:
        string = string.lower()
    for value in strings:
        tempstring = value['string']
        if tempstring and tempstring not in repeated:
            casestring = tempstring
            if config['insensitive']:
                casestring = casestring.lower()
            length = len(casestring)
            position = string.find(casestring)
            while position != -1:
                endposition = position + length
                success = True
                for value2 in pos:
                    start = value2['bounds']['start']
                    end = value2['bounds']['end']
                    startrange = position >= start and position < end
                    endrange = endposition > start and endposition < end
                    if startrange or endrange:
                        success = False
                        break

                if success:
                    pos.append({'bounds': {'start': position, 
                                  'end': endposition}, 
                       'string': tempstring, 
                       'type': value['type']})
                position = string.find(casestring, position + 1)

            repeated.add(tempstring)

    pos.sort(key=lambda item: item['bounds']['start'])
    dumped = json.dumps(pos, separators=separators)
    hashkey = md5(dumped).hexdigest()
    cache['hash'][hashkey] = dumped
    cache['tokens'][cachekey] = hashkey
    return pos


def treeappend(append, tree):
    """Add to the tree contents in the appropriate place if necessary.

    ``append``
        list - The items to add.

    ``tree``
        list - The contents of the tree to add the item on.

    Returns: list - The updated tree contents.
    """
    if append:
        if tree and not closed(tree[(len(tree) - 1)]):
            pop = tree.pop()
            for value in append:
                pop['contents'].append(value)

            tree.append(pop)
        else:
            for value in append:
                tree.append(value)

    return tree


def walk(rules, tree, config=None):
    """Walk through the tree and generate the string.

    ``rules``
        dict - The rules used to specify how to walk through the tree.

    ``tree``
        dict - The tree to walk through.

    ``config``
        dict - Specifics on how the function should work.
        (Optional. See `defaultconfig`)

    Returns: str - The generated string.
    """
    config = defaultconfig(config)
    string = ''
    for (key, value) in enumerate(tree['contents']):
        if isinstance(value, dict):
            if 'closed' in value and value['closed'] or config['unclosed']:
                params = {'config': config, 
                   'rules': rules, 
                   'string': '', 
                   'tree': value}
                params['tree']['key'] = key
                params['tree']['parent'] = tree
                if 'rule' in value and 'functions' in rules[value['rule']]:
                    params = functions(params)
                try:
                    function = unicode
                except NameError:
                    function = str
                else:
                    string += function(params['string'])
            else:
                rulestring = value['rule']
                if 'createrule' in value:
                    rulestring = value['createrule']
                string += ('').join((
                 rulestring,
                 walk(rules, value, config)))
        else:
            string += value

    return string