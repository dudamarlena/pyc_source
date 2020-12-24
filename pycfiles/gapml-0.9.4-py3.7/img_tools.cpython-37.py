# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gapml/utils/img_tools.py
# Compiled at: 2018-10-05 12:20:41
# Size of source mod 2**32: 12121 bytes
""" Image Utils
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""
import os, random, shutil

class ImgUtils(object):
    __doc__ = '\n    Image Utils: The img_utils module alows users to manage images datasets\n                 (folders and images files) directly on disk.\n\n    Type of Folder Tree\n\n    ## tree = 1 ##\n    [root_path] "folder_name"/..\n        [subfolder] class_0/..\n        [subfolder] class_1/..\n        [subfolder] errors/..\n\n    ## tree = 2 ##\n    [root_path] "folder_name"/..\n        [subfolder] train_tr/..\n            [subfolder] class_0/..\n            [subfolder] class_1/..\n        [subfolder] train_val/..\n            [subfolder] class_0/..\n            [subfolder] class_1/..\n        [subfolder] test/test/..\n        [subfolder] errors/..\n    '

    def __init__(self, root_path='./', tree=1, remove_folder=False):
        """
        Class Constructor
            :param root_path:      main image folder root
            :param tree:           type of folder tree
            :param remove_folder:  remove folder from directory
        """
        self.labels = None
        self.root_path = None
        self.tree = tree
        self.remove_folder = remove_folder
        self._transf = '1to2'
        self._labels_org = []
        self._end = None
        self._end2 = None
        if not os.path.isdir(root_path):
            raise TypeError('String expected for directory path')
        else:
            self.labels = os.listdir(root_path)
            self.root_path = root_path
        if remove_folder:
            answere_ok = False
            while answere_ok is False:
                try:
                    warning = input('Warning! this will delete your image dataset. Are you sure? [Yes/no]: ')
                    warning = warning[0].lower()
                    if warning in ('y', 'n'):
                        answere_ok = True
                except:
                    continue

            if warning == 'y':
                shutil.rmtree(self.root_path)
                print('Your files were deleted')

    def _tree2_path(self):
        """ Getting path for 2to1 """
        if self._transf == '2to1':
            self.root_path = self.root_path.split('/')
            self.root_path = '/'.join(self.root_path[:-1])

    def _list_labels_org(self):
        """ List Labels Origin """
        if self._transf == '1to2':
            self._labels_org = ['{}/{}'.format(self.root_path, lb) for lb in self.labels]
        else:
            if self._transf == '2to1':
                train_tr = ['{}/train_tr/{}'.format(self.root_path, lb) for lb in self.labels]
                train_val = ['{}/train_val/{}'.format(self.root_path, lb) for lb in self.labels]
                self._labels_org = train_tr + train_val

    def _makedirs(self):
        """ Make Directories """
        if self.tree == 1:
            if self._transf == '2to1':
                self.root_path = self.root_path[:-3]
            for lb in self.labels:
                os.makedirs(('{}{}/{}'.format(self.root_path, self._end, lb)), exist_ok=True)

        else:
            if self.tree == 2:
                for lb in self.labels:
                    os.makedirs(('{}{}/train_tr/{}'.format(self.root_path, self._end2, lb)), exist_ok=True)
                    os.makedirs(('{}{}/train_val/{}'.format(self.root_path, self._end2, lb)), exist_ok=True)

                os.makedirs(('{}{}/test/test'.format(self.root_path, self._end2)), exist_ok=True)
                os.makedirs(('{}{}/errors'.format(self.root_path, self._end2)), exist_ok=True)
            else:
                if self.tree is None:
                    pass
                else:
                    print('select between tree=1 or tree=2')

    def _copy_move(self, ppath, action, lb, img_list, index):
        """
        Copy or Move images
        :param ppath:     Required. Partial path
        :param action:    Required. Select between 'copy' or 'move'
        :param lb:        Required. Label name
        :param img_list:  Required. List of images per class
        :param index:     Required. Index image in the list
        """
        label = lb.split('/')[(-1)]
        if self._transf == '1to2':
            org_file = '{}/{}'.format(lb, img_list[index])
            dst_file = '{}{}/{}/{}'.format(self.root_path, ppath, label, img_list[index])
        else:
            if self._transf == '2to1':
                org_file = '{}/{}'.format(lb, img_list)
                dst_file = '{}/{}/{}'.format(self.root_path, label, img_list)
            elif action == 'copy':
                shutil.copy(org_file, dst_file)
            else:
                if action == 'move':
                    shutil.move(org_file, dst_file)
                else:
                    print('select copy or move')

    def img_container(self, action='copy', spl=5, shufle=False, img_split=0.2):
        """
        Images Container
        :param action:    Select between 'copy' or 'move'
        :param spl:       Select the number of pictures for label to create the sample
        :param shufle:    select ramdom images per label or the first images on the list
        :param img_split: percentage of split between train / val
        """
        if action == 'copy':
            self._end = '_spl'
            self._end2 = '_t2' + self._end
        else:
            if action == 'move':
                self._end = ''
                self._end2 = '_t2'
            else:
                print('select copy or move')
        self._list_labels_org()
        self._makedirs()
        for lb in self._labels_org:
            img_list = os.listdir(lb)
            len_img_list = len(img_list)
            if action == 'copy':
                spl = spl
            else:
                if action == 'move':
                    spl = len_img_list
                else:
                    print('select copy or move')
            if shufle:
                list_index = random.sample(range(len_img_list), spl)
            else:
                list_index = list(range(spl))
            if self._transf == '2to1':
                for img in img_list:
                    ppath = None
                    action = 'move'
                    index = None
                    self._copy_move(ppath, action, lb, img, index)

                self.tree = None
            if self.tree == 1:
                for index in list_index:
                    self._copy_move('_spl', action, lb, img_list, index)

            elif self.tree == 2:
                img_tr = int(len(list_index) * (1 - img_split))
                count = 0
                for index in list_index:
                    if count <= img_tr:
                        self._copy_move('{}/train_tr'.format(self._end2), action, lb, img_list, index)
                    else:
                        self._copy_move('{}/train_val'.format(self._end2), action, lb, img_list, index)
                    count += 1

            elif self.tree is None:
                continue
            print('select 1 or 2')

    def transform(self, shufle=False, img_split=0.2):
        """
        Transform
        :param shufle:    select ramdom images per label or the first images on the list
        :param img_split: percentage of split between train / val
        :param transf:    type of folder tree to tranform '1to2' or '2to1'
        """
        self._tree2_path()
        action = 'move'
        if self._transf == '1to2':
            self.tree = 2
            spl = None
            self.img_container(action, spl, shufle, img_split)
            shutil.rmtree(self.root_path)
        else:
            if self._transf == '2to1':
                old_path = self.root_path
                self.img_container(action)
                shutil.rmtree(old_path)
            else:
                print('select 1to2 or 2to1')

    def img_rename(self, text=None):
        """
        Rename Images
        :param text: Give a text for your images name
        """
        if self.tree == 2:
            self._transf = '2to1'
        self._tree2_path()
        self._list_labels_org()
        for lb in self._labels_org:
            img_list = os.listdir(lb)
            text_lb = lb.split('/')[(-1)]
            for i, img in enumerate(img_list):
                if os.path.isdir('{}/{}'.format(lb, img)):
                    print('There is not images to rename')
                    break
                else:
                    dtype = img.split('.')[(-1)]
                    if text is True:
                        img_name = '{}_{}'.format(text_lb, i)
                    else:
                        if text is not None:
                            img_name = '{}_{}'.format(text, i)
                        else:
                            img_name = i
                os.rename('{}/{}'.format(lb, img), '{}/{}.{}'.format(lb, img_name, dtype))

    def img_replace(self, old, new, img_id=False):
        """
        Rename Images
        :param old:    Required. The text you want to replace.
        :param new:    Required. The text you want to replace "old" with.
        :param img_id: True to enumerate by id name_id
        """
        if self.tree == 2:
            self._transf = '2to1'
        self._tree2_path()
        self._list_labels_org()
        for lb in self._labels_org:
            img_list = os.listdir(lb)
            for i, img in enumerate(img_list):
                if os.path.isdir('{}/{}'.format(lb, img)):
                    print('There is not images to replace')
                    break
                if img_id:
                    os.rename('{}/{}'.format(lb, img), '{}/{}'.format(lb, img.replace(old, '{}_{}'.format(new, i))))
                else:
                    os.rename('{}/{}'.format(lb, img), '{}/{}'.format(lb, img.replace(old, new)))

    @property
    def transf(self):
        """ Getter for image transform """
        return self._transf

    @transf.setter
    def transf(self, transf):
        """
        Setter for image transform
            :param transf: type of folder tree to tranform '1to2' or '2to1'
        """
        self._transf = transf

    @property
    def labels_org(self):
        """ Getter for list of origen paths """
        return self._labels_org

    @property
    def end(self):
        """ Getter for name folder extentions (e.g. '_spl', ...) """
        return self._end

    @property
    def end2(self):
        """ Getter for name folder extentions (e.g. '_spl', ...) """
        return self._end2