# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/test_kinematics.py
# Compiled at: 2017-08-01 14:59:15
# Size of source mod 2**32: 15983 bytes
import os
from pytrack_analysis.profile import *
from pytrack_analysis.database import *
from pytrack_analysis.logger import Logger
import pytrack_analysis.preprocessing as prep
from pytrack_analysis.kinematics import Kinematics, get_path
get_path('Kinematics log path:')
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

def analysis(db):
    this_session = db.experiment('CANS').session('005')
    raw_data, meta_data = this_session.load()
    clean_data = prep.interpolate(raw_data)
    clean_data = prep.to_mm(clean_data, meta_data.px2mm)
    window_len = 16
    smoothed_data = prep.gaussian_filter(clean_data, _len=window_len, _sigma=(window_len / 10))
    body_pos, head_pos = smoothed_data[['body_x', 'body_y']], smoothed_data[['head_x', 'head_y']]
    kinematics = Kinematics(smoothed_data, meta_data.dict)
    distance_patch = kinematics.distance_to_patch(head_pos, meta_data)
    head_speed = kinematics.linear_speed(head_pos, meta_data)
    window_len = 60
    smooth_head_speed = prep.gaussian_filter(head_speed, _len=window_len, _sigma=(window_len / 10))
    window_len = 120
    smoother_head = prep.gaussian_filter(smooth_head_speed, _len=window_len, _sigma=(window_len / 10))
    body_speed = kinematics.linear_speed(body_pos, meta_data)
    smooth_body_speed = prep.gaussian_filter(body_speed, _len=window_len, _sigma=(window_len / 10))
    speeds = pd.DataFrame({'head':smooth_head_speed['speed'],  'body':smooth_body_speed['speed'],  'smoother_head':smoother_head['speed']})
    angular_heading = kinematics.head_angle(smoothed_data)
    angular_speed = kinematics.angular_speed(angular_heading, meta_data)
    angles = pd.DataFrame({'heading':angular_heading['heading'],  'speed':angular_speed['speed']})
    etho_dict = {0:'resting', 
     1:'micromovement', 
     2:'walking', 
     3:'sharp turn', 
     4:'yeast micromovement', 
     5:'sucrose micromovement'}
    meta_data.dict['etho_class'] = etho_dict
    etho_vector, visits = kinematics.ethogram(speeds, angular_speed, distance_patch, meta_data)
    this_session.add_data('head_pos', head_pos, descr='Head positions of fly in [mm].')
    this_session.add_data('distance_patches', distance_patch, descr='Distances between fly and individual patches in [mm].')
    this_session.add_data('speeds', speeds, descr='Linear speeds of body and head trajectory of fly in [mm/s].')
    this_session.add_data('angle', angular_heading, descr='Angular heading of fly in [o].')
    this_session.add_data('angl_speed', angular_speed, descr='Angular speed of fly in [o/s].')
    this_session.add_data('angles', angles, descr='Angular heading and speed of fly in [o] and in [o/s], respectively.')
    this_session.add_data('etho', etho_vector, descr='Ethogram classification.')
    this_session.add_data('visits', visits, descr='Food patch visits.')


def plotting(db):
    this_session = db.experiment('CANS').session('005')
    start = 56100
    end = start + 9000
    meta = this_session
    data = this_session.data['distance_patches'].loc[start:end, ['dist_patch_0']]
    fci, axci = fig_1c(data, meta, 0)
    data = this_session.data['speeds'].loc[start:end, ['head', 'body']]
    fcii, axcii = fig_1c(data, meta, 1)
    data = this_session.data['angles'].loc[start:end, ['heading', 'speed']]
    fciii, axciii = fig_1c(data, meta, 2)
    data = this_session.data['etho'].loc[start:end, ['etho']]
    fciv, axciv = fig_1c(data, meta, 3)
    data = this_session.data['visits'].loc[start:end, ['visits']]
    fciv, axciv = fig_1c(data, meta, 4)
    data = this_session.data['head_pos'].loc[start:end, ['head_x', 'head_y']]
    fd, axd = fig_1d(data, meta)
    fciname = './fci.pdf'
    fdname = './fd.pdf'
    plt.show()


def fig_test(data, meta):
    f, ax = plt.subplots(1, num='Test',
      figsize=(4.5, 1.5),
      dpi=300)
    a = np.array(data)[:, 0]
    dy = 0.5
    x = np.arange(0, len(a))
    _lw = 0.1
    ax.vlines((x[(a == 1)]), (-dy), dy, colors='#c97aaa', lw=_lw)
    ax.vlines((x[(a == 2)]), (-dy), dy, colors='#5bd5ff', lw=_lw)
    ax.vlines((x[(a == 3)]), (-dy), dy, colors='#04bf11', lw=_lw)
    ax.vlines((x[(a == 4)]), (-dy), dy, colors='#f0e442', lw=_lw)
    ax.vlines((x[(a == 5)]), (-dy), dy, colors='k', lw=_lw)
    ax.set_ylim([-dy, dy])
    return (f, ax)


def fig_1c_all(data, meta):
    pass


def fig_1c(data, meta, index):
    figlabels = {0:'i: Distance to Patch', 
     1:'ii: Linear Speed', 
     2:'iii: Angular Speed', 
     3:'iv: Ethogram', 
     4:'v: Food Patch Visits'}
    ylabels = {0:'Distance\nto patch\n[mm]', 
     1:'Linear\nspeed\n[mm/s]', 
     2:'Angular\nspeed\n[$^\\circ$/s]', 
     3:'Etho-\ngram', 
     4:'Food\npatch\nvisits'}
    start = data.first_valid_index()
    end = start + 9000
    nsubs = [2, 2, 1, 1, 1]
    if index < 2:
        splits = [0, 1]
        end_at = [25, 20]
        break_at = 6
        scale1 = 1
        scale2 = 5
        ylim = [
         break_at, end_at[index]]
        ylim2 = [
         0.0, break_at]
        ylimratio = (ylim[1] - ylim[0]) / (ylim2[1] - ylim2[0] + ylim[1] - ylim[0]) / scale2
        ylim2ratio = (ylim2[1] - ylim2[0]) / (ylim2[1] - ylim2[0] + ylim[1] - ylim[0]) / scale1
        f, axes = plt.subplots((nsubs[index]), num=('Fig. 1C' + figlabels[index]),
          sharex=True,
          figsize=(4.5, 1.5),
          dpi=300,
          gridspec_kw={'height_ratios': [ylimratio, ylim2ratio]})
        axes[0].set_ylim(ylim)
        axes[1].set_ylim(ylim2)
    else:
        f, axes = plt.subplots((nsubs[index]), num=('Fig. 1C' + figlabels[index]),
          sharex=True,
          figsize=(4.5, 1.5),
          dpi=300)
    if index == 0:
        axes[0].set_title('C', fontsize=16, fontweight='bold', loc='left', x=(-0.3), y=1.05)
    else:
        if index == 1:
            axes[0].set_title('C', fontsize=16, color='w', fontweight='bold', loc='left', x=(-0.3), y=1.05)
        else:
            axes.set_title('C', fontsize=16, color='w', fontweight='bold', loc='left', x=(-0.3), y=1.05)
    if index < 2:
        axes[1].set_ylabel((ylabels[index]), fontsize=12)
        axes[0].spines['top'].set_visible(False)
        axes[1].spines['top'].set_visible(False)
        axes[0].spines['bottom'].set_visible(False)
        axes[1].spines['bottom'].set_visible(False)
        axes[0].spines['right'].set_visible(False)
        axes[1].spines['right'].set_visible(False)
        axes[0].tick_params(labeltop='off')
        axes[0].set_xticks([])
        majors = np.arange(10, end_at[0] + 1, 15)
        minors = np.arange(10, end_at[0] + 1, 5)
        axes[0].tick_params(axis='both', which='major', labelsize=12)
        axes[0].tick_params(axis='both', which='minor', labelsize=0)
        axes[0].set_yticks(majors)
        axes[0].set_yticks(minors, minor=True)
        majors = np.arange(0, break_at, 2)
        minors = np.arange(0, break_at, scale1)
        axes[1].tick_params(axis='both', which='major', labelsize=12)
        axes[1].tick_params(axis='both', which='minor', labelsize=0)
        axes[1].set_yticks(majors)
        axes[1].set_yticks(minors, minor=True)
    else:
        if index == 4:
            axes.spines['top'].set_visible(False)
            axes.spines['right'].set_visible(False)
            axes.set_ylabel((ylabels[index]), fontsize=12)
            axes.set_xlabel('Time [s]', fontsize=12)
        else:
            axes.spines['top'].set_visible(False)
            axes.spines['bottom'].set_visible(False)
            axes.spines['right'].set_visible(False)
            axes.set_ylabel((ylabels[index]), fontsize=12)
            axes.set_xticks([])
        if index == 2:
            axes.set_yticks(np.arange(-400, 401, 200))
        lx1 = start
        lx2 = end
        if index == 0:
            axes[0].plot(data, 'k-', lw=1)
            axes[1].plot(data, 'k-', lw=1)
            axes[0].set_ylim([break_at, end_at[0]])
            axes[1].hlines(5, lx1, lx2, colors='#bbbbbb', linestyles='--', lw=1)
            axes[1].hlines(2.5, lx1, lx2, colors='#bbbbbb', linestyles='--', lw=1)
            axes[1].text((lx2 + 100), 4.5, '5 mm', color='#bbbbbb', fontsize=8)
            axes[1].text((lx2 + 100), 2.0, '2.5 mm', color='#bbbbbb', fontsize=8)
            axes[0].set_xlim([lx1, lx2])
            axes[1].set_xlim([lx1, lx2])
            axes[1].set_ylim([0, break_at])
        else:
            if index == 1:
                axes[0].plot((data['head']), 'b-', lw=1)
                axes[0].plot((data['body']), 'k-', lw=1)
                axes[1].plot((data['head']), 'b-', lw=1)
                axes[1].plot((data['body']), 'k-', lw=1)
                axes[1].hlines(2.0, lx1, lx2, colors='#bbbbbb', linestyles='--', lw=1)
                axes[1].hlines(0.2, lx1, lx2, colors='#bbbbbb', linestyles='--', lw=1)
                axes[1].text((lx2 + 100), 1.6, '2 mm', color='#bbbbbb', fontsize=8)
                axes[1].text((lx2 + 100), (-0.2), '0.2 mm', color='#bbbbbb', fontsize=8)
                lx1 = start
                lx2 = end
                axes[0].set_xlim([lx1, lx2])
                axes[1].set_xlim([lx1, lx2])
                axes[1].set_ylim([0, break_at])
            else:
                if index == 2:
                    axes.plot((data['speed']), 'k-', lw=1)
                    axes.hlines(125.0, lx1, lx2, colors='#bbbbbb', linestyles='--', lw=1)
                    axes.hlines((-125), lx1, lx2, colors='#bbbbbb', linestyles='--', lw=1)
                    axes.text((lx2 + 100), 85, '125 $^\\circ$', color='#bbbbbb', fontsize=8)
                    axes.text((lx2 + 100), (-165), '-125 $^\\circ$', color='#bbbbbb', fontsize=8)
                    lx1 = start
                    lx2 = end
                    axes.set_xlim([lx1, lx2])
                    axes.set_ylim([-400, 400])
                else:
                    if index == 3:
                        a = np.array(data)[:, 0]
                        dy = 0.5
                        x = np.arange(lx1, lx2 + 1)
                        _lw = 0.1
                        axes.vlines((x[(a == 0)]), (-dy), dy, colors='#ffffff', lw=_lw)
                        axes.vlines((x[(a == 1)]), (-dy), dy, colors='#c97aaa', lw=_lw)
                        axes.vlines((x[(a == 2)]), (-dy), dy, colors='#5bd5ff', lw=_lw)
                        axes.vlines((x[(a == 3)]), (-dy), dy, colors='#04bf11', lw=_lw)
                        axes.vlines((x[(a == 4)]), (-dy), dy, colors='#f0e442', lw=_lw)
                        axes.vlines((x[(a == 5)]), (-dy), dy, colors='k', lw=_lw)
                        axes.set_xlim([lx1, lx2])
                        axes.set_ylim([-dy, dy])
                        axes.spines['left'].set_visible(False)
                        axes.set_yticks([])
                    elif index == 4:
                        a = np.array(data)[:, 0]
                        dy = 0.5
                        x = np.arange(lx1, lx2 + 1)
                        _lw = 0.1
                        axes.vlines((x[(a == 1)]), (-dy), dy, colors='#ffc04c', lw=_lw)
                        axes.vlines((x[(a == 2)]), (-dy), dy, colors='#4c8bff', lw=_lw)
                        axes.set_xlim([lx1, lx2])
                        axes.set_ylim([-dy, dy])
                        axes.spines['left'].set_visible(False)
                        axes.set_yticks([])
    if index < 2:
        d = 0.005
        b = 0.0225
        points = [0, 0.271 - b, 0.715 - b, 0.735 - b]
        for dp in points:
            kwargs = dict(transform=(axes[0].transAxes), color='#666666', clip_on=False, zorder=10, lw=1)
            (axes[0].plot)((dp - d, dp + d), (-2 * d, 2 * d), **kwargs)
            kwargs.update(transform=(axes[1].transAxes))
            (axes[1].plot)((dp - d, dp + d), (1 - 2 * d, 1 + 2 * d), **kwargs)

        plt.tight_layout()
        axes[1].yaxis.set_label_coords(0.18, 0.45, transform=(f.transFigure))
        plt.subplots_adjust(hspace=0.0)
    else:
        plt.tight_layout()
    if index == 3:
        axes.yaxis.set_label_coords(0.16, 0.42, transform=(f.transFigure))
    if index == 0:
        for ax in axes:
            currpos = ax.get_position()
            print(currpos)

    if index == 1:
        for ax in axes:
            currpos = ax.get_position()
            print(currpos)

    if index > 1:
        currpos = axes.get_position()
        print(currpos)
    return (f, axes)


def fig_1d(data, meta):
    f = plt.figure('Fig. 1D Representative trajectory of a fly walking in the arena', figsize=(3.1,
                                                                                               3.1), dpi=300)
    ax = f.gca()
    ax.set_title('D', fontsize=16, fontweight='bold', loc='left', x=(-0.05))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.axis('off')
    ax.set_xlim([-12, 22])
    ax.set_ylim([-20, 14])
    subsampl = 1
    x, y = np.array(data[data.columns[0]]), np.array(data[data.columns[1]])
    ax.plot((x[::subsampl]), (y[::subsampl]), ls='-', lw=1, color='#888888')
    patch_color = {1:'#ffc04c', 
     2:'#4c8bff',  3:'#ffffff'}
    allowed = [0, 2, 3, 4, 5, 6, 12, 13]
    zoom = False
    for i, patch in enumerate(meta.patches()):
        c = patch_color[patch['substrate']]
        pos = (patch['position'][0], patch['position'][1])
        rad = patch['radius']
        if zoom:
            ax.set_xlim([pos[0] - 2.5, pos[0] + 5])
            ax.set_ylim([pos[1] - 2.5, pos[1] + 5])
            circle = plt.Circle(pos, 2.5, edgecolor='#aaaaaa', fill=False, ls=(0, (4, 4)), lw=2)
            circle.set_zorder(0)
            ax.add_artist(circle)
        if i in allowed:
            circle = plt.Circle(pos, rad, color=c, alpha=0.5)
            circle.set_zorder(0)
            ax.add_artist(circle)
        if i == 6:
            circle = plt.Circle(pos, 5.0, edgecolor='#aaaaaa', fill=False, ls=(0, (4, 4)), lw=2)
            circle.set_zorder(0)
            ax.add_artist(circle)

    ax.set_aspect('equal', 'datalim')
    return (f, ax)


if __name__ == '__main__':
    thisscript = os.path.basename(__file__).split('.')[0]
    profile = get_profile('Vero eLife 2016', 'degoldschmidt', script=thisscript)
    db = Database(get_db(profile))
    log = Logger(profile, scriptname=thisscript)
    analysis(db)
    log.close()
    plotting(db)