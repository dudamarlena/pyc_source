# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\phaseshifts\phsh.py
# Compiled at: 2014-09-04 17:24:24
"""
phsh.py - quickly generate phase shifts

phsh provides convenience functions to create phase shifts files
suitable for input into LEED-IV programs such as SATLEED and CLEED.

Examples
--------
.. code:: bash
   
   phsh.py -i *.inp -b *.bul -f CLEED -S phase_dir

"""
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division, with_statement
import sys, os, tempfile
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from glob import glob
from shutil import copy
from phaseshifts import model, atorb
from phaseshifts.leed import Converter, CLEED_validator, CSearch
from phaseshifts.lib.libphsh import phsh_rel, phsh_wil, phsh_cav
from phaseshifts.conphas import Conphas
from subprocess import Popen
import platform
__all__ = []
__version__ = b'0.1.5-dev'
__date__ = b'2013-11-15'
__updated__ = b'2014-09-04'
__contact__ = b'liam.deacon@diamond.ac.uk'
DEBUG = 0
TESTRUN = 0
PROFILE = 0
import argparse

def required_length(nmin, nmax):
    """custom action to check range"""

    class RequiredLength(argparse.Action):

        def __call__(self, parser, args, values, option_string=None):
            if not nmin <= len(values) <= nmax:
                msg = b'argument "{f}" requires between '
                (b'{nmin} and {nmax} arguments').format(f=self.dest, nmin=nmin, nmax=nmax)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)

    return RequiredLength


class Wrapper(object):
    """Wrapper class to easily generate phase shifts"""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def autogen_from_input(bulk_file, slab_file, tmp_dir=None, model_name=None, **kwargs):
        """
        Description
        -----------
        Generate phase shifts from a slab/cluster input file.
        
        Parameters
        ----------
        slab_file : str
            Path to the cluster slab MTZ input file.
        bulk_file : str
            Path to the cluster bulk MTZ input file.
        tmp_dir : str
            Temporary directory for intermediate files.
        store : bool or int
            Specify whether to keep generated files.
        format : str
            Specify formatting of generated phase shift files
        range : tuple(float, float, float)
            Specify the energy of the start, stop and step in eV.
        model_name : str
            Name of model.
            
        Returns
        -------
        output_files : list(str)
           A list of phase shift output filenames 
        """
        dummycell = model.Unitcell(1, 2, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        if model_name == None:
            model_name = b'atomic'
        if b'format' in kwargs:
            out_format = kwargs[b'format'].lower()
        else:
            out_format = None
        if b'lmax' in kwargs:
            lmax = kwargs[b'lmax']
        else:
            lmax = 10
        tmp_dir = str(tmp_dir)
        if not os.path.isdir(tmp_dir):
            tmp_dir = tempfile.gettempdir()
        bulk_mtz = model.MTZ_model(dummycell, atoms=[])
        if CLEED_validator.is_CLEED_file(bulk_file):
            bulk_mtz = Converter.import_CLEED(bulk_file, verbose=VERBOSE)
            full_fname = glob(os.path.expanduser(os.path.expandvars(bulk_file)))[0]
            bulk_file = os.path.join(tmp_dir, os.path.splitext(os.path.basename(full_fname))[0] + b'_bulk.i')
            bulk_mtz.gen_input(filename=bulk_file)
        else:
            bulk_mtz.load_from_file(bulk_file)
        slab_mtz = model.MTZ_model(dummycell, atoms=[])
        if CLEED_validator.is_CLEED_file(slab_file):
            slab_mtz = Converter.import_CLEED(slab_file)
            full_fname = glob(os.path.expanduser(os.path.expandvars(slab_file)))[0]
            slab_file = os.path.join(tmp_dir, os.path.splitext(os.path.basename(full_fname))[0] + b'_slab.i')
            slab_mtz.gen_input(filename=slab_file)
        else:
            slab_mtz.load_from_file(slab_file)
        if not isinstance(bulk_mtz, model.MTZ_model):
            raise AttributeError(b'bulk_mtz is not an MTZ_model')
        atomic_dict = {}
        bulk_elements = [ atom.element.symbol for atom in bulk_mtz.atoms ]
        slab_elements = [ atom.element.symbol for atom in slab_mtz.atoms ]
        for elem in set(bulk_elements + slab_elements):
            at_file = os.path.join(tmp_dir, b'at_%s.i' % elem)
            if not os.path.isfile(at_file):
                print(b'\nCalculating atomic charge density for %s...' % elem)
                atomic_dict[elem] = atorb.Atorb.calculate_Q_density(element=elem, output_dir=tmp_dir)
            else:
                atomic_dict[elem] = at_file

        bulk_at_files = [ atomic_dict[atom.element.symbol] for atom in set(bulk_mtz.atoms)
                        ]
        bulk_model_name = os.path.basename(os.path.splitext(bulk_file)[0])
        bulk_atomic_file = bulk_mtz.gen_atomic(input_files=bulk_at_files, output_file=os.path.join(tmp_dir, bulk_model_name + b'_bulk.i'))
        if VERBOSE:
            print(b'\nModel')
            print(b'bulk atoms: %s' % [ s for s in bulk_mtz.atoms ])
            print(b'slab atoms: %s' % [ s for s in slab_mtz.atoms ])
        print(b'\nCalculating bulk muffin-tin potential...')
        if VERBOSE:
            print(b"\tcluster file: '%s'" % bulk_file)
            print(b"\tatomic file: '%s'" % bulk_atomic_file)
            print(b"\tslab calculation: '%s'" % str(False))
            print(b"\toutput file: '%s'" % os.path.join(tmp_dir, bulk_model_name + b'.bmtz'))
            print(b"\tmufftin file: '%s'" % os.path.join(tmp_dir, bulk_model_name + b'_mufftin.d'))
        bulk_mtz_file = bulk_mtz.calculate_MTZ(cluster_file=bulk_file, atomic_file=bulk_atomic_file, slab=False, output_file=os.path.join(tmp_dir, bulk_model_name + b'.bmtz'), mufftin_file=os.path.join(tmp_dir, bulk_model_name + b'_mufftin.d'))
        print(b'Bulk MTZ = %f' % bulk_mtz.mtz)
        slab_at_files = [ atomic_dict[atom.element.symbol] for atom in set(slab_mtz.atoms)
                        ]
        slab_model_name = os.path.basename(os.path.splitext(slab_file)[0])
        slab_atomic_file = slab_mtz.gen_atomic(input_files=slab_at_files, output_file=os.path.join(tmp_dir, slab_model_name + b'_slab.i'))
        mufftin_filepath = os.path.join(tmp_dir, slab_model_name + b'_mufftin.d')
        print(b'\nCalculating slab muff-tin potential...')
        if VERBOSE:
            print(b"\tcluster file: '%s'" % slab_file)
            print(b"\tatomic file: '%s'" % slab_atomic_file)
            print(b'\tslab calculation: %s' % str(True))
            print(b"\toutput file: '%s'" % os.path.join(tmp_dir, slab_model_name + b'.bmtz'))
            print(b"\tmufftin file: '%s'" % os.path.join(tmp_dir, mufftin_filepath))
            print(b'\tmtz value: %s' % str(bulk_mtz.mtz))
        slab_mtz_file = slab_mtz.calculate_MTZ(cluster_file=slab_file, output_file=os.path.join(tmp_dir, slab_model_name + b'.mtz'), atomic_file=slab_atomic_file, mufftin_file=mufftin_filepath, mtz_string=str(bulk_mtz.mtz), slab=True)
        print(b"\nGenerating phase shifts from '%s'..." % os.path.basename(mufftin_filepath))
        filepath = os.path.join(tmp_dir, slab_model_name)
        phasout_filepath = filepath + b'_phasout.i'
        dataph_filepath = filepath + b'_dataph.d'
        phaseshifts = [ atom.tag for atom in set(slab_mtz.atoms) ]
        phasout_files = [ os.path.join(tmp_dir, atom.tag + b'.ph') for atom in set(slab_mtz.atoms)
                        ]
        phsh_files = []
        lmax_dict = {}
        for atom in set(slab_mtz.atoms + bulk_mtz.atoms):
            try:
                lmax_dict[atom.tag] = atom.lmax
            except AttributeError:
                print(atom.tag, b'default lmax used:', lmax)
                lmax_dict[atom.tag] = lmax

        try:
            if slab_mtz.nform == 0 or str(slab_mtz.nform).lower().startswith(b'cav'):
                phsh_cav(mufftin_filepath, phasout_filepath, dataph_filepath, filepath + b'_zph.o')
                phasout_files = Conphas.split_phasout(filename=phasout_filepath, output_filenames=phasout_files)
                for i, phaseshift in enumerate(phaseshifts):
                    filename = os.path.splitext(phasout_files[i])[0]
                    if out_format == b'curve':
                        filename += b'.cur'
                    else:
                        filename += b'.phs'
                    phsh_files.append(filename)
                    print(b"\nRemoving pi/2 jumps in '%s':\n" % os.path.basename(filename))
                    phsh = Conphas(input_files=[phasout_files[i]], output_file=filename, formatting=out_format, lmax=lmax_dict[phaseshift])
                    phsh.calculate()

            if slab_mtz.nform == 1 or str(slab_mtz.nform).lower().startswith(b'wil'):
                phsh_wil(mufftin_filepath, phasout_filepath, dataph_filepath, filepath + b'_zph.o')
                phasout_files = Conphas.split_phasout(filename=phasout_filepath, output_filenames=phasout_files)
            if slab_mtz.nform == 2 or str(slab_mtz.nform).lower().startswith(b'rel'):
                if b'range' in kwargs:
                    try:
                        with open(mufftin_filepath, b'r') as (f):
                            lines = [ line for line in f ]
                        ei, de, ef, lsm, vc = [ t(s) for t, s in zip((float, float, float, int, float), lines[1].replace(b'D', b'E').split()[:5])
                                              ]
                        ei, ef, de = [ t(s) for t, s in zip((
                         float, float, float), kwargs[b'range'])
                                     ]
                        lines[1] = str(b'%12.4f%12.4f%12.4f    %3i    %12.4f\n' % (
                         ei, de, ef, lsm, vc)).replace(b'e', b'D')
                        with open(mufftin_filepath, b'w') as (f):
                            f.write((b'').join([ str(line) for line in lines ]))
                    except any as e:
                        sys.stderr.write(b'Unable to change phase shift energy range - using Barbieri/Van Hove default of 20-300eV in 5eV steps\n')
                        sys.stderr.flush()

                phsh_rel(mufftin_filepath, phasout_filepath, dataph_filepath, filepath + b'_inpdat.txt')
                phasout_files = Conphas.split_phasout(filename=phasout_filepath, output_filenames=phasout_files)
                for i, phaseshift in enumerate(phaseshifts):
                    filename = os.path.splitext(phasout_files[i])[0]
                    if out_format == b'curve':
                        filename += b'.cur'
                    else:
                        filename += b'.phs'
                    phsh_files.append(filename)
                    print(b"\nRemoving pi/2 jumps in '%s':\n" % os.path.basename(filename))
                    phsh = Conphas(input_files=[phasout_files[i]], output_file=filename, formatting=out_format, lmax=lmax_dict[phaseshift])
                    phsh.calculate()

        except AttributeError:
            raise AttributeError(b'MTZ_model has no NFORM (0-2) specified!')

        if b'store' in kwargs and out_format != b'cleed':
            if kwargs[b'store'] != b'.':
                dst = os.path.abspath(os.path.expanduser(os.path.expandvars(kwargs[b'store'])))
            else:
                dst = os.path.abspath(b'.')
            Wrapper._copy_files(phsh_files, dst, verbose=True)
        elif b'CLEED_PHASE' in os.environ and out_format == b'cleed':
            dst = os.path.abspath(os.path.expanduser(os.path.expandvars(b'$CLEED_PHASE')))
            Wrapper._copy_files(phsh_files, dst, verbose=True)
        else:
            Wrapper._copy_files(phsh_files, os.path.abspath(b'.'), verbose=True)
        return phsh_files

    @staticmethod
    def _copy_files(files, dst, verbose=False):
        """copy list of files into destination directory"""
        env = b''
        if platform.system() == b'Windows' and dst.startswith(b'/cygdrive'):
            if os.environ[b'CLEED_PHASE'] == dst:
                env = b'CLEED_PHASE='
            dst = b'"%s"' % (dst.split(b'/')[2] + b':' + os.path.sep.join(dst.split(b'/')[3:]))
        if os.path.isfile(dst):
            dst = os.path.dirname(dst)
        if not os.path.exists(dst):
            try:
                os.makedirs(dst)
            except WindowsError:
                pass

        if verbose:
            print(b"\nCopying files to %s'%s'" % (env, dst))
        for filename in files:
            try:
                copy(filename, dst)
                if verbose:
                    print(os.path.basename(filename))
            except IOError:
                sys.stderr.write(b"Cannot copy file '%s'\n" % filename)
                sys.stderr.flush()


class CLIError(Exception):
    """Generic exception to raise and log different fatal errors."""

    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = b'E: %s' % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def main(argv=None):
    """Command line options."""
    global VERBOSE
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
    if len(argv) == 1:
        argv.append(b'--help')
    program_name = os.path.basename(sys.argv[0])
    program_version = b'v%s' % __version__
    program_build_date = str(__updated__)
    program_version_message = b'%%(prog)s %s (%s)' % (program_version,
     program_build_date)
    program_shortdesc = __import__(b'__main__').__doc__.split(b'\n')[1]
    program_license = b'%s\n\n      Created by Liam Deacon on %s.\n      Copyright 2013-2014 Liam Deacon. All rights reserved.\n\n      Licensed under the MIT license (see LICENSE file for details)\n\n      Please send your feedback, including bug notifications\n      and fixes, to: %s\n\n    usage:-\n    ' % (program_shortdesc, str(__date__), __contact__)
    try:
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument(b'-b', b'--bulk', dest=b'bulk', metavar=b'<bulk_file>', help=b'path to MTZ bulk or CLEED *.bul input file')
        parser.add_argument(b'-i', b'--slab', dest=b'slab', metavar=b'<slab_file>', help=b'path to MTZ slab or CLEED *.inp input file', required=True)
        parser.add_argument(b'-t', b'--tmpdir', dest=b'tmpdir', metavar=b'<temp_dir>', help=b'temporary directory for intermediate file generation')
        parser.add_argument(b'-l', b'--lmax', dest=b'lmax', metavar=b'<lmax>', default=10, type=int, help=b'Maximum angular momentum quantum number [default: %(default)s]')
        parser.add_argument(b'-f', b'--format', dest=b'format', metavar=b'<format>', default=b'CLEED', help=b"Use specific phase shift format i.e. 'cleed' or 'curve' [default: %(default)s]")
        parser.add_argument(b'-r', b'--range', dest=b'range', nargs=b'+', action=required_length(2, 3), type=float, metavar=b'<energy>', default=(20.0,
                                                                                                                                                  600.0,
                                                                                                                                                  5.0), help=b"Energy range in eV with the format: '<start> <stop> [<step>]'. The <step> value is optional. Valid for relativistic calculations only. [default: %(default)s]")
        parser.add_argument(b'-g', b'--generate-only', dest=b'generate', action=b'store_true', default=False, help=b'Exit after generating phaseshifts; do not launch subprocess using PHASESHIFTS_LEED environment variable. [default: %(default)s]')
        parser.add_argument(b'-S', b'--store', dest=b'store', metavar=b'<subdir>', default=False, help=b'Keep intermediate files in subdir when done')
        parser.add_argument(b'-v', b'--verbose', dest=b'verbose', action=b'count', help=b'set verbosity level [default: %(default)s]')
        parser.add_argument(b'-V', b'--version', action=b'version', version=program_version_message)
        args, unknown = parser.parse_known_args()
        verbose = False
        try:
            verbose = args.verbose
            VERBOSE = verbose
        except:
            pass

        if verbose > 0 and len(unknown) > 0:
            for arg in unknown:
                sys.stderr.write(b"phsh - warning: Unknown option '%s'\n" % arg)

            sys.stderr.flush()
        if args.bulk == None:
            args.bulk = str(os.path.splitext(args.slab)[0] + b'.bul')
        if args.store == False:
            args.store = b'.'
        if args.lmax < 1 or args.lmax > 18:
            raise argparse.ArgumentError(b'lmax is not between 1 and 18')
        if len(args.range) < 3:
            args.range = list(args.range).append(5)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise e
        indent = len(program_name) * b' '
        sys.stderr.write(program_name + b': ' + repr(e) + b'\n')
        sys.stderr.write(indent + b'  for help use --help')
        return 2

    if verbose:
        print(b'Phase shift auto-generation parameters')
        print(b'\tbulk input file: %s' % args.bulk)
        print(b'\tslab input file: %s' % args.slab)
        print(b'\tformat: %s' % args.format)
        print(b'\tlmax: %s' % args.lmax)
        print(b'\trange: %s eV' % [ s for s in args.range ])
    phsh_files = Wrapper.autogen_from_input(args.bulk, args.slab, tmp_dir=args.tmpdir, lmax=int(args.lmax), format=args.format, store=args.store, range=args.range)
    if b'PHASESHIFTS_LEED' in os.environ and not args.generate:
        csearch = CSearch(os.path.splitext(args.slab)[0])
        last_iteration = csearch.getIteration(-1)
        if last_iteration is not None:
            it = str(last_iteration).split(b'par:')[0].replace(b' ', b'').replace(b'#', b'').rjust(3, b'0')
            model = os.path.splitext(os.path.basename(args.slab))[0]
            parent = os.path.dirname(args.slab)
            name, ext = os.path.splitext(os.path.basename(args.slab))
            dest = os.path.join(parent, b'phsh_' + model, name + b'_' + it + ext)
            Wrapper._copy_files(phsh_files, dest, verbose)
        leed_cmd = [
         os.environ[b'PHASESHIFTS_LEED']]
        if platform.system() == b'Windows' and leed_cmd.startwith(b'/cygdrive'):
            leed_cmd = b'"%s"' % (leed_cmd.split(b'/')[2] + b':' + os.path.sep.join(leed_cmd.split(b'/')[3:]))
        for arg in argv:
            leed_cmd.append(arg)

        if verbose:
            print(b"phsh - starting subprocess: '%s'..." % (b' ').join(leed_cmd))
        Popen(leed_cmd)
    return


if __name__ == b'__main__':
    if DEBUG:
        sys.argv.append(b'-v')
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile, pstats
        profile_filename = b'wrapper_profile.txt'
        cProfile.run(b'main()', profile_filename)
        statsfile = open(b'profile_stats.txt', b'wb')
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats(b'cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())