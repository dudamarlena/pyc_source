# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/sh2dis/mitsubishi.py
# Compiled at: 2017-12-04 17:32:05
"""Mitsubishi-specific annotations."""
from . import segment
from . import sh2

def fixup_mova(meta, model):
    """Mitsubishi-specific MOVA-related fixups"""
    jump_tbl = meta.extra.args['target']
    jump_off = 0
    while True:
        jumper_addr = jump_tbl + jump_off
        jumper = model.get_location(jumper_addr)
        if isinstance(jumper, sh2.CodeField):
            break
        jumper = sh2.WordField(location=jumper_addr, model=model)
        model.set_location(jumper)
        model.add_reference(jumper_addr, meta.location)
        jumper_ref = jump_tbl + jumper.extra
        sh2.disassemble([(jumper_ref, jumper_addr)], model)
        jumper.comment = 'jsr %s' % model.get_label(jumper_ref)
        jump_off += 2


def fixup_table_axes(meta, registers, model, axes):
    """Annotate the axes for a table."""
    tbl_loc = registers[4]
    tbl = model.get_location(tbl_loc)
    if tbl is None:
        tbl = sh2.LongField(location=tbl_loc, model=model, comment='Result address')
        model.set_location(tbl)
        tbl_ref = sh2.LongField(location=tbl_loc + 4, model=model, comment='Lookup value address')
        model.set_location(tbl_ref)
        tbl_len = sh2.WordField(location=tbl_loc + 8, model=model, comment='Axis length')
        model.set_location(tbl_len)
        cdata = segment.CompositeData(items_per_line=tbl_len.extra, model=model)
        tbl_start = tbl_loc + 10
        tbl_end = tbl_start + tbl_len.extra * 2
        for i in range(tbl_start, tbl_end, 2):
            tbl_data = sh2.WordField(location=i, member_of=cdata, model=model)
            cdata.members.append(tbl_data)
            model.set_location(tbl_data)

        model.add_reference(meta.location, tbl_loc)
        model.add_reference(tbl_loc, meta.location)
        axes[tbl.extra] = tbl.location
    return


def fixup_tables(meta, registers, model, axes):
    """Annotate Mitsubishi-specific tables."""
    tbl_loc = registers[4]
    tbl = model.get_location(tbl_loc)
    if tbl is None:
        tbl_width = 1 if registers[meta.extra.args['m']] == 3112 else 2
        tbl_type = sh2.ByteField if tbl_width == 1 else sh2.WordField
        tbl = tbl_type(location=tbl_loc, model=model)
        model.set_location(tbl)
        tbl.comment = '%dD %s-width table' % (
         tbl.extra, 'byte' if tbl_width == 1 else 'word')
        adder = tbl_type(location=tbl_loc + tbl_width, model=model, comment='Adder')
        model.set_location(adder)
        yaxis = sh2.LongField(location=tbl_loc + 2 * tbl_width, model=model, comment='Y-Axis')
        yaxis_len = 0
        if yaxis.extra in axes:
            yloc = model.get_location(axes[yaxis.extra]).location
            yaxis.comment = 'Y-Axis: 0x%X' % yloc
            yaxis_len = model.get_location(axes[yaxis.extra] + 8).extra
        model.set_location(yaxis)
        tbl_pos = 4 + tbl_width * 2
        xaxis_len = 1
        if tbl.extra == 3:
            xaxis = sh2.LongField(location=tbl_loc + tbl_pos, model=model, comment='X-Axis')
            xaxis_len = 0
            if xaxis.extra in axes:
                xloc = model.get_location(axes[xaxis.extra])
                xloc = xloc.location
                xaxis.comment = 'X-Axis: 0x%X' % xloc
                xaxis_len = model.get_location(axes[xaxis.extra] + 8).extra
            model.set_location(xaxis)
            tbl_pos += 4
            rlen = tbl_type(location=tbl_loc + tbl_pos, model=model, comment='Row length')
            model.set_location(rlen)
            tbl_pos += tbl_width
        if yaxis_len > 0:
            cdata = segment.CompositeData(items_per_line=yaxis_len, model=model)
            tbl_start = tbl_loc + tbl_pos
            tbl_end = tbl_start + yaxis_len * xaxis_len * tbl_width
            for i in range(tbl_start, tbl_end, tbl_width):
                if model.location_isset(i) or tbl_width == 2 and model.location_isset(i + 1):
                    print '!!!!! Short table: 0x%X (at 0x%X)' % (
                     tbl_loc, i)
                    break
                tdata = tbl_type(location=i, model=model, member_of=cdata)
                model.set_location(tdata)
                cdata.members.append(tdata)

    return


def fixup_mut(meta, model):
    """Mitsubishi-specific MUT table annotation"""
    mut_loc = model.get_location(meta.extra.args['target']).extra
    mut_off = 0
    while True:
        mut_entry = sh2.LongField(location=mut_loc + (mut_off << 2), model=model)
        if mut_entry.extra == 4294967295:
            break
        model.set_location(mut_entry)
        model.set_label(mut_entry.extra, 'MUT_%X' % mut_off)
        mut_off += 1

    model.set_label(mut_loc, 'MUT_TABLE')


def callback(meta, registers, model, axes={}):
    """Automatically generate tables and their axes, if possible."""
    if meta.extra.opcode['cmd'] not in sh2.REGISTER_BRANCHERS:
        return
    else:
        reg = registers[meta.extra.args['m']]
        if reg is None or registers[4] is None:
            return
        if reg == 3270:
            fixup_table_axes(meta, registers, model, axes)
        elif reg == 3112 or reg == 3586:
            fixup_tables(meta, registers, model, axes)
        return


def multiscan(model):
    """Scan all physical ranges for multiple items (MOVA, MUT table)."""
    for start, end in model.get_phys_ranges():
        countdown = 0
        movw_found = shll2_found = mut_found = False
        for i in range(start, end):
            if countdown > 0:
                countdown -= 1
                continue
            meta = model.get_location(i)
            if isinstance(meta, sh2.CodeField):
                if meta.extra.opcode['cmd'] == 'mova':
                    fixup_mova(meta, model)
                elif not mut_found:
                    if not movw_found and meta.extra.opcode['cmd'] == 'mov.w':
                        if meta.extra.args['target'] is not None:
                            target = model.get_location(meta.extra.args['target'])
                            if target is not None and target.extra == 191:
                                movw_found = True
                    elif movw_found and meta.extra.opcode['cmd'] == 'shll2':
                        if shll2_found:
                            movw_found = shll2_found = False
                        else:
                            shll2_found = True
                    elif movw_found and shll2_found:
                        if meta.extra.opcode['cmd'] == 'mov.l':
                            if meta.extra.args['target'] is not None:
                                fixup_mut(meta, model)
                                mut_found = True
                        movw_found = shll2_found = False
            if meta is not None:
                countdown = meta.width - 1

    return


def fixups(model):
    """Mitsubishi-specific fixups"""
    meta = model.get_location(0)
    model.set_label(meta.extra, 'init')
    meta = model.get_location(4)
    model.set_label(meta.extra, 'sp')
    meta = model.get_location(16)
    model.set_label(meta.extra, 'reset')
    meta = sh2.WordField(location=3892, model=model)
    model.set_location(meta)
    meta = sh2.WordField(location=3900, model=model)
    model.set_location(meta)
    for pos in range(3904, 3931, 2):
        meta = sh2.WordField(location=pos, model=model)
        if pos == 3908:
            model.set_label(pos, 'ECU_ID1')
        elif pos == 3924:
            model.set_label(pos, 'ECU_ID2')
        model.set_location(meta)

    meta = sh2.LongField(location=3946, model=model)
    model.set_label(3946, 'ECU_part_number')
    model.set_location(meta)
    for pos in range(3950, 3977, 4):
        meta = sh2.LongField(location=pos, model=model)
        model.set_location(meta)

    for pos in range(3978, 3978 + 144, 16):
        meta = sh2.WordField(location=pos, model=model)
        if pos == 4090:
            model.set_label(pos, 'periphery_IMMOB')
        else:
            model.set_label(pos, 'periphery_%X' % pos)
        model.set_location(meta)
        for pos1 in range(pos + 2, pos + 16, 2):
            meta = sh2.WordField(location=pos1, model=model)
            model.set_location(meta)

    meta = sh2.WordField(location=262094, model=model)
    model.set_location(meta)
    model.set_label(meta.location, 'immobilizer')
    model.set_label(3112, 'tbl_lookup_byte')
    model.set_label(3270, 'axis_lookup')
    model.set_label(3586, 'tbl_lookup_word')
    multiscan(model)