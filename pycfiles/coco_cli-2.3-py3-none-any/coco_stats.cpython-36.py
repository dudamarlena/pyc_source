# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ashwin/Desktop/Projects/COCO-Assistant/coco_assistant/coco_stats.py
# Compiled at: 2019-11-17 11:40:26
# Size of source mod 2**32: 6881 bytes
import logging, os, matplotlib.pyplot as plt, pandas as pd
from pycocotools.coco import COCO
import seaborn as sns
logging.basicConfig(level=(logging.DEBUG))

def cat_count(anns, names, show_count=False, save=False):
    fig, axes = plt.subplots(1, (len(anns)), sharey=False)
    if len(anns) == 1:
        axes = [
         axes]
    for ann, name, ax in zip(anns, names, axes):
        ann_df = pd.DataFrame(ann.anns).transpose()
        if 'category_name' in ann_df.columns:
            chart = sns.countplot(data=ann_df, x='category_name',
              order=(ann_df['category_name'].value_counts().index),
              palette='Set1',
              ax=ax)
        else:
            ann_df['category_name'] = ann_df.apply((lambda row: ann.cats[row.category_id]['name']), axis=1)
            chart = sns.countplot(data=ann_df, x='category_name',
              order=(ann_df['category_name'].value_counts().index),
              palette='Set1',
              ax=ax)
        chart.set_title(name)
        chart.set_xticklabels((chart.get_xticklabels()), rotation=90)
        if show_count is True:
            for p in chart.patches:
                height = p.get_height()
                chart.text((p.get_x() + p.get_width() / 2.0), (height + 0.9),
                  height,
                  ha='center')

    plt.suptitle('Instances per category', fontsize=14, fontweight='bold')
    plt.tight_layout()
    fig = plt.gcf()
    fig.set_size_inches(11, 11)
    out_dir = os.path.join(os.getcwd(), 'results', 'plots')
    if save is True:
        if os.path.exists(out_dir) is False:
            os.mkdir(out_dir)
        plt.savefig((os.path.join(out_dir, 'cat_dist.png')), bbox_inches='tight',
          pad_inches=0,
          dpi=(plt.gcf().dpi))
    plt.show()


def get_areas(ann):
    obj_areas = []
    for key in ann.anns:
        obj_areas.append(ann.anns[key]['area'])

    return obj_areas


def view_area_dist(ann):
    obj_areas = get_areas(ann)
    plt.plot(range(len(obj_areas)), obj_areas)
    plt.xlabel('Objects')
    plt.ylabel('Areas')
    plt.title('Area Distribution')
    plt.show()


def get_object_size_split(ann, areaRng):
    obj_areas = get_areas(ann)
    if areaRng != sorted(areaRng):
        raise AssertionError('Area ranges incorrectly provided')
    small = len(ann.getAnnIds(areaRng=[areaRng[0] ** 2, areaRng[1] ** 2]))
    medium = len(ann.getAnnIds(areaRng=[areaRng[1] ** 2, areaRng[2] ** 2]))
    large = len(ann.getAnnIds(areaRng=[areaRng[2] ** 2, areaRng[3] ** 2]))
    left_out = len(ann.getAnnIds(areaRng=[0, areaRng[0] ** 2])) + len(ann.getAnnIds(areaRng=[areaRng[3] ** 2, 10000000000.0]))
    logging.debug('Number of small objects in set = %s', small)
    logging.debug('Number of medium objects in set = %s'.medium)
    logging.debug('Number of large objects in set = %s'.large)
    if left_out != 0:
        logging.debug('Number of objects ignored in set = %s', left_out)
    logging.debug('Number of objects = %s'.len(obj_areas))
    if len(obj_areas) != small + medium + large + left_out:
        raise AssertionError('Sum of objects in different area ranges != Total number of objects')
    return (small, medium, large, left_out)


def pi_area_split_single(ann, areaRng):
    small, medium, large, left_out = get_object_size_split(ann, areaRng)
    if left_out != 0:
        sizes = [
         small, large, left_out, medium]
        labels = ('Small', 'Large', 'Ignored', 'Medium')
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    else:
        sizes = [
         small, large, medium]
        labels = ('Small', 'Large', 'Medium')
        colors = ['#ff9999', '#66b3ff', '#ffcc99']
    _, ax1 = plt.subplots()
    ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.2f%%', startangle=90)
    centre_circle = plt.Circle((0, 0), 0.7, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis('equal')
    plt.title('Object Size Distribution', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.show()


def pi_area_split(anns, names, areaRng, save=False):
    stuff = []
    for ann in anns:
        small, medium, large, left_out = get_object_size_split(ann, areaRng)
        if left_out != 0:
            sizes = [
             small, large, left_out, medium]
            labels = ('Small', 'Large', 'Ignored', 'Medium')
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        else:
            sizes = [
             small, large, medium]
            labels = ('Small', 'Large', 'Medium')
            colors = ['#ff9999', '#66b3ff', '#ffcc99']
        stuff.append([sizes, labels, colors])

    fig, axs = plt.subplots(1, (len(anns)), figsize=(11, 11))
    for s, name, ax in zip(stuff, names, axs.flat):
        ax.clear()
        ax.pie((s[0]), labels=(s[1]), colors=(s[2]), autopct='%1.2f%%', startangle=90)
        ax.set_title(name)

    fig.suptitle('Object Size Distribution', fontsize=14, fontweight='bold')
    out_dir = os.path.join(os.getcwd(), 'results', 'plots')
    if save is True:
        if os.path.exists(out_dir) is False:
            os.mkdir(out_dir)
        plt.savefig((os.path.join(out_dir, 'area_dist.png')), dpi=(fig.dpi))
    plt.show()


if __name__ == '__main__':
    folder1 = 'test1'
    annFile1 = os.path.join(os.getcwd(), 'annotations', '{}.json'.format(folder1))
    ann1 = COCO(annFile1)
    folder2 = 'test2'
    annFile2 = os.path.join(os.getcwd(), 'annotations', '{}.json'.format(folder2))
    ann2 = COCO(annFile2)
    folder3 = 'test3'
    annFile3 = os.path.join(os.getcwd(), 'annotations', '{}.json'.format(folder3))
    ann3 = COCO(annFile3)