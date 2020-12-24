# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uta/loading.py
# Compiled at: 2014-09-03 18:12:35
from __future__ import absolute_import, division, print_function, unicode_literals
import datetime, gzip, itertools, logging, time
from bioutils.coordinates import strand_pm_to_int, MINUS_STRAND
import uta, uta.formats.exonset as ufes, uta.formats.geneinfo as ufgi, uta.formats.seqinfo as ufsi, uta.formats.txinfo as ufti
usam = uta.models
logger = logging.getLogger(__name__)

def drop_schema(session, opts, cf):
    if session.bind.name == b'postgresql' and usam.use_schema:
        ddl = b'drop schema if exists ' + usam.schema_name + b' cascade'
        session.execute(ddl)
        session.commit()
        logger.info(ddl)


def create_schema(session, opts, cf):
    """Create and populate initial schema"""
    session.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
    if session.bind.name == b'postgresql' and usam.use_schema:
        session.execute(b'create schema ' + usam.schema_name)
        session.execute((b'alter database {db} set search_path = {search_path}').format(db=session.bind.url.database, search_path=usam.schema_name))
        session.execute(b'set search_path = ' + usam.schema_name)
        session.commit()
    usam.Base.metadata.create_all(session.bind)
    session.add(usam.Meta(key=b'schema_version', value=usam.schema_version))
    session.add(usam.Meta(key=b'created', value=datetime.datetime.now().isoformat()))
    session.commit()
    logger.info(b'created schema')


def load_sql(session, opts, cf):
    """Create views"""
    session.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
    for fn in opts[b'FILES']:
        logger.info(b'loading ' + fn)
        session.execute(open(fn).read())

    session.commit()


def initialize_schema(session, opts, cf):
    """Create and populate initial schema"""
    session.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
    session.add(usam.Origin(name=b'NCBI', url=b'http://www.ncbi.nlm.nih.gov/'))
    session.add(usam.Origin(name=b'NCBI Gene', descr=b'NCBI gene repository', url=b'http://www.ncbi.nlm.nih.gov/gene/', url_ac_fmt=b'http://www.ncbi.nlm.nih.gov/gene/{ac}'))
    session.add(usam.Origin(name=b'NCBI RefSeq', descr=b'NCBI RefSeq (nuccore) repository', url=b'http://www.ncbi.nlm.nih.gov/refseq/', url_ac_fmt=b'http://www.ncbi.nlm.nih.gov/nuccore/{ac}'))
    session.add(usam.Origin(name=b'NCBI seq_gene', descr=b'NCBI "seq_gene" files from FTP site', url=b'ftp://ftp.ncbi.nih.gov/genomes/MapView/Homo_sapiens/sequence/current/initial_release/'))
    session.add(usam.Origin(name=b'Ensembl', descr=b'Ensembl', url=b'http://ensembl.org/'))
    session.add(usam.Origin(name=b'BIC', descr=b'Breast Cancer Information Core', url=b'http://research.nhgri.nih.gov/bic/'))
    session.add(usam.Origin(name=b'LRG', descr=b'Locus Reference Genomic sequence', url=b'http://www.lrg-sequence.org/'))
    session.add(usam.Origin(name=b'uta0', descr=b'UTA version 0', url=b'http://bitbucket.org/uta/uta'))
    session.commit()
    logger.info(b'initialized schema')


def load_seqinfo(session, opts, cf):
    """load Seq entries with accessions from fasta file
    """
    session.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
    sir = ufsi.SeqInfoReader(gzip.open(opts[b'FILE']))
    logger.info(b'opened ' + opts[b'FILE'])
    i_md5 = 0
    for md5, si_iter in itertools.groupby(sorted(sir, key=lambda si: si.md5), key=lambda si: si.md5):
        sis = list(si_iter)
        si = sis[0]
        i_md5 += 1
        if i_md5 % 25 == 1:
            logger.info((b'{i_md5}/???: updated/added seq {md5} with {n} acs ({acs})').format(i_md5=i_md5, md5=md5, n=len(sis), acs=(b',').join(si.ac for si in sis)))
        u_seq = session.query(usam.Seq).filter(usam.Seq.seq_id == md5).first()
        if u_seq is None:
            u_seq = usam.Seq(seq_id=md5, len=si.len, seq=si.seq)
            session.add(u_seq)
            for si in sis:
                u_ori = session.query(usam.Origin).filter(usam.Origin.name == si.origin).one()
                u_seqanno = usam.SeqAnno(origin_id=u_ori.origin_id, seq_id=si.md5, ac=si.ac, descr=si.descr)
                session.add(u_seqanno)

            session.commit()
        else:
            for si in sis:
                u_ori = session.query(usam.Origin).filter(usam.Origin.name == si.origin).one()
                u_seqanno = session.query(usam.SeqAnno).filter(usam.SeqAnno.origin_id == u_ori.origin_id, usam.SeqAnno.seq_id == si.md5, usam.SeqAnno.ac == si.ac).first()
                if u_seqanno:
                    if si.descr and u_seqanno.descr != si.descr:
                        u_seqanno.descr = si.descr
                        session.merge(u_seqanno)
                        logger.info(b'updated description for ' + si.ac)
                else:
                    u_seqanno = usam.SeqAnno(origin_id=u_ori.origin_id, seq_id=si.md5, ac=si.ac, descr=si.descr)
                    session.add(u_seqanno)

            session.commit()
            logger.debug((b'updated annotations for seq {md5} with {n} acs ({acs})').format(md5=md5, n=len(sis), acs=(b',').join(si.ac for si in sis)))

    return


def load_exonsets(session, opts, cf):
    session.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
    known_es = set([ (u_es.tx_ac, u_es.alt_ac, u_es.alt_aln_method) for u_es in session.query(usam.ExonSet) ])
    logger.info((b'{n} known exon_set keys; will skip those during loading').format(n=len(known_es)))
    n_lines = len(gzip.open(opts[b'FILE']).readlines())
    esr = ufes.ExonSetReader(gzip.open(opts[b'FILE']))
    logger.info(b'opened ' + opts[b'FILE'])
    for i_es, es in enumerate(esr):
        key = (es.tx_ac, es.alt_ac, es.method)
        if i_es % 50 == 0 or i_es + 1 == n_lines:
            logger.info((b'{i_es}/{n_lines} {p:.1f}%: loading exonset  ({key})').format(i_es=i_es, n_lines=n_lines, p=(i_es + 1) / n_lines * 100, key=str(key)))
        if key in known_es:
            continue
        known_es.add(key)
        u_es = usam.ExonSet(tx_ac=es.tx_ac, alt_ac=es.alt_ac, alt_aln_method=es.method, alt_strand=es.strand)
        session.add(u_es)
        exons = [ map(int, ex.split(b',')) for ex in es.exons_se_i.split(b';') ]
        exons.sort(reverse=int(es.strand) == MINUS_STRAND)
        for i_ex, ex in enumerate(exons):
            s, e = ex
            u_ex = usam.Exon(exon_set=u_es, start_i=s, end_i=e, ord=i_ex)
            session.add(u_ex)

        session.commit()


def load_geneinfo(session, opts, cf):
    session.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
    gir = ufgi.GeneInfoReader(gzip.open(opts[b'FILE']))
    logger.info(b'opened ' + opts[b'FILE'])
    for i_gi, gi in enumerate(gir):
        session.add(usam.Gene(hgnc=gi.hgnc, maploc=gi.maploc, descr=gi.descr, summary=gi.summary, aliases=gi.aliases))

    session.commit()


def load_txinfo(session, opts, cf):
    session.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
    self_aln_method = b'transcript'
    from bioutils.digests import seq_md5
    from multifastadb import MultiFastaDB
    mfdb = MultiFastaDB([cf.get(b'sequences', b'fasta_directory')], use_meta_index=True)
    known_acs = set([ u_ti.ac for u_ti in session.query(usam.Transcript) ])
    n_lines = len(gzip.open(opts[b'FILE']).readlines())
    tir = ufti.TxInfoReader(gzip.open(opts[b'FILE']))
    logger.info(b'opened ' + opts[b'FILE'])
    for i_ti, ti in enumerate(tir):
        if i_ti % 50 == 0 or i_ti + 1 == n_lines:
            logger.info((b'{i_ti}/{n_lines} {p:.1f}%: loading transcript {ac}').format(i_ti=i_ti, n_lines=n_lines, p=(i_ti + 1) / n_lines * 100, ac=ti.ac))
        if ti.ac in known_acs:
            logger.warning(b'skipping new definition of transcript ' + ti.ac)
            continue
        known_acs.add(ti.ac)
        if ti.exons_se_i == b'':
            logger.warning(ti.ac + b': no exons?!; skipping.')
            continue
        ori = session.query(usam.Origin).filter(usam.Origin.name == ti.origin).one()
        cds_start_i, cds_end_i = map(int, ti.cds_se_i.split(b','))
        cds_seq = mfdb.fetch(ti.ac, cds_start_i, cds_end_i)
        if not cds_seq:
            raise RuntimeError((b'{ac}: not in FASTA database').format(ac=ti.ac))
        cds_md5 = seq_md5(cds_seq)
        u_tx = usam.Transcript(ac=ti.ac, origin=ori, hgnc=ti.hgnc, cds_start_i=cds_start_i, cds_end_i=cds_end_i, cds_md5=cds_md5)
        session.add(u_tx)
        u_es = usam.ExonSet(tx_ac=ti.ac, alt_ac=ti.ac, alt_strand=1, alt_aln_method=self_aln_method)
        session.add(u_es)
        exons = [ map(int, ex.split(b',')) for ex in ti.exons_se_i.split(b';') ]
        for i_ex, ex in enumerate(exons):
            s, e = ex
            u_ex = usam.Exon(exon_set=u_es, start_i=s, end_i=e, ord=i_ex)
            session.add(u_ex)

        session.commit()


aln_sel_sql = b'\nSELECT * FROM tx_alt_exon_pairs_v TAEP\nWHERE NOT EXISTS (\n    SELECT tx_exon_id,alt_exon_id\n    FROM exon_aln EA\n    WHERE EA.tx_exon_id=TAEP.tx_exon_id AND EA.alt_exon_id=TAEP.alt_exon_id\n    )\n'
aln_ins_sql = b'\nINSERT INTO exon_aln (tx_exon_id,alt_exon_id,cigar,added,tx_aseq,alt_aseq) VALUES (%s,%s,%s,%s,%s,%s)\n'

def align_exons(session, opts, cf):
    from bioutils.sequences import reverse_complement
    import psycopg2.extras
    from multifastadb import MultiFastaDB
    update_period = 50
    aligner = cf.get(b'loading', b'aligner', b'needle')
    if aligner == b'utaa':
        import uta_tools_align.align.algorithms as utaaa

        def align_with_utaaa(s1, s2):
            score, cigar = utaaa.needleman_wunsch_gotoh_align(str(s1), str(s2), extended_cigar=True)
            tx_aseq, alt_aseq = utaaa.cigar_alignment(tx_seq, alt_seq, cigar, hide_match=False)
            return (tx_aseq, alt_aseq, cigar.to_string())

        align = align_with_utaaa
    else:
        if aligner == b'llbaa':
            import locus_lib_bio.align.algorithms as llbaa

            def align_with_llb(s1, s2):
                score, cigar = llbaa.needleman_wunsch_gotoh_align(s1, s2, extended_cigar=True)
                tx_aseq, alt_aseq = llbaa.cigar_alignment(tx_seq, alt_seq, cigar, hide_match=False)
                return (tx_aseq, alt_aseq, cigar.to_string())

            align = align_with_llb
        elif aligner == b'needle':
            import uta.utils.alignment as uua

            def align_with_uua(s1, s2):
                tx_aseq, alt_aseq = uua.align2(s1, s2)
                return (tx_aseq, alt_aseq, uua.alignment_cigar_string(tx_aseq, alt_aseq))

            align = align_with_uua
        elif aligner is None:
            raise RuntimeError(b'No aligner specified')
        else:
            raise RuntimeError(b"aligner '" + aligner + b"' not recognized")
        mfdb = MultiFastaDB([cf.get(b'sequences', b'fasta_directory')], use_meta_index=True)
        con = session.bind.pool.connect()
        cur = con.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        cur.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
        sql = aln_sel_sql
        if opts[b'--sql']:
            sql += b' ' + opts[b'SQL']
        sql += b' ORDER BY hgnc'
        cur.execute(sql)
        rows = cur.fetchall()
        n_rows = len(rows)
        ac_warning = set()
        t0 = time.time()
        tx_acs = set()
        for i_r, r in enumerate(rows):
            if r.tx_ac in ac_warning or r.alt_ac in ac_warning:
                continue
            try:
                tx_seq = mfdb.fetch(r.tx_ac, r.tx_start_i, r.tx_end_i)
            except KeyError:
                logger.warning((b"{r.tx_ac}: Not in sequence sources; can't align").format(r=r))
                ac_warning.add(r.tx_ac)
                continue

            try:
                alt_seq = mfdb.fetch(r.alt_ac, r.alt_start_i, r.alt_end_i)
            except KeyError:
                logger.warning((b"{r.alt_ac}: Not in sequence sources; can't align").format(r=r))
                ac_warning.add(r.alt_ac)
                continue

            if r.alt_strand == MINUS_STRAND:
                alt_seq = reverse_complement(alt_seq)
            tx_seq = tx_seq.upper()
            alt_seq = alt_seq.upper()
            tx_aseq, alt_aseq, cigar_str = align(tx_seq, alt_seq)
            added = datetime.datetime.now()
            cur.execute(aln_ins_sql, [r.tx_exon_id, r.alt_exon_id, cigar_str, added, tx_aseq, alt_aseq])
            tx_acs.add(r.tx_ac)
            if i_r == n_rows - 1 or i_r % update_period == 0:
                con.commit()
                speed = (i_r + 1) / (time.time() - t0)
                etr = (n_rows - i_r - 1) / speed
                etr_s = str(datetime.timedelta(seconds=round(etr)))
                logger.info((b'{i_r}/{n_rows} {p_r:.1f}%; committed; speed={speed:.1f} aln/sec; etr={etr:.0f}s ({etr_s}); {n_tx} tx').format(i_r=i_r, n_rows=n_rows, p_r=i_r / n_rows * 100, speed=speed, etr=etr, etr_s=etr_s, n_tx=len(tx_acs)))
                tx_acs = set()

    cur.close()
    con.close()
    return


def load_ncbi_geneinfo(session, opts, cf):
    """
    import data as downloaded (by you) from 
    ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/gene_info.gz
    """
    import uta.parsers.geneinfo
    session.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
    o = session.query(usam.Origin).filter(usam.Origin.name == b'NCBI Gene').one()
    gip = uta.parsers.geneinfo.GeneInfoParser(gzip.open(opts[b'FILE']))
    for gi in gip:
        if gi[b'tax_id'] != b'9606' or gi[b'Symbol_from_nomenclature_authority'] == b'-':
            continue
        g = usam.Gene(gene_id=gi[b'GeneID'], hgnc=gi[b'Symbol_from_nomenclature_authority'], maploc=gi[b'map_location'], descr=gi[b'Full_name_from_nomenclature_authority'], aliases=gi[b'Synonyms'], strand=gi[b''])
        session.add(g)
        logger.info((b'loaded gene {g.hgnc} ({g.descr})').format(g=g))

    session.commit()


def load_sequences(session, opts, cf):
    from multifastadb import MultiFastaDB
    session.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
    mfdb = MultiFastaDB([cf.get(b'sequences', b'fasta_directory')], use_meta_index=True)
    sql = b"\n    select S.seq_id,S.len,array_agg(SA.ac order by SA.ac) as acs\n    from seq S\n    join seq_anno SA on S.seq_id=SA.seq_id\n    where SA.ac ~ '^(U|NP|NG|ENST|NM)' and S.seq is NULL\n    group by S.seq_id,len\n    "

    def _fetch_first(acs):
        for ac in row[b'acs']:
            try:
                return mfdb.fetch(ac)
            except KeyError:
                pass

        return

    for row in session.execute(sql):
        seq = _fetch_first(row[b'acs']).upper()
        if seq is None:
            logger.warn((b'No sequence found for {acs}').format(acs=row[b'acs']))
            continue
        assert row[b'len'] == len(seq), (b'expected a sequence of length {len} for {md5} ({acs}); length {len2}').format(len=len(seq), md5=row[b'seq_id'], acs=row[b'acs'], len2=len(seq))
        session.execute(usam.Seq.__table__.update().values(seq=seq).where(usam.Seq.seq_id == row[b'seq_id']))
        logger.info((b'loaded sequence of length {len} for {md5} ({acs})').format(len=len(seq), md5=row[b'seq_id'], acs=row[b'acs']))
        session.commit()

    return


def load_ncbi_seqgene(session, opts, cf):
    """
    import data as downloaded (by you) as from
    ftp.ncbi.nih.gov/genomes/MapView/Homo_sapiens/sequence/current/initial_release/seq_gene.md.gz
    """

    def _seqgene_recs_to_tx_info(ac, assy, recs):
        ti = {b'ac': ac, 
           b'assy': assy, 
           b'strand': strand_pm_to_int(recs[0][b'chr_orient']), 
           b'gene_id': int(recs[0][b'feature_id'].replace(b'GeneID:', b'')) if b'GeneID' in recs[0][b'feature_id'] else None}
        segs = [ (r[b'feature_type'], int(r[b'chr_start']) - 1, int(r[b'chr_stop'])) for r in recs ]
        cds_seg_idxs = [ i for i in range(len(segs)) if segs[i][0] == b'CDS' ]
        ei = cds_seg_idxs[(-1)]
        ti[b'cds_end_i'] = segs[ei][2]
        if ei < len(segs) - 1:
            if segs[ei][2] == segs[(ei + 1)][1]:
                segs[ei:(ei + 2)] = [
                 (
                  b'M', segs[ei][1], segs[(ei + 1)][2])]
        ei = cds_seg_idxs[0]
        ti[b'cds_start_i'] = segs[ei][1]
        if ei > 0:
            if segs[(ei - 1)][2] == segs[ei][1]:
                segs[(ei - 1):(ei + 1)] = [
                 (
                  b'M', segs[(ei - 1)][1], segs[ei][2])]
        ti[b'exon_se_i'] = [ s[1:3] for s in segs ]
        return ti

    import uta.parsers.seqgene
    session.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
    o_refseq = session.query(usam.Origin).filter(usam.Origin.name == b'NCBI RefSeq').one()
    o_seqgene = session.query(usam.Origin).filter(usam.Origin.name == b'NCBI seq_gene').one()
    sg_filter = lambda r: r[b'transcript'].startswith(b'NM_') and r[b'group_label'] == b'GRCh37.p10-Primary Assembly' and r[b'feature_type'] in ('CDS',
                                                                                                                       'UTR')
    sgparser = uta.parsers.seqgene.SeqGeneParser(gzip.open(opts[b'FILE']), filter=sg_filter)
    slurp = sorted(list(sgparser), key=lambda r: (
     r[b'transcript'], r[b'group_label'], r[b'chr_start'], r[b'chr_stop']))
    for k, i in itertools.groupby(slurp, key=lambda r: (r[b'transcript'], r[b'group_label'])):
        ac, assy = k
        ti = _seqgene_recs_to_tx_info(ac, assy, list(i))
        resp = session.query(usam.Transcript).filter(usam.Transcript.ac == ac)
        if resp.count() == 0:
            t = usam.Transcript(ac=ac, origin=o_refseq, gene_id=ti[b'gene_id'])
            session.add(t)
        else:
            t = resp.one()
        chr_ac = uta.lut.chr_to_NC()
        es = usam.ExonSet(transcript_id=t.transcript_id, ref_nseq_id=99, strand=ti[b'strand'], cds_start_i=ti[b'cds_start_i'], cds_end_i=ti[b'cds_end_i'])


def grant_permissions(session, opts, cf):
    session.execute((b'set role {admin_role};').format(admin_role=cf.get(b'uta', b'admin_role')))
    schema = b'uta1'
    cmds = [
     (b'alter database {db} set search_path = {schema}').format(db=cf.get(b'uta', b'database'), schema=schema),
     b'grant usage on schema ' + schema + b' to PUBLIC']
    sql = (b"select concat(schemaname,'.',tablename) as fqrn from pg_tables where schemaname='{schema}'").format(schema=schema)
    rows = list(session.execute(sql))
    cmds += [ (b'grant select on {fqrn} to PUBLIC').format(fqrn=row[b'fqrn']) for row in rows ]
    cmds += [ (b'alter table {fqrn} owner to uta_admin').format(fqrn=row[b'fqrn']) for row in rows ]
    sql = (b"select concat(schemaname,'.',viewname) as fqrn from pg_views where schemaname='{schema}'").format(schema=schema)
    rows = list(session.execute(sql))
    cmds += [ (b'grant select on {fqrn} to PUBLIC').format(fqrn=row[b'fqrn']) for row in rows ]
    cmds += [ (b'alter view {fqrn} owner to uta_admin').format(fqrn=row[b'fqrn']) for row in rows ]
    sql = (b"select concat(schemaname,'.',matviewname) as fqrn from pg_matviews where schemaname='{schema}'").format(schema=schema)
    rows = list(session.execute(sql))
    cmds += [ (b'grant select on {fqrn} to PUBLIC').format(fqrn=row[b'fqrn']) for row in rows ]
    cmds += [ (b'alter materialized view {fqrn} owner to uta_admin').format(fqrn=row[b'fqrn']) for row in rows ]
    for cmd in sorted(cmds):
        logger.info(cmd)
        session.execute(cmd)

    session.commit()