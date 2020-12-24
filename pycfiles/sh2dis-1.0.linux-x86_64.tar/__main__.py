# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/sh2dis/__main__.py
# Compiled at: 2017-12-04 18:02:08
from __future__ import print_function
import argparse, sys
from . import mitsubishi
from . import segment
from . import sh2
from . import sh7052
from . import sh7055
OUTPUT_SEPARATOR = '         ! ' + '-' * 60

def get_segments(phys):
    """Determine if this is an Evo VIII (7052) or IX (7055) ROM."""
    if len(phys) == 262144:
        return (
         sh7052,
         (
          (
           'ROM', 0, len(phys), phys),
          ('RAM', 4294934528, 4294946816, None),
          ('REG', 4294960128, 4294965344, None)))
    else:
        if len(phys) == 524288:
            return (
             sh7055,
             (
              (
               'ROM', 0, len(phys), phys),
              ('RAM', 4294926336, 4294959104, None),
              ('REG', 4294960128, 4294965344, None)))
        raise ROMError('invalid or unrecognized ROM')
        return


def setup_vectors(model):
    """Pre-define the vector table."""
    for i in range(0, 1024, 4):
        label = None
        comment = None
        kind = sh2.LongField
        if i in model.processor.VECTORS:
            vec = model.processor.VECTORS[i]
            label = vec['name']
            comment = vec['comment']
            if vec['size'] == 1:
                kind = sh2.ByteField
            elif vec['size'] == 2:
                kind = sh2.WordField
        vector = kind(location=i, model=model, comment=comment)
        model.set_location(vector)
        model.set_label(i, label)
        if label is not None and label.startswith('v_'):
            model.set_label(vector.extra, label[2:])

    for addr, vec in list(model.processor.REGISTERS.items()):
        kind = sh2.LongField
        if vec['size'] == 1:
            kind = sh2.ByteField
        elif vec['size'] == 2:
            kind = sh2.WordField
        meta = kind(location=addr, model=model, comment=vec['comment'])
        model.set_location(meta)
        model.set_label(addr, vec['name'])

    return


def disassemble_vectors(model, callback=None):
    """Disassemble the locations referenced by the vector table."""
    vectors = []
    for i in range(0, 1024, 4):
        meta = model.get_location(i)
        try:
            model.get_phys(meta.extra)
        except segment.SegmentError:
            continue

        vectors.append((meta.extra, meta.location))

    sh2.disassemble(vectors, model, callback)


def scan_free_space(model):
    """Scan for contiguous blocks of 0xFF, replace with NullField."""
    for start, end in model.get_phys_ranges():
        countdown = 0
        ff_seen = 0
        for i in range(start, end):
            if countdown > 0:
                countdown -= 1
                continue
            meta = model.get_location(i)
            if meta is None and model.get_phys(i, 1) == chr(255):
                ff_seen += 1
            else:
                if ff_seen > 511:
                    null = sh2.NullField(location=i - ff_seen, width=ff_seen, model=model)
                    model.set_location(null)
                ff_seen = 0
                if meta is not None:
                    countdown = meta.width - 1

    return


def final_output(model, outfile, ranges):
    """Produce a moderately-useful disassembly output"""
    countdown = 0
    in_code = False
    for start, end in ranges:
        for i in range(start, end):
            if countdown > 0:
                countdown -= 1
                continue
            meta = model.get_location(i)
            if in_code:
                if isinstance(meta, sh2.CodeField):
                    rts = model.get_location(i - 4)
                    if isinstance(rts, sh2.CodeField) and rts.extra.opcode['cmd'] == 'rts':
                        print(OUTPUT_SEPARATOR, file=outfile)
                else:
                    in_code = False
                    print(OUTPUT_SEPARATOR, file=outfile)
            elif isinstance(meta, sh2.CodeField):
                in_code = True
                print(OUTPUT_SEPARATOR, file=outfile)
            if meta is None:
                meta = sh2.ByteField(location=i, model=model, unknown_prefix='unk')
            countdown = meta.width - 1
            out = str(meta)
            if isinstance(meta, sh2.NullField):
                out = '%s\n%s\n%s' % (OUTPUT_SEPARATOR, out, OUTPUT_SEPARATOR)
            if out:
                print(out, file=outfile)

    return


def main():
    parser = argparse.ArgumentParser(description='An automated SuperH SH2 disassembler.')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='specify a destination file (default is standard output)')
    parser.add_argument('-m', '--mitsu', action='store_true', help='perform fixups specific to Mitsubishi ECUs')
    parser.add_argument('-r', '--ram', action='store_true', help='include RAM addresses in output')
    parser.add_argument('rom', type=argparse.FileType('rb'), default=sys.stdout)
    args = parser.parse_args()
    processor, segments = get_segments(args.rom.read())
    model = segment.MemoryModel(processor, segments)
    setup_vectors(model)
    disassemble_vectors(model, mitsubishi.callback if args.mitsu else None)
    if args.mitsu:
        mitsubishi.fixups(model)
    scan_free_space(model)
    ranges = []
    if args.ram:
        for seg in model.segments:
            ranges.append((seg.start, seg.end))

    else:
        ranges = model.get_phys_ranges()
    final_output(model, args.output, ranges)
    return


if __name__ == '__main__':
    main()