# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/diffval/interface.py
# Compiled at: 2010-10-25 19:41:32
import optparse, os, sys, idlval, pyval, log

def index(path, log=None, types={'py': 'python', 'pro': 'idl'}, include=None):
    if include is None:
        (head, tail) = os.path.split(path)
        while tail and tail != 'tests':
            (head, tail) = os.path.split(head)

        if tail == 'tests':
            include = [
             head]
            return index(path, log, types, include)
        include = []
    items = []
    if os.path.isfile(path):
        ext = os.path.splitext(path)[1][1:]
        if ext in types:
            if log:
                log.openElement('file', {'type': types[ext], 'path': path})
            items += [(path, include)]
            if log:
                log.closeElement('file')
    elif os.path.isdir(path):
        if log:
            log.openElement('directory', {'path': path})
        for child in os.listdir(path):
            if child[0] == '.':
                continue
            recurse = os.path.join(path, child)
            if os.path.isdir(recurse):
                if child == 'tests':
                    items += index(path=recurse, log=log, types=types, include=include + [path])
                else:
                    items += index(path=recurse, log=log, types=types, include=include)
            elif os.path.isfile(recurse):
                if len(include) > 0:
                    items += index(path=recurse, log=log, types=types, include=include)

        if log:
            log.closeElement('directory')
    return items


def validate(paths, file=sys.stdout, mailto=None, format='diff'):
    if format == 'xml':
        logger = log.xmllog(file=file)
    else:
        logger = log.difflog(file=file)
    logger.openElement('index')
    candidates = [ os.path.abspath(path) for path in paths ]
    paths = []
    for candidate in candidates:
        paths += index(path=candidate, log=logger)

    logger.openElement('result', {'success': str(len(paths) > 0)})
    logger.closeElement('result')
    logger.closeElement('index')
    logger.openElement('execute')
    succeeded = 0
    tests = len(paths)
    for (path, include) in paths:
        result = None
        ext = os.path.splitext(path)[1]
        if ext == '.pro':
            result = idlval.idltest(path, include, log=logger).run()
        elif ext == '.py':
            result = pyval.pytest(path, include, log=logger).run()
        if result == True:
            succeeded += 1
        elif result == None:
            tests -= 1

    logger.openElement('result', {'success': str(succeeded == tests), 'tests': str(tests), 
       'failures': str(tests - succeeded)})
    logger.closeElement('result')
    logger.closeElement('execute')
    if mailto:
        import smtplib
        mailfrom = 'noreply@ssl.berkeley.edu'
        message = 'From: ' + mailfrom + '\r\n'
        message += 'To: ' + mailto + '\r\n'
        message += 'Subject: Validation ' + str(tests - succeeded) + '/' + str(tests) + '\r\n'
        server = smtplib.SMTP('mail.ssl.berkeley.edu')
        server.sendmail(mailfrom, mailto, message)
        server.quit()
    return tests == succeeded


def main():
    parser = optparse.OptionParser('usage: %prog [options] [path1 [path2 [...]]]')
    delivery = optparse.OptionGroup(parser, 'Output delivery', 'Control how the log file is delivered to you after a run.')
    delivery.add_option('-t', '--mailto', dest='mailto', help='Email results to MAILTO', metavar='MAILTO', default=None)
    delivery.add_option('-l', '--log', dest='logfile', help='Log results to FILE (default behavior with stdout as FILE)', metavar='FILE', default=sys.stdout)
    parser.add_option_group(delivery)
    formatting = optparse.OptionGroup(parser, 'Output formatting', 'Control how the log file is formatted.')
    formatting.add_option('-x', '--xml', action='store_true', help='Log file is in XML')
    formatting.add_option('-d', '--diff', action='store_true', help='Log file is concatenated diffs (default behavior)')
    parser.add_option_group(formatting)
    (options, args) = parser.parse_args()
    format = 'diff'
    if options.xml and options.diff:
        parser.error('Output formatting options are mutually exclusive')
    elif options.xml:
        format = 'xml'
    if len(args) == 0:
        args.append(os.getcwd())
    sys.exit(0 if validate(paths=args, mailto=options.mailto, file=options.logfile, format=format) else 1)
    return


if __name__ == '__main__':
    main()