# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/BioClients/pubchem/soap/pug_substance_search.py
# Compiled at: 2020-03-30 12:51:55
# Size of source mod 2**32: 9796 bytes
import sys, os, re, urllib, time, getopt, tempfile, pug_utils
PROG = os.path.basename(sys.argv[0])
PUGURL = 'http://pubchem.ncbi.nlm.nih.gov/pug/pug.cgi'
POLL_WAIT = 10
MAX_WAIT = 300
SIM_CUTOFF = 0.8
NMAX = 0

def QueryPug_qkey(qkey, webenv, fmt='smiles', gzip=False, verbose=0):
    if gzip:
        compres = 'gzip'
    else:
        compres = 'none'
    qxml = '<PCT-Data><PCT-Data_input><PCT-InputData>\n  <PCT-InputData_download><PCT-Download> \n    <PCT-Download_uids><PCT-QueryUids>\n      <PCT-QueryUids_entrez><PCT-Entrez>\n        <PCT-Entrez_db>pcsubstance</PCT-Entrez_db>\n        <PCT-Entrez_query-key>%(QKEY)s</PCT-Entrez_query-key>\n        <PCT-Entrez_webenv>%(WEBENV)s</PCT-Entrez_webenv>\n      </PCT-Entrez></PCT-QueryUids_entrez>\n    </PCT-QueryUids></PCT-Download_uids>\n    <PCT-Download_format value="%(FMT)s"/>\n    <PCT-Download_compression value="%(COMPRES)s"/>\n  </PCT-Download></PCT-InputData_download>\n</PCT-InputData></PCT-Data_input></PCT-Data>\n' % {'QKEY':qkey, 
     'WEBENV':webenv,  'FMT':fmt,  'COMPRES':compres}
    if verbose:
        (
         print >> sys.stderr, 'connecting %s...' % PUGURL)
        (print >> sys.stderr, 'submitting query for qkey: %s ...' % qkey)
    f = pug_utils.UrlOpenTry(PUGURL, qxml)
    pugxml = f.read()
    f.close()
    status, reqid, url, qkey, wenv, error = pug_utils.ParsePugXml(pugxml)
    return (status, reqid, url, qkey, wenv, error)


def QueryPug_struct(smiles, sim=False, sim_cutoff=0.8, active=False, mlsmr=False, nmax=10000, verbose=0):
    qxml = '<PCT-Data><PCT-Data_input><PCT-InputData><PCT-InputData_query><PCT-Query>\n  <PCT-Query_type><PCT-QueryType><PCT-QueryType_css>\n    <PCT-QueryCompoundCS>\n    <PCT-QueryCompoundCS_query>\n      <PCT-QueryCompoundCS_query_data>%(SMILES)s</PCT-QueryCompoundCS_query_data>\n    </PCT-QueryCompoundCS_query>\n    <PCT-QueryCompoundCS_type>\n' % {'SMILES': smiles}
    if sim:
        qxml += '      <PCT-QueryCompoundCS_type_similar><PCT-CSSimilarity>\n        <PCT-CSSimilarity_threshold>%(SIM_CUTOFF)d</PCT-CSSimilarity_threshold>\n      </PCT-CSSimilarity></PCT-QueryCompoundCS_type_similar>\n' % {'SIM_CUTOFF': sim_cutoff * 100}
    else:
        qxml += '      <PCT-QueryCompoundCS_type_subss><PCT-CSStructure>\n        <PCT-CSStructure_isotopes value="false"/>\n        <PCT-CSStructure_charges value="false"/>\n        <PCT-CSStructure_tautomers value="false"/>\n        <PCT-CSStructure_rings value="false"/>\n        <PCT-CSStructure_bonds value="true"/>\n        <PCT-CSStructure_chains value="true"/>\n        <PCT-CSStructure_hydrogen value="false"/>\n      </PCT-CSStructure></PCT-QueryCompoundCS_type_subss>\n'
    qxml += '    </PCT-QueryCompoundCS_type>\n    <PCT-QueryCompoundCS_results>%(NMAX)d</PCT-QueryCompoundCS_results>\n    </PCT-QueryCompoundCS>\n  </PCT-QueryType_css></PCT-QueryType>\n' % {'NMAX': nmax}
    if active:
        qxml += '  <PCT-QueryType><PCT-QueryType_cel><PCT-QueryCompoundEL>\n    <PCT-QueryCompoundEL_activity>\n      <PCT-CLByBioActivity value="active">2</PCT-CLByBioActivity>\n    </PCT-QueryCompoundEL_activity>\n  </PCT-QueryCompoundEL></PCT-QueryType_cel></PCT-QueryType>\n'
    else:
        if mlsmr:
            qxml += '  <PCT-QueryType><PCT-QueryType_cel><PCT-QueryCompoundEL>\n    <PCT-QueryCompoundEL_source><PCT-CLByString>\n      <PCT-CLByString_qualifier value="must">1</PCT-CLByString_qualifier>\n      <PCT-CLByString_category>MLSMR</PCT-CLByString_category>\n    </PCT-CLByString></PCT-QueryCompoundEL_source>\n  </PCT-QueryCompoundEL></PCT-QueryType_cel></PCT-QueryType>\n'
        qxml += '  </PCT-Query_type></PCT-Query>\n</PCT-InputData_query></PCT-InputData></PCT-Data_input></PCT-Data>\n'
        if verbose:
            (
             print >> sys.stderr, 'connecting %s...' % PUGURL)
            if sim:
                (
                 print >> sys.stderr, 'query (%f): %s ...' % (sim_cutoff, smiles))
            else:
                (
                 print >> sys.stderr, 'substructure query: %s ...' % smiles)
    f = pug_utils.UrlOpenTry(PUGURL, qxml)
    pugxml = f.read()
    f.close()
    status, reqid, url, qkey, wenv, error = pug_utils.ParsePugXml(pugxml)
    return (status, reqid, qkey, wenv, error)


def ElapsedTime(t_start):
    t_elapsed = time.time() - t_start
    tsec = t_elapsed % 60
    tmin = t_elapsed / 60
    return '%d:%02d' % (tmin, tsec)


if __name__ == '__main__':
    usage = '\n  %(PROG)s - PubChem substructure or similarity search, fetch smiles\n\n  required:\n  --name_substr=<str>   ... name substring query\n  --o=<OUTSMIS> ... output smiles file (w/ CIDs)\n  --fmt=<FMT> ... smiles|sdf [default via filename]\n  --gz           ... output gzipped [default via filename]\n  --out_sids=<OUTSIDS> ... output SIDs (only w/ smiles output)\n  --active            ... active mols only (in any assay)\n  --mlsmr             ... MLSMR mols only\n  --nmax            ... max hits returned\n  --max_wait     ... max wait for query\n  --v            ... verbose\n  --vv           ... very verbose\n  --h            ... this help\n' % {'PROG':PROG, 
     'SIM_CUTOFF':SIM_CUTOFF}

    def ErrorExit(msg):
        (
         print >> sys.stderr, msg)
        sys.exit(1)


    smiles = None
    ofile = None
    verbose = 0
    out_cids_file = None
    similarity = False
    active = False
    mlsmr = False
    fmt = None
    gzip = False
    opts, pargs = getopt.getopt(sys.argv[1:], '', ['h', 'v', 'vv', 'smi=', 'smiles=',
     'o=', 'out=', 'nmax=', 'n=', 'sim_cutoff=', 'similarity', 'sim', 'out_cids=',
     'fmt=', 'gz', 'max_wait=', 'active', 'mlsmr'])
    if not opts:
        ErrorExit(usage)
    for opt, val in opts:
        if opt == '--h':
            ErrorExit(usage)
        elif opt in ('--smiles', '--smi'):
            smiles = val
        elif opt in ('--o', '--out'):
            ofile = val
        elif opt in ('--fmt', '--format'):
            fmt = val
        elif opt == '--out_cids':
            out_cids_file = val
        elif opt in ('--similarity', '--sim'):
            similarity = True
        elif opt == '--active':
            active = True
        elif opt == '--mlsmr':
            mlsmr = True
        elif opt == '--sim_cutoff':
            SIM_CUTOFF = float(val)
        elif opt == '--max_wait':
            MAX_WAIT = int(val)
        elif opt in ('--n', '--nmax'):
            NMAX = int(val)
        elif opt == '--vv':
            verbose = 2
        elif opt == '--v':
            verbose = 1
        else:
            ErrorExit('Illegal option: %s' % val)
    else:
        if not smiles:
            ErrorExit('smiles required\n' + usage)
        elif verbose:
            (
             print >> sys.stderr, 'query: "%s"' % smiles)
        else:
            if ofile:
                fout = file(ofile, 'wb')
                if not fout:
                    ErrorExit('cannot open: %s\n%s' % (ofile, usage))
                elif ofile[-3:] == '.gz':
                    gzip = True
                    ext = re.sub('^.*\\.', '', ofile[:-3])
                else:
                    ext = re.sub('^.*\\.', '', ofile)
                if not fmt:
                    fmt = ext
                if fmt == 'smi':
                    fmt = 'smiles'
                if fmt not in ('smiles', 'sdf'):
                    ErrorExit('format "smiles" or "sdf" required\n' + usage)
            if out_cids_file:
                if fmt == 'sdf':
                    ErrorExit('--out_cids not allowed with SDF output.\n' + usage)
                fout_cids = file(out_cids_file, 'wb')
                if not fout_cids:
                    ErrorExit('cannot open: %s\n%s' % (out_cids_file, usage))
            t0 = time.time()
            status, reqid, qkey, wenv, error = QueryPug_struct(smiles, similarity, SIM_CUTOFF, active, mlsmr, NMAX, verbose)
            if status not in ('success', 'queued', 'running'):
                ErrorExit('query failed; quitting (status=%s,error="%s").' % (status, error))
            if verbose:
                (
                 print >> sys.stderr, 'query status: %s' % status)
            reqid or qkey or ErrorExit('query ok but no ID; quitting.')
        i_poll = 0

    if not qkey:
        if time.time() - t0 > MAX_WAIT:
            pug_utils.PollPug(reqid, 'cancel', verbose)
            ErrorExit('max wait exceeded (%d sec); quitting.' % MAX_WAIT)
        (
         print >> sys.stderr, 'polling PUG [ID=%d]...' % reqid)
        status, reqid_new, url, qkey, wenv, error = pug_utils.PollPug(reqid, 'status', verbose)
        if reqid_new:
            reqid = reqid_new
        if qkey:
            break
        if verbose:
            (
             print >> sys.stderr, '%s elapsed; %d sec wait; status=%s' % (ElapsedTime(t0), POLL_WAIT, status))
        (
         print >> sys.stderr, '%s' % error)
        if re.search('No result found', error, re.I):
            ErrorExit(error)
        time.sleep(POLL_WAIT)
        i_poll += 1
    else:
        status, reqid, url, qkey, wenv, error = QueryPug_qkey(qkey, wenv, fmt, gzip, verbose)
        i_poll = 0
        if not url:
            if time.time() - t0 > MAX_WAIT:
                pug_utils.PollPug(reqid, 'cancel', verbose)
                ErrorExit('max wait exceeded (%d sec); quitting.' % MAX_WAIT)
            (
             print >> sys.stderr, 'polling PUG [ID=%d]...' % reqid)
            status, reqid, url, qkey, wenv, error = pug_utils.PollPug(reqid, 'status', verbose)
            if url:
                break
            if verbose:
                (
                 print >> sys.stderr, '%s elapsed; %d sec wait; status=%s' % (ElapsedTime(t0), POLL_WAIT, status))
            time.sleep(POLL_WAIT)
            i_poll += 1
        else:
            if verbose:
                (
                 print >> sys.stderr, 'query elapsed time: %s' % ElapsedTime(t0))
            elif ofile:
                if verbose:
                    (
                     print >> sys.stderr, 'URL: %s' % url)
                    (print >> sys.stderr, 'downloading to %s...' % ofile)
                fd, tmpfile = tempfile.mkstemp('.txt', PROG)
                f = os.fdopen(fd, 'w')
                nbytes = pug_utils.DownloadUrl(url, f)
                f.close()
                if fmt == 'smiles':
                    ftmp = open(tmpfile)
                    n = 0
                    while True:
                        line = ftmp.readline()
                        if not line:
                            break
                        fields = line.split()
                        if ofile:
                            fout.write('%s %s\n' % (fields[1], fields[0]))
                        if out_cids_file:
                            fout_cids.write('%s\n' % fields[0])
                        n += 1

                    (
                     print >> sys.stderr, 'compounds: %d' % n)
                    ftmp.close()
            else:
                os.system('cp %s %s' % (tmpfile, ofile))
            os.unlink(tmpfile)
            sys.stderr.write('%s: format: %s' % (PROG, fmt))
            if gzip:
                sys.stderr.write('(gzipped)')
            sys.stderr.write('\n')
            if ofile:
                fout.close()
                nbytes = os.stat(ofile).st_size
                (print >> sys.stderr, '%s (%.2fMB)' % (ofile, nbytes / 1000000.0))
            if out_cids_file:
                fout_cids.close()
                nbytes = os.stat(out_cids_file).st_size
                (print >> sys.stderr, '%s (%.2fMB)' % (out_cids_file, nbytes / 1000000.0))
# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break
#      L. 216   996_998  BREAK_LOOP         1100  'to 1100'
# not in loop:
#	break
#      L. 234  1232_1234  BREAK_LOOP         1292  'to 1292'