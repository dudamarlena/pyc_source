# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uta/cli.py
# Compiled at: 2014-08-27 16:21:43
from __future__ import absolute_import, division, print_function, unicode_literals
__doc__ = b'uta -- Universal Transcript Archive command line tool\n\nUsage:\n  uta ( -h | --help )\n  uta --version\n  uta (-C CONF ...) [options] shell\n  uta (-C CONF ...) [options] drop-schema\n  uta (-C CONF ...) [options] create-schema\n  uta (-C CONF ...) [options] load-sql FILES ...\n  uta (-C CONF ...) [options] initialize-schema\n  uta (-C CONF ...) [options] rebuild\n  uta (-C CONF ...) [options] load-seqinfo FILE\n  uta (-C CONF ...) [options] load-geneinfo FILE\n  uta (-C CONF ...) [options] load-txinfo FILE\n  uta (-C CONF ...) [options] load-exonsets FILE\n  uta (-C CONF ...) [options] load-sequences\n  uta (-C CONF ...) [options] align-exons [--sql SQL]\n  uta (-C CONF ...) [options] load-ncbi-seqgene FILE\n  uta (-C CONF ...) [options] grant-permissions\n  \nOptions:\n  -C CONF, --conf CONF\tConfiguration to read (required)\n\nExamples:\n  $ ./bin/uta --conf etc/uta.conf create-schema --drop-current\n\n'
import ConfigParser, logging, time, docopt, uta, uta.loading as ul
usam = uta.models

def shell(session, opts, cf):
    import IPython
    IPython.embed()


def rebuild(*args):
    ul.drop_schema(*args)
    ul.create_schema(*args)
    ul.initialize_schema(*args)
    ul.grant_permissions(*args)


def run(argv=None):
    dispatch_table = [
     (
      b'drop-schema', ul.drop_schema),
     (
      b'create-schema', ul.create_schema),
     (
      b'initialize-schema', ul.initialize_schema),
     (
      b'grant-permissions', ul.grant_permissions),
     (
      b'rebuild', rebuild),
     (
      b'load-sql', ul.load_sql),
     (
      b'load-exonsets', ul.load_exonsets),
     (
      b'load-geneinfo', ul.load_geneinfo),
     (
      b'load-seqinfo', ul.load_seqinfo),
     (
      b'load-txinfo', ul.load_txinfo),
     (
      b'load-sequences', ul.load_sequences),
     (
      b'align-exons', ul.align_exons),
     (
      b'load-ncbi-seqgene', ul.load_ncbi_seqgene),
     (
      b'shell', shell)]
    opts = docopt.docopt(__doc__, argv=argv, version=uta.__version__)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    cf = ConfigParser.SafeConfigParser()
    cf_loaded = dict()
    for conf_fn in opts[b'--conf']:
        if conf_fn not in cf_loaded:
            cf.readfp(open(conf_fn))
            cf_loaded[conf_fn] = True
            logger.info(b'loaded ' + conf_fn)

    db_url = cf.get(b'uta', b'db_url')
    session = uta.connect(db_url)
    sub = None
    for cmd, func in dispatch_table:
        if opts[cmd]:
            sub = func
            break

    if sub is None:
        raise UTAError(b'No valid actions specified')
    t0 = time.time()
    sub(session, opts, cf)
    logger.info((b'{cmd}: {elapsed:.1f}s elapsed').format(cmd=cmd, elapsed=time.time() - t0))
    return