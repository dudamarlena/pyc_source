# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jcanady/repos/Utterson/bin/utterson_lib/core.py
# Compiled at: 2013-09-05 09:42:09
import yaml, curses, curses.textpad, os, subprocess, shutil, argparse, collections
from curses import wrapper
import time, os.path, datetime
config = None
startup_opts = None
utterson_version = '0.02 - Dev'
jekyll_config = None
jekyll_local_server = None

def window_prep(stdscr, title, options):
    """Prepare the window by clearing it and adding a border."""
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()
    stdscr.border(0)
    window_header(stdscr, title)
    if options is not None:
        window_menu(stdscr, options)
    return


def window_header(stdscr, title):
    """Adds a header to the window with the title on the left."""
    header = ' ' + title + ' ' * (curses.COLS - len(title) - 1)
    stdscr.addstr(0, 0, header, curses.A_STANDOUT)


def notice_header(stdscr, notice):
    """Adds the first 50 characters of the notice to the header."""
    notice = notice.strip()
    if len(notice) > 50:
        text = notice[:50]
    else:
        text = ' ' * (50 - len(notice)) + notice
    stdscr.addstr(0, curses.COLS - 50, text, curses.A_STANDOUT)


def window_menu(stdscr, options):
    """
  Displays the menu items at the bottom of the screen.

  Options = (<letter>: <title>)

  Example

  ('Q':'quit', 'P':'publish') => Q - Quit  P - Publish

  """
    opstr = ''
    for key, value in options.items():
        opstr += key + '-' + value + '   '
        stdscr.addstr(curses.LINES - 1, 2, opstr[:curses.COLS - 3])


def build_full_screen_menu(stdscr, opts):
    """

  Builds a fulls screen menu based on opts.

  [title, desc, display]

  Example:
  opts = collections.OrderedDict()
      opts['I'] = ['Posts', 'Created/Edit/Delete blog posts.', 'dim']
      opts['G'] = ['Pages', 'Manage static pages']
      opts['C'] = ['Categories', 'Created/Edit/Delete categories posts']
      opts['T'] = ['Tags', 'Created/Edit/Delete tags posts']
      opts['S'] = ['Settings', 'Manage utterson settings']
      opts['Q'] = ['Quit', 'exit utterson']

  """
    largest_total_length = 0
    largest_word_to_desc_offset = 0
    for key, value in opts.items():
        if len(value[0]) + 1 > largest_word_to_desc_offset:
            largest_word_to_desc_offset = len(value[0]) + 1
        if len(key + value[0] + value[1]) > largest_total_length:
            largest_total_length = len(key + value[0] + value[1])
            continue

    line_offset = (curses.LINES - 2 - len(opts) - len(opts) + 1) // 2
    cols_offset = (curses.COLS - largest_total_length - 4 - 3) // 2
    item_num = 0
    for key, value in opts.items():
        line = key + '    ' + value[0] + ' ' * (largest_word_to_desc_offset - len(value[0])) + '- ' + value[1]
        if len(value) >= 3:
            if value[2] == 'dim':
                stdscr.addstr(line_offset + item_num, cols_offset, line, curses.A_DIM)
            if value[2] == 'normal':
                stdscr.addstr(line_offset + item_num, cols_offset, line, curses.A_NORMAL)
        else:
            stdscr.addstr(line_offset + item_num, cols_offset, line, curses.A_NORMAL)
        item_num += 2


def home_screen(stdscr):
    """Runs the home screen"""
    redraw = True
    key = 0
    while not check_key(key, 'q'):
        if redraw:
            lines_offset = (curses.LINES - 2 - 11) // 2
            cols_offset = (curses.COLS - 45) // 2
            window_prep(stdscr, 'utterson', None)
            opts = collections.OrderedDict()
            opts['P'] = ['Posts', 'Created/Edit/Delete blog posts', 'normal']
            opts['X'] = [
             'Tools', 'Publish Site, Local Server, etc', 'normal']
            opts['S'] = ['Settings', 'Manage utterson settings', 'normal']
            opts['Q'] = ['Quit', 'Exit utterson', 'normal']
            build_full_screen_menu(stdscr, opts)
        key = stdscr.getch()
        if check_key(key, 'p'):
            posts_main_screen(stdscr)
        elif check_key(key, 'u'):
            update_server(stdscr)
        elif check_key(key, 's'):
            setting_screen(stdscr)
        elif check_key(key, 'x'):
            tools_screen(stdscr)
            window_prep(stdscr, 'utterson: Home', None)
            redraw = True
            continue

    if is_jekyll_server_running():
        start_stop_jekyll_server()
    return


def tools_screen(stdscr):
    """Runs the tools screen"""
    redraw = True
    key = 0
    notice_txt = None
    while not check_key(key, 'q'):
        if redraw:
            lines_offset = (curses.LINES - 2 - 11) // 2
            cols_offset = (curses.COLS - 45) // 2
            local_server_menu_text = None
            if is_jekyll_server_running():
                local_server_menu_text = 'Stop Server'
            else:
                local_server_menu_text = 'Start Server'
            window_prep(stdscr, 'utterson', None)
            opts = collections.OrderedDict()
            opts['P'] = ['Publish', 'Publishes the site to the remote server', 'normal']
            opts['S'] = [local_server_menu_text, 'Starts and stops the local server', 'normal']
            opts['B'] = ['Build', 'Build the static site.']
            opts['Q'] = ['Quit', 'Exit utterson', 'normal']
            build_full_screen_menu(stdscr, opts)
            if notice_txt is not None:
                notice_header(stdscr, notice_txt)
                notice_txt = None
        key = stdscr.getch()
        if check_key(key, 's'):
            start_stop_jekyll_server()
            if is_jekyll_server_running():
                notice_txt = 'Server running...'
            else:
                notice_txt = 'Server stopped'
            redraw = True
        elif check_key(key, 'p'):
            update_server(stdscr)
        elif check_key(key, 'b'):
            build_jekyll_site()
            notice_txt = 'Site Build Completed'
            redraw = True
            continue

    return


def setting_screen(stdscr):
    """Starts the setting screen."""
    global config
    global jekyll_config
    global startup_opts
    redraw = True
    notice_txt = None
    reload_settings = True
    key = 0
    while not check_key(key, 'q'):
        if reload_settings:
            load_configuration(startup_opts['config_file'])
            load_jekyll_configuration(config['site']['jekyll_root'] + '/_config.yml')
            rows = []
            rows.append({'return_value': 'jekyll_root',  'col1': 'Jekyll Root', 
             'col2': config['site']['jekyll_root']})
            rows.append({'return_value': 'editing_app',  'col1': 'Editing App', 
             'col2': config['editing_app']})
            rows.append({'return_value': 'site_name',  'col1': 'Site Name', 
             'col2': jekyll_config['name']})
            rows.append({'return_value': 'site_description',  'col1': 'Site Description', 
             'col2': jekyll_config['description']})
            columns = collections.OrderedDict()
            columns['col1'] = {'title': 'Name',  'size': 18}
            columns['col2'] = {'title': 'Value',  'size': 0}
            il = ItemsListWindow(rows, columns)
            il.set_window_size({'left_type': 'relative',  'left_value': 2,  'right_type': 'relative', 
             'right_value': 2,  'bottom_type': 'relative', 
             'bottom_value': 2,  'top_type': 'relative', 
             'top_value': 2,  'height': 10, 
             'width': 15})
            reload_settings = False
        if redraw:
            window_prep(stdscr, 'utterson: Settings', {'Q': 'Quit',  'E': 'Edit'})
            if notice_txt is not None:
                notice_header(stdscr, notice_txt)
                notice_txt = None
            stdscr.refresh()
            il.build_item_list()
            il.refresh_window()
            redraw = False
        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            il.select_down()
        elif key == curses.KEY_UP:
            il.select_up()
        elif check_key(key, 'e'):
            selected = il.get_selected()
            not_valid = True
            if selected == 'site_name':
                while not_valid:
                    new_value = get_string_prompt(stdscr, 'Site Name', default_text=jekyll_config['name'])
                    if new_value != '' and new_value is not None:
                        jekyll_config['name'] = new_value
                        save_jekyll_config(config['site']['jekyll_root'] + '/_config.yml')
                        not_valid = False
                        redraw = True
                        reload_settings = True
                        notice_txt = 'Updated: ' + selected
                        continue

            else:
                if selected == 'site_description':
                    while not_valid:
                        new_value = get_string_prompt(stdscr, 'Site Description', default_text=jekyll_config['description'])
                        if new_value != '' and new_value is not None:
                            jekyll_config['description'] = new_value
                            save_jekyll_config(config['site']['jekyll_root'] + '/_config.yml')
                            not_valid = False
                            redraw = True
                            reload_settings = True
                            notice_txt = 'Updated: ' + selected
                            continue

                else:
                    if selected == 'editing_app':
                        while not_valid:
                            new_value = get_string_prompt(stdscr, 'Editing App', default_text=config['editing_app'])
                            if new_value != '' and new_value is not None:
                                config['editing_app'] = new_value
                                save_config(startup_opts['config_file'])
                                not_valid = False
                                redraw = True
                                reload_settings = True
                                notice_txt = 'Updated: ' + selected
                                continue

                    elif selected == 'jekyll_root':
                        while not_valid:
                            new_value = get_string_prompt(stdscr, 'Jekyll Root', default_text=config['site']['jekyll_root'])
                            if new_value != '' and new_value is not None:
                                config['site']['jekyll_root'] = new_value
                                save_config(startup_opts['config_file'])
                                not_valid = False
                                redraw = True
                                reload_settings = True
                                notice_txt = 'Updated: ' + selected
                                continue

            if reload_settings and is_jekyll_server_running():
                start_stop_jekyll_server()
                start_stop_jekyll_server()
            else:
                continue

    return


def update_server(stdscr):
    subprocess.call(config['site']['update_cmd'])


def published_post_screen(stdscr):
    """Starts the published post screen."""
    redraw = True
    rebuild_file_list = True
    notice_txt = None
    key = 0
    while not check_key(key, 'q'):
        if rebuild_file_list:
            posts = []
            for f in os.listdir(config['site']['jekyll_root'] + '/_posts/'):
                if os.path.isfile(config['site']['jekyll_root'] + '/_posts/' + f):
                    f_time = time.localtime(os.path.getmtime(config['site']['jekyll_root'] + '/_posts/' + f))
                    f_time_str = str(f_time.tm_year) + '-' + str(f_time.tm_mon) + '-' + str(f_time.tm_mday)
                    temp_dict = {'return_value': f,  'col2': f, 
                     'col1': f_time_str}
                    posts.append(temp_dict)
                    continue

            posts.sort(key=lambda x: x['col1'], reverse=True)
            columns = {'col2': {'title': 'Name',  'size': 0},  'col1': {'title': 'Modify Date',  'size': 11}}
            il = ItemsListWindow(posts, columns)
            il.set_window_size({'left_type': 'relative',  'left_value': 2,  'right_type': 'relative', 
             'right_value': 2,  'bottom_type': 'relative', 
             'bottom_value': 2,  'top_type': 'relative', 
             'top_value': 2,  'height': 10, 
             'width': 15})
            rebuild_file_list = False
        if redraw:
            window_prep(stdscr, 'utterson: Published Posts', {'Q': 'Quit',  'U': 'Unpublish',  'I': 'Info', 
             'D': 'Delete',  'C': 'Change PDate'})
            if notice_txt is not None:
                notice_header(stdscr, notice_txt)
                notice_txt = None
            stdscr.refresh()
            il.build_item_list()
            il.refresh_window()
            redraw = False
        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            il.select_down()
        elif key == curses.KEY_UP:
            il.select_up()
        elif check_key(key, 'u'):
            selected = il.get_selected()
            sure = yes_no_prompt(stdscr, 'Unpublish?: ' + selected + ' (y/n)')
            if sure:
                shutil.move(config['site']['jekyll_root'] + '/_posts/' + selected, config['site']['jekyll_root'] + '/_posts/_drafts/' + selected[11:])
                rebuild_file_list = True
                redraw = True
                notice_txt = 'Unpublished: ' + selected
            else:
                redraw = True
        elif check_key(key, 'I'):
            selected = il.get_selected()
            post_info_window(stdscr, config['site']['jekyll_root'] + '/_posts/' + selected)
            redraw = True
        elif check_key(key, 'c'):
            not_valid = True
            selected = il.get_selected()
            while not_valid:
                date_str = get_string_prompt(stdscr, 'New Publish Date', default_text=selected[:10])
                if validate_date(date_str):
                    update_publication_date(selected, date_str)
                    not_valid = False
                    continue

            redraw = True
            rebuild_file_list = True
            notice_txt = 'Changed PDate: ' + selected
        elif check_key(key, 'd'):
            selected = il.get_selected()
            sure = yes_no_prompt(stdscr, 'Delete?: ' + selected + ' (y/n)')
            if sure:
                shutil.move(config['site']['jekyll_root'] + '/_posts/' + selected, config['site']['jekyll_root'] + '/_posts/_deleted/' + 'p_' + selected)
                rebuild_file_list = True
                redraw = True
                notice_txt = 'Deleted: ' + selected
            else:
                redraw = True
                continue

    return


def draft_post_screen(stdscr):
    """Starts the draft post screen."""
    redraw = True
    rebuild_file_list = True
    notice_txt = None
    key = 0
    while not check_key(key, 'q'):
        if rebuild_file_list:
            posts = []
            for f in os.listdir(config['site']['jekyll_root'] + '/_posts/_drafts'):
                if os.path.isfile(config['site']['jekyll_root'] + '/_posts/_drafts/' + f):
                    f_time = time.localtime(os.path.getmtime(config['site']['jekyll_root'] + '/_posts/_drafts/' + f))
                    f_time_str = str(f_time.tm_year) + '-' + str(f_time.tm_mon) + '-' + str(f_time.tm_mday)
                    temp_dict = {'return_value': f,  'col2': f, 
                     'col1': f_time_str}
                    posts.append(temp_dict)
                    continue

            posts.sort(key=lambda x: x['col1'], reverse=True)
            columns = {'col2': {'title': 'Name',  'size': 0},  'col1': {'title': 'Modify Date',  'size': 11}}
            il = ItemsListWindow(posts, columns)
            il.set_window_size({'left_type': 'relative',  'left_value': 2,  'right_type': 'relative', 
             'right_value': 2,  'bottom_type': 'relative', 
             'bottom_value': 2,  'top_type': 'relative', 
             'top_value': 2,  'height': 10, 
             'width': 15})
            rebuild_file_list = False
        if redraw:
            window_prep(stdscr, 'utterson: Draft Posts', {'Q': 'Quit',  'E': 'Edit',  'P': 'Publish',  'N': 'New', 
             'I': 'Info',  'R': 'Rename',  'D': 'Delete'})
            if notice_txt is not None:
                notice_header(stdscr, notice_txt)
                notice_txt = None
            stdscr.refresh()
            il.build_item_list()
            il.refresh_window()
            redraw = False
        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            il.select_down()
        elif key == curses.KEY_UP:
            il.select_up()
        elif check_key(key, 'e'):
            selected = il.get_selected()
            edit_post(config['site']['jekyll_root'] + '/_posts/_drafts/' + selected)
            curses.curs_set(1)
            curses.curs_set(0)
            redraw = True
        elif check_key(key, 'p'):
            selected = il.get_selected()
            sure = yes_no_prompt(stdscr, 'Publish?: ' + selected + ' (y/n)')
            if sure:
                publish_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                post = JekyllPost(config['site']['jekyll_root'] + '/_posts/_drafts/' + selected)
                post.meta_data['date_published'] = publish_date
                post.meta_data['date_updated'] = publish_date
                post_file_path = config['site']['jekyll_root'] + '/_posts/' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '-' + selected
                post.save_post(post_file_path)
                os.remove(config['site']['jekyll_root'] + '/_posts/_drafts/' + selected)
                rebuild_file_list = True
                redraw = True
                notice_txt = 'Published: ' + selected
            else:
                redraw = True
        elif check_key(key, 'n'):
            title = get_string_prompt(stdscr, 'New Post Name')
            notice_txt = config['site']['jekyll_root'] + '/_posts/_templates/template.textile'
            if os.path.isfile(config['site']['jekyll_root'] + '/_posts/_templates/template.textile'):
                notice_txt = config['site']['jekyll_root'] + '/_posts/_templates/template.textile'
                shutil.copy(config['site']['jekyll_root'] + '/_posts/_templates/template.textile', config['site']['jekyll_root'] + '/_posts/_drafts/' + title)
            edit_post(config['site']['jekyll_root'] + '/_posts/_drafts/' + title)
            curses.curs_set(1)
            curses.curs_set(0)
            redraw = True
            rebuild_file_list = True
        elif check_key(key, 'r'):
            not_valid = True
            selected = il.get_selected()
            while not_valid:
                title = get_string_prompt(stdscr, 'New Post Name', default_text=selected)
                if os.path.isfile(config['site']['jekyll_root'] + '/_posts/_drafts/' + title):
                    not_valid = True
                else:
                    shutil.move(config['site']['jekyll_root'] + '/_posts/_drafts/' + selected, config['site']['jekyll_root'] + '/_posts/_drafts/' + title)
                    not_valid = False

            redraw = True
            rebuild_file_list = True
            notice_txt = 'Renamed: ' + selected
        elif check_key(key, 'I'):
            selected = il.get_selected()
            post_info_window(stdscr, config['site']['jekyll_root'] + '/_posts/_drafts/' + selected)
            redraw = True
        elif check_key(key, 'd'):
            selected = il.get_selected()
            sure = yes_no_prompt(stdscr, 'Delete?: ' + selected + ' (y/n)')
            if sure:
                shutil.move(config['site']['jekyll_root'] + '/_posts/_drafts/' + selected, config['site']['jekyll_root'] + '/_posts/_deleted/' + 'd_' + selected)
                rebuild_file_list = True
                redraw = True
                notice_txt = 'Deleted: ' + selected
            else:
                redraw = True
                continue

    return


def deleted_post_screen(stdscr):
    """Starts the draft post screen."""
    redraw = True
    rebuild_file_list = True
    notice_txt = None
    key = 0
    while not check_key(key, 'q'):
        if rebuild_file_list:
            posts = []
            for f in os.listdir(config['site']['jekyll_root'] + '/_posts/_deleted'):
                if os.path.isfile(config['site']['jekyll_root'] + '/_posts/_deleted/' + f):
                    f_time = time.localtime(os.path.getmtime(config['site']['jekyll_root'] + '/_posts/_deleted/' + f))
                    f_time_str = str(f_time.tm_year) + '-' + str(f_time.tm_mon) + '-' + str(f_time.tm_mday)
                    temp_dict = {'return_value': f,  'col2': f, 
                     'col1': f_time_str}
                    posts.append(temp_dict)
                    continue

            posts.sort(key=lambda x: x['col1'], reverse=True)
            columns = {'col2': {'title': 'Name',  'size': 0},  'col1': {'title': 'Modify Date',  'size': 11}}
            il = ItemsListWindow(posts, columns)
            il.set_window_size({'left_type': 'relative',  'left_value': 2,  'right_type': 'relative', 
             'right_value': 2,  'bottom_type': 'relative', 
             'bottom_value': 2,  'top_type': 'relative', 
             'top_value': 2,  'height': 10, 
             'width': 15})
            rebuild_file_list = False
        if redraw:
            window_prep(stdscr, 'utterson: Deleted Posts', {'Q': 'Quit',  'E': 'Edit',  'R': 'Restore',  'D': 'Delete Forever'})
            if notice_txt is not None:
                notice_header(stdscr, notice_txt)
                notice_txt = None
            stdscr.refresh()
            il.build_item_list()
            il.refresh_window()
            redraw = False
        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            il.select_down()
        elif key == curses.KEY_UP:
            il.select_up()
        elif check_key(key, 'e'):
            selected = il.get_selected()
            edit_post(config['site']['jekyll_root'] + '_posts/_deleted/' + selected)
            curses.curs_set(1)
            curses.curs_set(0)
            redraw = True
        elif check_key(key, 'r'):
            selected = il.get_selected()
            sure = yes_no_prompt(stdscr, 'Restore' + selected + ' (y/n)')
            if sure:
                location = None
                if selected[0:1] == 'd':
                    location = '_posts/_drafts/'
                else:
                    if selected[0:1] == 'p':
                        location = '_posts/'
                    elif selected[0:1] == 't':
                        location = '_posts/_templates/'
                    if location is not None:
                        shutil.move(config['site']['jekyll_root'] + '/_posts/_deleted/' + selected, config['site']['jekyll_root'] + '/' + location + selected[2:])
                rebuild_file_list = True
                redraw = True
                notice_txt = 'Restored: ' + selected[:2]
            else:
                redraw = True
        elif check_key(key, 'd'):
            selected = il.get_selected()
            sure = yes_no_prompt(stdscr, 'Delete Forever?: ' + selected + ' (y/n)')
            if sure:
                os.remove(config['site']['jekyll_root'] + '/_posts/_deleted/' + selected)
                rebuild_file_list = True
                redraw = True
                notice_txt = 'Deleted: ' + selected
            else:
                redraw = True
                continue

    return


def check_key(key, expected_chr):
    """Checks the key against the expected_chr. Specifically running ord() on the expected_chr"""
    if key == ord(expected_chr.upper()) or key == ord(expected_chr.lower()):
        return True
    return False


def template_post_screen(stdscr):
    """Starts the template screen."""
    redraw = True
    rebuild_file_list = True
    notice_txt = None
    key = 0
    while not check_key(key, 'q'):
        if rebuild_file_list:
            posts = []
            for f in os.listdir(config['site']['jekyll_root'] + '/_posts/_templates'):
                if os.path.isfile(config['site']['jekyll_root'] + '/_posts/_templates/' + f):
                    f_time = time.localtime(os.path.getmtime(config['site']['jekyll_root'] + '/_posts/_templates/' + f))
                    f_time_str = str(f_time.tm_year) + '-' + str(f_time.tm_mon) + '-' + str(f_time.tm_mday)
                    temp_dict = {'return_value': f,  'col2': f, 
                     'col1': f_time_str}
                    posts.append(temp_dict)
                    continue

            posts.sort(key=lambda x: x['col1'], reverse=True)
            columns = {'col2': {'title': 'Name',  'size': 0},  'col1': {'title': 'Modify Date',  'size': 11}}
            il = ItemsListWindow(posts, columns)
            il.set_window_size({'left_type': 'relative',  'left_value': 2,  'right_type': 'relative', 
             'right_value': 2,  'bottom_type': 'relative', 
             'bottom_value': 2,  'top_type': 'relative', 
             'top_value': 2,  'height': 10, 
             'width': 15})
            rebuild_file_list = False
        if redraw:
            window_prep(stdscr, 'utterson: Templates', {'Q': 'Quit',  'E': 'Edit',  'N': 'New', 
             'R': 'Rename',  'D': 'Delete'})
            if notice_txt is not None:
                notice_header(stdscr, notice_txt)
                notice_txt = None
            stdscr.refresh()
            il.build_item_list()
            il.refresh_window()
            redraw = False
        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            il.select_down()
        elif key == curses.KEY_UP:
            il.select_up()
        elif check_key(key, 'e'):
            selected = il.get_selected()
            edit_post(config['site']['jekyll_root'] + '/_posts/_templates/' + selected)
            curses.curs_set(1)
            curses.curs_set(0)
            redraw = True
        elif check_key(key, 'n'):
            title = get_string_prompt(stdscr, 'New Post Name')
            if os.path.isfile(config['site']['jekyll_root'] + '/_posts/_templates/template.textile'):
                shutil.copy(config['site']['jekyll_root'] + '/_posts/_templates/template.textile', config['site']['jekyll_root'] + '/_posts/_templates/' + title)
                edit_post(config['site']['jekyll_root'] + '/_posts/_templates/' + title)
            curses.curs_set(1)
            curses.curs_set(0)
            redraw = True
            rebuild_file_list = True
        elif check_key(key, 'r'):
            not_valid = True
            selected = il.get_selected()
            while not_valid:
                title = get_string_prompt(stdscr, 'New Template Name', default_text=selected)
                if os.path.isfile(config['site']['jekyll_root'] + '/_posts/_templates/' + title):
                    not_valid = True
                else:
                    shutil.move(config['site']['jekyll_root'] + '/_posts/_templates/' + selected, config['site']['jekyll_root'] + '/_posts/_templates/' + title)
                    not_valid = False

            redraw = True
            rebuild_file_list = True
            notice_txt = 'Renamed: ' + selected
        elif check_key(key, 'I'):
            selected = il.get_selected()
            post_info_window(stdscr, config['site']['jekyll_root'] + '/_posts/_templates/' + selected)
            redraw = True
        elif check_key(key, 'd'):
            selected = il.get_selected()
            sure = yes_no_prompt(stdscr, 'Delete?: ' + selected + ' (y/n)')
            if sure:
                shutil.move(config['site']['jekyll_root'] + '/_posts/_templates/' + selected, config['site']['jekyll_root'] + '/_posts/_deleted/' + 't_' + selected)
                rebuild_file_list = True
                redraw = True
                notice_txt = 'Deleted: ' + selected
            else:
                redraw = True
                continue

    return


def posts_main_screen(stdscr):
    """Displays and manages the posts main screen."""
    redraw = True
    key = 0
    while not check_key(key, 'q'):
        if redraw:
            window_prep(stdscr, 'utterson: Posts', {'Q': 'Quit'})
            opts = collections.OrderedDict()
            opts['D'] = ['Drafts', 'Created/Edit/Delete drafts.']
            opts['P'] = ['Published Posts', 'Manage published posts']
            opts['T'] = ['Templates', 'Created/Edit/Delete templates']
            opts['X'] = ['Deleted', 'Managed deleted posts.']
            opts['Q'] = ['Quit', 'Return to home screen']
            build_full_screen_menu(stdscr, opts)
        key = stdscr.getch()
        if check_key(key, 'd'):
            draft_post_screen(stdscr)
            redraw = True
        elif check_key(key, 'p'):
            published_post_screen(stdscr)
            redraw = True
        elif check_key(key, 't'):
            template_post_screen(stdscr)
            redraw = True
        elif check_key(key, 'x'):
            deleted_post_screen(stdscr)
            redraw = True
            continue


def load_configuration(config_file_dir):
    global config
    stream = open(config_file_dir, 'r')
    config = yaml.load(stream)
    stream.close()


def load_jekyll_configuration(config_file_path):
    global jekyll_config
    stream = open(config_file_path, 'r')
    jekyll_config = yaml.load(stream)
    stream.close()


def yes_no_prompt(stdscr, question):
    lines_offset = (curses.LINES - 3) // 2
    cols_offset = (curses.COLS - len(question) - 2) // 2
    window = curses.newwin(3, len(question) + 2, lines_offset, cols_offset)
    window.border(0)
    window.addstr(1, 1, question)
    window.refresh()
    while True:
        key = stdscr.getch()
        if check_key(key, 'y'):
            return True
        if check_key(key, 'n'):
            return False


def post_info_window(stdscr, post_path):
    post = JekyllPost(post_path)
    lines_offset = (curses.LINES - 16) // 2
    cols_offset = (curses.COLS - 70) // 2
    window = curses.newwin(16, 70, lines_offset, cols_offset)
    window.border(0)
    window.addstr(1, 1, ('Title: ' + post.meta_data['title'])[:61])
    window.addstr(2, 1, 'Summary:')
    if post.meta_data['summary'] is not None:
        window.addstr(3, 1, ' ' + post.meta_data['summary'][:66])
        window.addstr(4, 1, ' ' + post.meta_data['summary'][66:132])
    window.addstr(5, 1, 'Categories:' + str(post.meta_data['categories']))
    window.addstr(6, 1, 'Tags: ' + str(post.meta_data['tags']))
    window.refresh()
    while True:
        if check_key(stdscr.getch(), 'q'):
            return False

    return


def get_string_prompt(stdscr, question, default_text=None):
    """

  Displays a text box in the center of screen. Allows users to enter a single
  string

  """
    question = question[:48].strip()
    question_offset = (50 - len(question)) // 2 + 1
    lines_offset = (curses.LINES - 3) // 2
    cols_offset = (curses.COLS - 50) // 2
    window = curses.newwin(3, 52, lines_offset, cols_offset)
    window.border(0)
    window.addstr(0, question_offset, question)
    window.refresh()
    curses.curs_set(1)
    textbox_window = curses.newwin(1, 50, lines_offset + 1, cols_offset + 1)
    if default_text is not None:
        textbox_window.addstr(0, 0, default_text[:50])
    textbox = curses.textpad.Textbox(textbox_window, insert_mode=True)
    textbox.edit()
    curses.curs_set(0)
    return textbox.gather().strip()


def parse_startup_arguments():
    """Builds and processes the startup arguments."""
    global startup_opts
    parser = argparse.ArgumentParser(description='utterson: A terrible Jekyll management system.')
    parser.add_argument('--version', action='version', version='%(prog)s ' + utterson_version)
    parser.add_argument('-config_file', default='config.yml')
    build_generate_group = parser.add_mutually_exclusive_group()
    build_generate_group.add_argument('-generate_config', action='store_true')
    build_generate_group.add_argument('-new')
    startup_opts = vars(parser.parse_args())


def generate_jekyll_config(path, site_title):
    """Builds a jekyll site configuration file."""
    cf = open(path + '/_config.yml', 'w')
    cf.write('name: ' + site_title + '\n')
    cf.write('paginate: 7\n')
    cf.close()


def save_config(config_file_path):
    config_file = open(config_file_path, 'w')
    config_file.write(yaml.dump(config, default_flow_style=False))
    config_file.close()


def save_jekyll_config(config_file_path):
    jekyll_config_file = open(config_file_path, 'w')
    jekyll_config_file.write(yaml.dump(jekyll_config, default_flow_style=False))
    jekyll_config_file.close()


def build_new_utterson_site(root_folder_name):
    """Builds an empty utterson site based on jekyll."""
    print('Creating new utterson site at: ' + root_folder_name)
    os.mkdir(root_folder_name)
    shutil.copyfile(os.path.dirname(os.path.realpath(__file__)) + '/templates/config.yml', root_folder_name + '/config.yml')
    shutil.copytree(os.path.dirname(os.path.realpath(__file__)) + '/templates/jc_simple_blue/jekyll_root', root_folder_name + '/jekyll_root')
    exit(1)


def test_for_requirements():
    """Tests for utterson requirements."""
    if is_executable_in_path('jekyll') is None:
        print('Could not find Jekyll. Exiting....')
        exit(1)
    return


def is_executable_in_path(executable_name):
    """Tests to see if the executable can be found in the current paths."""
    path, name = os.path.split(executable_name)
    if path:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return executable_name
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            executable_location = os.path.join(path, executable_name)
            if os.path.isfile(executable_location) and os.access(executable_location, os.X_OK):
                return executable_location

    return


def main():
    test_for_requirements()
    parse_startup_arguments()
    if startup_opts['generate_config']:
        print('Not Implemented')
        exit(1)
    if startup_opts['new'] is not None:
        build_new_utterson_site(startup_opts['new'])
        exit(1)
    load_configuration(startup_opts['config_file'])
    wrapper(window_main)
    return


def window_main(stdscr):
    curses.use_default_colors()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)
    home_screen(stdscr)
    stdscr.clear()
    stdscr.refresh()
    curses.endwin()


def edit_post(path):
    if config['editing_app'] is not None:
        subprocess.call([config['editing_app'], path])
    else:
        subprocess.call(['vim', path])
    return


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

    return False


def update_publication_date(file_name, date_str):
    """Edits the publication date if it's changed."""
    if validate_date(date_str):
        post = JekyllPost(config['site']['jekyll_root'] + '/_posts/' + file_name)
        post.meta_data['date_published'] = date_str
        post.meta_data['date_published'] = date_str
        file_short_name = file_name[11:]
        post_file_path = config['site']['jekyll_root'] + '/_posts/' + date_str + '-' + file_name[11:]
        post.save_post(post_file_path)
        os.remove(config['site']['jekyll_root'] + '/_posts/' + file_name)
        return True
    else:
        return False


def build_jekyll_site():
    site_root = config['site']['jekyll_root']
    deploy_root = config['site']['jekyll_root'] + '/_site'
    subprocess.call(['jekyll', 'build', '-s', site_root, '-d', deploy_root])


def start_stop_jekyll_server():
    """Stars or stops the jekyll server in watch mode."""
    global jekyll_local_server
    if is_jekyll_server_running():
        jekyll_local_server.terminate()
        jekyll_local_server.wait()
        jekyll_local_server = None
    else:
        site_root = config['site']['jekyll_root']
        deploy_root = config['site']['jekyll_root'] + '/_site'
        jekyll_local_server = subprocess.Popen(['jekyll', 'server', '--watch', '-s', site_root, '-d', deploy_root], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return


def is_jekyll_server_running():
    """Checks if the jekyll server is running. If so returns true."""
    if jekyll_local_server is not None and jekyll_local_server.poll() is None:
        return True
    else:
        return False


class JekyllPost:
    """Basic class that represents a jekyll post."""

    def __init__(self, file_path):
        self.file_path = file_path
        self.meta_data = None
        self.meta_data_str = ''
        self.text = []
        temp_file = open(file_path, 'r')
        self.file = temp_file.readlines()
        temp_file.close()
        self._parse_jekyll_post()
        return

    def _parse_jekyll_post(self):
        meta_start = False
        for line in self.file:
            if line.strip() == '---':
                if meta_start:
                    meta_start = False
                else:
                    meta_start = True
            else:
                if meta_start:
                    self.meta_data_str += line
                else:
                    self.text.append(line.strip())
            self._parse_meta_data()

    def _parse_meta_data(self):
        self.meta_data = yaml.load(self.meta_data_str)

    def save_post(self, path):
        post_f = open(path, 'w')
        post_f.write('---\n')
        post_f.write(yaml.dump(self.meta_data, default_flow_style=False))
        post_f.write('---\n')
        for line in self.text:
            post_f.write(line + '\n')

        post_f.close()


class ItemsListWindow:
    """

  Creates a navigable items list.

  The ItemsListWindow class provides a basic ncurses based items list. and a
  dedicated ncurses window is created for it. The location and size of the 
  window may be specified. The instance also provides navigation/selection. 

  """

    def __init__(self, items, columns, header=True):
        """

    Initialized the default values.

    items = ({"return_value":"value",
             {"col1":"value"})

    columns = ({"col1": {'title': '<text>', 'size': <int>}},)

    """
        self.items = items
        self.selected_line = -1
        self.last_top_line = 0
        self.columns = columns
        self.header = header

    def set_window_size(self, options):
        """

    Sets the size of the ncurses window that the list will utilize.

    The window size may be supplied as both absolute and relative values.
    The options parameter should be a dictionary containing the following
    items. By default the height and width are only utilized when
    an absolute type is specified.

    {'left_type': 'relative', 'left_value': 2,
     'right_type': 'relative', 'right_value': 15,
     'bottom_type': 'relative', 'bottom_value': 10,
     'top_type': 'relative', 'top_value': 10,
     'height': 10,
     'width': 10}

    """
        self.window_width = 0
        self.window_cols_offset = 0
        self.window_height = 0
        self.window_rows_offset = 0
        if options['left_type'] == 'relative':
            if options['right_type'] == 'relative':
                self.window_width = curses.COLS - options['left_value'] - options['right_value']
                self.window_cols_offset = options['left_value']
            else:
                if curses.COLS < options['left_value'] + options['width']:
                    self.window_width = curses.COLS - options['left_value']
                else:
                    self.window_width = options['width']
                self.window_cols_offset = options['left_value']
        else:
            if options['right_type'] == 'relative':
                if curses.COLS < options['right_value'] + options['width']:
                    self.window_width = curses.COLS - options['right_value']
                else:
                    self.window_width = options['width']
                self.window_cols_offset = curses.COLS - options['width'] - options['right_value']
            else:
                self.window_width = options['width']
                self.window_cols_offset = 0
            if options['top_type'] == 'relative':
                if options['bottom_type'] == 'relative':
                    self.window_height = curses.LINES - options['top_value'] - options['bottom_value']
                    self.window_rows_offset = options['top_value']
                else:
                    if curses.LINES < options['top_value'] + options['height']:
                        self.window_height = curses.LINES - options['top_value']
                    else:
                        self.window_height = options['height']
                    self.window_rows_offset = options['top_value']
            else:
                if options['bottom_type'] == 'relative':
                    if curses.LINES < options['bottom_value'] + options['height']:
                        self.window_height = curses.LINES - options['bottom_value']
                    else:
                        self.window_height = options['height']
                    self.window_rows_offset = curses.LINES - options['height'] - options['bottom_value']
                else:
                    self.window_height = options['height']
                    self.window_rows_offset = 0
        self.window = curses.newwin(self.window_height, self.window_width, self.window_rows_offset, self.window_cols_offset)

    def select_down(self):
        """Moves the selected row up."""
        if self.selected_line < len(self.items) - 1:
            self.selected_line += 1
            if self.selected_line - self.last_top_line >= self.get_visible_lines():
                self.last_top_line += 1
        self.build_item_list()
        self.refresh_window()

    def select_up(self):
        """Moves the selected row down."""
        if self.selected_line > 0:
            self.selected_line -= 1
            if self.last_top_line > self.selected_line:
                self.last_top_line = self.selected_line
        self.build_item_list()
        self.refresh_window()

    def get_selected(self):
        return self.items[self.selected_line]['return_value']

    def refresh_window(self):
        """Refreshes the window"""
        self.window.refresh()

    def get_visible_lines(self):
        """Determines the actual visible lines for redrawing."""
        if len(self.items) > self.window_height:
            visible_lines = self.window_height
            if self.header:
                visible_lines -= 1
        else:
            visible_lines = len(self.items)
        if self.header and visible_lines + 1 > self.window_height:
            visible_lines -= 1
        return visible_lines

    def build_item_list(self):
        """Rebuilds the ncurses window."""
        header_values = {}
        if self.header:
            line_number = 1
            shared_col_space = 0
            used_col_space = 0
            for key, value in self.columns.items():
                if value['size'] == 0:
                    shared_col_space += 1
                else:
                    used_col_space += value['size']

            shared_col_size = (self.window_width - used_col_space) // shared_col_space
            cur_col = 0
            for column in range(1, len(self.columns.items()) + 1, 1):
                key = 'col' + str(column)
                value = self.columns[key]
                if value['size'] == 0:
                    cur_col_size = shared_col_size
                else:
                    cur_col_size = value['size']
                temp = self.white_space_pad(value['title'], cur_col_size)
                self.window.addstr(0, cur_col, temp)
                header_values[key] = cur_col_size
                cur_col += cur_col_size

        else:
            line_number = 0
        visible_lines = self.get_visible_lines()
        for item_number in range(self.last_top_line, self.last_top_line + self.get_visible_lines()):
            if item_number == self.selected_line:
                col_num = 0
                for colNum in range(1, len(self.items[item_number].items()), 1):
                    key = 'col' + str(colNum)
                    self.window.addstr(line_number, col_num, self.white_space_pad(self.items[item_number][key], header_values[key]), curses.A_STANDOUT)
                    col_num += header_values[key]

            else:
                col_num = 0
                for colNum in range(1, len(self.items[item_number].items()), 1):
                    key = 'col' + str(colNum)
                    self.window.addstr(line_number, col_num, self.white_space_pad(self.items[item_number][key], header_values[key]))
                    col_num += header_values[key]

            line_number += 1

    def white_space_pad(self, input_str, length):
        if len(input_str) < length:
            return input_str + ' ' * (length - len(input_str))
        else:
            return input_str[:length]