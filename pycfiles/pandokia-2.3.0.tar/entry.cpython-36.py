# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/entry.py
# Compiled at: 2018-05-14 14:25:23
# Size of source mod 2**32: 6305 bytes
"""

pdk check_expected test_run_type test_run
    check that test_run contains a test result for each one listed as
    expected for type test_run_type; create a Missing record for any
    test that is missing.

pdk clean [ max_records records_per_step sleep_between_steps ]
    Run the background step that cleans deleted material from the database.

pdk clean_queries
    delete old qids

pdk delete -test_run xx -project xx -context xx -host xx -status xx
        -n -wild -count
    delete records from the database

pdk export test_run_pattern [ -h host ] [ -p project ] [ -c context ]
    export records from the database in pandokia import format

pdk gen_expected test_run_type test_run
    declares that all the tests seen in the named test_run are expected
    in runs of type test_run_type

pdk email

pdk getenv
    get environment that would be used

pdk import files
    import pdk result files into the database

pdk import_contact < contact_file
    purges the projects listed in contact_file from the contact table,
    then builds new contact table entries.  This uses the 'expected'
    table to generate the matching patterns, so you may need to
    'pdk gen_expected' first.

pdk ok [ okfiles ]
    Tests that use reference files can leave behind 'okfiles' when
    they run.  The okfile contains the information necessary to copy the
    output files to the reference files.  This command performs that copy.

pdk run
    run tests; use 'pdk run --help' for more detail

pdk runstatus
    show status of actively running tests

pdk webserver
    start up a development web server.  The root of the server is the
    current directory.  It serves pages on port localhost:7070.

fuller documentation is available at http://ssb.stsci.edu/testing/pandokia/

"""
import os, sys

def run(argv=sys.argv):
    if 'QUERY_STRING' in os.environ or 'GATEWAY_INTERFACE' in os.environ:
        import pandokia.pcgi
        pandokia.pcgi.run()
        return
    else:
        if len(argv) < 2:
            print(__doc__)
            return
        else:
            cmd = argv[1]
            args = argv[2:]
            if cmd == 'check_expected':
                import pandokia.check_expected as x
                return x.run(args)
            if cmd == 'chronic':
                import pandokia.chronic as x
                return x.run(args)
            if cmd == 'clean':
                import pandokia.cleaner
                return pandokia.cleaner.delete_background(args)
            if cmd == 'clean_queries':
                import pandokia.cleaner
                return pandokia.cleaner.clean_queries()
            if cmd == 'clean_db':
                import pandokia.cleaner
                return pandokia.cleaner.clean_db(args)
            if cmd == 'config':
                import pandokia
                f = pandokia.cfg.__file__
                if f.endswith('.pyc') or f.endswith('.pyo'):
                    f = f[:-1]
                print(f)
                return 0
            if cmd == 'delete':
                import pandokia.cleaner
                return pandokia.cleaner.delete(args)
            if cmd == 'dump_table':
                import pandokia.db
                return pandokia.db.cmd_dump_table(args)
            if cmd == 'email':
                import pandokia.contact_notify_select
                return pandokia.contact_notify_select.run(args)
            if cmd == 'export':
                import pandokia.export
                return pandokia.export.run(args)
            if cmd == 'gen_contact':
                import pandokia.gen_contact as x
                return x.run(args)
            if cmd == 'gen_expected':
                import pandokia.gen_expected as x
                return x.run(args)
            if cmd == 'getenv':
                import pandokia.run as x
                return x.export_environment(args)
            if cmd == 'help' or cmd == '-h' or cmd == '--help':
                print(__doc__)
                return
            if cmd == 'import':
                import pandokia.import_data as x
                return x.run(args)
            if cmd == 'hackimport':
                import pandokia.import_data as x
                return x.hack_import(args)
            if cmd == 'import_contact':
                import pandokia.import_contact as x
                return x.run()
            if cmd == 'ok' or cmd == 'okify':
                import pandokia.ok
                return pandokia.ok.run(args)
            if cmd == 'run':
                import pandokia.run as x
                err, lstat = x.run(args)
                return err
            if cmd == 'sql':
                import pandokia.db
                return pandokia.db.sql_files(args)
            if cmd == 'runstatus':
                import pandokia.run_status as x
                err = x.display_interactive(args)
                return err
            if cmd == 'version' or cmd == '--version' or cmd == '-v' or cmd == '-V':
                import pandokia
                print('pandokia %s' % pandokia.__version__)
                print(os.path.dirname(pandokia.__file__))
                return 0
            if cmd == 'webserver':
                import pandokia.webserver
                return pandokia.webserver.run(args)
            if cmd == 'maker':
                import pandokia.runners as x
                print('%s' % os.path.join(os.path.dirname(x.__file__), 'maker'))
                return 0
            if cmd == 'query':
                import pandokia
                return pandokia.cfg.pdk_db.query_to_csv(args[0], sys.stdout)
            if cmd == 'recount':
                import pandokia.cleaner
                return pandokia.cleaner.recount(args)
            if cmd == 'hack':
                import pandokia.hack
                return pandokia.hack.run(args)
        sys.stderr.write('command %s not known\n' % cmd)
        return 1