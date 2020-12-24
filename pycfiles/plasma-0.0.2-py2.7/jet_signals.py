# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plasma/jet_signals.py
# Compiled at: 2017-02-17 21:50:27
da_current = [
 'c2-ipla']
da_lock = ['c2-loca']
db_out = [
 'b5r-ptot>out']
db = []
db += [ ('b5vr-pbol:{:03d}').format(i) for i in range(1, 28) if i != 16 and i != 23 ]
db += [ ('b5hr-pbol:{:03d}').format(i) for i in range(1, 24) ]
df = []
df += [ ('g1r-lid:{:03d}').format(i) for i in range(2, 9) ]
gs_inductance = [
 'bl-li<s']
gs_fdwdt = ['bl-fdwdt<s']
gs_power_in = ['bl-ptot<s']
gs_wmhd = ['bl-wmhd<s']
gs_gwdens = ['bl-gwdens<s']
gs_torb0 = ['bl-torb0<s']
gs_minrad = ['bl-minrad<s']
kk3 = []
kk3 += [ ('te{:02d}').format(i) for i in range(1, 97) ]
kk3 += [ ('ra{:02d}').format(i) for i in range(1, 97) ]
kk3 += [ ('rc{:02d}').format(i) for i in range(1, 97) ]
kk3 += ['gen']
jpf = [
 da_current,
 da_lock,
 db_out,
 db,
 df,
 gs_inductance,
 gs_fdwdt,
 gs_power_in,
 gs_wmhd,
 gs_gwdens,
 gs_torb0,
 gs_minrad]
ppf = [
 kk3]
jpf_str = [
 'da',
 'da',
 'db',
 'db',
 'df',
 'gs',
 'gs',
 'gs',
 'gs',
 'gs',
 'gs',
 'gs']
ppf_str = [
 'kk3']
subsys_str = [jpf_str, ppf_str]
signal_type = [
 jpf, ppf]
signal_type_str = ['jpf', 'ppf']
signals_dirs = []
for i in range(0, len(signal_type)):
    for j in range(0, len(signal_type[i])):
        signal_group = []
        for k in range(0, len(signal_type[i][j])):
            signal_group += [signal_type_str[i] + '/' + subsys_str[i][j] + '/' + signal_type[i][j][k]]

        signals_dirs += [signal_group]

download_masks = [ [True] * len(sig_list) for sig_list in signals_dirs ]
download_masks[3] = [
 False] * len(signals_dirs[3])
download_masks[(-1)][-1] = [False]
signals_masks = [ [False] * len(sig_list) for sig_list in signals_dirs ]
signals_masks[6] = [
 False]
signals_masks[2] = [
 False]
signals_masks[1] = [False]
signals_masks[0] = [True]
for i, group in enumerate(signals_dirs):
    for j, signal in enumerate(group):
        if 'ra' in signal:
            signals_masks[i][j] = False

plot_masks = [ [False] * len(sig_list) for sig_list in signals_dirs ]
plot_masks[0][0] = True
plot_masks[6][0] = True
group_labels = [
 [
  ' $I_{plasma}$ [A]'],
 [
  ' Mode L. A. [A]'],
 [
  ' $P_{radiated}$ [W]'],
 [
  ' $P_{radiated}$ [W]'],
 [
  ' $\\rho_{plasma}$ [m^-2]'],
 [
  ' $L_{plasma,internal}$'],
 [
  '$\\frac{d}{dt} E_{D}$ [W]'],
 [
  ' $P_{input}$ [W]'],
 [
  '$E_{D}$'],
 [
  'ECE unit?']]