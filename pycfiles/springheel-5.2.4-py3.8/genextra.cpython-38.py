# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/genextra.py
# Compiled at: 2019-12-29 20:38:14
# Size of source mod 2**32: 3186 bytes
import json, os, shutil

class EXpage:
    __doc__ = "\n    An extras page.\n\n    Parameters\n    ----------\n    headings : list\n        The page's navigational headings.\n    content : str\n        The generated HTML for the extras page.\n    "

    def __init__(self):
        """Constructor for the EXpage class."""
        self.headings = []


def gen_extra(i_path, o_path, extras_j, translated_strings):
    """
    Generate an extras page.

    Parameters
    ----------
    i_path : str
        Path to the input folder.
    o_path : str
        Path to the output folder.
    extras_j : str
        Path to the Extra.json file.
    translated_strings : dict
        The translation file contents for this site.
    Returns
    -------
    extras : EXpage
        The completed extras page.
    j : dict
        Raw JSON of the extras page.
    """
    with open(extras_j, 'r') as (f):
        f_raw = f.read()
    j = json.loads(f_raw)
    extras = EXpage()
    extra_elements = []
    for cat in sorted(j.keys()):
        extras.headings.append(cat)
        subhead = '<h2>{cat}</h2>'.format(cat=cat)
        extra_elements.append(subhead)
        for el in j[cat]:
            title = '<h3>{title}</h3>'.format(title=(el['title']))
            if el['type'] == 'image':
                images = []
                for image in el['files']:
                    images.append('<img src="{image}" alt="{title}" />'.format(title=(el['title']), image=image))
                    shutil.copy(os.path.join(i_path, image), os.path.join(o_path, image))
                else:
                    images = ''.join(images)
                    el_template = '<figure>{images}<figcaption>{image_s}{desc}</figcaption></figure>'.format(images=images, image_s=(translated_strings['image_s']), desc=(el['desc']))

            else:
                fils = []
                for fil in el['files']:
                    fils.append('<li><a href="{path}">{link}</a></li>'.format(path=(fil['path']), link=(fil['link'])))
                    shutil.copy(os.path.join(i_path, fil['path']), os.path.join(o_path, fil['path']))
                else:
                    fils = ''.join(fils)
                    el_template = '<p>{desc}</p><ul>{fils}</ul>'.format(desc=(el['desc']), fils=fils)

            elem = '\n'.join([title, el_template])
            extra_elements.append(elem)
        else:
            extra_combined = '\n'.join(extra_elements)
            extras.content = extra_combined
            return (extras, j)