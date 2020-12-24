# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/image/image_utils.py
# Compiled at: 2016-06-13 14:11:03
"""
Helper methods to deal with images.

This is essentially a copy from nova.virt.images.py
Some slight modifications, but at some point
we should look at maybe pushign this up to OSLO
"""
import os, re, tempfile
from oslo.config import cfg
from vsm import exception
from vsm import flags
from vsm.openstack.common import log as logging
from vsm import utils
LOG = logging.getLogger(__name__)
image_helper_opt = [
 cfg.StrOpt('image_conversion_dir', default='/tmp', help='parent dir for tempdir used for image conversion')]
FLAGS = flags.FLAGS
FLAGS.register_opts(image_helper_opt)

class QemuImgInfo(object):
    BACKING_FILE_RE = re.compile('^(.*?)\\s*\\(actual\\s+path\\s*:\\s+(.*?)\\)\\s*$', re.I)
    TOP_LEVEL_RE = re.compile('^([\\w\\d\\s\\_\\-]+):(.*)$')
    SIZE_RE = re.compile('\\(\\s*(\\d+)\\s+bytes\\s*\\)', re.I)

    def __init__(self, cmd_output):
        details = self._parse(cmd_output)
        self.image = details.get('image')
        self.backing_file = details.get('backing_file')
        self.file_format = details.get('file_format')
        self.virtual_size = details.get('virtual_size')
        self.cluster_size = details.get('cluster_size')
        self.disk_size = details.get('disk_size')
        self.snapshots = details.get('snapshot_list', [])
        self.encryption = details.get('encryption')

    def __str__(self):
        lines = [
         'image: %s' % self.image,
         'file_format: %s' % self.file_format,
         'virtual_size: %s' % self.virtual_size,
         'disk_size: %s' % self.disk_size,
         'cluster_size: %s' % self.cluster_size,
         'backing_file: %s' % self.backing_file]
        if self.snapshots:
            lines.append('snapshots: %s' % self.snapshots)
        return ('\n').join(lines)

    def _canonicalize(self, field):
        field = field.lower().strip()
        for c in (' ', '-'):
            field = field.replace(c, '_')

        return field

    def _extract_bytes(self, details):
        real_size = self.SIZE_RE.search(details)
        if real_size:
            details = real_size.group(1)
        try:
            details = utils.to_bytes(details)
        except (TypeError, ValueError):
            pass

        return details

    def _extract_details(self, root_cmd, root_details, lines_after):
        consumed_lines = 0
        real_details = root_details
        if root_cmd == 'backing_file':
            backing_match = self.BACKING_FILE_RE.match(root_details)
            if backing_match:
                real_details = backing_match.group(2).strip()
        elif root_cmd in ('virtual_size', 'cluster_size', 'disk_size'):
            real_details = self._extract_bytes(root_details)
        elif root_cmd == 'file_format':
            real_details = real_details.strip().lower()
        elif root_cmd == 'snapshot_list':
            if not lines_after or not lines_after[0].startswith('ID'):
                msg = _('Snapshot list encountered but no header found!')
                raise ValueError(msg)
            consumed_lines += 1
            possible_contents = lines_after[1:]
            real_details = []
            for line in possible_contents:
                line_pieces = line.split(None)
                if len(line_pieces) != 6:
                    break
                else:
                    date_pieces = line_pieces[5].split(':')
                    if len(date_pieces) != 3:
                        break
                    real_details.append({'id': line_pieces[0], 
                       'tag': line_pieces[1], 
                       'vm_size': line_pieces[2], 
                       'date': line_pieces[3], 
                       'vm_clock': line_pieces[4] + ' ' + line_pieces[5]})
                    consumed_lines += 1

        return (
         real_details, consumed_lines)

    def _parse(self, cmd_output):
        if not cmd_output:
            cmd_output = ''
        contents = {}
        lines = cmd_output.splitlines()
        i = 0
        line_am = len(lines)
        while i < line_am:
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            consumed_lines = 0
            top_level = self.TOP_LEVEL_RE.match(line)
            if top_level:
                root = self._canonicalize(top_level.group(1))
                if not root:
                    i += 1
                    continue
                root_details = top_level.group(2).strip()
                details, consumed_lines = self._extract_details(root, root_details, lines[i + 1:])
                contents[root] = details
            i += consumed_lines + 1

        return contents


def qemu_img_info(path):
    """Return a object containing the parsed output from qemu-img info."""
    out, err = utils.execute('env', 'LC_ALL=C', 'LANG=C', 'qemu-img', 'info', path, run_as_root=True)
    return QemuImgInfo(out)


def convert_image(source, dest, out_format):
    """Convert image to other format"""
    cmd = (
     'qemu-img', 'convert', '-O', out_format, source, dest)
    utils.execute(run_as_root=True, *cmd)


def fetch(context, image_service, image_id, path, _user_id, _project_id):
    with utils.remove_path_on_error(path):
        with open(path, 'wb') as (image_file):
            image_service.download(context, image_id, image_file)


def fetch_to_raw(context, image_service, image_id, dest, user_id=None, project_id=None):
    if FLAGS.image_conversion_dir and not os.path.exists(FLAGS.image_conversion_dir):
        os.makedirs(FLAGS.image_conversion_dir)
    fd, tmp = tempfile.mkstemp(dir=FLAGS.image_conversion_dir)
    os.close(fd)
    with utils.remove_path_on_error(tmp):
        fetch(context, image_service, image_id, tmp, user_id, project_id)
        data = qemu_img_info(tmp)
        fmt = data.file_format
        if fmt is None:
            raise exception.ImageUnacceptable(reason=_("'qemu-img info' parsing failed."), image_id=image_id)
        backing_file = data.backing_file
        if backing_file is not None:
            raise exception.ImageUnacceptable(image_id=image_id, reason=_('fmt=%(fmt)s backed by:%(backing_file)s') % locals())
        LOG.debug('%s was %s, converting to raw' % (image_id, fmt))
        convert_image(tmp, dest, 'raw')
        data = qemu_img_info(dest)
        if data.file_format != 'raw':
            raise exception.ImageUnacceptable(image_id=image_id, reason=_('Converted to raw, but format is now %s') % data.file_format)
        os.unlink(tmp)
    return


def upload_storage(context, image_service, image_meta, storage_path):
    image_id = image_meta['id']
    if image_meta['disk_format'] == 'raw':
        LOG.debug('%s was raw, no need to convert to %s' % (
         image_id, image_meta['disk_format']))
        with utils.temporary_chown(storage_path):
            with utils.file_open(storage_path) as (image_file):
                image_service.update(context, image_id, {}, image_file)
        return
    if FLAGS.image_conversion_dir and not os.path.exists(FLAGS.image_conversion_dir):
        os.makedirs(FLAGS.image_conversion_dir)
    fd, tmp = tempfile.mkstemp(dir=FLAGS.image_conversion_dir)
    os.close(fd)
    with utils.remove_path_on_error(tmp):
        LOG.debug('%s was raw, converting to %s' % (
         image_id, image_meta['disk_format']))
        convert_image(storage_path, tmp, image_meta['disk_format'])
        data = qemu_img_info(tmp)
        if data.file_format != image_meta['disk_format']:
            raise exception.ImageUnacceptable(image_id=image_id, reason=_('Converted to %(f1)s, but format is now %(f2)s') % {'f1': image_meta['disk_format'], 'f2': data.file_format})
        with utils.file_open(tmp) as (image_file):
            image_service.update(context, image_id, {}, image_file)
        os.unlink(tmp)