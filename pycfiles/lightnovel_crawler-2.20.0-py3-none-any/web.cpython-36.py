# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/binders/web.py
# Compiled at: 2020-03-23 11:49:43
# Size of source mod 2**32: 2873 bytes
import logging, os
from ..assets.html_style import get_value as get_css_style
logger = logging.getLogger('WEB_BINDER')

def bind_html_chapter(chapter, prev_chapter, next_chapter, direction='ltr'):
    prev_button = '%s.html' % str(prev_chapter['id']).rjust(5, '0') if prev_chapter else '#'
    next_button = '%s.html' % str(next_chapter['id']).rjust(5, '0') if next_chapter else '#'
    button_group = '<div class="link-group">'
    button_group += '<a class="btn" href="%s">Previous</a>' % prev_button
    button_group += '<a class="btn" href="%s">Next</a>' % next_button
    button_group += '</div>'
    script = "\n    window.addEventListener('scroll', function(e) {\n        try {\n            var scroll = window.scrollY;\n            var height = document.body.scrollHeight - window.innerHeight + 10;\n            var percent = Math.round(100.0 * scroll / height);\n            document.getElementById('readpos').innerText = percent + '%';\n        } catch (err) {\n            // ignore\n        }\n    })\n    "
    main_body = chapter['body']
    if not main_body:
        main_body = '<h1>%s</h1><p>No contents</p>' % chapter['title']
    html = '<!DOCTYPE html>\n'
    html += '<html dir="%s"><head>' % direction
    html += '<meta charset="utf-8"/>'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
    html += '<title>%s</title>' % chapter['title']
    html += '<style>%s</style>' % get_css_style()
    html += '<script>%s</script>' % script
    html += '</head><body><div id="content">'
    html += button_group
    html += '<main>%s</main>' % main_body
    html += button_group
    html += '</div>'
    html += '<div id="readpos">0%</div>'
    html += '</body></html>'
    file_name = '%s.html' % str(chapter['id']).rjust(5, '0')
    return (html, file_name)


def make_webs(app, data):
    web_files = []
    for vol in data:
        dir_name = os.path.join(app.output_path, 'web', vol)
        os.makedirs(dir_name, exist_ok=True)
        for i in range(len(data[vol])):
            chapter = data[vol][i]
            prev_chapter = data[vol][(i - 1)] if i > 0 else None
            next_chapter = data[vol][(i + 1)] if i + 1 < len(data[vol]) else None
            direction = 'rtl' if app.crawler.is_rtl else 'ltr'
            html, file_name = bind_html_chapter(chapter, prev_chapter, next_chapter, direction)
            file_name = os.path.join(dir_name, file_name)
            with open(file_name, 'w', encoding='utf-8') as (file):
                file.write(html)
            web_files.append(file_name)

    print('Created: %d web files' % len(web_files))
    return web_files