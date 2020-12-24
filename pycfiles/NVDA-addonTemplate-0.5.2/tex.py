# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\tex.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.tex

Tool-specific initialization for TeX.
Generates .dvi files from .tex files

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/tex.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os.path, re, shutil, sys, platform, glob, SCons.Action, SCons.Node, SCons.Node.FS, SCons.Util, SCons.Scanner.LaTeX
Verbose = False
must_rerun_latex = True
check_suffixes = [
 '.toc', '.lof', '.lot', '.out', '.nav', '.snm']
all_suffixes = check_suffixes + ['.bbl', '.idx', '.nlo', '.glo', '.acn', '.bcf']
openout_aux_re = re.compile('OUTPUT *(.*\\.aux)')
openout_bcf_re = re.compile('OUTPUT *(.*\\.bcf)')
warning_rerun_str = '(^LaTeX Warning:.*Rerun)|(^Package \\w+ Warning:.*Rerun)'
warning_rerun_re = re.compile(warning_rerun_str, re.MULTILINE)
rerun_citations_str = '^LaTeX Warning:.*\n.*Rerun to get citations correct'
rerun_citations_re = re.compile(rerun_citations_str, re.MULTILINE)
undefined_references_str = '(^LaTeX Warning:.*undefined references)|(^Package \\w+ Warning:.*undefined citations)'
undefined_references_re = re.compile(undefined_references_str, re.MULTILINE)
auxfile_re = re.compile('.', re.MULTILINE)
tableofcontents_re = re.compile('^[^%\\n]*\\\\tableofcontents', re.MULTILINE)
makeindex_re = re.compile('^[^%\\n]*\\\\makeindex', re.MULTILINE)
bibliography_re = re.compile('^[^%\\n]*\\\\bibliography', re.MULTILINE)
bibunit_re = re.compile('^[^%\\n]*\\\\begin\\{bibunit\\}', re.MULTILINE)
multibib_re = re.compile('^[^%\\n]*\\\\newcites\\{([^\\}]*)\\}', re.MULTILINE)
addbibresource_re = re.compile('^[^%\\n]*\\\\(addbibresource|addglobalbib|addsectionbib)', re.MULTILINE)
listoffigures_re = re.compile('^[^%\\n]*\\\\listoffigures', re.MULTILINE)
listoftables_re = re.compile('^[^%\\n]*\\\\listoftables', re.MULTILINE)
hyperref_re = re.compile('^[^%\\n]*\\\\usepackage.*\\{hyperref\\}', re.MULTILINE)
makenomenclature_re = re.compile('^[^%\\n]*\\\\makenomenclature', re.MULTILINE)
makeglossary_re = re.compile('^[^%\\n]*\\\\makeglossary', re.MULTILINE)
makeglossaries_re = re.compile('^[^%\\n]*\\\\makeglossaries', re.MULTILINE)
makeacronyms_re = re.compile('^[^%\\n]*\\\\makeglossaries', re.MULTILINE)
beamer_re = re.compile('^[^%\\n]*\\\\documentclass\\{beamer\\}', re.MULTILINE)
regex = '^[^%\\n]*\\\\newglossary\\s*\\[([^\\]]+)\\]?\\s*\\{([^}]*)\\}\\s*\\{([^}]*)\\}\\s*\\{([^}]*)\\}\\s*\\{([^}]*)\\}'
newglossary_re = re.compile(regex, re.MULTILINE)
biblatex_re = re.compile('^[^%\\n]*\\\\usepackage.*\\{biblatex\\}', re.MULTILINE)
newglossary_suffix = []
include_re = re.compile('^[^%\\n]*\\\\(?:include|input){([^}]*)}', re.MULTILINE)
includeOnly_re = re.compile('^[^%\\n]*\\\\(?:include){([^}]*)}', re.MULTILINE)
includegraphics_re = re.compile('^[^%\\n]*\\\\(?:includegraphics(?:\\[[^\\]]+\\])?){([^}]*)}', re.MULTILINE)
openout_re = re.compile('OUTPUT *(.*)')
TexGraphics = SCons.Scanner.LaTeX.TexGraphics
LatexGraphics = SCons.Scanner.LaTeX.LatexGraphics
TeXAction = None
LaTeXAction = None
BibTeXAction = None
BiberAction = None
MakeIndexAction = None
MakeNclAction = None
MakeGlossaryAction = None
MakeAcronymsAction = None
MakeNewGlossaryAction = None
_null = SCons.Scanner.LaTeX._null
modify_env_var = SCons.Scanner.LaTeX.modify_env_var

def check_file_error_message(utility, filename='log'):
    msg = '%s returned an error, check the %s file\n' % (utility, filename)
    sys.stdout.write(msg)


def FindFile(name, suffixes, paths, env, requireExt=False):
    if requireExt:
        name, ext = SCons.Util.splitext(name)
        if ext:
            name = name + ext
    if Verbose:
        print " searching for '%s' with extensions: " % name, suffixes
    for path in paths:
        testName = os.path.join(path, name)
        if Verbose:
            print " look for '%s'" % testName
        if os.path.isfile(testName):
            if Verbose:
                print " found '%s'" % testName
            return env.fs.File(testName)
        name_ext = SCons.Util.splitext(testName)[1]
        if name_ext:
            continue
        for suffix in suffixes:
            testNameExt = testName + suffix
            if Verbose:
                print " look for '%s'" % testNameExt
            if os.path.isfile(testNameExt):
                if Verbose:
                    print " found '%s'" % testNameExt
                return env.fs.File(testNameExt)

    if Verbose:
        print " did not find '%s'" % name
    return


def InternalLaTeXAuxAction(XXXLaTeXAction, target=None, source=None, env=None):
    """A builder for LaTeX files that checks the output in the aux file
    and decides how many times to use LaTeXAction, and BibTeXAction."""
    global BibTeXAction
    global BiberAction
    global LaTeXAction
    global MakeAcronymsAction
    global MakeGlossaryAction
    global MakeIndexAction
    global MakeNclAction
    global must_rerun_latex
    if XXXLaTeXAction == LaTeXAction:
        callerSuffix = '.dvi'
    else:
        callerSuffix = env['PDFSUFFIX']
    basename = SCons.Util.splitext(str(source[0]))[0]
    basedir = os.path.split(str(source[0]))[0]
    basefile = os.path.split(str(basename))[1]
    abspath = os.path.abspath(basedir)
    targetext = os.path.splitext(str(target[0]))[1]
    targetdir = os.path.split(str(target[0]))[0]
    saved_env = {}
    for var in SCons.Scanner.LaTeX.LaTeX.env_variables:
        saved_env[var] = modify_env_var(env, var, abspath)

    targetbase = os.path.join(targetdir, basefile)
    src_content = source[0].get_text_contents()
    run_makeindex = makeindex_re.search(src_content) and not os.path.isfile(targetbase + '.idx')
    run_nomenclature = makenomenclature_re.search(src_content) and not os.path.isfile(targetbase + '.nlo')
    run_glossary = makeglossary_re.search(src_content) and not os.path.isfile(targetbase + '.glo')
    run_glossaries = makeglossaries_re.search(src_content) and not os.path.isfile(targetbase + '.glo')
    run_acronyms = makeacronyms_re.search(src_content) and not os.path.isfile(targetbase + '.acn')
    saved_hashes = {}
    suffix_nodes = {}
    for suffix in all_suffixes + sum(newglossary_suffix, []):
        theNode = env.fs.File(targetbase + suffix)
        suffix_nodes[suffix] = theNode
        saved_hashes[suffix] = theNode.get_csig()

    if Verbose:
        print 'hashes: ', saved_hashes
    must_rerun_latex = True
    already_bibtexed = []

    def check_MD5(filenode, suffix):
        global must_rerun_latex
        filenode.clear_memoized_values()
        filenode.ninfo = filenode.new_ninfo()
        new_md5 = filenode.get_csig()
        if saved_hashes[suffix] == new_md5:
            if Verbose:
                print 'file %s not changed' % (targetbase + suffix)
            return False
        saved_hashes[suffix] = new_md5
        must_rerun_latex = True
        if Verbose:
            print 'file %s changed, rerunning Latex, new hash = ' % (targetbase + suffix), new_md5
        return True

    resultfilename = targetbase + callerSuffix
    count = 0
    while must_rerun_latex and count < int(env.subst('$LATEXRETRIES')):
        result = XXXLaTeXAction(target, source, env)
        if result != 0:
            return result
        count = count + 1
        must_rerun_latex = False
        logfilename = targetbase + '.log'
        logContent = ''
        if os.path.isfile(logfilename):
            logContent = open(logfilename, 'rb').read()
        flsfilename = targetbase + '.fls'
        flsContent = ''
        auxfiles = []
        if os.path.isfile(flsfilename):
            flsContent = open(flsfilename, 'rb').read()
            auxfiles = openout_aux_re.findall(flsContent)
            dups = {}
            for x in auxfiles:
                dups[x] = 1

            auxfiles = list(dups.keys())
        bcffiles = []
        if os.path.isfile(flsfilename):
            flsContent = open(flsfilename, 'rb').read()
            bcffiles = openout_bcf_re.findall(flsContent)
            dups = {}
            for x in bcffiles:
                dups[x] = 1

            bcffiles = list(dups.keys())
        if Verbose:
            print 'auxfiles ', auxfiles
            print 'bcffiles ', bcffiles
        for auxfilename in auxfiles:
            if auxfilename not in already_bibtexed:
                already_bibtexed.append(auxfilename)
                target_aux = os.path.join(targetdir, auxfilename)
                if os.path.isfile(target_aux):
                    content = open(target_aux, 'rb').read()
                    if content.find('bibdata') != -1:
                        if Verbose:
                            print 'Need to run bibtex on ', auxfilename
                        bibfile = env.fs.File(SCons.Util.splitext(target_aux)[0])
                        result = BibTeXAction(bibfile, bibfile, env)
                        if result != 0:
                            check_file_error_message(env['BIBTEX'], 'blg')
                        must_rerun_latex = True

        for bcffilename in bcffiles:
            if bcffilename not in already_bibtexed:
                already_bibtexed.append(bcffilename)
                target_bcf = os.path.join(targetdir, bcffilename)
                if os.path.isfile(target_bcf):
                    content = open(target_bcf, 'rb').read()
                    if content.find('bibdata') != -1:
                        if Verbose:
                            print 'Need to run biber on ', bcffilename
                        bibfile = env.fs.File(SCons.Util.splitext(target_bcf)[0])
                        result = BiberAction(bibfile, bibfile, env)
                        if result != 0:
                            check_file_error_message(env['BIBER'], 'blg')
                        must_rerun_latex = True

        if check_MD5(suffix_nodes['.idx'], '.idx') or count == 1 and run_makeindex:
            if Verbose:
                print 'Need to run makeindex'
            idxfile = suffix_nodes['.idx']
            result = MakeIndexAction(idxfile, idxfile, env)
            if result != 0:
                check_file_error_message(env['MAKEINDEX'], 'ilg')
                return result
        for index in check_suffixes:
            check_MD5(suffix_nodes[index], index)

        if check_MD5(suffix_nodes['.nlo'], '.nlo') or count == 1 and run_nomenclature:
            if Verbose:
                print 'Need to run makeindex for nomenclature'
            nclfile = suffix_nodes['.nlo']
            result = MakeNclAction(nclfile, nclfile, env)
            if result != 0:
                check_file_error_message('%s (nomenclature)' % env['MAKENCL'], 'nlg')
        if check_MD5(suffix_nodes['.glo'], '.glo') or count == 1 and run_glossaries or count == 1 and run_glossary:
            if Verbose:
                print 'Need to run makeindex for glossary'
            glofile = suffix_nodes['.glo']
            result = MakeGlossaryAction(glofile, glofile, env)
            if result != 0:
                check_file_error_message('%s (glossary)' % env['MAKEGLOSSARY'], 'glg')
        if check_MD5(suffix_nodes['.acn'], '.acn') or count == 1 and run_acronyms:
            if Verbose:
                print 'Need to run makeindex for acronyms'
            acrfile = suffix_nodes['.acn']
            result = MakeAcronymsAction(acrfile, acrfile, env)
            if result != 0:
                check_file_error_message('%s (acronyms)' % env['MAKEACRONYMS'], 'alg')
                return result
        for ig in range(len(newglossary_suffix)):
            if check_MD5(suffix_nodes[newglossary_suffix[ig][2]], newglossary_suffix[ig][2]) or count == 1:
                if Verbose:
                    print 'Need to run makeindex for newglossary'
                newglfile = suffix_nodes[newglossary_suffix[ig][2]]
                MakeNewGlossaryAction = SCons.Action.Action('$MAKENEWGLOSSARYCOM ${SOURCE.filebase}%s -s ${SOURCE.filebase}.ist -t ${SOURCE.filebase}%s -o ${SOURCE.filebase}%s' % (newglossary_suffix[ig][2], newglossary_suffix[ig][0], newglossary_suffix[ig][1]), '$MAKENEWGLOSSARYCOMSTR')
                result = MakeNewGlossaryAction(newglfile, newglfile, env)
                if result != 0:
                    check_file_error_message('%s (newglossary)' % env['MAKENEWGLOSSARY'], newglossary_suffix[ig][0])
                    return result

        if warning_rerun_re.search(logContent):
            must_rerun_latex = True
            if Verbose:
                print 'rerun Latex due to latex or package rerun warning'
        if rerun_citations_re.search(logContent):
            must_rerun_latex = True
            if Verbose:
                print "rerun Latex due to 'Rerun to get citations correct' warning"
        if undefined_references_re.search(logContent):
            must_rerun_latex = True
            if Verbose:
                print 'rerun Latex due to undefined references or citations'
        if count >= int(env.subst('$LATEXRETRIES')) and must_rerun_latex:
            print 'reached max number of retries on Latex ,', int(env.subst('$LATEXRETRIES'))

    if not (str(target[0]) == resultfilename and os.path.isfile(resultfilename)):
        if os.path.isfile(resultfilename):
            print 'move %s to %s' % (resultfilename, str(target[0]))
            shutil.move(resultfilename, str(target[0]))
    for var in SCons.Scanner.LaTeX.LaTeX.env_variables:
        if var == 'TEXPICTS':
            continue
        if saved_env[var] is _null:
            try:
                del env['ENV'][var]
            except KeyError:
                pass

        else:
            env['ENV'][var] = saved_env[var]

    return result


def LaTeXAuxAction(target=None, source=None, env=None):
    result = InternalLaTeXAuxAction(LaTeXAction, target, source, env)
    return result


LaTeX_re = re.compile('\\\\document(style|class)')

def is_LaTeX(flist, env, abspath):
    """Scan a file list to decide if it's TeX- or LaTeX-flavored."""
    savedpath = modify_env_var(env, 'TEXINPUTS', abspath)
    paths = env['ENV']['TEXINPUTS']
    if SCons.Util.is_List(paths):
        pass
    else:
        paths = paths.split(os.pathsep)
    if savedpath is _null:
        try:
            del env['ENV']['TEXINPUTS']
        except KeyError:
            pass

    else:
        env['ENV']['TEXINPUTS'] = savedpath
    if Verbose:
        print 'is_LaTeX search path ', paths
        print 'files to search :', flist
    for f in flist:
        if Verbose:
            print ' checking for Latex source ', str(f)
        content = f.get_text_contents()
        if LaTeX_re.search(content):
            if Verbose:
                print 'file %s is a LaTeX file' % str(f)
            return 1
        if Verbose:
            print 'file %s is not a LaTeX file' % str(f)
        inc_files = []
        inc_files.extend(include_re.findall(content))
        if Verbose:
            print "files included by '%s': " % str(f), inc_files
        for src in inc_files:
            srcNode = FindFile(src, ['.tex', '.ltx', '.latex'], paths, env, requireExt=False)
            fileList = [
             srcNode]
            if Verbose:
                print 'FindFile found ', srcNode
            if srcNode is not None:
                file_test = is_LaTeX(fileList, env, abspath)
            if file_test:
                return file_test

        if Verbose:
            print ' done scanning ', str(f)

    return 0


def TeXLaTeXFunction(target=None, source=None, env=None):
    """A builder for TeX and LaTeX that scans the source file to
    decide the "flavor" of the source and then executes the appropriate
    program."""
    global TeXAction
    basedir = os.path.split(str(source[0]))[0]
    abspath = os.path.abspath(basedir)
    if is_LaTeX(source, env, abspath):
        result = LaTeXAuxAction(target, source, env)
        if result != 0:
            check_file_error_message(env['LATEX'])
    else:
        result = TeXAction(target, source, env)
        if result != 0:
            check_file_error_message(env['TEX'])
    return result


def TeXLaTeXStrFunction(target=None, source=None, env=None):
    """A strfunction for TeX and LaTeX that scans the source file to
    decide the "flavor" of the source and then returns the appropriate
    command string."""
    if env.GetOption('no_exec'):
        basedir = os.path.split(str(source[0]))[0]
        abspath = os.path.abspath(basedir)
        if is_LaTeX(source, env, abspath):
            result = env.subst('$LATEXCOM', 0, target, source) + ' ...'
        else:
            result = env.subst('$TEXCOM', 0, target, source) + ' ...'
    else:
        result = ''
    return result


def tex_eps_emitter(target, source, env):
    """An emitter for TeX and LaTeX sources when
    executing tex or latex. It will accept .ps and .eps
    graphics files
    """
    target, source = tex_emitter_core(target, source, env, TexGraphics)
    return (
     target, source)


def tex_pdf_emitter(target, source, env):
    """An emitter for TeX and LaTeX sources when
    executing pdftex or pdflatex. It will accept graphics
    files of types .pdf, .jpg, .png, .gif, and .tif
    """
    target, source = tex_emitter_core(target, source, env, LatexGraphics)
    return (
     target, source)


def ScanFiles(theFile, target, paths, file_tests, file_tests_search, env, graphics_extensions, targetdir, aux_files):
    """ For theFile (a Node) update any file_tests and search for graphics files
    then find all included files and call ScanFiles recursively for each of them"""
    content = theFile.get_text_contents()
    if Verbose:
        print ' scanning ', str(theFile)
    for i in range(len(file_tests_search)):
        if file_tests[i][0] is None:
            if Verbose:
                print 'scan i ', i, ' files_tests[i] ', file_tests[i], file_tests[i][1]
            file_tests[i][0] = file_tests_search[i].search(content)
            if Verbose and file_tests[i][0]:
                print '   found match for ', file_tests[i][1][(-1)]
            if file_tests[i][0] and file_tests[i][1][(-1)] == 'newglossary':
                findresult = file_tests_search[i].findall(content)
                for l in range(len(findresult)):
                    file_tests[i][1].insert(0, '.' + findresult[l][3])
                    file_tests[i][1].insert(0, '.' + findresult[l][2])
                    file_tests[i][1].insert(0, '.' + findresult[l][0])
                    suffix_list = ['.' + findresult[l][0], '.' + findresult[l][2], '.' + findresult[l][3]]
                    newglossary_suffix.append(suffix_list)

                if Verbose:
                    print ' new suffixes for newglossary ', newglossary_suffix

    incResult = includeOnly_re.search(content)
    if incResult:
        aux_files.append(os.path.join(targetdir, incResult.group(1)))
    if Verbose:
        print '\\include file names : ', aux_files
    inc_files = []
    inc_files.extend(include_re.findall(content))
    if Verbose:
        print "files included by '%s': " % str(theFile), inc_files
    for src in inc_files:
        srcNode = FindFile(src, ['.tex', '.ltx', '.latex'], paths, env, requireExt=False)
        if srcNode is not None:
            file_tests = ScanFiles(srcNode, target, paths, file_tests, file_tests_search, env, graphics_extensions, targetdir, aux_files)

    if Verbose:
        print ' done scanning ', str(theFile)
    return file_tests


def tex_emitter_core(target, source, env, graphics_extensions):
    """An emitter for TeX and LaTeX sources.
    For LaTeX sources we try and find the common created files that
    are needed on subsequent runs of latex to finish tables of contents,
    bibliographies, indices, lists of figures, and hyperlink references.
    """
    basename = SCons.Util.splitext(str(source[0]))[0]
    basefile = os.path.split(str(basename))[1]
    targetdir = os.path.split(str(target[0]))[0]
    targetbase = os.path.join(targetdir, basefile)
    basedir = os.path.split(str(source[0]))[0]
    abspath = os.path.abspath(basedir)
    target[0].attributes.path = abspath
    emit_suffixes = [
     '.aux', '.log', '.ilg', '.blg', '.nls', '.nlg', '.gls', '.glg', '.alg'] + all_suffixes
    auxfilename = targetbase + '.aux'
    logfilename = targetbase + '.log'
    flsfilename = targetbase + '.fls'
    syncfilename = targetbase + '.synctex.gz'
    env.SideEffect(auxfilename, target[0])
    env.SideEffect(logfilename, target[0])
    env.SideEffect(flsfilename, target[0])
    env.SideEffect(syncfilename, target[0])
    if Verbose:
        print 'side effect :', auxfilename, logfilename, flsfilename, syncfilename
    env.Clean(target[0], auxfilename)
    env.Clean(target[0], logfilename)
    env.Clean(target[0], flsfilename)
    env.Clean(target[0], syncfilename)
    content = source[0].get_text_contents()
    file_tests_search = [
     auxfile_re,
     makeindex_re,
     bibliography_re,
     bibunit_re,
     multibib_re,
     addbibresource_re,
     tableofcontents_re,
     listoffigures_re,
     listoftables_re,
     hyperref_re,
     makenomenclature_re,
     makeglossary_re,
     makeglossaries_re,
     makeacronyms_re,
     beamer_re,
     newglossary_re,
     biblatex_re]
    file_tests_suff = [
     [
      '.aux', 'aux_file'],
     [
      '.idx', '.ind', '.ilg', 'makeindex'],
     [
      '.bbl', '.blg', 'bibliography'],
     [
      '.bbl', '.blg', 'bibunit'],
     [
      '.bbl', '.blg', 'multibib'],
     [
      '.bbl', '.blg', '.bcf', 'addbibresource'],
     [
      '.toc', 'contents'],
     [
      '.lof', 'figures'],
     [
      '.lot', 'tables'],
     [
      '.out', 'hyperref'],
     [
      '.nlo', '.nls', '.nlg', 'nomenclature'],
     [
      '.glo', '.gls', '.glg', 'glossary'],
     [
      '.glo', '.gls', '.glg', 'glossaries'],
     [
      '.acn', '.acr', '.alg', 'acronyms'],
     [
      '.nav', '.snm', '.out', '.toc', 'beamer'],
     [
      'newglossary'],
     [
      '.bcf', '.blg', 'biblatex']]
    file_tests = []
    for i in range(len(file_tests_search)):
        file_tests.append([None, file_tests_suff[i]])

    savedpath = modify_env_var(env, 'TEXINPUTS', abspath)
    paths = env['ENV']['TEXINPUTS']
    if SCons.Util.is_List(paths):
        pass
    else:
        paths = paths.split(os.pathsep)
    if savedpath is _null:
        try:
            del env['ENV']['TEXINPUTS']
        except KeyError:
            pass

    else:
        env['ENV']['TEXINPUTS'] = savedpath
    if Verbose:
        print 'search path ', paths
    aux_files = []
    file_tests = ScanFiles(source[0], target, paths, file_tests, file_tests_search, env, graphics_extensions, targetdir, aux_files)
    for theSearch, suffix_list in file_tests:
        if Verbose and theSearch:
            print 'check side effects for ', suffix_list[(-1)]
        if theSearch != None or not source[0].exists():
            file_list = [
             targetbase]
            if suffix_list[(-1)] == 'bibunit':
                file_basename = os.path.join(targetdir, 'bu*.aux')
                file_list = glob.glob(file_basename)
                for i in range(len(file_list)):
                    file_list.append(SCons.Util.splitext(file_list[i])[0])

            if suffix_list[(-1)] == 'multibib':
                for multibibmatch in multibib_re.finditer(content):
                    if Verbose:
                        print 'multibib match ', multibibmatch.group(1)
                    if multibibmatch != None:
                        baselist = multibibmatch.group(1).split(',')
                        if Verbose:
                            print 'multibib list ', baselist
                        for i in range(len(baselist)):
                            file_list.append(os.path.join(targetdir, baselist[i]))

            for file_name in file_list:
                for suffix in suffix_list[:-1]:
                    env.SideEffect(file_name + suffix, target[0])
                    if Verbose:
                        print 'side effect tst :', file_name + suffix, ' target is ', str(target[0])
                    env.Clean(target[0], file_name + suffix)

    for aFile in aux_files:
        aFile_base = SCons.Util.splitext(aFile)[0]
        env.SideEffect(aFile_base + '.aux', target[0])
        if Verbose:
            print 'side effect aux :', aFile_base + '.aux'
        env.Clean(target[0], aFile_base + '.aux')

    if os.path.isfile(flsfilename):
        content = open(flsfilename, 'rb').read()
        out_files = openout_re.findall(content)
        myfiles = [auxfilename, logfilename, flsfilename, targetbase + '.dvi', targetbase + '.pdf']
        for filename in out_files[:]:
            if filename in myfiles:
                out_files.remove(filename)

        env.SideEffect(out_files, target[0])
        if Verbose:
            print 'side effect fls :', out_files
        env.Clean(target[0], out_files)
    return (target, source)


TeXLaTeXAction = None

def generate(env):
    """Add Builders and construction variables for TeX to an Environment."""
    global TeXLaTeXAction
    if TeXLaTeXAction is None:
        TeXLaTeXAction = SCons.Action.Action(TeXLaTeXFunction, strfunction=TeXLaTeXStrFunction)
    env.AppendUnique(LATEXSUFFIXES=SCons.Tool.LaTeXSuffixes)
    generate_common(env)
    import dvi
    dvi.generate(env)
    bld = env['BUILDERS']['DVI']
    bld.add_action('.tex', TeXLaTeXAction)
    bld.add_emitter('.tex', tex_eps_emitter)
    return


def generate_darwin(env):
    try:
        environ = env['ENV']
    except KeyError:
        environ = {}
        env['ENV'] = environ

    if platform.system() == 'Darwin':
        try:
            ospath = env['ENV']['PATHOSX']
        except:
            ospath = None

        if ospath:
            env.AppendENVPath('PATH', ospath)
    return


def generate_common(env):
    """Add internal Builders and construction variables for LaTeX to an Environment."""
    global BibTeXAction
    global BiberAction
    global LaTeXAction
    global MakeAcronymsAction
    global MakeGlossaryAction
    global MakeIndexAction
    global MakeNclAction
    global TeXAction
    generate_darwin(env)
    if TeXAction is None:
        TeXAction = SCons.Action.Action('$TEXCOM', '$TEXCOMSTR')
    if LaTeXAction is None:
        LaTeXAction = SCons.Action.Action('$LATEXCOM', '$LATEXCOMSTR')
    if BibTeXAction is None:
        BibTeXAction = SCons.Action.Action('$BIBTEXCOM', '$BIBTEXCOMSTR')
    if BiberAction is None:
        BiberAction = SCons.Action.Action('$BIBERCOM', '$BIBERCOMSTR')
    if MakeIndexAction is None:
        MakeIndexAction = SCons.Action.Action('$MAKEINDEXCOM', '$MAKEINDEXCOMSTR')
    if MakeNclAction is None:
        MakeNclAction = SCons.Action.Action('$MAKENCLCOM', '$MAKENCLCOMSTR')
    if MakeGlossaryAction is None:
        MakeGlossaryAction = SCons.Action.Action('$MAKEGLOSSARYCOM', '$MAKEGLOSSARYCOMSTR')
    if MakeAcronymsAction is None:
        MakeAcronymsAction = SCons.Action.Action('$MAKEACRONYMSCOM', '$MAKEACRONYMSCOMSTR')
    try:
        environ = env['ENV']
    except KeyError:
        environ = {}
        env['ENV'] = environ

    v = os.environ.get('HOME')
    if v:
        environ['HOME'] = v
    CDCOM = 'cd '
    if platform.system() == 'Windows':
        CDCOM = 'cd /D '
    env['TEX'] = 'tex'
    env['TEXFLAGS'] = SCons.Util.CLVar('-interaction=nonstopmode -recorder')
    env['TEXCOM'] = CDCOM + '${TARGET.dir} && $TEX $TEXFLAGS ${SOURCE.file}'
    env['PDFTEX'] = 'pdftex'
    env['PDFTEXFLAGS'] = SCons.Util.CLVar('-interaction=nonstopmode -recorder')
    env['PDFTEXCOM'] = CDCOM + '${TARGET.dir} && $PDFTEX $PDFTEXFLAGS ${SOURCE.file}'
    env['LATEX'] = 'latex'
    env['LATEXFLAGS'] = SCons.Util.CLVar('-interaction=nonstopmode -recorder')
    env['LATEXCOM'] = CDCOM + '${TARGET.dir} && $LATEX $LATEXFLAGS ${SOURCE.file}'
    env['LATEXRETRIES'] = 4
    env['PDFLATEX'] = 'pdflatex'
    env['PDFLATEXFLAGS'] = SCons.Util.CLVar('-interaction=nonstopmode -recorder')
    env['PDFLATEXCOM'] = CDCOM + '${TARGET.dir} && $PDFLATEX $PDFLATEXFLAGS ${SOURCE.file}'
    env['BIBTEX'] = 'bibtex'
    env['BIBTEXFLAGS'] = SCons.Util.CLVar('')
    env['BIBTEXCOM'] = CDCOM + '${TARGET.dir} && $BIBTEX $BIBTEXFLAGS ${SOURCE.filebase}'
    env['BIBER'] = 'biber'
    env['BIBERFLAGS'] = SCons.Util.CLVar('')
    env['BIBERCOM'] = CDCOM + '${TARGET.dir} && $BIBER $BIBERFLAGS ${SOURCE.filebase}'
    env['MAKEINDEX'] = 'makeindex'
    env['MAKEINDEXFLAGS'] = SCons.Util.CLVar('')
    env['MAKEINDEXCOM'] = CDCOM + '${TARGET.dir} && $MAKEINDEX $MAKEINDEXFLAGS ${SOURCE.file}'
    env['MAKEGLOSSARY'] = 'makeindex'
    env['MAKEGLOSSARYSTYLE'] = '${SOURCE.filebase}.ist'
    env['MAKEGLOSSARYFLAGS'] = SCons.Util.CLVar('-s ${MAKEGLOSSARYSTYLE} -t ${SOURCE.filebase}.glg')
    env['MAKEGLOSSARYCOM'] = CDCOM + '${TARGET.dir} && $MAKEGLOSSARY ${SOURCE.filebase}.glo $MAKEGLOSSARYFLAGS -o ${SOURCE.filebase}.gls'
    env['MAKEACRONYMS'] = 'makeindex'
    env['MAKEACRONYMSSTYLE'] = '${SOURCE.filebase}.ist'
    env['MAKEACRONYMSFLAGS'] = SCons.Util.CLVar('-s ${MAKEACRONYMSSTYLE} -t ${SOURCE.filebase}.alg')
    env['MAKEACRONYMSCOM'] = CDCOM + '${TARGET.dir} && $MAKEACRONYMS ${SOURCE.filebase}.acn $MAKEACRONYMSFLAGS -o ${SOURCE.filebase}.acr'
    env['MAKENCL'] = 'makeindex'
    env['MAKENCLSTYLE'] = 'nomencl.ist'
    env['MAKENCLFLAGS'] = '-s ${MAKENCLSTYLE} -t ${SOURCE.filebase}.nlg'
    env['MAKENCLCOM'] = CDCOM + '${TARGET.dir} && $MAKENCL ${SOURCE.filebase}.nlo $MAKENCLFLAGS -o ${SOURCE.filebase}.nls'
    env['MAKENEWGLOSSARY'] = 'makeindex'
    env['MAKENEWGLOSSARYCOM'] = CDCOM + '${TARGET.dir} && $MAKENEWGLOSSARY '
    return


def exists(env):
    generate_darwin(env)
    return env.Detect('tex')