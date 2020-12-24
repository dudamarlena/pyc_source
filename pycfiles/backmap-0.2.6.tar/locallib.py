# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./local_imports/locallib.py
# Compiled at: 2017-12-29 12:33:42
import os, sys, copy, math, re, matplotlib.pyplot as plt, numpy as np
from Bio import PDB
import matplotlib.pyplot as plt, matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import Geometry, PeptideBuilder
omega_start = -90.0
phi_start = -180.0
psi_start = -180.0
COLORSWITCH = 0.5
c1 = [
 0, 0, 0]
c2 = [1, 1, 0]
c3 = [1, 0, 0]
c4 = [0, 0, 1]
bc = [1, 1, 1]
import seaborn as sns, colorsys
custom_colors = [
 colorsys.hsv_to_rgb(0.5, 0.8, 0.5), colorsys.hsv_to_rgb(0, 0.6, 0.8)]
c3 = custom_colors[0]
c4 = custom_colors[(-1)]
helix_start = 0.31
helix_end = 0.39
sheet_start = 0.45
sheet_end = 0.62
polyproline_end = 0.66
helixR = (
 1, 0, 0)
sheet = (0, 0, 1)
polyproline = (0, 1, 1)
cdict = {'red': (
         (
          0.0, bc[0], bc[0]), (COLORSWITCH, c3[0], c4[0]), (1.0, bc[0], bc[0])), 
   'green': (
           (
            0.0, bc[1], bc[1]), (COLORSWITCH, c3[1], c4[1]), (1.0, bc[1], bc[1])), 
   'blue': (
          (
           0.0, bc[2], bc[2]), (COLORSWITCH, c3[2], c4[2]), (1.0, bc[2], bc[2]))}
cmap_chirality = LinearSegmentedColormap('chirality', cdict)
plt.register_cmap(cmap=cmap_chirality)
cdict = {'red': (
         (
          0.0, c3[0], c3[0]), (COLORSWITCH, bc[0], bc[0]), (1.0, c4[0], c4[0])), 
   'green': (
           (
            0.0, c3[1], c3[1]), (COLORSWITCH, bc[1], bc[1]), (1.0, c4[1], c4[1])), 
   'blue': (
          (
           0.0, c3[2], c3[2]), (COLORSWITCH, bc[2], bc[2]), (1.0, c4[2], c4[2]))}
cmap_chirality_r = LinearSegmentedColormap('chirality_r', cdict)
plt.register_cmap(cmap=cmap_chirality_r)
cdict = {'red': (
         (
          0.0, bc[0], bc[0]), (0.25, c1[0], c2[0]), (0.5, bc[0], bc[0]), (0.75, c3[0], c4[0]), (1.0, bc[0], bc[0])), 
   'green': (
           (
            0.0, bc[1], bc[1]), (0.25, c1[1], c2[1]), (0.5, bc[1], bc[1]), (0.75, c3[1], c4[1]), (1.0, bc[1], bc[1])), 
   'blue': (
          (
           0.0, bc[2], bc[2]), (0.25, c1[2], c2[2]), (0.5, bc[2], bc[2]), (0.75, c3[2], c4[2]), (1.0, bc[2], bc[2]))}
cmap_chirality_signed = LinearSegmentedColormap('chirality_signed', cdict)
plt.register_cmap(cmap=cmap_chirality_signed)
cdict = {'red': (
         (
          0.0, c1[0], c1[0]), (0.25, bc[0], bc[0]), (0.5, c2[0], c3[0]), (0.75, bc[0], bc[0]), (1.0, c4[0], c4[0])), 
   'green': (
           (
            0.0, c1[1], c1[1]), (0.25, bc[1], bc[1]), (0.5, c2[1], c3[1]), (0.75, bc[1], bc[1]), (1.0, c4[1], c4[1])), 
   'blue': (
          (
           0.0, c1[2], c1[2]), (0.25, bc[2], bc[2]), (0.5, c2[2], c3[2]), (0.75, bc[2], bc[2]), (1.0, c4[2], c4[2]))}
cmap_chirality_signed_r = LinearSegmentedColormap('chirality_signed_r', cdict)
plt.register_cmap(cmap=cmap_chirality_signed_r)
cdict = {'red': (
         (
          0.0, bc[0], bc[0]), (helix_start, bc[0], helixR[0]), (helix_end, helixR[0], bc[0]), (sheet_start, bc[0], sheet[0]), (sheet_end, sheet[0], polyproline[0]), (polyproline_end, polyproline[0], bc[0]), (1, bc[0], bc[0])), 
   'green': (
           (
            0.0, bc[1], bc[1]), (helix_start, bc[1], helixR[1]), (helix_end, helixR[1], bc[1]), (sheet_start, bc[1], sheet[1]), (sheet_end, sheet[1], polyproline[1]), (polyproline_end, polyproline[1], bc[1]), (1, bc[1], bc[1])), 
   'blue': (
          (
           0.0, bc[2], bc[2]), (helix_start, bc[2], helixR[2]), (helix_end, helixR[2], bc[2]), (sheet_start, bc[2], sheet[2]), (sheet_end, sheet[2], polyproline[2]), (polyproline_end, polyproline[2], bc[2]), (1, bc[2], bc[2]))}
cmap_ss = LinearSegmentedColormap('ss', cdict)
plt.register_cmap(cmap=cmap_ss)
cdict = {'red': [
         [
          -1, bc[0], bc[0]], [polyproline_end * -1, bc[0], polyproline[0]], [sheet_end * -1, polyproline[0], sheet[0]], [sheet_start * -1, sheet[0], bc[0]], [helix_end * -1, bc[0], helixR[0]], [helix_start * -1, helixR[0], bc[0]], [helix_start, bc[0], helixR[0]], [helix_end, helixR[0], bc[0]], [sheet_start, bc[0], sheet[0]], [sheet_end, sheet[0], polyproline[0]], [polyproline_end, polyproline[0], bc[0]], [1, bc[0], bc[0]]], 
   'green': [
           [
            -1, bc[1], bc[1]], [polyproline_end * -1, bc[1], polyproline[1]], [sheet_end * -1, polyproline[1], sheet[1]], [sheet_start * -1, sheet[1], bc[1]], [helix_end * -1, bc[1], helixR[1]], [helix_start * -1, helixR[1], bc[1]], [helix_start, bc[1], helixR[1]], [helix_end, helixR[1], bc[1]], [sheet_start, bc[1], sheet[1]], [sheet_end, sheet[1], polyproline[1]], [polyproline_end, polyproline[1], bc[1]], [1, bc[1], bc[1]]], 
   'blue': [
          [
           -1, bc[2], bc[2]], [polyproline_end * -1, bc[2], polyproline[2]], [sheet_end * -1, polyproline[2], sheet[2]], [sheet_start * -1, sheet[2], bc[2]], [helix_end * -1, bc[2], helixR[2]], [helix_start * -1, helixR[2], bc[2]], [helix_start, bc[2], helixR[2]], [helix_end, helixR[2], bc[2]], [sheet_start, bc[2], sheet[2]], [sheet_end, sheet[2], polyproline[2]], [polyproline_end, polyproline[2], bc[2]], [1, bc[2], bc[2]]]}
minpos = False
maxpos = False
for color in cdict.keys():
    for i in range(len(cdict[color])):
        if minpos == False:
            minpos = cdict[color][i][0]
        if maxpos == False:
            maxpos = cdict[color][i][0]
        if minpos > cdict[color][i][0]:
            minpos = cdict[color][i][0]
        if maxpos < cdict[color][i][0]:
            maxpos = cdict[color][i][0]

for color in cdict.keys():
    for i in range(len(cdict[color])):
        cdict[color][i][0] = float(cdict[color][i][0] - minpos) / (maxpos - minpos)

cmap_ss_signed = LinearSegmentedColormap('ss_signed', cdict)
plt.register_cmap(cmap=cmap_ss_signed)

def draw_ramachandran_lines(amin=-180, amax=180):
    plt.clf()
    xticks = range(int(amin), int(amax) + 1, 180)
    yticks = range(int(amin), int(amax) + 1, 180)
    for x in xticks:
        if x != amin and x != amax:
            ls = 'solid'
            if x % 360 == 0.0:
                ls = 'dashed'
            plt.plot([x, x], [amin, amax], c='k', ls=ls, lw=1)

    for y in yticks:
        if y != amin and y != amax:
            ls = 'solid'
            if y % 360 == 0.0:
                ls = 'dashed'
            plt.plot([amin, amax], [y, y], c='k', ls=ls, lw=1)

    return 1


def calculate_rmsd(ref_structure, sample_structure, atoms_to_be_aligned1=[], atoms_to_be_aligned2=[]):
    ref_model = ref_structure[0]
    sample_model = sample_structure[0]
    ref_atoms = []
    sample_atoms = []
    align_all = 0
    if not len(atoms_to_be_aligned1):
        align_all = 1
    for ref_chain in ref_model:
        for ref_res in ref_chain:
            if align_all or ref_res.get_id()[1] in atoms_to_be_aligned1:
                ref_atoms.append(ref_res['CA'])
                ref_atoms.append(ref_res['N'])
                ref_atoms.append(ref_res['C'])

    for sample_chain in sample_model:
        for sample_res in sample_chain:
            if align_all or sample_res.get_id()[1] in atoms_to_be_aligned2:
                sample_atoms.append(sample_res['CA'])
                sample_atoms.append(sample_res['N'])
                sample_atoms.append(sample_res['C'])

    super_imposer = PDB.Superimposer()
    super_imposer.set_atoms(ref_atoms, sample_atoms)
    super_imposer.apply(sample_model.get_atoms())
    return (
     super_imposer.rms, sample_structure)


def calculate_rg(ref_structure):
    ref_model = ref_structure[0]
    ref_atoms = []
    for ref_chain in ref_model:
        for ref_res in ref_chain:
            ref_atoms.append(ref_res['CA'].get_coord())

    rc = np.array([0.0, 0.0, 0.0])
    for r in ref_atoms:
        rc += r

    rc = rc / len(ref_atoms)
    rg = 0.0
    for r in ref_atoms:
        rg = np.sqrt((r[0] - rc[0]) ** 2 + (r[1] - rc[1]) ** 2 + (r[2] - rc[2]) ** 2)

    return rg


def calculate_re(ref_structure):
    if len(ref_structure) != 1:
        print 'The structure should only have one conformation/model for a meaningful calculation of r_e. Exiting.'
        exit()
    ref_model = ref_structure[0]
    ref_atoms = []
    for ref_chain in ref_model:
        for ref_res in ref_chain:
            ref_atoms.append(ref_res['CA'].get_coord())

    r1 = ref_atoms[0]
    r2 = ref_atoms[(-1)]
    re = np.sqrt((r1[0] - r2[0]) ** 2 + (r1[1] - r2[1]) ** 2 + (r1[2] - r2[2]) ** 2)
    return re


def cos(a):
    return np.cos(a)


def sin(a):
    return np.sin(a)


r12 = 1.525
r23 = 1.336
r31 = 1.459
phi1 = np.radians(117.2)
phi2 = np.radians(121.7)
phi3 = np.radians(111.0)
r = {}
r[1] = {}
r[2] = {}
r[3] = {}
r[1][2] = r[2][1] = 1.525
r[2][3] = r[3][2] = 1.336
r[3][1] = r[1][3] = 1.459
phi = {}
phi[1] = np.radians(117.2)
phi[2] = np.radians(121.7)
phi[3] = np.radians(111.0)

def calculate_d_theta_r(rama_phi, rama_psi, rama_omega):
    """
        -------------------------
        Based on the publication:
        -------------------------
        Miyazawa T. 1961. Journal of Polymer Science 55(161):215--231.
        TITLE: Molecular vibrations and structure of high polymers. ii. 
        helical parameters of infinite polymer chains as functions of bond lengths, 
        bond angles, and internal rotation angles. 
        """
    rama_omega = (rama_omega - omega_start) % 360.0 + omega_start
    rama_phi = (rama_phi - phi_start) % 360.0 + phi_start
    rama_psi = (rama_psi - psi_start) % 360.0 + psi_start
    tau31 = np.radians(rama_phi)
    tau12 = np.radians(rama_psi)
    tau23 = np.radians(rama_omega)
    tau = {}
    tau[1] = {}
    tau[2] = {}
    tau[3] = {}
    tau[1][2] = tau[2][1] = tau12
    tau[2][3] = tau[3][2] = tau23
    tau[3][1] = tau[1][3] = tau31
    a1 = 1
    a2 = 2
    a3 = 3
    cos_theta_by_two = cos(+tau[a1][a2] / 2 + tau[a2][a3] / 2 + tau[a3][a1] / 2) * sin(phi[a1] / 2) * sin(phi[a2] / 2) * sin(phi[a3] / 2) - cos(-tau[a1][a2] / 2 + tau[a2][a3] / 2 + tau[a3][a1] / 2) * cos(phi[a1] / 2) * cos(phi[a2] / 2) * sin(phi[a3] / 2) - cos(+tau[a1][a2] / 2 - tau[a2][a3] / 2 + tau[a3][a1] / 2) * sin(phi[a1] / 2) * cos(phi[a2] / 2) * cos(phi[a3] / 2) - cos(+tau[a1][a2] / 2 + tau[a2][a3] / 2 - tau[a3][a1] / 2) * cos(phi[a1] / 2) * sin(phi[a2] / 2) * cos(phi[a3] / 2)
    theta = 2.0 * np.arccos(cos_theta_by_two)
    d_times_sin_theta_by_two = (+r[a1][a2] + r[a2][a3] + r[a3][a1]) * sin(+tau[a1][a2] / 2 + tau[a2][a3] / 2 + tau[a3][a1] / 2) * sin(phi[a1] / 2) * sin(phi[a2] / 2) * sin(phi[a3] / 2) - (-r[a1][a2] + r[a2][a3] + r[a3][a1]) * sin(-tau[a1][a2] / 2 + tau[a2][a3] / 2 + tau[a3][a1] / 2) * cos(phi[a1] / 2) * cos(phi[a2] / 2) * sin(phi[a3] / 2) - (+r[a1][a2] - r[a2][a3] + r[a3][a1]) * sin(+tau[a1][a2] / 2 - tau[a2][a3] / 2 + tau[a3][a1] / 2) * sin(phi[a1] / 2) * cos(phi[a2] / 2) * cos(phi[a3] / 2) - (+r[a1][a2] + r[a2][a3] - r[a3][a1]) * sin(+tau[a1][a2] / 2 + tau[a2][a3] / 2 - tau[a3][a1] / 2) * cos(phi[a1] / 2) * sin(phi[a2] / 2) * cos(phi[a3] / 2)
    d = d_times_sin_theta_by_two / sin(theta / 2.0)
    rhos = {}
    for i in [1, 2, 3]:
        a1 = i
        a2 = i + 1
        a3 = i + 2
        if a2 > 3:
            a2 = a2 - 3
        if a3 > 3:
            a3 = a3 - 3
        number_to_atom_dict = {1: 'ca', 2: 'c', 3: 'n'}
        a1text = number_to_atom_dict[a1]
        rhos[a1text] = r[a1][a2] ** 2 + r[a2][a3] ** 2 + r[a3][a1] ** 2 - 2.0 * r[a2][a3] * (r[a1][a2] * cos(phi[a2]) + r[a3][a1] * cos(phi[a3]))
        rhos[a1text] += 2 * r[a1][a2] * r[a3][a1] * (cos(phi[a2]) * cos(phi[a3]) - sin(phi[a2]) * sin(a3) * cos(tau[a2][a3]))
        rhos[a1text] = (rhos[a1text] ** 2.0 - d ** 2.0) / (2.0 * (1 - cos(theta)))
        rhos[a1text] = np.sqrt(rhos[a1text])

    chi = sin(theta) * d / np.abs(d)
    return (
     d, np.degrees(theta), rhos)


def return_secondary_structure_stride(fn):
    """
        #EXAMPLE FILE FOR STRIDE:
        ASG  GLN A   14    1    C          Coil    360.00    128.25     171.3      1KKC
        ASG  ALA A   27   14    T          Turn    -65.17    -16.80      20.2      1KKC
        ASG  GLU A   38   25    H    AlphaHelix    -62.62    -51.33      68.3      1KKC
        ASG  ILE A  155  142    E        Strand   -100.70    129.56      34.9      1KKC
        ASG  GLU A  177  164    G      310Helix    -60.86    -30.95      13.2      1KKC
        """
    get_resno = re.compile('\\d+')
    f = open(fn, 'r')
    secondary_structure_file = f.read()
    f.close()
    resno_to_data = {}
    for l in re.findall('^ASG .+', secondary_structure_file, re.M):
        info = re.split('\\s+', l)
        if len(info) == 11:
            restype = info[1]
            resno = info[3]
            try:
                resno = int(resno)
            except ValueError:
                q = get_resno.match(resno)
                if q:
                    resno = int(q.group())
            except:
                print '# LINE FORMAT FAIL (fn: %s): %s' % (fn, l)

            ss_type = info[5]
            if isinstance(resno, int):
                resno_to_data[resno] = {'ss': ss_type, 'type': restype}
        elif len(info) == 10:
            restype = info[1]
            resno = info[2]
            try:
                resno = int(resno)
            except ValueError:
                q = get_resno.match(resno)
                if q:
                    resno = int(q.group())
            except:
                print '# LINE FORMAT FAIL (fn: %s): %s' % (fn, l)

            ss_type = info[5]
            if isinstance(resno, int):
                resno_to_data[resno] = {'ss': ss_type, 'type': restype}

    return resno_to_data


def return_secondary_structure_dssp(fn):
    """    .-- sequential resnumber, including chain breaks as extra residues
            |    .-- original PDB resname, not nec. sequential, may contain letters
            |    |   .-- amino acid sequence in one letter code
            |    |   |  .-- secondary structure summary based on columns 19-38
            |    |   |  |     .-- chirality  .-- solvent accessibility
            |    |   |  |     |              |
          #  RESIDUE AA STRUCTURE BP1 BP2  ACC
        0   |    |1  |  |   2 |       3      |  ... index
        01234567890123456789012345678901234567     
           35   47   I  E     +     0   0    2
           36   48   R  E >  S- K   0  39C  97
           37   49   Q  T 3  S+     0   0   86
           38   50   N  T 3  S+     0   0   34
           39   51   W  E <   -KL  36  98C   6
        """
    get_resno = re.compile('\\d+')
    resno_to_data = {}
    f = open(fn)
    ssfile = f.read()
    f.close()
    split_dssp = re.compile('^\\s+\\#\\s+RESIDUE\\s+AA\\s+STRUCTURE.+$', re.M)
    q = split_dssp.split(ssfile)
    if len(q) == 2:
        for l in q[1].split('\n'):
            if len(l):
                resno = l[5:10].lstrip()
                subunit = l[11]
                restype = l[13]
                ss_type = l[16]
                chirality = l[22]
                try:
                    resno = int(resno)
                except ValueError:
                    q = get_resno.match(resno)
                    if q:
                        resno = int(q.group())
                except:
                    print '# LINE FORMAT FAIL (fn: %s): %s' % (fn, l)

                if isinstance(resno, int):
                    resno_to_data[resno] = {'ss': ss_type, 'type': restype}

    return resno_to_data


def calculate_handedness_from_theory(phi, psi, omega):
    """
        --------------------------
        Main metric in publication
        --------------------------
        Mannige R. 2017. An exhaustive survey of regular peptide conformations using a new metric for backbone handedness (h). PeerJ.
        --------------------------
        Based on the publication
        --------------------------
        Miyazawa T. 1961. Molecular vibrations and structure of high polymers. ii. helical parameters of infinite polymer chains 
        as functions of bond lengths, bond angles, and internal rotation angles. Journal of Polymer Science 55(161):215--231.
        """
    omega = (omega - omega_start) % 360.0 + omega_start
    phi = (phi - phi_start) % 360.0 + phi_start
    psi = (psi - psi_start) % 360.0 + psi_start
    tau12 = np.radians(psi)
    tau23 = np.radians(omega)
    tau31 = np.radians(phi)
    cos_theta_by_two = cos(+tau12 / 2 + tau23 / 2 + tau31 / 2) * sin(phi1 / 2) * sin(phi2 / 2) * sin(phi3 / 2) - cos(-tau12 / 2 + tau23 / 2 + tau31 / 2) * cos(phi1 / 2) * cos(phi2 / 2) * sin(phi3 / 2) - cos(+tau12 / 2 - tau23 / 2 + tau31 / 2) * sin(phi1 / 2) * cos(phi2 / 2) * cos(phi3 / 2) - cos(+tau12 / 2 + tau23 / 2 - tau31 / 2) * cos(phi1 / 2) * sin(phi2 / 2) * cos(phi3 / 2)
    theta = 2.0 * np.arccos(cos_theta_by_two)
    d_times_sin_theta_by_two = (+r12 + r23 + r31) * sin(+tau12 / 2 + tau23 / 2 + tau31 / 2) * sin(phi1 / 2) * sin(phi2 / 2) * sin(phi3 / 2) - (-r12 + r23 + r31) * sin(-tau12 / 2 + tau23 / 2 + tau31 / 2) * cos(phi1 / 2) * cos(phi2 / 2) * sin(phi3 / 2) - (+r12 - r23 + r31) * sin(+tau12 / 2 - tau23 / 2 + tau31 / 2) * sin(phi1 / 2) * cos(phi2 / 2) * cos(phi3 / 2) - (+r12 + r23 - r31) * sin(+tau12 / 2 + tau23 / 2 - tau31 / 2) * cos(phi1 / 2) * sin(phi2 / 2) * cos(phi3 / 2)
    d = d_times_sin_theta_by_two / sin(theta / 2.0)
    chi = sin(theta) * d / np.abs(d)
    return (
     chi, np.degrees(theta), d)


def calculate_handedness1(ref_structure, atoms_to_be_used=[]):
    """ THIS METRIC FROM (USED IN EQN. 11 AND FIG. 6-(II) OF THE PEERJ MANNIGE PAPER):
        Kwiecinska JI, Cieplak M. 2005. Chirality and protein folding. Journal of Physics: Condensed Matter 17(18):S1565.
        """
    ref_model = ref_structure[0]
    ref_atomsCA = []
    for ref_chain in ref_model:
        for ref_res in ref_chain:
            use_residue = 0
            if not len(atoms_to_be_used):
                use_residue = 1
            elif ref_res.get_id()[1] in atoms_to_be_used:
                use_residue = 1
            if use_residue:
                ref_atomsCA.append(ref_res['CA'].get_coord())

    orientations = []
    for resid in range(len(ref_atomsCA)):
        if resid > 0 and resid + 3 < len(ref_atomsCA):
            CAm = ref_atomsCA[(resid - 1)]
            CA = ref_atomsCA[resid]
            CAp = ref_atomsCA[(resid + 1)]
            CApp = ref_atomsCA[(resid + 2)]
            atoms = [
             CAm, CA, CAp, CApp]
            r1 = atoms[0]
            r2 = atoms[1]
            r3 = atoms[2]
            r4 = atoms[3]
            v1m = r2 - r1
            v1 = r3 - r2
            v1p = r4 - r3
            chirality = np.dot(np.cross(v1m, v1), v1p) / float(np.linalg.norm(v1m) * np.linalg.norm(v1) * np.linalg.norm(v1p))
            if not math.isnan(chirality):
                orientations.append(chirality)

    final_chirality = np.average(orientations)
    return final_chirality


def calculate_handedness2(ref_structure, atoms_to_be_used=[]):
    """ THIS METRIC FROM (USED IN EQN. 12 AND FIG 6-(III) OF THE PEERJ MANNIGE PAPER):
        Kabsch W, Sander C. 1983. Dictionary of protein secondary structure: pattern recognition of hydrogen-bonded 
                and geometrical features. Biopolymers 22(12):2577--2637
        Gruziel M, Dzwolak W, Szymczak P. 2013. Chirality inversions in self-assembly of fibrillar superstructures:
                a computational study. Soft Matter 9(33):8005--8013.
        """
    ref_model = ref_structure[0]
    ref_atomsCA = []
    ref_atomsC = []
    ref_atomsN = []
    ref_atomsO = []
    for ref_chain in ref_model:
        for ref_res in ref_chain:
            use_residue = 0
            if not len(atoms_to_be_used):
                use_residue = 1
            elif ref_res.get_id()[1] in atoms_to_be_used:
                use_residue = 1
            if use_residue:
                ref_atomsCA.append(ref_res['CA'].get_coord())

    orientations = []
    for resid in range(len(ref_atomsCA)):
        if resid > 0 and resid + 3 < len(ref_atomsCA):
            CAm = ref_atomsCA[(resid - 1)]
            CA = ref_atomsCA[resid]
            CAp = ref_atomsCA[(resid + 1)]
            CApp = ref_atomsCA[(resid + 2)]
            atoms = [
             CAm, CA, CAp, CApp]
            r1 = atoms[0]
            r2 = atoms[1]
            r3 = atoms[2]
            r4 = atoms[3]
            v1m = r2 - r1
            v1 = r3 - r2
            v1p = r4 - r3
            v1crossv1p = np.cross(v1, v1p)
            chirality = np.arctan2(np.dot(np.linalg.norm(v1) * v1m, v1crossv1p), np.dot(np.cross(v1m, v1), v1crossv1p))
            if not math.isnan(chirality):
                orientations.append(chirality)

    final_chirality = np.average(orientations) / np.pi
    return final_chirality


def calculate_handedness3(ref_structure, atoms_to_be_used=[]):
    """ THIS METRIC (EQN. 13 IN THE PEERJ MANNIGE PAPER) IS $G_{0S}$ IN:
        Solymosi M, Low RJ, Grayson M, Neal MP. 2002. A generalized scaling of a chiral index for molecules.
                The Journal of Chemical Physics 116(22):9875--9881.
        Neal MP, Solymosi M, Wilson MR, Earl DJ. 2003. Helical twisting power and scaled chiral indices.
                The Journal of Chemical Physics 119(6):3567--3573.
        """
    ref_model = ref_structure[0]
    ref_atomsCA = []
    for ref_chain in ref_model:
        for ref_res in ref_chain:
            use_residue = 0
            if not len(atoms_to_be_used):
                use_residue = 1
            elif ref_res.get_id()[1] in atoms_to_be_used:
                use_residue = 1
            if use_residue:
                ref_atomsCA.append(ref_res['CA'].get_coord())

    orientations = []
    n = 2.0
    m = 1.0
    four_prime = 24.0
    N_to_the_fourth = float(len(ref_atomsCA) ** 4.0)
    range_len_ref_atomsCA = range(len(ref_atomsCA))
    for i in range_len_ref_atomsCA:
        for j in range_len_ref_atomsCA:
            rij = ref_atomsCA[i] - ref_atomsCA[j]
            rij_norm = np.linalg.norm(rij)
            for k in range_len_ref_atomsCA:
                rjk = ref_atomsCA[j] - ref_atomsCA[k]
                rjk_norm = np.linalg.norm(rjk)
                for l in range_len_ref_atomsCA:
                    if len(set([i, j, k, l])) == 4:
                        rkl = ref_atomsCA[k] - ref_atomsCA[l]
                        rkl_norm = np.linalg.norm(rkl)
                        ril = ref_atomsCA[i] - ref_atomsCA[l]
                        ril_norm = np.linalg.norm(ril)
                        G0 = float(np.dot(np.cross(rij, rkl), ril) * np.dot(rij, rjk) * np.dot(rjk, rkl)) / (3.0 * (rij_norm * rjk_norm * rkl_norm) ** n * ril_norm ** m)
                        G0S = four_prime * G0 / N_to_the_fourth
                        orientations.append(G0S)

    final_chirality = np.sum(orientations)
    return final_chirality


def draw_histogram(data, bins=20):
    from scipy.stats import gaussian_kde
    a, b = np.histogram(data, bins=bins)
    hisX = []
    hisY = []
    plt.clf()
    for i in range(len(a)):
        hisx = float(b[i] + b[(i + 1)]) / 2.0
        hisy = float(a[i]) / sum(a)
        hisX.append(hisx)
        hisY.append(hisy)

    plt.plot(hisX, hisY)
    plt.show()
    return 1


def xyz_to_image(X, Y, Z):
    xset = sorted(set(X))
    yset = sorted(set(Y))
    xstep = 1.0
    if len(xset) > 1:
        xstep = float(xset[1]) - float(xset[0])
    ystep = 1.0
    if len(yset) > 1:
        ystep = float(yset[1]) - float(yset[0])
    xset_boundaries = np.append(xset, [xset[(-1)] + xstep]) - xstep / 2
    yset_boundaries = np.append(yset, [yset[(-1)] + ystep]) - ystep / 2
    imagex, imagey = np.meshgrid(xset_boundaries, yset_boundaries)
    imagez = np.zeros((len(yset), len(xset)))
    for x, y, z in zip(X, Y, Z):
        xi = xset.index(x)
        yi = yset.index(y)
        imagez[yi][xi] = z

    return (imagex, imagey, imagez)


def make2Dfigure(Xoriginal, Yoriginal, Zoriginal, fn=None, cmap=plt.get_cmap('gray_r'), xscaling=2.0, xlim=[], ylim=[], zlim=[], ax=None, horizontallines=None, verticallines=None, title=None, signed=-1, show=0, start_fresh=0, colorbar=0, xtitle=None, xticks=None, xlabels=None, ytitle=None, yticks=None, ylabels=None):
    if ax is None:
        f, ax = plt.subplots()
    else:
        plt.axes(ax)
        if start_fresh:
            plt.cla()
    X = copy.deepcopy(Xoriginal)
    Y = copy.deepcopy(Yoriginal)
    Z = copy.deepcopy(Zoriginal)
    deleteindices = []
    if len(xlim):
        for i in range(len(X)):
            if X[i] < xlim[0] or X[i] > xlim[1]:
                deleteindices.append(i)

    if len(ylim):
        for i in range(len(Y)):
            if Y[i] < ylim[0] or Y[i] > ylim[1]:
                deleteindices.append(i)

    deleteindices = sorted(list(set(deleteindices)))
    deleteindices.reverse()
    if len(deleteindices):
        for i in deleteindices:
            del X[i]
            del Y[i]
            del Z[i]

    if len(zlim):
        zmin = sorted(zlim)[0]
        zmax = sorted(zlim)[(-1)]
        for i in range(len(Z)):
            if Z[i] < zmin:
                Z[i] = zmin
            elif Z[i] > zmax:
                Z[i] = zmax

    Xsorted = sorted(set(X))
    Ysorted = sorted(set(Y))
    pageMinY = 2.5
    pageMaxY = 14.5
    pageMinX = 3.0
    pageMaxX = pageMinX + float(pageMaxY - pageMinY) * xscaling
    xmin = Xsorted[0]
    xmax = Xsorted[(-1)]
    ymin = Ysorted[0]
    ymax = Ysorted[(-1)]
    if xlim is not None:
        if len(xlim) == 2 and xlim[0] < xlim[(-1)]:
            xmin = xlim[0]
            xmax = xlim[(-1)]
    if ylim is not None:
        if len(ylim) == 2 and ylim[0] < ylim[(-1)]:
            ymin = ylim[0]
            ymax = ylim[(-1)]
    zmin = round(sorted(Z)[0], 2)
    zmax = round(sorted(Z)[(-1)], 2)
    if zlim is not None:
        if len(zlim) == 2 and zlim[0] < zlim[(-1)]:
            zmin = zlim[0]
            zmax = zlim[1]
    imagex, imagey, imagez = xyz_to_image(X, Y, Z)
    xset = sorted(set(imagex.flatten()))
    yset = sorted(set(imagey.flatten()))
    extent = [xset[0], xset[(-1)], yset[0], yset[(-1)]]
    plt.pcolor(imagex, imagey, imagez, cmap=cmap, vmin=zmin, vmax=zmax)
    if xticks is not None:
        if xlabels is not None:
            plt.xticks(xticks, xlabels, ha='center')
        else:
            plt.xticks(xticks)
    if yticks is not None:
        if ylabels is not None:
            plt.yticks(yticks, ylabels)
        else:
            plt.yticks(yticks)
    if xtitle is not None:
        plt.xlabel(xtitle)
    if ytitle is not None:
        plt.ylabel(ytitle)
    if title is not None:
        t = plt.title(title)
        t.set_y(1.03)
    annotation_text_padding = 0.035
    if horizontallines is not None:
        padding = float(xset[(-1)] - xset[0]) * annotation_text_padding
        for y in horizontallines:
            text = ''
            if type(horizontallines) is dict:
                text = horizontallines[y]
            if yset[0] <= y and y <= yset[(-1)]:
                lineX = []
                lineY = []
                for x in [xset[0], xset[(-1)]]:
                    lineX.append(float(x))
                    lineY.append(float(y))

                point_x = xset[(-1)]
                point_y = float(y)
                text_x = xset[(-1)] + padding
                text_y = float(y)
                current_arrow_color = plt.rcParams['lines.color']
                linewidth = plt.rcParams['lines.linewidth']
                textsize = plt.rcParams['font.size'] * 0.8
                ax.annotate(str(text), xy=(point_x, point_y), xytext=(text_x, text_y), xycoords='data', arrowprops=dict(arrowstyle='-', color=current_arrow_color, lw=linewidth), ha='left', va='center', fontsize=textsize)

    if verticallines is not None:
        padding = float(yset[(-1)] - yset[0]) * annotation_text_padding
        for x in verticallines:
            text = ''
            if type(verticallines) is dict:
                text = verticallines[x]
            if xset[0] <= x and x <= xset[(-1)]:
                lineX = []
                lineY = []
                for y in [yset[0], yset[(-1)]]:
                    lineX.append(float(x))
                    lineY.append(float(y))

                current_arrow_color = plt.rcParams['lines.color']
                linewidth = plt.rcParams['lines.linewidth']
                ax.plot(lineX, lineY, '-', color=current_arrow_color, lw=linewidth)

    plt.axis(extent)
    if colorbar:
        plt.colorbar()
    if fn:
        filenames = []
        if isinstance(fn, str):
            filenames.append(fn)
        else:
            filenames = fn
        for fn in filenames:
            plt.savefig(fn, dpi=170, bbox_inches='tight')

    if show:
        if len(filenames) and filenames[0][-len('.pdf'):].lower() == '.pdf':
            os.system('evince ' + filenames[0])
        else:
            plt.show()
    return 1


def xyz_to_ndarrays(x, y, z):
    setx = sorted(set(x))
    sety = sorted(set(y))
    x_to_index = {}
    for xv in setx:
        x_to_index[xv] = setx.index(xv)

    y_to_index = {}
    for yv in sety:
        y_to_index[yv] = sety.index(yv)

    X = np.nan * np.empty((len(setx), len(sety)))
    Y = np.nan * np.empty((len(setx), len(sety)))
    Z = np.nan * np.empty((len(setx), len(sety)))
    for xv, yv, zv in zip(x, y, z):
        xi = x_to_index[xv]
        yi = y_to_index[yv]
        X[(xi, yi)] = xv
        Y[(xi, yi)] = yv
        Z[(xi, yi)] = zv

    return (
     X, Y, Z)


def open_file(fn, write_mode='r'):
    print "# Opening the following file in '" + write_mode + "' mode:", fn
    return open(fn, 'w')


def build_structure(angles):
    geo = Geometry.geometry('G')
    geo.phi = angles[0][0]
    geo.psi_im1 = angles[0][1]
    geo.omega = angles[0][2]
    structure = PeptideBuilder.initialize_res(geo)
    for i in range(1, len(angles)):
        geo = Geometry.geometry('G')
        geo.phi = angles[i][0]
        geo.psi_im1 = angles[(i - 1)][1]
        geo.omega = angles[(i - 1)][2]
        structure = PeptideBuilder.add_residue(structure, geo)

    return structure


def write_fake_pdb_file(pdbfilename, coordinates, connect_atoms=[], coordinate_multiplier=1.0):
    coordinates = np.array(coordinates)
    help = '\n\tBelow, N = number of atoms in coordinates, F = the number of frames/models\n\t\n\t<coordinates> can be of shape (N,3), like so:\n\t\n\t\t[[x1,y1,z1],[x2,y2,z2],...,[xN,yN,zN]]\n\t\n\tOR: it can be of the shape (F,N,3)\n\t\t[ \n\t \t   [[x1,y1,z1],[x2,y2,z2],...,[xN,yN,zN]], # 1\n\t\t   [[x1,y1,z1],[x2,y2,z2],...,[xN,yN,zN]], # 2\n\t\t   .                                       # .\n\t\t   .                                       # .\n\t\t   .                                       # .\n\t\t   [[x1,y1,z1],[x2,y2,z2],...,[xN,yN,zN]]  # F\n\t\t ]\n\tIn case of coordinates that are two dimensional, i.e., shape = (N,2) or (F,N,2), \n\tthen we can set all z values to 0.0\n\t'
    if len(coordinates.shape) == 2 or len(coordinates.shape) == 3:
        N = coordinates.shape[(-2)]
        if coordinates.shape[(-1)] == 2:
            zshape = list(coordinates.shape)
            zshape[-1] = 1
            zs = np.zeros(zshape)
            coordinates = np.append(coordinates, zs, axis=len(zshape) - 1)
        elif coordinates.shape[(-1)] == 3:
            pass
        else:
            print 'coordinates are not of the correct format: '
            print help
            exit()
    else:
        print 'coordinates are not of the correct format: '
        print help
        exit()
    basedir = os.path.split(pdbfilename)[0]
    if len(basedir.rstrip()) != 0:
        if not os.path.isdir(basedir):
            os.makedirs(basedir)
    pdbfile = ''
    if len(coordinates.shape) == 2:
        count = 0
        for x, y, z in coordinates:
            count += 1
            pdbfile += ('ATOM{:>7}  CA  VAL A{:>4}{:>12.3f}{:>8.3f}{:>8.3f}  1.00  0.00\n').format(count, count, float(x) * coordinate_multiplier, float(y) * coordinate_multiplier, float(z) * coordinate_multiplier)

    elif len(coordinates.shape) == 3:
        for c in coordinates:
            count = 0
            pdbfile += 'MODEL\n'
            for x, y, z in c:
                count += 1
                pdbfile += ('ATOM{:>7}  CA  VAL A{:>4}{:>12.3f}{:>8.3f}{:>8.3f}  1.00  0.00\n').format(count, count, float(x) * coordinate_multiplier, float(y) * coordinate_multiplier, float(z) * coordinate_multiplier)

            pdbfile += 'ENDMDL\n'

    if len(connect_atoms):
        connect_atoms = np.array(connect_atoms)
        if len(connect_atoms.shape) == 2:
            if connect_atoms.shape[1] == 2:
                for atom1, atom2 in connect_atoms:
                    pdbfile += ('CONECT{:>5}{:>5}\n').format(atom1, atom2)

            else:
                print '<connect_atoms> must be a list of pairs of atom numbers (shape: (N,2)). But present shape: ' + str(connect_atoms.shape) + ' Ignoring.'
        else:
            print '<connect_atoms> must be a list of pairs of atom numbers (shape: (N,2)). But present shape: ' + str(connect_atoms.shape) + ' Ignoring.'
    f = open(pdbfilename, 'w')
    f.write(pdbfile)
    f.close()
    return 1


def calculate_dihedral_angle(p):
    b = p[:-1] - p[1:]
    b[0] *= -1
    v = np.array([ v - v.dot(b[1]) / b[1].dot(b[1]) * b[1] for v in [b[0], b[2]] ])
    v /= np.sqrt(np.einsum('...i,...i', v, v)).reshape(-1, 1)
    b1 = b[1] / np.linalg.norm(b[1])
    x = np.dot(v[0], v[1])
    m = np.cross(v[0], b1)
    y = np.dot(m, v[1])
    d = np.degrees(np.arctan2(y, x))
    return d


def read_pdb_manual(fn, signed=0):
    """
        ATOM     10 1H   LYS A   1       0.763   3.548  -0.564
        ATOM    482  N   PRO A  61      27.194  -5.761  14.684  1.00  9.09           N  
        ATOM      4  CE  BLYSX   1     -80.894 -24.467   8.039  1.00  0.00      U1    
        ATOM      2  HT1 MET U   1       0.208   0.762 -12.141  0.00  0.00      UBIQ  
        ATOM   3158  N   EC0     4      17.160  35.270  66.280  1.00  0.00            
                  |   |   |  |   |        |       |       |                     |
             atomno   |   |  |   |        x       y       z                 segname
               atom type  |  |   |                                          (CHAIN)
                    resname  |   resno
                         chainID
        """
    f = open(fn, 'r')
    pdbblock = f.read()
    f.close()
    getlines = re.compile('ATOM\\s+(?P<atomno>\\d+)\\s+(?P<atomtype>\\S+)\\s+(?P<resname>...).(?P<subname>.)\\s+(?P<resno>\\d+)\\s+(?P<x>\\-*\\d+\\.*\\d*)\\s+(?P<y>\\-*\\d+\\.*\\d*)\\s+(?P<z>\\-*\\d+\\.*\\d*)\\s+(?P<occu>\\S+)\\s+(?P<bfac>\\S+)\\s*(?P<segname>\\S*)\\s*$', re.M)
    resnos = []
    models = re.split('\nEND|\nMODEL', pdbblock)
    model_number = 0
    model_to_chain_to_resno_atom_to_vals = {}
    for model_index in range(len(models)):
        model = models[model_index].rstrip()
        if len(model) > 1:
            model_number += 1
            if model_number not in model_to_chain_to_resno_atom_to_vals:
                model_to_chain_to_resno_atom_to_vals[model_number] = {}
            segname_exists = 1
            atomidentifiers = []
            current_default_subunit = 'A'
            currentlines = getlines.finditer(model)
            for i in currentlines:
                vals = i.groupdict()
                atomtype = vals['atomtype']
                if atomtype == 'CA' or atomtype == 'N' or atomtype == 'C':
                    resno = int(vals['resno'])
                    xyz = np.array([float(vals['x']), float(vals['y']), float(vals['z'])])
                    segname = current_default_subunit
                    if vals['subname'] != ' ':
                        segname = vals['subname']
                    atomidentifier = segname + '_' + vals['resno'] + vals['atomtype']
                    if atomidentifier in atomidentifiers:
                        if vals['occu'][0] == '1':
                            new_subunit_index = subunit_choices.index(segname) + 1
                            if new_subunit_index >= len_subunit_choices:
                                new_subunit_index = 0
                            current_default_subunit = subunit_choices[new_subunit_index]
                    atomidentifiers.append(atomidentifier)
                    if segname not in model_to_chain_to_resno_atom_to_vals[model_number]:
                        model_to_chain_to_resno_atom_to_vals[model_number][segname] = {}
                    if resno not in model_to_chain_to_resno_atom_to_vals[model_number][segname]:
                        model_to_chain_to_resno_atom_to_vals[model_number][segname][resno] = {}
                    model_to_chain_to_resno_atom_to_vals[model_number][segname][resno][atomtype.lower()] = xyz
                    model_to_chain_to_resno_atom_to_vals[model_number][segname][resno]['resname'] = vals['resname']

            if not len(model_to_chain_to_resno_atom_to_vals[model_number]):
                del model_to_chain_to_resno_atom_to_vals[model_number]
                model_number -= 1

    for model in sorted(model_to_chain_to_resno_atom_to_vals.keys()):
        for chain in sorted(model_to_chain_to_resno_atom_to_vals[model].keys()):
            for resno in sorted(model_to_chain_to_resno_atom_to_vals[model][chain].keys()):
                triplet_found = 0
                if 'ca' in model_to_chain_to_resno_atom_to_vals[model][chain][resno]:
                    triplet_found += 1
                if 'n' in model_to_chain_to_resno_atom_to_vals[model][chain][resno]:
                    triplet_found += 1
                if 'c' in model_to_chain_to_resno_atom_to_vals[model][chain][resno]:
                    triplet_found += 1
                if triplet_found == 3:
                    i = resno
                    im = i - 1
                    ip = i + 1
                    neighbors_found = 0
                    if im in model_to_chain_to_resno_atom_to_vals[model][chain]:
                        if 'c' in model_to_chain_to_resno_atom_to_vals[model][chain][im]:
                            neighbors_found += 1
                    if ip in model_to_chain_to_resno_atom_to_vals[model][chain]:
                        if 'n' in model_to_chain_to_resno_atom_to_vals[model][chain][ip]:
                            neighbors_found += 1
                        if 'ca' in model_to_chain_to_resno_atom_to_vals[model][chain][ip]:
                            neighbors_found += 1
                    if neighbors_found == 3:
                        a = model_to_chain_to_resno_atom_to_vals[model][chain][im]['c']
                        b = model_to_chain_to_resno_atom_to_vals[model][chain][i]['n']
                        c = model_to_chain_to_resno_atom_to_vals[model][chain][i]['ca']
                        d = model_to_chain_to_resno_atom_to_vals[model][chain][i]['c']
                        e = model_to_chain_to_resno_atom_to_vals[model][chain][ip]['n']
                        f = model_to_chain_to_resno_atom_to_vals[model][chain][ip]['ca']
                        phi = calculate_dihedral_angle(np.array([a, b, c, d]))
                        psi = calculate_dihedral_angle(np.array([b, c, d, e]))
                        omega = calculate_dihedral_angle(np.array([c, d, e, f]))
                        R = (phi + psi + 360.0) / 720.0
                        d, theta, rs = calculate_d_theta_r(phi, psi, omega)
                        model_to_chain_to_resno_atom_to_vals[model][chain][i]['phi'] = phi
                        model_to_chain_to_resno_atom_to_vals[model][chain][i]['psi'] = psi
                        model_to_chain_to_resno_atom_to_vals[model][chain][i]['omega'] = omega
                        model_to_chain_to_resno_atom_to_vals[model][chain][i]['r'] = R
                        model_to_chain_to_resno_atom_to_vals[model][chain][i]['d'] = d
                        model_to_chain_to_resno_atom_to_vals[model][chain][i]['theta'] = theta

    return model_to_chain_to_resno_atom_to_vals


def R(phi, psi, sigma=10.0, bound=360.0, signed=0):
    """
        A SIMPLE DEFINITION THAT RETURNS RAMACHANDRAN NUMBERS (see Mannige, Kundu, Whitelam, 2016). 
        Usage example: R = R(phi,psi); below, we equate R() with r().
        Use the class "RamachandranCalculator" if one is to calculate many R numbers 
        (it is 2.3 times faster). This speedup is not very important, since this function 
        takes ~4.8 seconds to calculate 1 million R numbers, versus 3.8/2.3 = 2.09 seconds
        for the ramachandran number class.  However, the main reason to use the class is that 
        you can self-consistently change various internal variables (sigma, bound) 
        for testing purposes. For that reason, and for completeness, the class has been 
        left in this file.
        """
    bound_by_two = bound / 2.0
    angleMin = -1.0 * bound_by_two
    angleMax = bound_by_two
    sqrt = np.sqrt(2.0)
    if not (angleMin <= phi and phi <= angleMax):
        phi = float(phi + bound_by_two) % bound - bound_by_two
    if not (angleMin <= psi and psi <= angleMax):
        psi = float(psi + bound_by_two) % bound - bound_by_two
    multiplier = int(round(sigma * (bound * 1.4142135623730951), 0))

    def raw_ramachandran_number_collapse(current_phi, current_psi):
        a = round(sigma * (current_phi - current_psi + bound) / sqrt, 0)
        b = round(sigma * (current_phi + current_psi + bound) / sqrt, 0)
        return a + b * multiplier

    raw_R_min = raw_ramachandran_number_collapse(angleMin, angleMin)
    raw_R_max = raw_ramachandran_number_collapse(angleMax, angleMax)
    raw_R_max_minus_R_min = float(raw_R_max - raw_R_min)
    raw_R = raw_ramachandran_number_collapse(phi, psi)
    final_R = (raw_R - raw_R_min) / raw_R_max_minus_R_min
    if signed:
        if phi > psi:
            final_R = final_R * -1.0
    return final_R


def plot_ramachandran_histogram(X, Y, xlabel='$\\phi$', ylabel='$\\psi$', levels=0, cmap=plt.get_cmap('Blues'), show=0, lines=0, fill=0, label_contours=0, smooth=2, ax=None, linestyles='solid', linewidths=1.5, linecolors=None, show_diag=0):
    from scipy import interpolate
    import scipy.ndimage
    X = np.round(X, 0)
    Y = np.round(Y, 0)
    if ax is None:
        f, ax = plt.subplots()
    xy_tuples = zip(X, Y)
    xy_to_z = {}
    for t in xy_tuples:
        if t not in xy_to_z:
            xy_to_z[t] = 0.0
        xy_to_z[t] += 1

    amin = -180.0
    amax = 180.0
    oldX = []
    oldY = []
    oldZ = []
    for x in np.arange(amin, amax + 0.5, 1.0):
        for y in np.arange(amin, amax + 0.5, 1.0):
            hits = 0
            t = (x, y)
            if t in xy_to_z:
                hits = xy_to_z[t]
            oldX.append(x)
            oldY.append(y)
            oldZ.append(hits)

    contour_label_format = '%1.1f'
    X, Y, Z = xyz_to_ndarrays(oldX, oldY, oldZ)
    Z = Z / Z.sum()
    if smooth:
        Z = scipy.ndimage.filters.gaussian_filter(Z, smooth)
    f = copy.deepcopy(Z)
    try:
        n = 1000
        t = np.linspace(0, f.max(), n)
        integral = ((f >= t[:, None, None]) * f).sum(axis=(1, 2))
        a = interpolate.interp1d(integral, t)
        levels = sorted(a(np.array(levels)))
        levels = levels + [f.max()]
    except:
        print 'Failed getting the values for  levels provided. Using min and max values instead.'
        levels = [f.min(), f.max()]

    colors = None
    linecolors = None
    if type(cmap) == str or type(cmap) == list or type(cmap) == tuple:
        colors = cmap
        linecolors = cmap
        cmap = None
    if fill:
        ax.contourf(X, Y, Z, levels, cmap=cmap, colors=colors)
    if lines:
        new_levels = []
        new_linestyles = []
        for level, linestyle in zip(levels[:-1], linestyles):
            if linestyle is not None:
                new_levels.append(level)
                new_linestyles.append(linestyle)

        if len(new_levels):
            CS = ax.contour(X, Y, Z, new_levels, cmap=cmap, colors=linecolors, linestyles=new_linestyles, linewidths=linewidths)
            if label_contours:
                ax.clabel(CS, fmt=contour_label_format)
    xticks = range(int(amin), int(amax) + 1, 180)
    yticks = range(int(amin), int(amax) + 1, 180)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if show:
        plt.show()
    return