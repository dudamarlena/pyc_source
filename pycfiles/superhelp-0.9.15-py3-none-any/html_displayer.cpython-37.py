# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/g/projects/superhelp/build/lib/superhelp/displayers/html_displayer.py
# Compiled at: 2020-04-18 17:34:33
# Size of source mod 2**32: 23466 bytes
from pathlib import Path
from textwrap import dedent, indent
import webbrowser
from .. import conf
from markdown import markdown
MESSAGE_LEVEL2CLASS = {message_level:f"help help-{message_level}" for message_level in conf.MESSAGE_LEVELS}
LOGO_SVG = '<svg\n   xmlns:dc="http://purl.org/dc/elements/1.1/"\n   xmlns:cc="http://creativecommons.org/ns#"\n   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n   xmlns:svg="http://www.w3.org/2000/svg"\n   xmlns="http://www.w3.org/2000/svg"\n   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"\n   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"\n   width="93.345726mm"\n   height="65.921318mm"\n   viewBox="0 0 93.345726 65.921318"\n   version="1.1"\n   id="svg8"\n   inkscape:version="0.92.4 (5da689c313, 2019-01-14)"\n   sodipodi:docname="superhelp_logo.svg"\n   inkscape:export-filename="/home/g/projects/superhelp/superhelp_logo.png"\n   inkscape:export-xdpi="96"\n   inkscape:export-ydpi="96">\n  <defs\n     id="defs2">\n    <inkscape:path-effect\n       effect="skeletal"\n       id="path-effect4972"\n       is_visible="true"\n       pattern="m 60.80692,207.585 -0.62276,-0.0405 -0.15389,-0.6048 0.527651,-0.33326 0.479996,0.39885 z"\n       copytype="repeated"\n       prop_scale="1"\n       scale_y_rel="false"\n       spacing="0"\n       normal_offset="0"\n       tang_offset="0"\n       prop_units="false"\n       vertical_pattern="false"\n       fuse_tolerance="0" />\n    <inkscape:path-effect\n       effect="skeletal"\n       id="path-effect4944"\n       is_visible="true"\n       pattern="m 58.866112,205.1261 h 0.701582 v 0.66817 h -0.701582 z"\n       copytype="single_stretched"\n       prop_scale="1"\n       scale_y_rel="false"\n       spacing="0"\n       normal_offset="0"\n       tang_offset="0"\n       prop_units="false"\n       vertical_pattern="false"\n       fuse_tolerance="0" />\n    <inkscape:path-effect\n       effect="skeletal"\n       id="path-effect4907"\n       is_visible="true"\n       pattern="m 61.427734,769.66211 v 9.31641 h 7.748047 v -9.31641 z m 8.271485,0.0156 v 9.31446 h 7.748047 v -9.31446 z"\n       copytype="repeated"\n       prop_scale="1"\n       scale_y_rel="false"\n       spacing="0"\n       normal_offset="0"\n       tang_offset="0"\n       prop_units="false"\n       vertical_pattern="false"\n       fuse_tolerance="0" />\n    <inkscape:path-effect\n       effect="skeletal"\n       id="path-effect4889"\n       is_visible="true"\n       pattern="m 61.427734,769.66211 v 9.31641 h 7.748047 v -9.31641 z m 8.271485,0.0156 v 9.31446 h 7.748047 v -9.31446 z"\n       copytype="repeated_stretched"\n       prop_scale="1"\n       scale_y_rel="false"\n       spacing="0"\n       normal_offset="0"\n       tang_offset="0"\n       prop_units="false"\n       vertical_pattern="false"\n       fuse_tolerance="0" />\n    <inkscape:path-effect\n       effect="skeletal"\n       id="path-effect4861"\n       is_visible="true"\n       pattern="M 0,0 H 1"\n       copytype="single_stretched"\n       prop_scale="1"\n       scale_y_rel="false"\n       spacing="0"\n       normal_offset="0"\n       tang_offset="0"\n       prop_units="false"\n       vertical_pattern="false"\n       fuse_tolerance="0" />\n    <inkscape:path-effect\n       effect="skeletal"\n       id="path-effect4820"\n       is_visible="true"\n       pattern="m 61.427734,769.66211 v 9.31641 h 7.748047 v -9.31641 z m 8.271485,0.0156 v 9.31446 h 7.748047 v -9.31446 z"\n       copytype="repeated_stretched"\n       prop_scale="1"\n       scale_y_rel="false"\n       spacing="0"\n       normal_offset="0"\n       tang_offset="0"\n       prop_units="false"\n       vertical_pattern="false"\n       fuse_tolerance="0" />\n    <inkscape:path-effect\n       effect="skeletal"\n       id="path-effect4721"\n       is_visible="true"\n       pattern="m 61.427734,769.66211 v 9.31641 h 7.748047 v -9.31641 z m 8.271485,0.0156 v 9.31446 h 7.748047 v -9.31446 z"\n       copytype="repeated"\n       prop_scale="1"\n       scale_y_rel="false"\n       spacing="0.1"\n       normal_offset="0"\n       tang_offset="0"\n       prop_units="false"\n       vertical_pattern="false"\n       fuse_tolerance="0" />\n    <inkscape:path-effect\n       effect="skeletal"\n       id="path-effect4694"\n       is_visible="true"\n       pattern="M 0,0 H 1"\n       copytype="single_stretched"\n       prop_scale="1"\n       scale_y_rel="false"\n       spacing="0"\n       normal_offset="0"\n       tang_offset="0"\n       prop_units="false"\n       vertical_pattern="false"\n       fuse_tolerance="0" />\n    <inkscape:path-effect\n       effect="skeletal"\n       id="path-effect935"\n       is_visible="true"\n       pattern="M 0,0 H 1"\n       copytype="single_stretched"\n       prop_scale="1"\n       scale_y_rel="false"\n       spacing="0"\n       normal_offset="0"\n       tang_offset="0"\n       prop_units="false"\n       vertical_pattern="false"\n       fuse_tolerance="0" />\n  </defs>\n  <sodipodi:namedview\n     id="base"\n     pagecolor="#ffffff"\n     bordercolor="#666666"\n     borderopacity="1.0"\n     inkscape:pageopacity="1"\n     inkscape:pageshadow="2"\n     inkscape:zoom="1.979899"\n     inkscape:cx="8.2743457"\n     inkscape:cy="95.321425"\n     inkscape:document-units="mm"\n     inkscape:current-layer="layer1"\n     showgrid="false"\n     inkscape:window-width="1869"\n     inkscape:window-height="1056"\n     inkscape:window-x="1971"\n     inkscape:window-y="24"\n     inkscape:window-maximized="1"\n     fit-margin-top="0"\n     fit-margin-left="0"\n     fit-margin-right="0"\n     fit-margin-bottom="0"\n     inkscape:pagecheckerboard="false" />\n  <metadata\n     id="metadata5">\n    <rdf:RDF>\n      <cc:Work\n         rdf:about="">\n        <dc:format>image/svg+xml</dc:format>\n        <dc:type\n           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />\n        <dc:title></dc:title>\n      </cc:Work>\n    </rdf:RDF>\n  </metadata>\n  <g\n     inkscape:label="Layer 1"\n     inkscape:groupmode="layer"\n     id="layer1"\n     transform="translate(-55.880255,-89.849988)">\n    <path\n       style="fill:#3b3f74;fill-opacity:1;stroke:none;stroke-width:33.15284348;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"\n       d="M 281.68359 0.00390625 C 277.92668 -0.0091550074 274.18542 0.01817 270.50586 0.03125 L 83.767578 0.03125 L 82.986328 0.03125 L 82.986328 0.04296875 A 82.216504 82.216504 0 0 0 11.845703 40.632812 A 82.216504 82.216504 0 0 0 11.480469 123.2207 A 82.216504 82.216504 0 0 0 81.882812 164.40234 L 81.882812 164.68555 L 268.19727 164.68555 L 268.2168 169.17773 L 82.296875 169.17773 L 0 169.17773 A 82.216501 84.506075 0 0 0 10.863281 206.99219 A 82.216501 84.506075 0 0 0 76.419922 248.88281 L 76.419922 249.14062 L 81.845703 249.14062 A 82.216501 84.506075 0 0 0 82.296875 249.15039 L 82.296875 249.14062 L 268.57031 249.14062 L 268.57031 249.15039 A 82.216504 82.216504 0 0 0 268.7793 249.14062 L 269.40234 249.14062 L 269.40234 249.11133 A 82.216504 82.216504 0 0 0 340.12891 207.91406 A 82.216504 82.216504 0 0 0 339.76367 125.32617 A 82.216504 82.216504 0 0 0 269.40234 84.746094 L 269.40234 84.722656 L 83.392578 84.722656 L 83.414062 79.994141 L 270.50586 79.994141 L 270.50586 80.003906 L 352.80273 80.003906 C 352.1333 66.694753 354.48107 36.631983 348.00977 25.083984 C 335.10234 2.1735036 307.98199 0.095335052 281.68359 0.00390625 z "\n       transform="matrix(0.26458333,0,0,0.26458333,55.880255,89.849988)"\n       id="path4991-7-1" />\n    <path\n       style="fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:6.38603258;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"\n       id="path5097"\n       sodipodi:type="arc"\n       sodipodi:cx="140.07877"\n       sodipodi:cy="98.10202"\n       sodipodi:rx="3.2002347"\n       sodipodi:ry="3.2002347"\n       sodipodi:start="3.1432891"\n       sodipodi:end="3.1403035"\n       d="m 136.87854,98.096591 a 3.2002347,3.2002347 0 0 1 3.20327,-3.194804 3.2002347,3.2002347 0 0 1 3.19719,3.200885 3.2002347,3.2002347 0 0 1 -3.1985,3.199578 3.2002347,3.2002347 0 0 1 -3.20197,-3.196104"\n       sodipodi:open="true" />\n    <path\n       style="fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:6.38603258;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"\n       id="path5097-0"\n       sodipodi:type="arc"\n       sodipodi:cx="78.337524"\n       sodipodi:cy="111.3783"\n       sodipodi:rx="3.2002347"\n       sodipodi:ry="3.2002347"\n       sodipodi:start="3.1432891"\n       sodipodi:end="3.1403035"\n       d="m 75.137294,111.37287 a 3.2002347,3.2002347 0 0 1 3.203271,-3.1948 3.2002347,3.2002347 0 0 1 3.197194,3.20089 3.2002347,3.2002347 0 0 1 -3.198498,3.19958 3.2002347,3.2002347 0 0 1 -3.201969,-3.19611"\n       sodipodi:open="true" />\n    <path\n       style="fill:#ffffff;fill-opacity:1;stroke:none;stroke-width:6.38603258;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1"\n       id="path5097-0-9"\n       sodipodi:type="arc"\n       sodipodi:cx="124.23225"\n       sodipodi:cy="133.99762"\n       sodipodi:rx="3.2002347"\n       sodipodi:ry="3.2002347"\n       sodipodi:start="3.1432891"\n       sodipodi:end="3.1403035"\n       d="m 121.03202,133.99219 a 3.2002347,3.2002347 0 0 1 3.20327,-3.1948 3.2002347,3.2002347 0 0 1 3.19719,3.20088 3.2002347,3.2002347 0 0 1 -3.1985,3.19958 3.2002347,3.2002347 0 0 1 -3.20197,-3.1961"\n       sodipodi:open="true" />\n  </g>\n</svg>\n'
BROWSER_HTML_WRAPPER = '<!DOCTYPE html>\n<html lang="en">\n{head}\n<body>\n{logo_svg}\n<h1>SuperHELP - Help for Humans!</h1>\n<p>Help is provided for each block of code in your snippet.\nToggle between different levels of detail.</p>\n{radio_buttons}\n{body_inner}\n{visibility_script}\n</body>\n</html>'
NOTEBOOK_HTML_WRAPPER = '<!DOCTYPE html>\n<html lang="en">\n{head}\n<body>\n<h1>Look here for some help on the snippet in the cell above</h1>\n<p>Help is provided for each block of code in your snippet.\nToggle between different levels of detail.</p>\n{radio_buttons}\n{body_inner}\n{visibility_script}\n</body>\n</html>'
CODE_CSS = '/*From https://richleland.github.io/pygments-css/ */\n.codehilite .hll { background-color: #ffffcc }\n.codehilite  { background: #f8f8f8; }\n.codehilite .c { color: #408080; font-style: italic } /* Comment */\n.codehilite .err { border: 1px solid #FF0000 } /* Error */\n.codehilite .k { color: #008000; font-weight: bold } /* Keyword */\n.codehilite .o { color: #666666 } /* Operator */\n.codehilite .ch { color: #408080; font-style: italic } /* Comment.Hashbang */\n.codehilite .cm { color: #408080; font-style: italic } /* Comment.Multiline */\n.codehilite .cp { color: #BC7A00 } /* Comment.Preproc */\n.codehilite .cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */\n.codehilite .c1 { color: #408080; font-style: italic } /* Comment.Single */\n.codehilite .cs { color: #408080; font-style: italic } /* Comment.Special */\n.codehilite .gd { color: #A00000 } /* Generic.Deleted */\n.codehilite .ge { font-style: italic } /* Generic.Emph */\n.codehilite .gr { color: #FF0000 } /* Generic.Error */\n.codehilite .gh { color: #000080; font-weight: bold } /* Generic.Heading */\n.codehilite .gi { color: #00A000 } /* Generic.Inserted */\n.codehilite .go { color: #888888 } /* Generic.Output */\n.codehilite .gp { color: #000080; font-weight: bold } /* Generic.Prompt */\n.codehilite .gs { font-weight: bold } /* Generic.Strong */\n.codehilite .gu { color: #800080; font-weight: bold } /* Generic.Subheading */\n.codehilite .gt { color: #0044DD } /* Generic.Traceback */\n.codehilite .kc { color: #008000; font-weight: bold } /* Keyword.Constant */\n.codehilite .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */\n.codehilite .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */\n.codehilite .kp { color: #008000 } /* Keyword.Pseudo */\n.codehilite .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */\n.codehilite .kt { color: #B00040 } /* Keyword.Type */\n.codehilite .m { color: #666666 } /* Literal.Number */\n.codehilite .s { color: #BA2121 } /* Literal.String */\n.codehilite .na { color: #7D9029 } /* Name.Attribute */\n.codehilite .nb { color: #008000 } /* Name.Builtin */\n.codehilite .nc { color: #0000FF; font-weight: bold } /* Name.Class */\n.codehilite .no { color: #880000 } /* Name.Constant */\n.codehilite .nd { color: #AA22FF } /* Name.Decorator */\n.codehilite .ni { color: #999999; font-weight: bold } /* Name.Entity */\n.codehilite .ne { color: #D2413A; font-weight: bold } /* Name.Exception */\n.codehilite .nf { color: #0000FF } /* Name.Function */\n.codehilite .nl { color: #A0A000 } /* Name.Label */\n.codehilite .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */\n.codehilite .nt { color: #008000; font-weight: bold } /* Name.Tag */\n.codehilite .nv { color: #19177C } /* Name.Variable */\n.codehilite .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */\n.codehilite .w { color: #bbbbbb } /* Text.Whitespace */\n.codehilite .mb { color: #666666 } /* Literal.Number.Bin */\n.codehilite .mf { color: #666666 } /* Literal.Number.Float */\n.codehilite .mh { color: #666666 } /* Literal.Number.Hex */\n.codehilite .mi { color: #666666 } /* Literal.Number.Integer */\n.codehilite .mo { color: #666666 } /* Literal.Number.Oct */\n.codehilite .sa { color: #BA2121 } /* Literal.String.Affix */\n.codehilite .sb { color: #BA2121 } /* Literal.String.Backtick */\n.codehilite .sc { color: #BA2121 } /* Literal.String.Char */\n.codehilite .dl { color: #BA2121 } /* Literal.String.Delimiter */\n.codehilite .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */\n.codehilite .s2 { color: #BA2121 } /* Literal.String.Double */\n.codehilite .se { color: #BB6622; font-weight: bold } /* Literal.String.Escape */\n.codehilite .sh { color: #BA2121 } /* Literal.String.Heredoc */\n.codehilite .si { color: #BB6688; font-weight: bold } /* Literal.String.Interpol */\n.codehilite .sx { color: #008000 } /* Literal.String.Other */\n.codehilite .sr { color: #BB6688 } /* Literal.String.Regex */\n.codehilite .s1 { color: #BA2121 } /* Literal.String.Single */\n.codehilite .ss { color: #19177C } /* Literal.String.Symbol */\n.codehilite .bp { color: #008000 } /* Name.Builtin.Pseudo */\n.codehilite .fm { color: #0000FF } /* Name.Function.Magic */\n.codehilite .vc { color: #19177C } /* Name.Variable.Class */\n.codehilite .vg { color: #19177C } /* Name.Variable.Global */\n.codehilite .vi { color: #19177C } /* Name.Variable.Instance */\n.codehilite .vm { color: #19177C } /* Name.Variable.Magic */\n.codehilite .il { color: #666666 } /* Literal.Number.Integer.Long */\n'
INTERNAL_CSS = 'body {\n  background-color: white;\n  %(margin_css)s\n}\nh1, h2 {\n  color: #3b3f74;\n  font-weight: bold;\n}\nh1 {\n  font-size: 16px;\n}\nh2 {\n  font-size: 14px;\n  margin-top: 24px;\n}\nh3 {\n  font-size: 12px;\n}\nh4 {\n  font-size: 11px;\n}\n.warning h4 {\n  margin: 0;\n}\nh5 {\n  font-size: 9px;\n  font-style: italic;\n}\np {\n  font-size: 10px;\n}\nli {\n  font-size: 10px;\n}\nlabel {\n  font-size: 12px;\n}\nsvg {\n  height: 50px;\n  width: 70px;\n}\n.warning {\n  border-radius: 3px;\n  padding: 6px;\n  margin: 10px 0 0 0;\n  border: 1px solid #d86231;\n}\n.help {\n  display: none;\n}\n.help.help-visible {\n  display: inherit;\n}\n%(code_css)s\n'
HTML_HEAD = '<head>\n<meta charset="utf-8">\n<meta content="IE=edge" http-equiv="X-UA-Compatible">\n<title>SuperHELP - Help for Humans!</title>\n<style type="text/css">\n%(internal_css)s\n</style>\n</head>'
VISIBILITY_SCRIPT = '<script>\n function updateVerbosity() {\n   var verbositySelectors = {\n     \'%(brief)s\': \'.help-%(brief)s\',\n     \'%(main)s\': \'.help-%(main)s\',\n     \'%(extra)s\': \'.help-%(main)s, .help-%(extra)s\'\n   }\n   // Get selected verbosity.\n   var verbosity = document.querySelector(\'input[name="verbosity"]:checked\').value;\n   // Hide all helps.\n   document.querySelectorAll(\'.help\').forEach(function(helpElement) {\n     helpElement.classList.remove(\'help-visible\');\n   });\n   // Show only selected helps.\n   document.querySelectorAll(verbositySelectors[verbosity]).forEach(function(helpElement) {\n     helpElement.classList.add(\'help-visible\');\n   });\n }\n\n // Update verbosity after page load.\n updateVerbosity();\n\n // Update verbosity whenever a radio is changed.\n var radios = document.querySelectorAll(\'input[name="verbosity"]\');\n radios.forEach(function(radio) {\n   radio.addEventListener(\'change\', updateVerbosity);\n });\n</script>\n' % {'brief':conf.BRIEF,  'main':conf.MAIN,  'extra':conf.EXTRA}
PART = 'part'
IS_CODE = 'is_code'

def _get_radio_buttons(*, message_level=conf.BRIEF):
    radio_buttons_dets = []
    for message_type in conf.MESSAGE_LEVELS:
        checked = ' checked' if message_type == message_level else ''
        radio_button_dets = f'            <input type="radio"\n             id="radio-verbosity-{message_type}"\n             name="verbosity"\n             value="{message_type}"{checked}>\n            <label for="radio-verbosity-{message_type}">{message_type}</label>\n            '
        radio_buttons_dets.append(radio_button_dets)

    radio_buttons = '\n'.join(radio_buttons_dets)
    return radio_buttons


def get_separate_code_message_parts(message):
    """
    Need to handle code portions differently so need to separate it out.

    :return: list of message part details
     [{'part': 'asdf', 'is_code': False}, ...]
    :rtype: list
    """
    message_parts = []
    open_code_block = False
    lines = message.split('\n')
    for i, line in enumerate(lines):
        first_line = i == 0
        line_in_code_block = line.startswith('    ')
        if line_in_code_block:
            if open_code_block:
                open_code_part = message_parts[(-1)]
                open_code_part[PART] += f"\n{line}"
            else:
                message_parts.append({PART: line, IS_CODE: True})
            open_code_block = True
        else:
            if first_line or open_code_block:
                message_parts.append({PART: line, IS_CODE: False})
            else:
                open_non_code_part = message_parts[(-1)]
                open_non_code_part[PART] += f"\n{line}"
            open_code_block = False

    return message_parts


def get_html_strs(message, message_type, *, warning=False):
    if not message:
        return []
    div_class = MESSAGE_LEVEL2CLASS[message_type]
    warning_class = ' warning' if warning else ''
    str_html_list = [f"<div class='{div_class}{warning_class}'>"]
    message_parts = get_separate_code_message_parts(message)
    for message_part in message_parts:
        if message_part[IS_CODE]:
            message_part_str = markdown((message_part[PART]),
              extensions=['codehilite'])
        else:
            message_part_str = markdown(dedent(message_part[PART]))
        str_html_list.append(message_part_str)

    str_html_list.append('</div>')
    return str_html_list


def get_message_html_strs(message_dets):
    """
    Process message.
    """
    message_html_strs = []
    for message_level in conf.MESSAGE_LEVELS:
        try:
            message = message_dets.message[message_level]
        except KeyError:
            if message_level != conf.EXTRA:
                raise Exception(f"Missing required message level {message_level}")
        except TypeError:
            raise TypeError(f"Missing message in message_dets {message_dets}")
        else:
            message = message.replace(conf.PYTHON_CODE_START, conf.MD_PYTHON_CODE_START).replace(f"\n    {conf.PYTHON_CODE_END}", '')
            message_level_html_strs = get_html_strs(message,
              message_level, warning=(message_dets.warning))
            message_html_strs.extend(message_level_html_strs)

    return message_html_strs


def repeat_overall_snippet(snippet):
    html_strs = []
    html_strs.append('<h2>Overall Snippet</h2>')
    overall_code_str = indent(f"{conf.MD_PYTHON_CODE_START}\n{snippet}", '    ')
    overall_code_str_highlighted = markdown(overall_code_str,
      extensions=['codehilite'])
    html_strs.append(overall_code_str_highlighted)
    return html_strs


def _get_all_html_strs(snippet, overall_messages_dets, block_messages_dets, *, in_notebook=False):
    """
    Display all message types - eventually will show brief and, if the user
    clicks to expand, main instead with the option of expanding to show Extra.

    Suppress overall snippet display if in notebook - it is right above already
    and repeating it is confusing and obscures the feedback.
    """
    all_html_strs = []
    if not in_notebook:
        overall_snippet_html_strs = repeat_overall_snippet(snippet)
        all_html_strs.extend(overall_snippet_html_strs)
    for message_dets in overall_messages_dets:
        message_html_strs = get_message_html_strs(message_dets)
        all_html_strs.extend(message_html_strs)

    block_messages_dets.sort(key=(lambda nt: nt.first_line_no))
    prev_line_no = None
    for message_dets in block_messages_dets:
        line_no = message_dets.first_line_no
        if line_no != prev_line_no:
            all_html_strs.append(f"<h2>Code block starting line {line_no:,}</h2>")
            block_code_str = indent(f"{conf.MD_PYTHON_CODE_START}\n{message_dets.code_str}", '    ')
            block_code_str_highlighted = markdown(block_code_str,
              extensions=['codehilite'])
            all_html_strs.append(block_code_str_highlighted)
            prev_line_no = line_no
        message_html_strs = get_message_html_strs(message_dets)
        all_html_strs.extend(message_html_strs)

    return all_html_strs


def _get_head(*, in_notebook=False):
    internal_css = INTERNAL_CSS % {'code_css':CODE_CSS, 
     'margin_css':'' if in_notebook else 'margin: 60px 80px 80px 80px;'}
    head = HTML_HEAD % {'internal_css': internal_css}
    return head


def display(snippet, messages_dets, *, message_level=conf.BRIEF, in_notebook=False):
    """
    Show for overall snippet and then by code blocks as appropriate.

    :param bool in_notebook: if True, return HTML as string; else open browser
     and display
    """
    radio_buttons = _get_radio_buttons(message_level=message_level)
    overall_messages_dets, block_messages_dets = messages_dets
    all_html_strs = _get_all_html_strs(snippet, overall_messages_dets,
      block_messages_dets, in_notebook=in_notebook)
    body_inner = '\n'.join(all_html_strs)
    head = _get_head(in_notebook=in_notebook)
    if in_notebook:
        html2write = NOTEBOOK_HTML_WRAPPER.format(head=head,
          radio_buttons=radio_buttons,
          body_inner=body_inner,
          visibility_script=VISIBILITY_SCRIPT)
        return html2write
    html2write = BROWSER_HTML_WRAPPER.format(head=head,
      logo_svg=LOGO_SVG,
      radio_buttons=radio_buttons,
      body_inner=body_inner,
      visibility_script=VISIBILITY_SCRIPT)
    explained_fpath = Path.cwd() / 'explained.html'
    with open(explained_fpath, 'w') as (f):
        f.write(html2write)
    url = explained_fpath.as_uri()
    webbrowser.open_new_tab(url)