# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <xlwings_pro-1.2.2>/xlwings/mac_dict.py
# Compiled at: 2020-03-09 05:37:56
"""
This file has been generated based on the Excel 2011 dictionary since Excel 2016 was screwing things up,
see:
http://lists.apple.com/archives/applescript-users/2015/Mar/msg00114.html
http://lists.apple.com/archives/applescript-users/2015/Mar/msg00290.html

Usage:
>>> from appscript.terminology import dump
>>> dump('Microsoft Excel', '/path/to/myappglue.py')

>>> import myappglue
>>> from appscript import app
>>> app = app('Microsoft Excel', terms=myappglue)
"""
version = 1.1
classes = [
 (
  'base_object', 'oItm'),
 (
  'base_application', 'cbap'),
 (
  'base_document', 'bDoc'),
 (
  'basic_window', 'bwin'),
 (
  'print_settings', 'pset'),
 (
  'command_bar_button', 'mCBB'),
 (
  'command_bar_combobox', 'mCBX'),
 (
  'command_bar_control', 'mCBC'),
 (
  'command_bar_popup', 'mCBP'),
 (
  'command_bar', 'msCB'),
 (
  'custom_document_property', 'mCDP'),
 (
  'document_property', 'mDPr'),
 (
  'web_page_font', 'mWPF'),
 (
  'Excel_comment', 'X229'),
 (
  'ODBC_error', 'X235'),
 (
  'Protection', 'Xpot'),
 (
  'above_average_format_condition', 'X322'),
 (
  'active_filter', 'Y903'),
 (
  'add_in', 'X133'),
 (
  'application', 'capp'),
 (
  'autofilter', 'X240'),
 (
  'border', 'X251'),
 (
  'button', 'Xbtn'),
 (
  'calculated_field', 'XPFc'),
 (
  'calculated_item', 'XPIi'),
 (
  'calculated_member', 'X901'),
 (
  'checkbox', 'Xckb'),
 (
  'child_item', 'XPIc'),
 (
  'color_scale_criteria', 'X310'),
 (
  'color_scale_criterion', 'X311'),
 (
  'color_scale_format_condition', 'X325'),
 (
  'colorstop', 'X305'),
 (
  'colorstops', 'X304'),
 (
  'column_field', 'XPFn'),
 (
  'column_item', 'XPIo'),
 (
  'condition_value', 'X324'),
 (
  'cube_field', 'X900'),
 (
  'custom_view', 'X225'),
 (
  'data_field', 'XPFd'),
 (
  'databar_border', 'X313'),
 (
  'databar_format_condition', 'X312'),
 (
  'default_web_options', 'X300'),
 (
  'dialog', 'X165'),
 (
  'display_format', 'X306'),
 (
  'document', 'docu'),
 (
  'dropdown', 'XdpD'),
 (
  'filter', 'X242'),
 (
  'format_color', 'X307'),
 (
  'format_condition_icon_object', 'X318'),
 (
  'format_condition_icon_set', 'X319'),
 (
  'format_condition_icon_sets', 'X320'),
 (
  'format_condition', 'X227'),
 (
  'graphic', 'X308'),
 (
  'groupbox', 'XGBc'),
 (
  'hidden_field', 'XPFh'),
 (
  'hidden_item', 'XPIh'),
 (
  'horizontal_page_break', 'X122'),
 (
  'hyperlink', 'X239'),
 (
  'icon_criteria', 'X316'),
 (
  'icon_criterion', 'X317'),
 (
  'icon_set_format_condition', 'X315'),
 (
  'international_macro_sheet', 'XiSH'),
 (
  'label', 'Xlbl'),
 (
  'linear_gradient', 'X302'),
 (
  'list_column', 'X248'),
 (
  'list_object', 'X244'),
 (
  'list_row', 'X246'),
 (
  'listbox', 'XLbx'),
 (
  'macro_sheet', 'XmSH'),
 (
  'named_item', 'X220'),
 (
  'negative_bar_format', 'X314'),
 (
  'option_button', 'XObn'),
 (
  'outline', 'X212'),
 (
  'page_field', 'XPFp'),
 (
  'page_setup', 'X218'),
 (
  'pane', 'X189'),
 (
  'parent_item', 'XPIp'),
 (
  'phonetic', 'X288'),
 (
  'pivot_axis', 'X902'),
 (
  'pivot_cache', 'X151'),
 (
  'pivot_cell', 'X908'),
 (
  'pivot_field', 'X157'),
 (
  'pivot_filter', 'X903'),
 (
  'pivot_formula', 'X153'),
 (
  'pivot_item', 'X160'),
 (
  'pivot_line', 'X907'),
 (
  'pivot_table', 'X155'),
 (
  'query_table', 'X231'),
 (
  'recent_file', 'X125'),
 (
  'rectangular_gradient', 'X303'),
 (
  'row_field', 'XPFr'),
 (
  'row_item', 'XPIr'),
 (
  'scenario', 'X191'),
 (
  'scrollbar', 'XSrl'),
 (
  'sheet', 'X128'),
 (
  'slicer', 'X906'),
 (
  'sort', 'Xsrt'),
 (
  'sortfield', 'Xsfd'),
 (
  'sortfields', 'Xsfs'),
 (
  'spinner', 'XSpn'),
 (
  'tab', 'Xtab'),
 (
  'table_style_element', 'TSET'),
 (
  'table_style', '1936'),
 (
  'textbox', 'XTbx'),
 (
  'top_10_format_condition', 'X321'),
 (
  'treeview_control', 'X911'),
 (
  'unique_values_format_condition', 'X323'),
 (
  'validation', 'X237'),
 (
  'value_change', 'X905'),
 (
  'vertical_page_break', 'X121'),
 (
  'web_options', 'X301'),
 (
  'window', 'cwin'),
 (
  'workbook_connection', 'X904'),
 (
  'workbook', 'X141'),
 (
  'worksheet', 'XwSH'),
 (
  'xlspelling_options', 'Xspo'),
 (
  'adjustment', 'mAdj'),
 (
  'arc', 'Xarc'),
 (
  'bullet_format', 'xbf2'),
 (
  'callout_format', 'X101'),
 (
  'callout', 'cD00'),
 (
  'connector_format', 'X294'),
 (
  'fill_format', 'X110'),
 (
  'glow_format', 'DGoF'),
 (
  'gradient_stop', 'GrdS'),
 (
  'line_format', 'X103'),
 (
  'line', 'Xlne'),
 (
  'major_theme_font', '1ThF'),
 (
  'minor_theme_font', '2ThF'),
 (
  'office_theme', 'DOfT'),
 (
  'oval', 'XOvl'),
 (
  'paragraph_format', 'xpf2'),
 (
  'picture_format', 'X106'),
 (
  'picture', 'cD04'),
 (
  'rectangle', 'XRct'),
 (
  'reflection_format', 'DReF'),
 (
  'ruler_level', 'xRlL'),
 (
  'ruler', 'xRul'),
 (
  'shadow_format', 'X107'),
 (
  'shape_connector', 'cD01'),
 (
  'shape_font', 'Fon2'),
 (
  'shape_line', 'cD12'),
 (
  'shape_text_frame', 'X295'),
 (
  'shape_textbox', 'cD07'),
 (
  'shape', 'pShp'),
 (
  'soft_edge_format', 'DSeF'),
 (
  'tab_stop', 'Tab2'),
 (
  'text_column', 'Tcl2'),
 (
  'text_frame', 'X293'),
 (
  'theme_color_scheme', 'DTcS'),
 (
  'theme_color', 'DThC'),
 (
  'theme_effect_scheme', 'DTeS'),
 (
  'theme_font_scheme', 'DTfS'),
 (
  'theme_font', 'DThF'),
 (
  'threeD_format', 'X109'),
 (
  'word_art_format', 'X108'),
 (
  'character', 'cha '),
 (
  'font', 'X111'),
 (
  'paragraph', 'cpar'),
 (
  'sentence', 'csen'),
 (
  'style', 'X129'),
 (
  'text_flow', 'cflo'),
 (
  'text_range_character', 'TrCh'),
 (
  'text_range_line', 'TrLn'),
 (
  'text_range', 'TObj'),
 (
  'word', 'cwor'),
 (
  'cell', 'ccel'),
 (
  'column', 'ccol'),
 (
  'range', 'X117'),
 (
  'row', 'crow'),
 (
  'autocorrect', 'X250'),
 (
  'area_group', 'cg01'),
 (
  'axis_title', 'X257'),
 (
  'axis', 'X255'),
 (
  'bar_group', 'cg05'),
 (
  'chart_area', 'X284'),
 (
  'chart_fill_format', 'X253'),
 (
  'chart_format', 'X115'),
 (
  'chart_group', 'X258'),
 (
  'chart_object', 'X221'),
 (
  'chart_sheet', 'XcSH'),
 (
  'chart_title', 'X256'),
 (
  'chart', 'X119'),
 (
  'column_group', 'cg04'),
 (
  'corners', 'X272'),
 (
  'data_label', 'X265'),
 (
  'data_table', 'X287'),
 (
  'display_unit_label', 'X299'),
 (
  'doughnut_group', 'cg03'),
 (
  'down_bars', 'X279'),
 (
  'drop_lines', 'X276'),
 (
  'error_bars', 'X286'),
 (
  'floor', 'X280'),
 (
  'gridlines', 'X275'),
 (
  'hilo_lines', 'X274'),
 (
  'interior', 'X252'),
 (
  'leader_lines', 'X277'),
 (
  'legend_entry', 'X267'),
 (
  'legend_key', 'X269'),
 (
  'legend', 'X285'),
 (
  'line_group', 'cg02'),
 (
  'pie_group', 'cg06'),
 (
  'plot_area', 'X283'),
 (
  'radar_group', 'cg07'),
 (
  'series_lines', 'X273'),
 (
  'series_point', 'X262'),
 (
  'series', 'X263'),
 (
  'tick_labels', 'X282'),
 (
  'trendline', 'X271'),
 (
  'up_bars', 'X278'),
 (
  'walls', 'X281'),
 (
  'xy_group', 'cg09')]
enums = [
 (
  'yes', 'yes '),
 (
  'no', 'no  '),
 (
  'ask', 'ask '),
 (
  'index', 'indx'),
 (
  'named', 'name'),
 (
  'id', 'ID  '),
 (
  'Macintosh_path', 'mPth'),
 (
  'Posix_path', 'file'),
 (
  'standard', 'lwst'),
 (
  'detailed', 'lwdt'),
 (
  'line_dash_style_unset', b'\x00\x92\xff\xfe'),
 (
  'line_dash_style_solid', b'\x00\x93\x00\x01'),
 (
  'line_dash_style_square_dot', b'\x00\x93\x00\x02'),
 (
  'line_dash_style_round_dot', b'\x00\x93\x00\x03'),
 (
  'line_dash_style_dash', b'\x00\x93\x00\x04'),
 (
  'line_dash_style_dash_dot', b'\x00\x93\x00\x05'),
 (
  'line_dash_style_dash_dot_dot', b'\x00\x93\x00\x06'),
 (
  'line_dash_style_long_dash', b'\x00\x93\x00\x07'),
 (
  'line_dash_style_long_dash_dot', b'\x00\x93\x00\x08'),
 (
  'line_dash_style_long_dash_dot_dot', b'\x00\x93\x00\t'),
 (
  'line_dash_style_system_dash', b'\x00\x93\x00\n'),
 (
  'line_dash_style_system_dot', b'\x00\x93\x00\x0b'),
 (
  'line_dash_style_system_dash_dot', b'\x00\x93\x00\x0c'),
 (
  'line_style_unset', b'\x00\x94\xff\xfe'),
 (
  'single_line', b'\x00\x95\x00\x01'),
 (
  'thin_thin_line', b'\x00\x95\x00\x02'),
 (
  'thin_thick_line', b'\x00\x95\x00\x03'),
 (
  'thick_thin_line', b'\x00\x95\x00\x04'),
 (
  'thick_between_thin_line', b'\x00\x95\x00\x05'),
 (
  'arrowhead_style_unset', b'\x00\x91\xff\xfe'),
 (
  'no_arrowhead', b'\x00\x92\x00\x01'),
 (
  'triangle_arrowhead', b'\x00\x92\x00\x02'),
 (
  'open_arrowhead', b'\x00\x92\x00\x03'),
 (
  'stealth_arrowhead', b'\x00\x92\x00\x04'),
 (
  'diamond_arrowhead', b'\x00\x92\x00\x05'),
 (
  'oval_arrowhead', b'\x00\x92\x00\x06'),
 (
  'arrowhead_width_unset', b'\x00\x90\xff\xfe'),
 (
  'narrow_width_arrowhead', b'\x00\x91\x00\x01'),
 (
  'medium_width_arrowhead', b'\x00\x91\x00\x02'),
 (
  'wide_arrowhead', b'\x00\x91\x00\x03'),
 (
  'arrowhead_length_unset', b'\x00\x93\xff\xfe'),
 (
  'short_arrowhead', b'\x00\x94\x00\x01'),
 (
  'medium_arrowhead', b'\x00\x94\x00\x02'),
 (
  'long_arrowhead', b'\x00\x94\x00\x03'),
 (
  'fill_unset', b'\x00c\xff\xfe'),
 (
  'fill_solid', '\x00d\x00\x01'),
 (
  'fill_patterned', '\x00d\x00\x02'),
 (
  'fill_gradient', '\x00d\x00\x03'),
 (
  'fill_textured', '\x00d\x00\x04'),
 (
  'fill_background', '\x00d\x00\x05'),
 (
  'fill_picture', '\x00d\x00\x06'),
 (
  'gradient_unset', b'\x00d\xff\xfe'),
 (
  'horizontal_gradient', '\x00e\x00\x01'),
 (
  'vertical_gradient', '\x00e\x00\x02'),
 (
  'diagonal_up_gradient', '\x00e\x00\x03'),
 (
  'diagonal_down_gradient', '\x00e\x00\x04'),
 (
  'from_corner_gradient', '\x00e\x00\x05'),
 (
  'from_title_gradient', '\x00e\x00\x06'),
 (
  'from_center_gradient', '\x00e\x00\x07'),
 (
  'gradient_type_unset', b'\x03\xef\xff\xfe'),
 (
  'single_shade_gradient_type', b'\x03\xf0\x00\x01'),
 (
  'two_colors_gradient_type', b'\x03\xf0\x00\x02'),
 (
  'preset_colors_gradient_type', b'\x03\xf0\x00\x03'),
 (
  'multi_colors_gradient_type', b'\x03\xf0\x00\x04'),
 (
  'texture_type_texture_type_unset', b'\x03\xf0\xff\xfe'),
 (
  'texture_type_preset_texture', b'\x03\xf1\x00\x01'),
 (
  'texture_type_user_defined_texture', b'\x03\xf1\x00\x02'),
 (
  'preset_texture_unset', b'\x00e\xff\xfe'),
 (
  'texture_papyrus', '\x00f\x00\x01'),
 (
  'texture_canvas', '\x00f\x00\x02'),
 (
  'texture_denim', '\x00f\x00\x03'),
 (
  'texture_woven_mat', '\x00f\x00\x04'),
 (
  'texture_water_droplets', '\x00f\x00\x05'),
 (
  'texture_paper_bag', '\x00f\x00\x06'),
 (
  'texture_fish_fossil', '\x00f\x00\x07'),
 (
  'texture_sand', '\x00f\x00\x08'),
 (
  'texture_green_marble', '\x00f\x00\t'),
 (
  'texture_white_marble', '\x00f\x00\n'),
 (
  'texture_brown_marble', '\x00f\x00\x0b'),
 (
  'texture_granite', '\x00f\x00\x0c'),
 (
  'texture_newsprint', '\x00f\x00\r'),
 (
  'texture_recycled_paper', '\x00f\x00\x0e'),
 (
  'texture_parchment', '\x00f\x00\x0f'),
 (
  'texture_stationery', '\x00f\x00\x10'),
 (
  'texture_blue_tissue_paper', '\x00f\x00\x11'),
 (
  'texture_pink_tissue_paper', '\x00f\x00\x12'),
 (
  'texture_purple_mesh', '\x00f\x00\x13'),
 (
  'texture_bouquet', '\x00f\x00\x14'),
 (
  'texture_cork', '\x00f\x00\x15'),
 (
  'texture_walnut', '\x00f\x00\x16'),
 (
  'texture_oak', '\x00f\x00\x17'),
 (
  'texture_medium_wood', '\x00f\x00\x18'),
 (
  'pattern_unset', b'\x00f\xff\xfe'),
 (
  'five_percent_pattern', '\x00g\x00\x01'),
 (
  'ten_percent_pattern', '\x00g\x00\x02'),
 (
  'twenty_percent_pattern', '\x00g\x00\x03'),
 (
  'twenty_five_percent_pattern', '\x00g\x00\x04'),
 (
  'thirty_percent_pattern', '\x00g\x00\x05'),
 (
  'forty_percent_pattern', '\x00g\x00\x06'),
 (
  'fifty_percent_pattern', '\x00g\x00\x07'),
 (
  'sixty_percent_pattern', '\x00g\x00\x08'),
 (
  'seventy_percent_pattern', '\x00g\x00\t'),
 (
  'seventy_five_percent_pattern', '\x00g\x00\n'),
 (
  'eighty_percent_pattern', '\x00g\x00\x0b'),
 (
  'ninety_percent_pattern', '\x00g\x00\x0c'),
 (
  'dark_horizontal_pattern', '\x00g\x00\r'),
 (
  'dark_vertical_pattern', '\x00g\x00\x0e'),
 (
  'dark_downward_diagonal_pattern', '\x00g\x00\x0f'),
 (
  'dark_upward_diagonal_pattern', '\x00g\x00\x10'),
 (
  'small_checker_board_pattern', '\x00g\x00\x11'),
 (
  'trellis_pattern', '\x00g\x00\x12'),
 (
  'light_horizontal_pattern', '\x00g\x00\x13'),
 (
  'light_vertical_pattern', '\x00g\x00\x14'),
 (
  'light_downward_diagonal_pattern', '\x00g\x00\x15'),
 (
  'light_upward_diagonal_pattern', '\x00g\x00\x16'),
 (
  'small_grid_pattern', '\x00g\x00\x17'),
 (
  'dotted_diamond_pattern', '\x00g\x00\x18'),
 (
  'wide_downward_diagonal', '\x00g\x00\x19'),
 (
  'wide_upward_diagonal_pattern', '\x00g\x00\x1a'),
 (
  'dashed_upward_diagonal_pattern', '\x00g\x00\x1b'),
 (
  'dashed_downward_diagonal_pattern', '\x00g\x00\x1c'),
 (
  'narrow_vertical_pattern', '\x00g\x00\x1d'),
 (
  'narrow_horizontal_pattern', '\x00g\x00\x1e'),
 (
  'dashed_vertical_pattern', '\x00g\x00\x1f'),
 (
  'dashed_horizontal_pattern', '\x00g\x00 '),
 (
  'large_confetti_pattern', '\x00g\x00!'),
 (
  'large_grid_pattern', '\x00g\x00"'),
 (
  'horizontal_brick_pattern', '\x00g\x00#'),
 (
  'large_checker_board_pattern', '\x00g\x00$'),
 (
  'small_confetti_pattern', '\x00g\x00%'),
 (
  'zig_zag_pattern', '\x00g\x00&'),
 (
  'solid_diamond_pattern', "\x00g\x00'"),
 (
  'diagonal_brick_pattern', '\x00g\x00('),
 (
  'outlined_diamond_pattern', '\x00g\x00)'),
 (
  'plaid_pattern', '\x00g\x00*'),
 (
  'sphere_pattern', '\x00g\x00+'),
 (
  'weave_pattern', '\x00g\x00,'),
 (
  'dotted_grid_pattern', '\x00g\x00-'),
 (
  'divot_pattern', '\x00g\x00.'),
 (
  'shingle_pattern', '\x00g\x00/'),
 (
  'wave_pattern', '\x00g\x000'),
 (
  'horizontal_pattern', '\x00g\x001'),
 (
  'vertical_pattern', '\x00g\x002'),
 (
  'cross_pattern', '\x00g\x003'),
 (
  'downward_diagonal_pattern', '\x00g\x004'),
 (
  'upward_diagonal_pattern', '\x00g\x005'),
 (
  'diagonal_cross_pattern', '\x00g\x005'),
 (
  'preset_gradient_unset', b'\x00g\xff\xfe'),
 (
  'gradient_early_sunset', '\x00h\x00\x01'),
 (
  'gradient_late_sunset', '\x00h\x00\x02'),
 (
  'gradient_nightfall', '\x00h\x00\x03'),
 (
  'gradient_daybreak', '\x00h\x00\x04'),
 (
  'gradient_horizon', '\x00h\x00\x05'),
 (
  'gradient_desert', '\x00h\x00\x06'),
 (
  'gradient_ocean', '\x00h\x00\x07'),
 (
  'gradient_calm_water', '\x00h\x00\x08'),
 (
  'gradient_fire', '\x00h\x00\t'),
 (
  'gradient_fog', '\x00h\x00\n'),
 (
  'gradient_moss', '\x00h\x00\x0b'),
 (
  'gradient_peacock', '\x00h\x00\x0c'),
 (
  'gradient_wheat', '\x00h\x00\r'),
 (
  'gradient_parchment', '\x00h\x00\x0e'),
 (
  'gradient_mahogany', '\x00h\x00\x0f'),
 (
  'gradient_rainbow', '\x00h\x00\x10'),
 (
  'gradient_rainbow2', '\x00h\x00\x11'),
 (
  'gradient_gold', '\x00h\x00\x12'),
 (
  'gradient_gold2', '\x00h\x00\x13'),
 (
  'gradient_brass', '\x00h\x00\x14'),
 (
  'gradient_chrome', '\x00h\x00\x15'),
 (
  'gradient_chrome2', '\x00h\x00\x16'),
 (
  'gradient_silver', '\x00h\x00\x17'),
 (
  'gradient_sapphire', '\x00h\x00\x18'),
 (
  'shadow_unset', b'\x03_\xff\xfe'),
 (
  'shadow1', '\x03`\x00\x01'),
 (
  'shadow2', '\x03`\x00\x02'),
 (
  'shadow3', '\x03`\x00\x03'),
 (
  'shadow4', '\x03`\x00\x04'),
 (
  'shadow5', '\x03`\x00\x05'),
 (
  'shadow6', '\x03`\x00\x06'),
 (
  'shadow7', '\x03`\x00\x07'),
 (
  'shadow8', '\x03`\x00\x08'),
 (
  'shadow9', '\x03`\x00\t'),
 (
  'shadow10', '\x03`\x00\n'),
 (
  'shadow11', '\x03`\x00\x0b'),
 (
  'shadow12', '\x03`\x00\x0c'),
 (
  'shadow13', '\x03`\x00\r'),
 (
  'shadow14', '\x03`\x00\x0e'),
 (
  'shadow15', '\x03`\x00\x0f'),
 (
  'shadow16', '\x03`\x00\x10'),
 (
  'shadow17', '\x03`\x00\x11'),
 (
  'shadow18', '\x03`\x00\x12'),
 (
  'shadow19', '\x03`\x00\x13'),
 (
  'shadow20', '\x03`\x00\x14'),
 (
  'shadow21', '\x03`\x00\x15'),
 (
  'shadow22', '\x03`\x00\x16'),
 (
  'shadow23', '\x03`\x00\x17'),
 (
  'shadow24', '\x03`\x00\x18'),
 (
  'shadow25', '\x03`\x00\x19'),
 (
  'shadow26', '\x03`\x00\x1a'),
 (
  'shadow27', '\x03`\x00\x1b'),
 (
  'shadow28', '\x03`\x00\x1c'),
 (
  'shadow29', '\x03`\x00\x1d'),
 (
  'shadow30', '\x03`\x00\x1e'),
 (
  'shadow31', '\x03`\x00\x1f'),
 (
  'shadow32', '\x03`\x00 '),
 (
  'shadow33', '\x03`\x00!'),
 (
  'shadow34', '\x03`\x00"'),
 (
  'shadow35', '\x03`\x00#'),
 (
  'shadow36', '\x03`\x00$'),
 (
  'shadow37', '\x03`\x00%'),
 (
  'shadow38', '\x03`\x00&'),
 (
  'shadow39', "\x03`\x00'"),
 (
  'shadow40', '\x03`\x00('),
 (
  'shadow41', '\x03`\x00)'),
 (
  'shadow42', '\x03`\x00*'),
 (
  'shadow43', '\x03`\x00+'),
 (
  'wordart_format_unset', b'\x03\xf1\xff\xfe'),
 (
  'wordart_format1', b'\x03\xf2\x00\x00'),
 (
  'wordart_format2', b'\x03\xf2\x00\x01'),
 (
  'wordart_format3', b'\x03\xf2\x00\x02'),
 (
  'wordart_format4', b'\x03\xf2\x00\x03'),
 (
  'wordart_format5', b'\x03\xf2\x00\x04'),
 (
  'wordart_format6', b'\x03\xf2\x00\x05'),
 (
  'wordart_format7', b'\x03\xf2\x00\x06'),
 (
  'wordart_format8', b'\x03\xf2\x00\x07'),
 (
  'wordart_format9', b'\x03\xf2\x00\x08'),
 (
  'wordart_format10', b'\x03\xf2\x00\t'),
 (
  'wordart_format11', b'\x03\xf2\x00\n'),
 (
  'wordart_format12', b'\x03\xf2\x00\x0b'),
 (
  'wordart_format13', b'\x03\xf2\x00\x0c'),
 (
  'wordart_format14', b'\x03\xf2\x00\r'),
 (
  'wordart_format15', b'\x03\xf2\x00\x0e'),
 (
  'wordart_format16', b'\x03\xf2\x00\x0f'),
 (
  'wordart_format17', b'\x03\xf2\x00\x10'),
 (
  'wordart_format18', b'\x03\xf2\x00\x11'),
 (
  'wordart_format19', b'\x03\xf2\x00\x12'),
 (
  'wordart_format20', b'\x03\xf2\x00\x13'),
 (
  'wordart_format21', b'\x03\xf2\x00\x14'),
 (
  'wordart_format22', b'\x03\xf2\x00\x15'),
 (
  'wordart_format23', b'\x03\xf2\x00\x16'),
 (
  'wordart_format24', b'\x03\xf2\x00\x17'),
 (
  'wordart_format25', b'\x03\xf2\x00\x18'),
 (
  'wordart_format26', b'\x03\xf2\x00\x19'),
 (
  'wordart_format27', b'\x03\xf2\x00\x1a'),
 (
  'wordart_format28', b'\x03\xf2\x00\x1b'),
 (
  'wordart_format29', b'\x03\xf2\x00\x1c'),
 (
  'wordart_format30', b'\x03\xf2\x00\x1d'),
 (
  'text_effect_shape_unset', b'\x00\x97\xff\xfe'),
 (
  'plain_text', b'\x00\x98\x00\x01'),
 (
  'stop', b'\x00\x98\x00\x02'),
 (
  'triangle_up', b'\x00\x98\x00\x03'),
 (
  'triangle_down', b'\x00\x98\x00\x04'),
 (
  'chevron_up', b'\x00\x98\x00\x05'),
 (
  'chevron_down', b'\x00\x98\x00\x06'),
 (
  'ring_inside', b'\x00\x98\x00\x07'),
 (
  'ring_outside', b'\x00\x98\x00\x08'),
 (
  'arch_up_curve', b'\x00\x98\x00\t'),
 (
  'arch_down_curve', b'\x00\x98\x00\n'),
 (
  'circle_curve', b'\x00\x98\x00\x0b'),
 (
  'button_curve', b'\x00\x98\x00\x0c'),
 (
  'arch_up_pour', b'\x00\x98\x00\r'),
 (
  'arch_down_pour', b'\x00\x98\x00\x0e'),
 (
  'circle_pour', b'\x00\x98\x00\x0f'),
 (
  'button_pour', b'\x00\x98\x00\x10'),
 (
  'curve_up', b'\x00\x98\x00\x11'),
 (
  'curve_down', b'\x00\x98\x00\x12'),
 (
  'can_up', b'\x00\x98\x00\x13'),
 (
  'can_down', b'\x00\x98\x00\x14'),
 (
  'wave1', b'\x00\x98\x00\x15'),
 (
  'wave2', b'\x00\x98\x00\x16'),
 (
  'double_wave1', b'\x00\x98\x00\x17'),
 (
  'double_wave2', b'\x00\x98\x00\x18'),
 (
  'inflate', b'\x00\x98\x00\x19'),
 (
  'deflate', b'\x00\x98\x00\x1a'),
 (
  'inflate_bottom', b'\x00\x98\x00\x1b'),
 (
  'deflate_bottom', b'\x00\x98\x00\x1c'),
 (
  'inflate_top', b'\x00\x98\x00\x1d'),
 (
  'deflate_top', b'\x00\x98\x00\x1e'),
 (
  'deflate_inflate', b'\x00\x98\x00\x1f'),
 (
  'deflate_inflate_deflate', b'\x00\x98\x00 '),
 (
  'fade_right', b'\x00\x98\x00!'),
 (
  'fade_left', b'\x00\x98\x00"'),
 (
  'fade_up', b'\x00\x98\x00#'),
 (
  'fade_down', b'\x00\x98\x00$'),
 (
  'slant_up', b'\x00\x98\x00%'),
 (
  'slant_down', b'\x00\x98\x00&'),
 (
  'cascade_up', b"\x00\x98\x00'"),
 (
  'cascade_down', b'\x00\x98\x00('),
 (
  'text_effect_alignment_unset', b'\x00\x96\xff\xfe'),
 (
  'left_text_effect_alignment', b'\x00\x97\x00\x01'),
 (
  'centered_text_effect_alignment', b'\x00\x97\x00\x02'),
 (
  'right_text_effect_alignment', b'\x00\x97\x00\x03'),
 (
  'justify_text_effect_alignment', b'\x00\x97\x00\x04'),
 (
  'word_justify_text_effect_alignment', b'\x00\x97\x00\x05'),
 (
  'stretch_justify_text_effect_alignment', b'\x00\x97\x00\x06'),
 (
  'preset_lighting_direction_unset', b'\x00\x9b\xff\xfe'),
 (
  'light_from_top_left', b'\x00\x9c\x00\x01'),
 (
  'light_from_top', b'\x00\x9c\x00\x02'),
 (
  'light_from_top_right', b'\x00\x9c\x00\x03'),
 (
  'light_from_left', b'\x00\x9c\x00\x04'),
 (
  'light_from_none', b'\x00\x9c\x00\x05'),
 (
  'light_from_right', b'\x00\x9c\x00\x06'),
 (
  'light_from_bottom_left', b'\x00\x9c\x00\x07'),
 (
  'light_from_bottom', b'\x00\x9c\x00\x08'),
 (
  'light_from_bottom_right', b'\x00\x9c\x00\t'),
 (
  'lighting_softness_unset', b'\x00\x9c\xff\xfe'),
 (
  'lighting_dim', b'\x00\x9d\x00\x01'),
 (
  'lighting_normal', b'\x00\x9d\x00\x02'),
 (
  'lighting_bright', b'\x00\x9d\x00\x03'),
 (
  'preset_material_unset', b'\x00\x9d\xff\xfe'),
 (
  'matte', b'\x00\x9e\x00\x01'),
 (
  'plastic', b'\x00\x9e\x00\x02'),
 (
  'metal', b'\x00\x9e\x00\x03'),
 (
  'wireframe', b'\x00\x9e\x00\x04'),
 (
  'matte2', b'\x00\x9e\x00\x05'),
 (
  'plastic2', b'\x00\x9e\x00\x06'),
 (
  'metal2', b'\x00\x9e\x00\x07'),
 (
  'warm_matte', b'\x00\x9e\x00\x08'),
 (
  'translucent_powder', b'\x00\x9e\x00\t'),
 (
  'powder', b'\x00\x9e\x00\n'),
 (
  'dark_edge', b'\x00\x9e\x00\x0b'),
 (
  'soft_edge', b'\x00\x9e\x00\x0c'),
 (
  'material_clear', b'\x00\x9e\x00\r'),
 (
  'flat', b'\x00\x9e\x00\x0e'),
 (
  'soft_metal', b'\x00\x9e\x00\x0f'),
 (
  'preset_extrusion_direction_unset', b'\x00\x99\xff\xfe'),
 (
  'extrude_bottom_right', b'\x00\x9a\x00\x01'),
 (
  'extrude_bottom', b'\x00\x9a\x00\x02'),
 (
  'extrude_bottom_left', b'\x00\x9a\x00\x03'),
 (
  'extrude_right', b'\x00\x9a\x00\x04'),
 (
  'extrude_none', b'\x00\x9a\x00\x05'),
 (
  'extrude_left', b'\x00\x9a\x00\x06'),
 (
  'extrude_top_right', b'\x00\x9a\x00\x07'),
 (
  'extrude_top', b'\x00\x9a\x00\x08'),
 (
  'extrude_top_left', b'\x00\x9a\x00\t'),
 (
  'preset_threeD_format_unset', b'\x00\x98\xff\xfe'),
 (
  'format1', b'\x00\x99\x00\x01'),
 (
  'format2', b'\x00\x99\x00\x02'),
 (
  'format3', b'\x00\x99\x00\x03'),
 (
  'format4', b'\x00\x99\x00\x04'),
 (
  'format5', b'\x00\x99\x00\x05'),
 (
  'format6', b'\x00\x99\x00\x06'),
 (
  'format7', b'\x00\x99\x00\x07'),
 (
  'format8', b'\x00\x99\x00\x08'),
 (
  'format9', b'\x00\x99\x00\t'),
 (
  'format10', b'\x00\x99\x00\n'),
 (
  'format11', b'\x00\x99\x00\x0b'),
 (
  'format12', b'\x00\x99\x00\x0c'),
 (
  'format13', b'\x00\x99\x00\r'),
 (
  'format14', b'\x00\x99\x00\x0e'),
 (
  'format15', b'\x00\x99\x00\x0f'),
 (
  'format16', b'\x00\x99\x00\x10'),
 (
  'format17', b'\x00\x99\x00\x11'),
 (
  'format18', b'\x00\x99\x00\x12'),
 (
  'format19', b'\x00\x99\x00\x13'),
 (
  'format20', b'\x00\x99\x00\x14'),
 (
  'extrusion_color_unset', b'\x00\x9a\xff\xfe'),
 (
  'extrusion_color_automatic', b'\x00\x9b\x00\x01'),
 (
  'extrusion_color_custom', b'\x00\x9b\x00\x02'),
 (
  'connector_type_unset', b'\x00h\xff\xfe'),
 (
  'straight', '\x00i\x00\x01'),
 (
  'elbow', '\x00i\x00\x02'),
 (
  'curve', '\x00i\x00\x03'),
 (
  'horizontal_anchor_unset', b'\x00\x9e\xff\xfe'),
 (
  'horizontal_anchor_none', b'\x00\x9f\x00\x01'),
 (
  'horizontal_anchor_center', b'\x00\x9f\x00\x02'),
 (
  'vertical_anchor_unset', b'\x00\x9f\xff\xfe'),
 (
  'anchor_top', b'\x00\xa0\x00\x01'),
 (
  'anchor_top_baseline', b'\x00\xa0\x00\x02'),
 (
  'anchor_middle', b'\x00\xa0\x00\x03'),
 (
  'anchor_bottom', b'\x00\xa0\x00\x04'),
 (
  'anchor_bottom_baseline', b'\x00\xa0\x00\x05'),
 (
  'autoshape_shape_type_unset', b'\x00i\xff\xfe'),
 (
  'autoshape_rectangle', '\x00j\x00\x01'),
 (
  'autoshape_parallelogram', '\x00j\x00\x02'),
 (
  'autoshape_trapezoid', '\x00j\x00\x03'),
 (
  'autoshape_diamond', '\x00j\x00\x04'),
 (
  'autoshape_rounded_rectangle', '\x00j\x00\x05'),
 (
  'autoshape_octagon', '\x00j\x00\x06'),
 (
  'autoshape_isosceles_triangle', '\x00j\x00\x07'),
 (
  'autoshape_right_triangle', '\x00j\x00\x08'),
 (
  'autoshape_oval', '\x00j\x00\t'),
 (
  'autoshape_hexagon', '\x00j\x00\n'),
 (
  'autoshape_cross', '\x00j\x00\x0b'),
 (
  'autoshape_regular_pentagon', '\x00j\x00\x0c'),
 (
  'autoshape_can', '\x00j\x00\r'),
 (
  'autoshape_cube', '\x00j\x00\x0e'),
 (
  'autoshape_bevel', '\x00j\x00\x0f'),
 (
  'autoshape_folded_corner', '\x00j\x00\x10'),
 (
  'autoshape_smiley_face', '\x00j\x00\x11'),
 (
  'autoshape_donut', '\x00j\x00\x12'),
 (
  'autoshape_no_symbol', '\x00j\x00\x13'),
 (
  'autoshape_block_arc', '\x00j\x00\x14'),
 (
  'autoshape_heart', '\x00j\x00\x15'),
 (
  'autoshape_lightning_bolt', '\x00j\x00\x16'),
 (
  'autoshape_sun', '\x00j\x00\x17'),
 (
  'autoshape_moon', '\x00j\x00\x18'),
 (
  'autoshape_arc', '\x00j\x00\x19'),
 (
  'autoshape_double_bracket', '\x00j\x00\x1a'),
 (
  'autoshape_double_brace', '\x00j\x00\x1b'),
 (
  'autoshape_plaque', '\x00j\x00\x1c'),
 (
  'autoshape_left_bracket', '\x00j\x00\x1d'),
 (
  'autoshape_right_bracket', '\x00j\x00\x1e'),
 (
  'autoshape_left_brace', '\x00j\x00\x1f'),
 (
  'autoshape_right_brace', '\x00j\x00 '),
 (
  'autoshape_right_arrow', '\x00j\x00!'),
 (
  'autoshape_left_arrow', '\x00j\x00"'),
 (
  'autoshape_up_arrow', '\x00j\x00#'),
 (
  'autoshape_down_arrow', '\x00j\x00$'),
 (
  'autoshape_left_right_arrow', '\x00j\x00%'),
 (
  'autoshape_up_down_arrow', '\x00j\x00&'),
 (
  'autoshape_quad_arrow', "\x00j\x00'"),
 (
  'autoshape_left_right_up_arrow', '\x00j\x00('),
 (
  'autoshape_bent_arrow', '\x00j\x00)'),
 (
  'autoshape_U_turn_arrow', '\x00j\x00*'),
 (
  'autoshape_left_up_arrow', '\x00j\x00+'),
 (
  'autoshape_bent_up_arrow', '\x00j\x00,'),
 (
  'autoshape_curved_right_arrow', '\x00j\x00-'),
 (
  'autoshape_curved_left_arrow', '\x00j\x00.'),
 (
  'autoshape_curved_up_arrow', '\x00j\x00/'),
 (
  'autoshape_curved_down_arrow', '\x00j\x000'),
 (
  'autoshape_striped_right_arrow', '\x00j\x001'),
 (
  'autoshape_notched_right_arrow', '\x00j\x002'),
 (
  'autoshape_pentagon', '\x00j\x003'),
 (
  'autoshape_chevron', '\x00j\x004'),
 (
  'autoshape_right_arrow_callout', '\x00j\x005'),
 (
  'autoshape_left_arrow_callout', '\x00j\x006'),
 (
  'autoshape_up_arrow_callout', '\x00j\x007'),
 (
  'autoshape_down_arrow_callout', '\x00j\x008'),
 (
  'autoshape_left_right_arrow_callout', '\x00j\x009'),
 (
  'autoshape_up_down_arrow_callout', '\x00j\x00:'),
 (
  'autoshape_quad_arrow_callout', '\x00j\x00;'),
 (
  'autoshape_circular_arrow', '\x00j\x00<'),
 (
  'autoshape_flowchart_process', '\x00j\x00='),
 (
  'autoshape_flowchart_alternate_process', '\x00j\x00>'),
 (
  'autoshape_flowchart_decision', '\x00j\x00?'),
 (
  'autoshape_flowchart_data', '\x00j\x00@'),
 (
  'autoshape_flowchart_predefined_process', '\x00j\x00A'),
 (
  'autoshape_flowchart_internal_storage', '\x00j\x00B'),
 (
  'autoshape_flowchart_document', '\x00j\x00C'),
 (
  'autoshape_flowchart_multi_document', '\x00j\x00D'),
 (
  'autoshape_flowchart_terminator', '\x00j\x00E'),
 (
  'autoshape_flowchart_preparation', '\x00j\x00F'),
 (
  'autoshape_flowchart_manual_input', '\x00j\x00G'),
 (
  'autoshape_flowchart_manual_operation', '\x00j\x00H'),
 (
  'autoshape_flowchart_connector', '\x00j\x00I'),
 (
  'autoshape_flowchart_offpage_connector', '\x00j\x00J'),
 (
  'autoshape_flowchart_card', '\x00j\x00K'),
 (
  'autoshape_flowchart_punched_tape', '\x00j\x00L'),
 (
  'autoshape_flowchart_summing_junction', '\x00j\x00M'),
 (
  'autoshape_flowchart_or', '\x00j\x00N'),
 (
  'autoshape_flowchart_collate', '\x00j\x00O'),
 (
  'autoshape_flowchart_sort', '\x00j\x00P'),
 (
  'autoshape_flowchart_extract', '\x00j\x00Q'),
 (
  'autoshape_flowchart_merge', '\x00j\x00R'),
 (
  'autoshape_flowchart_stored_data', '\x00j\x00S'),
 (
  'autoshape_flowchart_delay', '\x00j\x00T'),
 (
  'autoshape_flowchart_sequential_access_storage', '\x00j\x00U'),
 (
  'autoshape_flowchart_magnetic_disk', '\x00j\x00V'),
 (
  'autoshape_flowchart_direct_access_storage', '\x00j\x00W'),
 (
  'autoshape_flowchart_display', '\x00j\x00X'),
 (
  'autoshape_explosion_one', '\x00j\x00Y'),
 (
  'autoshape_explosion_two', '\x00j\x00Z'),
 (
  'autoshape_four_point_star', '\x00j\x00['),
 (
  'autoshape_five_point_star', '\x00j\x00\\'),
 (
  'autoshape_eight_point_star', '\x00j\x00]'),
 (
  'autoshape_sixteen_point_star', '\x00j\x00^'),
 (
  'autoshape_twenty_four_point_star', '\x00j\x00_'),
 (
  'autoshape_thirty_two_point_star', '\x00j\x00`'),
 (
  'autoshape_up_ribbon', '\x00j\x00a'),
 (
  'autoshape_down_ribbon', '\x00j\x00b'),
 (
  'autoshape_curved_up_ribbon', '\x00j\x00c'),
 (
  'autoshape_curved_down_ribbon', '\x00j\x00d'),
 (
  'autoshape_vertical_scroll', '\x00j\x00e'),
 (
  'autoshape_horizontal_scroll', '\x00j\x00f'),
 (
  'autoshape_wave', '\x00j\x00g'),
 (
  'autoshape_double_wave', '\x00j\x00h'),
 (
  'autoshape_rectangular_callout', '\x00j\x00i'),
 (
  'autoshape_rounded_rectangular_callout', '\x00j\x00j'),
 (
  'autoshape_oval_callout', '\x00j\x00k'),
 (
  'autoshape_cloud_callout', '\x00j\x00l'),
 (
  'autoshape_line_callout_one', '\x00j\x00m'),
 (
  'autoshape_line_callout_two', '\x00j\x00n'),
 (
  'autoshape_line_callout_three', '\x00j\x00o'),
 (
  'autoshape_line_callout_four', '\x00j\x00p'),
 (
  'autoshape_line_callout_one_accent_bar', '\x00j\x00q'),
 (
  'autoshape_line_callout_two_accent_bar', '\x00j\x00r'),
 (
  'autoshape_line_callout_three_accent_bar', '\x00j\x00s'),
 (
  'autoshape_line_callout_four_accent_bar', '\x00j\x00t'),
 (
  'autoshape_line_callout_one_no_border', '\x00j\x00u'),
 (
  'autoshape_line_callout_two_no_border', '\x00j\x00v'),
 (
  'autoshape_line_callout_three_no_border', '\x00j\x00w'),
 (
  'autoshape_line_callout_four_no_border', '\x00j\x00x'),
 (
  'autoshape_callout_one_border_and_accent_bar', '\x00j\x00y'),
 (
  'autoshape_callout_two_border_and_accent_bar', '\x00j\x00z'),
 (
  'autoshape_callout_three_border_and_accent_bar', '\x00j\x00{'),
 (
  'autoshape_callout_four_border_and_accent_bar', '\x00j\x00|'),
 (
  'autoshape_action_button_custom', '\x00j\x00}'),
 (
  'autoshape_action_button_home', '\x00j\x00~'),
 (
  'autoshape_action_button_help', '\x00j\x00\x7f'),
 (
  'autoshape_action_button_information', b'\x00j\x00\x80'),
 (
  'autoshape_action_button_back_or_previous', b'\x00j\x00\x81'),
 (
  'autoshape_action_button_forward_or_next', b'\x00j\x00\x82'),
 (
  'autoshape_action_button_beginning', b'\x00j\x00\x83'),
 (
  'autoshape_action_button_end', b'\x00j\x00\x84'),
 (
  'autoshape_action_button_return', b'\x00j\x00\x85'),
 (
  'autoshape_action_button_document', b'\x00j\x00\x86'),
 (
  'autoshape_action_button_sound', b'\x00j\x00\x87'),
 (
  'autoshape_action_button_movie', b'\x00j\x00\x88'),
 (
  'autoshape_balloon', b'\x00j\x00\x89'),
 (
  'autoshape_not_primitive', b'\x00j\x00\x8a'),
 (
  'autoshape_flowchart_offline_storage', b'\x00j\x00\x8b'),
 (
  'autoshape_left_right_ribbon', b'\x00j\x00\x8c'),
 (
  'autoshape_diagonal_stripe', b'\x00j\x00\x8d'),
 (
  'autoshape_pie', b'\x00j\x00\x8e'),
 (
  'autoshape_non_isosceles_trapezoid', b'\x00j\x00\x8f'),
 (
  'autoshape_Decagon', b'\x00j\x00\x90'),
 (
  'autoshape_Heptagon', b'\x00j\x00\x91'),
 (
  'autoshape_Dodecagon', b'\x00j\x00\x92'),
 (
  'autoshape_six_points_star', b'\x00j\x00\x93'),
 (
  'autoshape_seven_points_star', b'\x00j\x00\x94'),
 (
  'autoshape_ten_points_star', b'\x00j\x00\x95'),
 (
  'autoshape_twelve_points_star', b'\x00j\x00\x96'),
 (
  'autoshape_round_one_rectangle', b'\x00j\x00\x97'),
 (
  'autoshape_round_two_same_rectangle', b'\x00j\x00\x98'),
 (
  'autoshape_round_two_diagonal_rectangle', b'\x00j\x00\x99'),
 (
  'autoshape_snip_round_rectangle', b'\x00j\x00\x9a'),
 (
  'autoshape_snip_one_rectangle', b'\x00j\x00\x9b'),
 (
  'autoshape_snip_two_same_rectangle', b'\x00j\x00\x9c'),
 (
  'autoshape_snip_two_diagonal_rectangle', b'\x00j\x00\x9d'),
 (
  'autoshape_frame', b'\x00j\x00\x9e'),
 (
  'autoshape_half_frame', b'\x00j\x00\x9f'),
 (
  'autoshape_tear', b'\x00j\x00\xa0'),
 (
  'autoshape_chord', b'\x00j\x00\xa1'),
 (
  'autoshape_corner', b'\x00j\x00\xa2'),
 (
  'autoshape_math_plus', b'\x00j\x00\xa3'),
 (
  'autoshape_math_minus', b'\x00j\x00\xa4'),
 (
  'autoshape_math_multiply', b'\x00j\x00\xa5'),
 (
  'autoshape_math_divide', b'\x00j\x00\xa6'),
 (
  'autoshape_math_equal', b'\x00j\x00\xa7'),
 (
  'autoshape_math_not_equal', b'\x00j\x00\xa8'),
 (
  'autoshape_corner_tabs', b'\x00j\x00\xa9'),
 (
  'autoshape_square_tabs', b'\x00j\x00\xaa'),
 (
  'autoshape_plaque_tabs', b'\x00j\x00\xab'),
 (
  'autoshape_gear_six', b'\x00j\x00\xac'),
 (
  'autoshape_gear_nine', b'\x00j\x00\xad'),
 (
  'autoshape_funnel', b'\x00j\x00\xae'),
 (
  'autoshape_pie_wedge', b'\x00j\x00\xaf'),
 (
  'autoshape_left_circular_arrow', b'\x00j\x00\xb0'),
 (
  'autoshape_left_right_circular_arrow', b'\x00j\x00\xb1'),
 (
  'autoshape_swoosh_arrow', b'\x00j\x00\xb2'),
 (
  'autoshape_cloud', b'\x00j\x00\xb3'),
 (
  'autoshape_chart_x', b'\x00j\x00\xb4'),
 (
  'autoshape_chart_star', b'\x00j\x00\xb5'),
 (
  'autoshape_chart_plus', b'\x00j\x00\xb6'),
 (
  'autoshape_line_inverse', b'\x00j\x00\xb7'),
 (
  'shape_type_unset', b'\x00\x8b\xff\xfe'),
 (
  'shape_type_auto', b'\x00\x8c\x00\x01'),
 (
  'shape_type_callout', b'\x00\x8c\x00\x02'),
 (
  'shape_type_chart', b'\x00\x8c\x00\x03'),
 (
  'shape_type_comment', b'\x00\x8c\x00\x04'),
 (
  'shape_type_free_form', b'\x00\x8c\x00\x05'),
 (
  'shape_type_group', b'\x00\x8c\x00\x06'),
 (
  'shape_type_embedded_OLE_control', b'\x00\x8c\x00\x07'),
 (
  'shape_type_form_control', b'\x00\x8c\x00\x08'),
 (
  'shape_type_line', b'\x00\x8c\x00\t'),
 (
  'shape_type_linked_OLE_object', b'\x00\x8c\x00\n'),
 (
  'shape_type_linked_picture', b'\x00\x8c\x00\x0b'),
 (
  'shape_type_OLE_control', b'\x00\x8c\x00\x0c'),
 (
  'shape_type_picture', b'\x00\x8c\x00\r'),
 (
  'shape_type_place_holder', b'\x00\x8c\x00\x0e'),
 (
  'shape_type_word_art', b'\x00\x8c\x00\x0f'),
 (
  'shape_type_media', b'\x00\x8c\x00\x10'),
 (
  'shape_type_text_box', b'\x00\x8c\x00\x11'),
 (
  'shape_type_table', b'\x00\x8c\x00\x12'),
 (
  'shape_type_canvas', b'\x00\x8c\x00\x13'),
 (
  'shape_type_diagram', b'\x00\x8c\x00\x14'),
 (
  'shape_type_ink', b'\x00\x8c\x00\x15'),
 (
  'shape_type_ink_comment', b'\x00\x8c\x00\x16'),
 (
  'shape_type_smartart_graphic', b'\x00\x8c\x00\x17'),
 (
  'shape_type_slicer', b'\x00\x8c\x00\x18'),
 (
  'color_type_unset', b'\x00j\xff\xfe'),
 (
  'RGB', '\x00k\x00\x01'),
 (
  'Scheme', '\x00k\x00\x02'),
 (
  'picture_color_type_unset', b'\x00\xb5\xff\xfe'),
 (
  'picture_color_automatic', b'\x00\xb6\x00\x01'),
 (
  'picture_color_gray_scale', b'\x00\xb6\x00\x02'),
 (
  'picture_color_black_and_white', b'\x00\xb6\x00\x03'),
 (
  'picture_color_watermark', b'\x00\xb6\x00\x04'),
 (
  'angle_unset', b'\x00k\xff\xfe'),
 (
  'angle_automatic', '\x00l\x00\x01'),
 (
  'angle30', '\x00l\x00\x02'),
 (
  'angle45', '\x00l\x00\x03'),
 (
  'angle60', '\x00l\x00\x04'),
 (
  'angle90', '\x00l\x00\x05'),
 (
  'drop_unset', b'\x00l\xff\xfe'),
 (
  'drop_custom', '\x00m\x00\x01'),
 (
  'drop_top', '\x00m\x00\x02'),
 (
  'drop_center', '\x00m\x00\x03'),
 (
  'drop_bottom', '\x00m\x00\x04'),
 (
  'callout_unset', b'\x00m\xff\xfe'),
 (
  'callout_one', '\x00n\x00\x01'),
 (
  'callout_two', '\x00n\x00\x02'),
 (
  'callout_three', '\x00n\x00\x03'),
 (
  'callout_four', '\x00n\x00\x04'),
 (
  'text_orientation_unset', b'\x00\x8d\xff\xfe'),
 (
  'horizontal', b'\x00\x8e\x00\x01'),
 (
  'upward', b'\x00\x8e\x00\x02'),
 (
  'downward', b'\x00\x8e\x00\x03'),
 (
  'vertical_east_asian', b'\x00\x8e\x00\x04'),
 (
  'vertical', b'\x00\x8e\x00\x05'),
 (
  'horizontal_rotated_east_asian', b'\x00\x8e\x00\x06'),
 (
  'scale_from_top_left', '\x00o\x00\x00'),
 (
  'scale_from_middle', '\x00o\x00\x01'),
 (
  'scale_from_bottom_right', '\x00o\x00\x02'),
 (
  'preset_camera_unset', b'\x00\xae\xff\xfe'),
 (
  'camera_legacy_oblique_from_top_left', b'\x00\xaf\x00\x01'),
 (
  'camera_legacy_oblique_from_top', b'\x00\xaf\x00\x02'),
 (
  'camera_legacy_oblique_from_topright', b'\x00\xaf\x00\x03'),
 (
  'camera_legacy_oblique_from_left', b'\x00\xaf\x00\x04'),
 (
  'camera_legacy_oblique_from_front', b'\x00\xaf\x00\x05'),
 (
  'camera_legacy_oblique_from_right', b'\x00\xaf\x00\x06'),
 (
  'camera_legacy_oblique_from_bottom_left', b'\x00\xaf\x00\x07'),
 (
  'camera_legacy_oblique_from_bottom', b'\x00\xaf\x00\x08'),
 (
  'camera_legacy_oblique_from_bottom_right', b'\x00\xaf\x00\t'),
 (
  'camera_legacy_perspective_from_top_left', b'\x00\xaf\x00\n'),
 (
  'camera_legacy_perspective_from_top', b'\x00\xaf\x00\x0b'),
 (
  'camera_legacy_perspective_from_top_right', b'\x00\xaf\x00\x0c'),
 (
  'camera_legacy_perspective_from_left', b'\x00\xaf\x00\r'),
 (
  'camera_legacy_perspective_from_front', b'\x00\xaf\x00\x0e'),
 (
  'camera_legacy_perspective_from_right', b'\x00\xaf\x00\x0f'),
 (
  'camera_legacy_perspective_from_bottom_left', b'\x00\xaf\x00\x10'),
 (
  'camera_legacy_perspective_from_bottom', b'\x00\xaf\x00\x11'),
 (
  'camera_legacy_perspective_from_bottom_right', b'\x00\xaf\x00\x12'),
 (
  'camera_orthographic', b'\x00\xaf\x00\x13'),
 (
  'camera_isometric_from_top_up', b'\x00\xaf\x00\x14'),
 (
  'camera_isometric_from_top_down', b'\x00\xaf\x00\x15'),
 (
  'camera_isometric_from_bottom_up', b'\x00\xaf\x00\x16'),
 (
  'camera_isometric_from_bottom_down', b'\x00\xaf\x00\x17'),
 (
  'camera_isometric_from_left_up', b'\x00\xaf\x00\x18'),
 (
  'camera_isometric_from_left_down', b'\x00\xaf\x00\x19'),
 (
  'camera_isometric_from_right_up', b'\x00\xaf\x00\x1a'),
 (
  'camera_isometric_from_right_down', b'\x00\xaf\x00\x1b'),
 (
  'camera_isometric_off_axis1_from_left', b'\x00\xaf\x00\x1c'),
 (
  'camera_isometric_off_axis1_from_right', b'\x00\xaf\x00\x1d'),
 (
  'camera_isometric_off_axis1_from_top', b'\x00\xaf\x00\x1e'),
 (
  'camera_isometric_off_axis2_from_left', b'\x00\xaf\x00\x1f'),
 (
  'camera_isometric_off_axis2_from_right', b'\x00\xaf\x00 '),
 (
  'camera_isometric_off_axis2_from_top', b'\x00\xaf\x00!'),
 (
  'camera_isometric_off_axis3_from_left', b'\x00\xaf\x00"'),
 (
  'camera_isometric_off_axis3_from_right', b'\x00\xaf\x00#'),
 (
  'camera_isometric_off_axis3_from_bottom', b'\x00\xaf\x00$'),
 (
  'camera_isometric_off_axis4_from_left', b'\x00\xaf\x00%'),
 (
  'camera_isometric_off_axis4_from_right', b'\x00\xaf\x00&'),
 (
  'camera_isometric_off_axis4_from_bottom', b"\x00\xaf\x00'"),
 (
  'camera_oblique_from_top_left', b'\x00\xaf\x00('),
 (
  'camera_oblique_from_top', b'\x00\xaf\x00)'),
 (
  'camera_oblique_from_top_right', b'\x00\xaf\x00*'),
 (
  'camera_oblique_from_left', b'\x00\xaf\x00+'),
 (
  'camera_oblique_from_right', b'\x00\xaf\x00,'),
 (
  'camera_oblique_from_bottom_left', b'\x00\xaf\x00-'),
 (
  'camera_oblique_from_bottom', b'\x00\xaf\x00.'),
 (
  'camera_oblique_from_bottom_right', b'\x00\xaf\x00/'),
 (
  'camera_perspective_from_front', b'\x00\xaf\x000'),
 (
  'camera_perspective_from_left', b'\x00\xaf\x001'),
 (
  'camera_perspective_from_right', b'\x00\xaf\x002'),
 (
  'camera_perspective_from_above', b'\x00\xaf\x003'),
 (
  'camera_perspective_from_below', b'\x00\xaf\x004'),
 (
  'camera_perspective_from_above_facing_left', b'\x00\xaf\x005'),
 (
  'camera_perspective_from_above_facing_right', b'\x00\xaf\x006'),
 (
  'camera_perspective_contrasting_facing_left', b'\x00\xaf\x007'),
 (
  'camera_perspective_contrasting_facing_right', b'\x00\xaf\x008'),
 (
  'camera_perspective_heroic_facing_left', b'\x00\xaf\x009'),
 (
  'camera_perspective_heroic_facing_right', b'\x00\xaf\x00:'),
 (
  'camera_perspective_heroic_extreme_facing_left', b'\x00\xaf\x00;'),
 (
  'camera_perspective_heroic_extreme_facing_right', b'\x00\xaf\x00<'),
 (
  'camera_perspective_relaxed', b'\x00\xaf\x00='),
 (
  'camera_perspective_relaxed_moderately', b'\x00\xaf\x00>'),
 (
  'light_rig_unset', b'\x00\xaf\xff\xfe'),
 (
  'light_rig_flat1', b'\x00\xb0\x00\x01'),
 (
  'light_rig_flat2', b'\x00\xb0\x00\x02'),
 (
  'light_rig_flat3', b'\x00\xb0\x00\x03'),
 (
  'light_rig_flat4', b'\x00\xb0\x00\x04'),
 (
  'light_rig_Normal1', b'\x00\xb0\x00\x05'),
 (
  'light_rig_Normal2', b'\x00\xb0\x00\x06'),
 (
  'light_rig_Normal3', b'\x00\xb0\x00\x07'),
 (
  'light_rig_Normal4', b'\x00\xb0\x00\x08'),
 (
  'light_rig_Harsh1', b'\x00\xb0\x00\t'),
 (
  'light_rig_Harsh2', b'\x00\xb0\x00\n'),
 (
  'light_rig_Harsh3', b'\x00\xb0\x00\x0b'),
 (
  'light_rig_Harsh4', b'\x00\xb0\x00\x0c'),
 (
  'light_rig_three_point', b'\x00\xb0\x00\r'),
 (
  'light_rig_balanced', b'\x00\xb0\x00\x0e'),
 (
  'light_rig_soft', b'\x00\xb0\x00\x0f'),
 (
  'light_rig_harsh', b'\x00\xb0\x00\x10'),
 (
  'light_rig_flood', b'\x00\xb0\x00\x11'),
 (
  'light_rig_contrasting', b'\x00\xb0\x00\x12'),
 (
  'light_rig_morning', b'\x00\xb0\x00\x13'),
 (
  'light_rig_sunrise', b'\x00\xb0\x00\x14'),
 (
  'light_rig_sunset', b'\x00\xb0\x00\x15'),
 (
  'light_rig_chilly', b'\x00\xb0\x00\x16'),
 (
  'light_rig_freezing', b'\x00\xb0\x00\x17'),
 (
  'light_rig_flat', b'\x00\xb0\x00\x18'),
 (
  'light_rig_two_point', b'\x00\xb0\x00\x19'),
 (
  'light_rig_glow', b'\x00\xb0\x00\x1a'),
 (
  'light_rig_bright_room', b'\x00\xb0\x00\x1b'),
 (
  'bevel_type_unset', b'\x00\xb0\xff\xfe'),
 (
  'bevel_none', b'\x00\xb1\x00\x01'),
 (
  'bevel_relaxed_inset', b'\x00\xb1\x00\x02'),
 (
  'bevel_circle', b'\x00\xb1\x00\x03'),
 (
  'bevel_slope', b'\x00\xb1\x00\x04'),
 (
  'bevel_cross', b'\x00\xb1\x00\x05'),
 (
  'bevel_angle', b'\x00\xb1\x00\x06'),
 (
  'bevel_soft_round', b'\x00\xb1\x00\x07'),
 (
  'bevel_convex', b'\x00\xb1\x00\x08'),
 (
  'bevel_cool_slant', b'\x00\xb1\x00\t'),
 (
  'bevel_divot', b'\x00\xb1\x00\n'),
 (
  'bevel_riblet', b'\x00\xb1\x00\x0b'),
 (
  'bevel_hard_edge', b'\x00\xb1\x00\x0c'),
 (
  'bevel_art_deco', b'\x00\xb1\x00\r'),
 (
  'shadow_style_unset', b'\x00\xb1\xff\xfe'),
 (
  'shadow_style_inner', b'\x00\xb2\x00\x01'),
 (
  'shadow_style_outer', b'\x00\xb2\x00\x02'),
 (
  'paragraph_alignment_unset', b'\x00\xe6\xff\xfe'),
 (
  'paragraph_align_left', b'\x00\xe7\x00\x00'),
 (
  'paragraph_align_center', b'\x00\xe7\x00\x01'),
 (
  'paragraph_align_right', b'\x00\xe7\x00\x02'),
 (
  'paragraph_align_justify', b'\x00\xe7\x00\x03'),
 (
  'paragraph_align_distribute', b'\x00\xe7\x00\x04'),
 (
  'paragraph_align_Thai', b'\x00\xe7\x00\x05'),
 (
  'paragraph_align_justify_low', b'\x00\xe7\x00\x06'),
 (
  'strike_unset', b'\x00\xb3\xff\xfe'),
 (
  'no_strike', b'\x00\xb4\x00\x00'),
 (
  'single_strike', b'\x00\xb4\x00\x01'),
 (
  'double_strike', b'\x00\xb4\x00\x02'),
 (
  'caps_unset', b'\x00\xb4\xff\xfe'),
 (
  'no_caps', b'\x00\xb5\x00\x00'),
 (
  'small_caps', b'\x00\xb5\x00\x01'),
 (
  'all_caps', b'\x00\xb5\x00\x02'),
 (
  'underline_unset', b'\x03\xee\xff\xfe'),
 (
  'no_underline', b'\x03\xef\x00\x00'),
 (
  'underline_words_only', b'\x03\xef\x00\x01'),
 (
  'underline_single_line', b'\x03\xef\x00\x02'),
 (
  'underline_double_line', b'\x03\xef\x00\x03'),
 (
  'underline_heavy_line', b'\x03\xef\x00\x04'),
 (
  'underline_dotted_line', b'\x03\xef\x00\x05'),
 (
  'underline_heavy_dotted_line', b'\x03\xef\x00\x06'),
 (
  'underline_dash_line', b'\x03\xef\x00\x07'),
 (
  'underline_heavy_dash_line', b'\x03\xef\x00\x08'),
 (
  'underline_long_dash_line', b'\x03\xef\x00\t'),
 (
  'underline_heavy_long_dash_line', b'\x03\xef\x00\n'),
 (
  'underline_dot_dash_line', b'\x03\xef\x00\x0b'),
 (
  'underline_heavy_dot_dash_line', b'\x03\xef\x00\x0c'),
 (
  'underline_dot_dot_dash_line', b'\x03\xef\x00\r'),
 (
  'underline_heavy_dot_dot_dash_line', b'\x03\xef\x00\x0e'),
 (
  'underline_wavy_line', b'\x03\xef\x00\x0f'),
 (
  'underline_heavy_wavy_line', b'\x03\xef\x00\x10'),
 (
  'underline_wavy_double_line', b'\x03\xef\x00\x11'),
 (
  'tab_unset', b'\x00\xb6\xff\xfe'),
 (
  'left_tab', b'\x00\xb7\x00\x00'),
 (
  'center_tab', b'\x00\xb7\x00\x01'),
 (
  'right_tab', b'\x00\xb7\x00\x02'),
 (
  'decimal_tab', b'\x00\xb7\x00\x03'),
 (
  'character_wrap_unset', b'\x00\xb7\xff\xfe'),
 (
  'no_character_wrap', b'\x00\xb8\x00\x00'),
 (
  'standard_character_wrap', b'\x00\xb8\x00\x01'),
 (
  'strict_character_wrap', b'\x00\xb8\x00\x02'),
 (
  'custom_character_wrap', b'\x00\xb8\x00\x03'),
 (
  'font_alignment_unset', b'\x00\xb8\xff\xfe'),
 (
  'automatic_alignment', b'\x00\xb9\x00\x00'),
 (
  'top_alignment', b'\x00\xb9\x00\x01'),
 (
  'center_alignment', b'\x00\xb9\x00\x02'),
 (
  'baseline_alignment', b'\x00\xb9\x00\x03'),
 (
  'bottom_alignment', b'\x00\xb9\x00\x04'),
 (
  'auto_size_unset', b'\x00\xe4\xff\xfe'),
 (
  'auto_size_none', b'\x00\xe5\x00\x00'),
 (
  'shape_to_fit_text', b'\x00\xe5\x00\x01'),
 (
  'text_to_fit_shape', b'\x00\xe5\x00\x02'),
 (
  'path_type_unset', b'\x00\xba\xff\xfe'),
 (
  'no_path_type', b'\x00\xbb\x00\x00'),
 (
  'path_type1', b'\x00\xbb\x00\x01'),
 (
  'path_type2', b'\x00\xbb\x00\x02'),
 (
  'path_type3', b'\x00\xbb\x00\x03'),
 (
  'path_type4', b'\x00\xbb\x00\x04'),
 (
  'warp_format_unset', b'\x00\xbb\xff\xfe'),
 (
  'warp_format1', b'\x00\xbc\x00\x00'),
 (
  'warp_format2', b'\x00\xbc\x00\x01'),
 (
  'warp_format3', b'\x00\xbc\x00\x02'),
 (
  'warp_format4', b'\x00\xbc\x00\x03'),
 (
  'warp_format5', b'\x00\xbc\x00\x04'),
 (
  'warp_format6', b'\x00\xbc\x00\x05'),
 (
  'warp_format7', b'\x00\xbc\x00\x06'),
 (
  'warp_format8', b'\x00\xbc\x00\x07'),
 (
  'warp_format9', b'\x00\xbc\x00\x08'),
 (
  'warp_format10', b'\x00\xbc\x00\t'),
 (
  'warp_format11', b'\x00\xbc\x00\n'),
 (
  'warp_format12', b'\x00\xbc\x00\x0b'),
 (
  'warp_format13', b'\x00\xbc\x00\x0c'),
 (
  'warp_format14', b'\x00\xbc\x00\r'),
 (
  'warp_format15', b'\x00\xbc\x00\x0e'),
 (
  'warp_format16', b'\x00\xbc\x00\x0f'),
 (
  'warp_format17', b'\x00\xbc\x00\x10'),
 (
  'warp_format18', b'\x00\xbc\x00\x11'),
 (
  'warp_format19', b'\x00\xbc\x00\x12'),
 (
  'warp_format20', b'\x00\xbc\x00\x13'),
 (
  'warp_format21', b'\x00\xbc\x00\x14'),
 (
  'warp_format22', b'\x00\xbc\x00\x15'),
 (
  'warp_format23', b'\x00\xbc\x00\x16'),
 (
  'warp_format24', b'\x00\xbc\x00\x17'),
 (
  'warp_format25', b'\x00\xbc\x00\x18'),
 (
  'warp_format26', b'\x00\xbc\x00\x19'),
 (
  'warp_format27', b'\x00\xbc\x00\x1a'),
 (
  'warp_format28', b'\x00\xbc\x00\x1b'),
 (
  'warp_format29', b'\x00\xbc\x00\x1c'),
 (
  'warp_format30', b'\x00\xbc\x00\x1d'),
 (
  'warp_format31', b'\x00\xbc\x00\x1e'),
 (
  'warp_format32', b'\x00\xbc\x00\x1f'),
 (
  'warp_format33', b'\x00\xbc\x00 '),
 (
  'warp_format34', b'\x00\xbc\x00!'),
 (
  'warp_format35', b'\x00\xbc\x00"'),
 (
  'warp_format36', b'\x00\xbc\x00#'),
 (
  'case_sentence', b'\x00\xe4\x00\x01'),
 (
  'case_lower', b'\x00\xe4\x00\x02'),
 (
  'case_upper', b'\x00\xe4\x00\x03'),
 (
  'case_title', b'\x00\xe4\x00\x04'),
 (
  'case_toggle', b'\x00\xe4\x00\x05'),
 (
  'date_time_format_unset', b'\x00\xbd\xff\xfe'),
 (
  'date_time_format_Mdyy', b'\x00\xbe\x00\x01'),
 (
  'date_time_format_ddddMMMMddyyyy', b'\x00\xbe\x00\x02'),
 (
  'date_time_format_dMMMMyyyy', b'\x00\xbe\x00\x03'),
 (
  'date_time_format_MMMMdyyyy', b'\x00\xbe\x00\x04'),
 (
  'date_time_format_dMMMyy', b'\x00\xbe\x00\x05'),
 (
  'date_time_format_MMMMyy', b'\x00\xbe\x00\x06'),
 (
  'date_time_format_MMyy', b'\x00\xbe\x00\x07'),
 (
  'date_time_format_MMddyyHmm', b'\x00\xbe\x00\x08'),
 (
  'date_time_format_MMddyyhmmAMPM', b'\x00\xbe\x00\t'),
 (
  'date_time_format_Hmm', b'\x00\xbe\x00\n'),
 (
  'date_time_format_Hmmss', b'\x00\xbe\x00\x0b'),
 (
  'date_time_format_hmmAMPM', b'\x00\xbe\x00\x0c'),
 (
  'date_time_format_hmmssAMPM', b'\x00\xbe\x00\r'),
 (
  'date_time_format_figure_out', b'\x00\xbe\x00\x0e'),
 (
  'soft_edge_unset', b'\x00\xbf\xff\xfe'),
 (
  'no_soft_edge', b'\x00\xc0\x00\x00'),
 (
  'soft_edge_type1', b'\x00\xc0\x00\x01'),
 (
  'soft_edge_type2', b'\x00\xc0\x00\x02'),
 (
  'soft_edge_type3', b'\x00\xc0\x00\x03'),
 (
  'soft_edge_type4', b'\x00\xc0\x00\x04'),
 (
  'soft_edge_type5', b'\x00\xc0\x00\x05'),
 (
  'soft_edge_type6', b'\x00\xc0\x00\x06'),
 (
  'first_dark_scheme_color', b'\x00\xc1\x00\x01'),
 (
  'first_light_scheme_color', b'\x00\xc1\x00\x02'),
 (
  'second_dark_scheme_color', b'\x00\xc1\x00\x03'),
 (
  'second_light_scheme_color', b'\x00\xc1\x00\x04'),
 (
  'first_accent_scheme_color', b'\x00\xc1\x00\x05'),
 (
  'second_accent_scheme_color', b'\x00\xc1\x00\x06'),
 (
  'third_accent_scheme_color', b'\x00\xc1\x00\x07'),
 (
  'fourth_accent_scheme_color', b'\x00\xc1\x00\x08'),
 (
  'fifth_accent_scheme_color', b'\x00\xc1\x00\t'),
 (
  'sixth_accent_scheme_color', b'\x00\xc1\x00\n'),
 (
  'hyperlink_scheme_color', b'\x00\xc1\x00\x0b'),
 (
  'followed_hyperlink_scheme_color', b'\x00\xc1\x00\x0c'),
 (
  'theme_color_unset', b'\x00\xc1\xff\xfe'),
 (
  'no_theme_color', b'\x00\xc2\x00\x00'),
 (
  'first_dark_theme_color', b'\x00\xc2\x00\x01'),
 (
  'first_light_theme_color', b'\x00\xc2\x00\x02'),
 (
  'second_dark_theme_color', b'\x00\xc2\x00\x03'),
 (
  'second_light_theme_color', b'\x00\xc2\x00\x04'),
 (
  'first_accent_theme_color', b'\x00\xc2\x00\x05'),
 (
  'second_accent_theme_color', b'\x00\xc2\x00\x06'),
 (
  'third_accent_theme_color', b'\x00\xc2\x00\x07'),
 (
  'fourth_accent_theme_color', b'\x00\xc2\x00\x08'),
 (
  'fifth_accent_theme_color', b'\x00\xc2\x00\t'),
 (
  'sixth_accent_theme_color', b'\x00\xc2\x00\n'),
 (
  'hyperlink_theme_color', b'\x00\xc2\x00\x0b'),
 (
  'followed_hyperlink_theme_color', b'\x00\xc2\x00\x0c'),
 (
  'first_text_theme_color', b'\x00\xc2\x00\r'),
 (
  'first_background_theme_color', b'\x00\xc2\x00\x0e'),
 (
  'second_text_theme_color', b'\x00\xc2\x00\x0f'),
 (
  'second_background_theme_color', b'\x00\xc2\x00\x10'),
 (
  'theme_font_latin', b'\x00\xc3\x00\x01'),
 (
  'theme_font_complex_script', b'\x00\xc3\x00\x02'),
 (
  'theme_font_high_ansi', b'\x00\xc3\x00\x03'),
 (
  'theme_font_east_asian', b'\x00\xc3\x00\x04'),
 (
  'shape_style_unset', b'\x00\xc3\xff\xfe'),
 (
  'shape_not_a_preset', b'\x00\xc4\x00\x00'),
 (
  'shape_preset1', b'\x00\xc4\x00\x01'),
 (
  'shape_preset2', b'\x00\xc4\x00\x02'),
 (
  'shape_preset3', b'\x00\xc4\x00\x03'),
 (
  'shape_preset4', b'\x00\xc4\x00\x04'),
 (
  'shape_preset5', b'\x00\xc4\x00\x05'),
 (
  'shape_preset6', b'\x00\xc4\x00\x06'),
 (
  'shape_preset7', b'\x00\xc4\x00\x07'),
 (
  'shape_preset8', b'\x00\xc4\x00\x08'),
 (
  'shape_preset9', b'\x00\xc4\x00\t'),
 (
  'shape_preset10', b'\x00\xc4\x00\n'),
 (
  'shape_preset11', b'\x00\xc4\x00\x0b'),
 (
  'shape_preset12', b'\x00\xc4\x00\x0c'),
 (
  'shape_preset13', b'\x00\xc4\x00\r'),
 (
  'shape_preset14', b'\x00\xc4\x00\x0e'),
 (
  'shape_preset15', b'\x00\xc4\x00\x0f'),
 (
  'shape_preset16', b'\x00\xc4\x00\x10'),
 (
  'shape_preset17', b'\x00\xc4\x00\x11'),
 (
  'shape_preset18', b'\x00\xc4\x00\x12'),
 (
  'shape_preset19', b'\x00\xc4\x00\x13'),
 (
  'shape_preset20', b'\x00\xc4\x00\x14'),
 (
  'shape_preset21', b'\x00\xc4\x00\x15'),
 (
  'shape_preset22', b'\x00\xc4\x00\x16'),
 (
  'shape_preset23', b'\x00\xc4\x00\x17'),
 (
  'shape_preset24', b'\x00\xc4\x00\x18'),
 (
  'shape_preset25', b'\x00\xc4\x00\x19'),
 (
  'shape_preset26', b'\x00\xc4\x00\x1a'),
 (
  'shape_preset27', b'\x00\xc4\x00\x1b'),
 (
  'shape_preset28', b'\x00\xc4\x00\x1c'),
 (
  'shape_preset29', b'\x00\xc4\x00\x1d'),
 (
  'shape_preset30', b'\x00\xc4\x00\x1e'),
 (
  'shape_preset31', b'\x00\xc4\x00\x1f'),
 (
  'shape_preset32', b'\x00\xc4\x00 '),
 (
  'shape_preset33', b'\x00\xc4\x00!'),
 (
  'shape_preset34', b'\x00\xc4\x00"'),
 (
  'shape_preset35', b'\x00\xc4\x00#'),
 (
  'shape_preset36', b'\x00\xc4\x00$'),
 (
  'shape_preset37', b'\x00\xc4\x00%'),
 (
  'shape_preset38', b'\x00\xc4\x00&'),
 (
  'shape_preset39', b"\x00\xc4\x00'"),
 (
  'shape_preset40', b'\x00\xc4\x00('),
 (
  'shape_preset41', b'\x00\xc4\x00)'),
 (
  'shape_preset42', b'\x00\xc4\x00*'),
 (
  'line_preset1', b"\x00\xc4'\x11"),
 (
  'line_preset2', b"\x00\xc4'\x12"),
 (
  'line_preset3', b"\x00\xc4'\x13"),
 (
  'line_preset4', b"\x00\xc4'\x14"),
 (
  'line_preset5', b"\x00\xc4'\x15"),
 (
  'line_preset6', b"\x00\xc4'\x16"),
 (
  'line_preset7', b"\x00\xc4'\x17"),
 (
  'line_preset8', b"\x00\xc4'\x18"),
 (
  'line_preset9', b"\x00\xc4'\x19"),
 (
  'line_preset10', b"\x00\xc4'\x1a"),
 (
  'line_preset11', b"\x00\xc4'\x1b"),
 (
  'line_preset12', b"\x00\xc4'\x1c"),
 (
  'line_preset13', b"\x00\xc4'\x1d"),
 (
  'line_preset14', b"\x00\xc4'\x1e"),
 (
  'line_preset15', b"\x00\xc4'\x1f"),
 (
  'line_preset16', b"\x00\xc4' "),
 (
  'line_preset17', b"\x00\xc4'!"),
 (
  'line_preset18', b'\x00\xc4\'"'),
 (
  'line_preset19', b"\x00\xc4'#"),
 (
  'line_preset20', b"\x00\xc4'$"),
 (
  'line_preset21', b"\x00\xc4'%"),
 (
  'background_unset', b'\x00\xc4\xff\xfe'),
 (
  'background_not_a_preset', b'\x00\xc5\x00\x00'),
 (
  'background_preset1', b'\x00\xc5\x00\x01'),
 (
  'background_preset2', b'\x00\xc5\x00\x02'),
 (
  'background_preset3', b'\x00\xc5\x00\x03'),
 (
  'background_preset4', b'\x00\xc5\x00\x04'),
 (
  'background_preset5', b'\x00\xc5\x00\x05'),
 (
  'background_preset6', b'\x00\xc5\x00\x06'),
 (
  'background_preset7', b'\x00\xc5\x00\x07'),
 (
  'background_preset8', b'\x00\xc5\x00\x08'),
 (
  'background_preset9', b'\x00\xc5\x00\t'),
 (
  'background_preset10', b'\x00\xc5\x00\n'),
 (
  'background_preset11', b'\x00\xc5\x00\x0b'),
 (
  'background_preset12', b'\x00\xc5\x00\x0c'),
 (
  'text_direction_unset', b'\x00\xea\xff\xfe'),
 (
  'left_to_right', b'\x00\xeb\x00\x01'),
 (
  'right_to_left', b'\x00\xeb\x00\x02'),
 (
  'bullet_type_unset', b'\x00\xe7\xff\xfe'),
 (
  'bullet_type_none', b'\x00\xe8\x00\x00'),
 (
  'bullet_type_unnumbered', b'\x00\xe8\x00\x01'),
 (
  'bullet_type_numbered', b'\x00\xe8\x00\x02'),
 (
  'picture_bullet_type', b'\x00\xe8\x00\x03'),
 (
  'numbered_bullet_style_unset', b'\x00\xe8\xff\xfe'),
 (
  'numbered_bullet_style_alpha_lowercase_period', b'\x00\xe9\x00\x00'),
 (
  'numbered_bullet_style_alpha_uppercase_period', b'\x00\xe9\x00\x01'),
 (
  'numbered_bullet_style_arabic_right_paren', b'\x00\xe9\x00\x02'),
 (
  'numbered_bullet_style_arabic_period', b'\x00\xe9\x00\x03'),
 (
  'numbered_bullet_style_roman_lowercase_paren_both', b'\x00\xe9\x00\x04'),
 (
  'numbered_bullet_style_roman_lowercase_paren_right', b'\x00\xe9\x00\x05'),
 (
  'numbered_bullet_style_roman_lowercase_period', b'\x00\xe9\x00\x06'),
 (
  'numbered_bullet_style_roman_uppercase_period', b'\x00\xe9\x00\x07'),
 (
  'numbered_bullet_style_alpha_lowercase_paren_both', b'\x00\xe9\x00\x08'),
 (
  'numbered_bullet_style_alpha_lowercase_paren_right', b'\x00\xe9\x00\t'),
 (
  'numbered_bullet_style_alpha_uppercase_paren_both', b'\x00\xe9\x00\n'),
 (
  'numbered_bullet_style_alpha_uppercase_paren_right', b'\x00\xe9\x00\x0b'),
 (
  'numbered_bullet_style_arabic_paren_both', b'\x00\xe9\x00\x0c'),
 (
  'numbered_bullet_style_arabic_plain', b'\x00\xe9\x00\r'),
 (
  'numbered_bullet_style_roman_uppercase_paren_both', b'\x00\xe9\x00\x0e'),
 (
  'numbered_bullet_style_roman_uppercase_paren_right', b'\x00\xe9\x00\x0f'),
 (
  'numbered_bullet_style_simplified_chinese_plain', b'\x00\xe9\x00\x10'),
 (
  'numbered_bullet_style_simplified_chinese_period', b'\x00\xe9\x00\x11'),
 (
  'numbered_bullet_style_circle_number_plain', b'\x00\xe9\x00\x12'),
 (
  'numbered_bullet_style_circle_number_white_plain', b'\x00\xe9\x00\x13'),
 (
  'numbered_bullet_style_circle_number_black_plain', b'\x00\xe9\x00\x14'),
 (
  'numbered_bullet_style_traditional_chinese_plain', b'\x00\xe9\x00\x15'),
 (
  'numbered_bullet_style_traditional_chinese_period', b'\x00\xe9\x00\x16'),
 (
  'numbered_bullet_style_arabic_alpha_dash', b'\x00\xe9\x00\x17'),
 (
  'numbered_bullet_style_arabic_abjad_dash', b'\x00\xe9\x00\x18'),
 (
  'numbered_bullet_style_hebrew_alpha_dash', b'\x00\xe9\x00\x19'),
 (
  'numbered_bullet_style_kanji_korean_plain', b'\x00\xe9\x00\x1a'),
 (
  'numbered_bullet_style_kanji_korean_period', b'\x00\xe9\x00\x1b'),
 (
  'numbered_bullet_style_arabic_DB_plain', b'\x00\xe9\x00\x1c'),
 (
  'numbered_bullet_style_arabic_DB_period', b'\x00\xe9\x00\x1d'),
 (
  'numbered_bullet_style_thai_alpha_period', b'\x00\xe9\x00\x1e'),
 (
  'numbered_bullet_style_thai_alpha_paren_right', b'\x00\xe9\x00\x1f'),
 (
  'numbered_bullet_style_thai_alpha_paren_both', b'\x00\xe9\x00 '),
 (
  'numbered_bullet_style_thai_number_period', b'\x00\xe9\x00!'),
 (
  'numbered_bullet_style_thai_number_paren_right', b'\x00\xe9\x00"'),
 (
  'numbered_bullet_style_thai_paren_both', b'\x00\xe9\x00#'),
 (
  'numbered_bullet_style_hindi_alpha_period', b'\x00\xe9\x00$'),
 (
  'numbered_bullet_style_hindi_number_period', b'\x00\xe9\x00%'),
 (
  'numbered_bullet_style_kanji_simpified_chinese_DB_period', b'\x00\xe9\x00&'),
 (
  'numbered_bullet_style_hindi_number_paren_right', b"\x00\xe9\x00'"),
 (
  'numbered_bullet_style_hindi_alpha1_period', b'\x00\xe9\x00('),
 (
  'tabstop_unset', b'\x00\xf4\xff\xfe'),
 (
  'tabstop_left', b'\x00\xf5\x00\x01'),
 (
  'tabstop_center', b'\x00\xf5\x00\x02'),
 (
  'tabstop_right', b'\x00\xf5\x00\x03'),
 (
  'tabstop_decimal', b'\x00\xf5\x00\x04'),
 (
  'reflection_unset', b'\x03\xe9\xff\xfe'),
 (
  'reflection_type_none', b'\x03\xea\x00\x00'),
 (
  'reflection_type1', b'\x03\xea\x00\x01'),
 (
  'reflection_type2', b'\x03\xea\x00\x02'),
 (
  'reflection_type3', b'\x03\xea\x00\x03'),
 (
  'reflection_type4', b'\x03\xea\x00\x04'),
 (
  'reflection_type5', b'\x03\xea\x00\x05'),
 (
  'reflection_type6', b'\x03\xea\x00\x06'),
 (
  'reflection_type7', b'\x03\xea\x00\x07'),
 (
  'reflection_type8', b'\x03\xea\x00\x08'),
 (
  'reflection_type9', b'\x03\xea\x00\t'),
 (
  'texture_unset', b'\x03\xea\xff\xfe'),
 (
  'texture_top_left', b'\x03\xeb\x00\x00'),
 (
  'texture_top', b'\x03\xeb\x00\x01'),
 (
  'texture_top_right', b'\x03\xeb\x00\x02'),
 (
  'texture_left', b'\x03\xeb\x00\x03'),
 (
  'texture_center', b'\x03\xeb\x00\x04'),
 (
  'texture_right', b'\x03\xeb\x00\x05'),
 (
  'texture_bottom_left', b'\x03\xeb\x00\x06'),
 (
  'texture_botton', b'\x03\xeb\x00\x07'),
 (
  'texture_bottom_right', b'\x03\xeb\x00\x08'),
 (
  'text_baseline_alignment_unset', b'\x03\xeb\xff\xfe'),
 (
  'text_baseline_align_baseline', b'\x03\xec\x00\x01'),
 (
  'text_baseline_align_top', b'\x03\xec\x00\x02'),
 (
  'text_baseline_align_center', b'\x03\xec\x00\x03'),
 (
  'text_baseline_align_east_asian50', b'\x03\xec\x00\x04'),
 (
  'text_baseline_align_automatic', b'\x03\xec\x00\x05'),
 (
  'clipboard_format_unset', b'\x03\xec\xff\xfe'),
 (
  'native_clipboard_format', b'\x03\xed\x00\x01'),
 (
  'HTMl_clipboard_format', b'\x03\xed\x00\x02'),
 (
  'RTF_clipboard_format', b'\x03\xed\x00\x03'),
 (
  'plain_text_clipboard_format', b'\x03\xed\x00\x04'),
 (
  'insert_before', b'\x03\xee\x00\x00'),
 (
  'insert_after', b'\x03\xee\x00\x01'),
 (
  'save_as_default', b'\x03\xf2\xff\xfe'),
 (
  'save_as_PNG_file', b'\x03\xf3\x00\x00'),
 (
  'save_as_BMP_file', b'\x03\xf3\x00\x01'),
 (
  'save_as_GIF_file', b'\x03\xf3\x00\x02'),
 (
  'save_as_JPG_file', b'\x03\xf3\x00\x03'),
 (
  'save_as_PDF_file', b'\x03\xf3\x00\x04'),
 (
  'no_effect', b'\x03\xf4\x00\x00'),
 (
  'effect_background_removal', b'\x03\xf4\x00\x01'),
 (
  'effect_blur', b'\x03\xf4\x00\x02'),
 (
  'effect_brightness_contrast', b'\x03\xf4\x00\x03'),
 (
  'effect_cement', b'\x03\xf4\x00\x04'),
 (
  'effect_crisscross_etching', b'\x03\xf4\x00\x05'),
 (
  'effect_chalk_sketch', b'\x03\xf4\x00\x06'),
 (
  'effect_color_temperature', b'\x03\xf4\x00\x07'),
 (
  'effect_cutout', b'\x03\xf4\x00\x08'),
 (
  'effect_film_grain', b'\x03\xf4\x00\t'),
 (
  'effect_glass', b'\x03\xf4\x00\n'),
 (
  'effect_glow_diffused', b'\x03\xf4\x00\x0b'),
 (
  'effect_glow_edges', b'\x03\xf4\x00\x0c'),
 (
  'effect_light_screen', b'\x03\xf4\x00\r'),
 (
  'effect_line_drawing', b'\x03\xf4\x00\x0e'),
 (
  'effect_marker', b'\x03\xf4\x00\x0f'),
 (
  'effect_mosiaic_bubbles', b'\x03\xf4\x00\x10'),
 (
  'effect_paint_brush', b'\x03\xf4\x00\x11'),
 (
  'effect_paint_strokes', b'\x03\xf4\x00\x12'),
 (
  'effect_pastels_smooth', b'\x03\xf4\x00\x13'),
 (
  'effect_pencil_grayscale', b'\x03\xf4\x00\x14'),
 (
  'effect_pencil_sketch', b'\x03\xf4\x00\x15'),
 (
  'effect_photocopy', b'\x03\xf4\x00\x16'),
 (
  'effect_plastic_wrap', b'\x03\xf4\x00\x17'),
 (
  'effect_saturation', b'\x03\xf4\x00\x18'),
 (
  'effect_sharpen_soften', b'\x03\xf4\x00\x19'),
 (
  'effect_texturizer', b'\x03\xf4\x00\x1a'),
 (
  'effect_watercolor_sponge', b'\x03\xf4\x00\x1b'),
 (
  'line', b'\x00\x8f\x00\x00'),
 (
  'curve', b'\x00\x8f\x00\x01'),
 (
  'auto', b'\x00\x90\x00\x00'),
 (
  'corner', b'\x00\x90\x00\x01'),
 (
  'smooth', b'\x00\x90\x00\x02'),
 (
  'symmetric', b'\x00\x90\x00\x03'),
 (
  'default_node_position', b'\x03\xf5\x00\x01'),
 (
  'after_node', b'\x03\xf5\x00\x02'),
 (
  'before_node', b'\x03\xf5\x00\x03'),
 (
  'above_node', b'\x03\xf5\x00\x04'),
 (
  'below_node', b'\x03\xf5\x00\x05'),
 (
  'default_node', b'\x03\xf6\x00\x01'),
 (
  'assistant_node', b'\x03\xf6\x00\x02'),
 (
  'org_chart_layout_unset', b'\x03\xf6\xff\xfe'),
 (
  'org_chart_layout_standard', b'\x03\xf7\x00\x01'),
 (
  'org_chart_layout_both_hanging', b'\x03\xf7\x00\x02'),
 (
  'org_chart_layout_left_hanging', b'\x03\xf7\x00\x03'),
 (
  'org_chart_layout_right_hanging', b'\x03\xf7\x00\x04'),
 (
  'org_chart_layout_default', b'\x03\xf7\x00\x05'),
 (
  'align_lefts', '\x00\x00\x00\x00'),
 (
  'align_centers', '\x00\x00\x00\x01'),
 (
  'align_rights', '\x00\x00\x00\x02'),
 (
  'align_tops', '\x00\x00\x00\x03'),
 (
  'align_middles', '\x00\x00\x00\x04'),
 (
  'align_bottoms', '\x00\x00\x00\x05'),
 (
  'distribute_horizontally', '\x00\x00\x00\x00'),
 (
  'distribute_vertically', '\x00\x00\x00\x01'),
 (
  'orientation_unset', b'\x00\x8c\xff\xfe'),
 (
  'horizontal_orientation', b'\x00\x8d\x00\x01'),
 (
  'vertical_orientation', b'\x00\x8d\x00\x02'),
 (
  'bring_shape_to_front', '\x00p\x00\x00'),
 (
  'send_shape_to_back', '\x00p\x00\x01'),
 (
  'bring_shape_forward', '\x00p\x00\x02'),
 (
  'send_shape_backward', '\x00p\x00\x03'),
 (
  'bring_shape_in_front_of_text', '\x00p\x00\x04'),
 (
  'send_shape_behind_text', '\x00p\x00\x05'),
 (
  'flip_horizontal', '\x00q\x00\x00'),
 (
  'flip_vertical', '\x00q\x00\x01'),
 (
  'true', b'\x00\xa0\xff\xff'),
 (
  'false', b'\x00\xa1\x00\x00'),
 (
  'C_true', b'\x00\xa1\x00\x01'),
 (
  'toggle', b'\x00\xa0\xff\xfd'),
 (
  'tri_state_unset', b'\x00\xa0\xff\xfe'),
 (
  'black_and_white_unset', b'\x00\xac\xff\xfe'),
 (
  'black_and_white_mode_automatic', b'\x00\xad\x00\x01'),
 (
  'black_and_white_mode_gray_scale', b'\x00\xad\x00\x02'),
 (
  'black_and_white_mode_light_gray_scale', b'\x00\xad\x00\x03'),
 (
  'black_and_white_mode_inverse_gray_scale', b'\x00\xad\x00\x04'),
 (
  'black_and_white_mode_gray_outline', b'\x00\xad\x00\x05'),
 (
  'black_and_white_mode_black_text_and_line', b'\x00\xad\x00\x06'),
 (
  'black_and_white_mode_high_contrast', b'\x00\xad\x00\x07'),
 (
  'black_and_white_mode_black', b'\x00\xad\x00\x08'),
 (
  'black_and_white_mode_white', b'\x00\xad\x00\t'),
 (
  'black_and_white_mode_dont_show', b'\x00\xad\x00\n'),
 (
  'bar_left', '\x00r\x00\x00'),
 (
  'bar_top', '\x00r\x00\x01'),
 (
  'bar_right', '\x00r\x00\x02'),
 (
  'bar_bottom', '\x00r\x00\x03'),
 (
  'bar_floating', '\x00r\x00\x04'),
 (
  'bar_pop_up', '\x00r\x00\x05'),
 (
  'bar_menu', '\x00r\x00\x06'),
 (
  'no_protection', '\x00s\x00\x00'),
 (
  'no_customize', '\x00s\x00\x01'),
 (
  'no_resize', '\x00s\x00\x02'),
 (
  'no_move', '\x00s\x00\x04'),
 (
  'no_change_visible', '\x00s\x00\x08'),
 (
  'no_change_dock', '\x00s\x00\x10'),
 (
  'no_vertical_dock', '\x00s\x00 '),
 (
  'no_horizontal_dock', '\x00s\x00@'),
 (
  'normal_command_bar', '\x00t\x00\x00'),
 (
  'menubar_command_bar', '\x00t\x00\x01'),
 (
  'popup_command_bar', '\x00t\x00\x02'),
 (
  'control_custom', '\x00u\x00\x00'),
 (
  'control_button', '\x00u\x00\x01'),
 (
  'control_edit', '\x00u\x00\x02'),
 (
  'control_drop_down', '\x00u\x00\x03'),
 (
  'control_combobox', '\x00u\x00\x04'),
 (
  'button_drop_down', '\x00u\x00\x05'),
 (
  'split_drop_down', '\x00u\x00\x06'),
 (
  'OCX_drop_down', '\x00u\x00\x07'),
 (
  'generic_drop_down', '\x00u\x00\x08'),
 (
  'graphic_drop_down', '\x00u\x00\t'),
 (
  'control_popup', '\x00u\x00\n'),
 (
  'graphic_Popup', '\x00u\x00\x0b'),
 (
  'button_popup', '\x00u\x00\x0c'),
 (
  'split_button_popup', '\x00u\x00\r'),
 (
  'split_button_MRU_popup', '\x00u\x00\x0e'),
 (
  'control_label', '\x00u\x00\x0f'),
 (
  'expanding_grid', '\x00u\x00\x10'),
 (
  'split_expanding_grid', '\x00u\x00\x11'),
 (
  'control_grid', '\x00u\x00\x12'),
 (
  'control_gauge', '\x00u\x00\x13'),
 (
  'graphic_combobox', '\x00u\x00\x14'),
 (
  'control_pane', '\x00u\x00\x15'),
 (
  'active_X', '\x00u\x00\x16'),
 (
  'control_group', '\x00u\x00\x17'),
 (
  'control_tab', '\x00u\x00\x18'),
 (
  'control_spinner', '\x00u\x00\x19'),
 (
  'button_state_up', '\x00v\x00\x00'),
 (
  'button_state_down', b'\x00u\xff\xff'),
 (
  'button_state_unset', '\x00v\x00\x02'),
 (
  'neither', '\x00w\x00\x00'),
 (
  'server', '\x00w\x00\x01'),
 (
  'client', '\x00w\x00\x02'),
 (
  'both', '\x00w\x00\x03'),
 (
  'button_automatic', '\x00x\x00\x00'),
 (
  'button_icon', '\x00x\x00\x01'),
 (
  'button_caption', '\x00x\x00\x02'),
 (
  'button_icon_and_caption', '\x00x\x00\x03'),
 (
  'combobox_style_normal', '\x00y\x00\x00'),
 (
  'combobox_style_label', '\x00y\x00\x01'),
 (
  'None_', '\x00{\x00\x00'),
 (
  'Random', '\x00{\x00\x01'),
 (
  'Unfold', '\x00{\x00\x02'),
 (
  'Slide', '\x00{\x00\x03'),
 (
  'hyperlink_type_text_range', b'\x00\x96\x00\x00'),
 (
  'hyperlink_type_shape', b'\x00\x96\x00\x01'),
 (
  'hyperlink_type_inline_shape', b'\x00\x96\x00\x02'),
 (
  'append_string', b'\x00\xae\x00\x00'),
 (
  'post_string', b'\x00\xae\x00\x01'),
 (
  'idle', '\x00|\x00\x01'),
 (
  'greeting', '\x00|\x00\x02'),
 (
  'goodbye', '\x00|\x00\x03'),
 (
  'begin_speaking', '\x00|\x00\x04'),
 (
  'character_success_major', '\x00|\x00\x06'),
 (
  'get_attention_major', '\x00|\x00\x0b'),
 (
  'get_attention_minor', '\x00|\x00\x0c'),
 (
  'searching', '\x00|\x00\r'),
 (
  'printing', '\x00|\x00\x12'),
 (
  'gesture_right', '\x00|\x00\x13'),
 (
  'writing_noting_something', '\x00|\x00\x16'),
 (
  'working_at_something', '\x00|\x00\x17'),
 (
  'thinking', '\x00|\x00\x18'),
 (
  'sending_mail', '\x00|\x00\x19'),
 (
  'listens_to_computer', '\x00|\x00\x1a'),
 (
  'disappear', '\x00|\x00\x1f'),
 (
  'appear', '\x00|\x00 '),
 (
  'get_artsy', '\x00|\x00d'),
 (
  'get_techy', '\x00|\x00e'),
 (
  'get_wizardy', '\x00|\x00f'),
 (
  'checking_something', '\x00|\x00g'),
 (
  'look_down', '\x00|\x00h'),
 (
  'look_down_left', '\x00|\x00i'),
 (
  'look_down_right', '\x00|\x00j'),
 (
  'look_left', '\x00|\x00k'),
 (
  'look_right', '\x00|\x00l'),
 (
  'look_up', '\x00|\x00m'),
 (
  'look_up_left', '\x00|\x00n'),
 (
  'look_up_right', '\x00|\x00o'),
 (
  'saving', '\x00|\x00p'),
 (
  'gesture_down', '\x00|\x00q'),
 (
  'gesture_left', '\x00|\x00r'),
 (
  'gesture_up', '\x00|\x00s'),
 (
  'empty_trash', '\x00|\x00t'),
 (
  'button_none', '\x00}\x00\x00'),
 (
  'button_ok', '\x00}\x00\x01'),
 (
  'button_cancel', '\x00}\x00\x02'),
 (
  'buttons_ok_cancel', '\x00}\x00\x03'),
 (
  'buttons_yes_no', '\x00}\x00\x04'),
 (
  'buttons_yes_no_cancel', '\x00}\x00\x05'),
 (
  'buttons_back_close', '\x00}\x00\x06'),
 (
  'buttons_next_close', '\x00}\x00\x07'),
 (
  'buttons_back_next_close', '\x00}\x00\x08'),
 (
  'buttons_retry_cancel', '\x00}\x00\t'),
 (
  'buttons_abort_retry_ignore', '\x00}\x00\n'),
 (
  'buttons_search_close', '\x00}\x00\x0b'),
 (
  'buttons_back_next_snooze', '\x00}\x00\x0c'),
 (
  'buttons_tips_options_close', '\x00}\x00\r'),
 (
  'buttons_yes_all_no_cancel', '\x00}\x00\x0e'),
 (
  'icon_none', '\x00~\x00\x00'),
 (
  'icon_application', '\x00~\x00\x01'),
 (
  'icon_alert', '\x00~\x00\x02'),
 (
  'icon_tip', '\x00~\x00\x03'),
 (
  'icon_alert_critical', '\x00~\x00e'),
 (
  'icon_alert_warning', '\x00~\x00g'),
 (
  'icon_alert_info', '\x00~\x00h'),
 (
  'Inactive', b'\x00\x82\x00\x00'),
 (
  'Active', b'\x00\x82\x00\x01'),
 (
  'Suspend', b'\x00\x82\x00\x02'),
 (
  'Resume', b'\x00\x82\x00\x03'),
 (
  'property_type_number', b'\x00\xa2\x00\x01'),
 (
  'property_type_boolean', b'\x00\xa2\x00\x02'),
 (
  'property_type_date', b'\x00\xa2\x00\x03'),
 (
  'property_type_string', b'\x00\xa2\x00\x04'),
 (
  'property_type_float', b'\x00\xa2\x00\x05'),
 (
  'msoAutomationSecurityLow', b'\x00\xa3\x00\x01'),
 (
  'msoAutomationSecurityByUI', b'\x00\xa3\x00\x02'),
 (
  'msoAutomationSecurityForceDisable', b'\x00\xa3\x00\x03'),
 (
  'resolution544x376', b'\x00\x84\x00\x00'),
 (
  'resolution640x480', b'\x00\x84\x00\x01'),
 (
  'resolution720x512', b'\x00\x84\x00\x02'),
 (
  'resolution800x600', b'\x00\x84\x00\x03'),
 (
  'resolution1024x768', b'\x00\x84\x00\x04'),
 (
  'resolution1152x882', b'\x00\x84\x00\x05'),
 (
  'resolution1152x900', b'\x00\x84\x00\x06'),
 (
  'resolution1280x1024', b'\x00\x84\x00\x07'),
 (
  'resolution1600x1200', b'\x00\x84\x00\x08'),
 (
  'resolution1800x1440', b'\x00\x84\x00\t'),
 (
  'resolution1920x1200', b'\x00\x84\x00\n'),
 (
  'Arabic_character_set', b'\x00\x85\x00\x01'),
 (
  'Cyrillic_character_set', b'\x00\x85\x00\x02'),
 (
  'English_character_set', b'\x00\x85\x00\x03'),
 (
  'Greek_character_set', b'\x00\x85\x00\x04'),
 (
  'Hebrew_character_set', b'\x00\x85\x00\x05'),
 (
  'Japanese_character_set', b'\x00\x85\x00\x06'),
 (
  'Korean_character_set', b'\x00\x85\x00\x07'),
 (
  'Multilingual_Unicode_character_set', b'\x00\x85\x00\x08'),
 (
  'Simplified_Chinese_character_set', b'\x00\x85\x00\t'),
 (
  'Thai_character_set', b'\x00\x85\x00\n'),
 (
  'Traditional_Chinese_character_set', b'\x00\x85\x00\x0b'),
 (
  'Vietnamese_character_set', b'\x00\x85\x00\x0c'),
 (
  'encoding_Thai', b'\x00\x8b\x03j'),
 (
  'encoding_Japanese_ShiftJIS', b'\x00\x8b\x03\xa4'),
 (
  'encoding_simplified_Chinese', b'\x00\x8b\x03\xa8'),
 (
  'encoding_Korean', b'\x00\x8b\x03\xb5'),
 (
  'encoding_Big5_traditional_Chinese', b'\x00\x8b\x03\xb6'),
 (
  'encoding_little_endian', b'\x00\x8b\x04\xb0'),
 (
  'encoding_big_endian', b'\x00\x8b\x04\xb1'),
 (
  'encoding_central_European', b'\x00\x8b\x04\xe2'),
 (
  'encoding_Cyrillic', b'\x00\x8b\x04\xe3'),
 (
  'encoding_Western', b'\x00\x8b\x04\xe4'),
 (
  'encoding_Greek', b'\x00\x8b\x04\xe5'),
 (
  'encoding_Turkish', b'\x00\x8b\x04\xe6'),
 (
  'encoding_Hebrew', b'\x00\x8b\x04\xe7'),
 (
  'encoding_Arabic', b'\x00\x8b\x04\xe8'),
 (
  'encoding_Baltic', b'\x00\x8b\x04\xe9'),
 (
  'encoding_Vietnamese', b'\x00\x8b\x04\xea'),
 (
  'encoding_ISO88591_Latin1', b'\x00\x8bo\xaf'),
 (
  'encoding_ISO88592_central_Europe', b'\x00\x8bo\xb0'),
 (
  'encoding_ISO88593_Latin3', b'\x00\x8bo\xb1'),
 (
  'encoding_ISO88594_Baltic', b'\x00\x8bo\xb2'),
 (
  'encoding_ISO88595_Cyrillic', b'\x00\x8bo\xb3'),
 (
  'encoding_ISO88596_Arabic', b'\x00\x8bo\xb4'),
 (
  'encoding_ISO88597_Greek', b'\x00\x8bo\xb5'),
 (
  'encoding_ISO88598_Hebrew', b'\x00\x8bo\xb6'),
 (
  'encoding_ISO88599_Turkish', b'\x00\x8bo\xb7'),
 (
  'encoding_ISO885915_Latin9', b'\x00\x8bo\xbd'),
 (
  'encoding_ISO2022_Japanese_no_half_width_Katakana', b'\x00\x8b\xc4,'),
 (
  'encoding_ISO2022_Japanese_JISX02021984', b'\x00\x8b\xc4-'),
 (
  'encoding_ISO2022_Japanese_JISX02011989', b'\x00\x8b\xc4.'),
 (
  'encoding_ISO2022KR', b'\x00\x8b\xc41'),
 (
  'encoding_ISO2022CN_traditional_Chinese', b'\x00\x8b\xc43'),
 (
  'encoding_ISO2022CN_simplified_Chinese', b'\x00\x8b\xc45'),
 (
  'encoding_Mac_Roman', b"\x00\x8b'\x10"),
 (
  'encoding_Mac_Japanese', b"\x00\x8b'\x11"),
 (
  'encoding_Mac_traditional_Chinese', b"\x00\x8b'\x12"),
 (
  'encoding_Mac_Korean', b"\x00\x8b'\x13"),
 (
  'encoding_Mac_Arabic', b"\x00\x8b'\x14"),
 (
  'encoding_Mac_Hebrew', b"\x00\x8b'\x15"),
 (
  'encoding_Mac_Greek1', b"\x00\x8b'\x16"),
 (
  'encoding_Mac_Cyrillic', b"\x00\x8b'\x17"),
 (
  'encoding_Mac_simplified_Chinese_GB2312', b"\x00\x8b'\x18"),
 (
  'encoding_Mac_Romania', b"\x00\x8b'\x1a"),
 (
  'encoding_Mac_Ukraine', b"\x00\x8b'!"),
 (
  'encoding_Mac_Latin2', b"\x00\x8b'-"),
 (
  'encoding_Mac_Icelandic', b"\x00\x8b'_"),
 (
  'encoding_Mac_Turkish', b"\x00\x8b'a"),
 (
  'encoding_Mac_Croatia', b"\x00\x8b'b"),
 (
  'encoding_EBCDIC_US_Canada', b'\x00\x8b\x00%'),
 (
  'encoding_EBCDIC_International', b'\x00\x8b\x01\xf4'),
 (
  'encoding_EBCDIC_multilingual_ROECE_Latin2', b'\x00\x8b\x03f'),
 (
  'encoding_EBCDIC_Greek_modern', b'\x00\x8b\x03k'),
 (
  'encoding_EBCDIC_Turkish_Latin5', b'\x00\x8b\x04\x02'),
 (
  'encoding_EBCDIC_Germany', b'\x00\x8bO1'),
 (
  'encoding_EBCDIC_Denmark_Norway', b'\x00\x8bO5'),
 (
  'encoding_EBCDIC_Finland_Sweden', b'\x00\x8bO6'),
 (
  'encoding_EBCDIC_Italy', b'\x00\x8bO8'),
 (
  'encoding_EBCDIC_Latin_America_Spain', b'\x00\x8bO<'),
 (
  'encoding_EBCDIC_United_Kingdom', b'\x00\x8bO='),
 (
  'encoding_EBCDIC_Japanese_Katakana_extended', b'\x00\x8bOB'),
 (
  'encoding_EBCDIC_France', b'\x00\x8bOI'),
 (
  'encoding_EBCDIC_Arabic', b'\x00\x8bO\xc4'),
 (
  'encoding_EBCDIC_Greek', b'\x00\x8bO\xc7'),
 (
  'encoding_EBCDIC_Hebrew', b'\x00\x8bO\xc8'),
 (
  'encoding_EBCDIC_Korean_extended', b'\x00\x8bQa'),
 (
  'encoding_EBCDIC_Thai', b'\x00\x8bQf'),
 (
  'encoding_EBCDIC_Icelandic', b'\x00\x8bQ\x87'),
 (
  'encoding_EBCDIC_Turkish', b'\x00\x8bQ\xa9'),
 (
  'encoding_EBCDIC_Russian', b'\x00\x8bQ\x90'),
 (
  'encoding_EBCDIC_Serbian_Bulgarian', b'\x00\x8bR!'),
 (
  'encoding_EBCDIC_Japanese_Katakana_extended_and_Japanese',
  b'\x00\x8b\xc6\xf2'),
 (
  'encoding_EBCDIC_US_Canada_and_Japanese', b'\x00\x8b\xc6\xf3'),
 (
  'encoding_EBCDIC_extended_and_Korean', b'\x00\x8b\xc6\xf5'),
 (
  'encoding_EBCDIC_simplified_Chinese_extended_and_simplified_Chinese',
  b'\x00\x8b\xc6\xf7'),
 (
  'encoding_EBCDIC_US_Canada_and_traditional_Chinese', b'\x00\x8b\xc6\xf9'),
 (
  'encoding_EBCDIC_Japanese_Latin_extended_and_Japanese', b'\x00\x8b\xc6\xfb'),
 (
  'encoding_OEM_United_States', b'\x00\x8b\x01\xb5'),
 (
  'encoding_OEM_Greek', b'\x00\x8b\x02\xe1'),
 (
  'encoding_OEM_Baltic', b'\x00\x8b\x03\x07'),
 (
  'encoding_OEM_multilingual_LatinI', b'\x00\x8b\x03R'),
 (
  'encoding_OEM_multilingual_LatinII', b'\x00\x8b\x03T'),
 (
  'encoding_OEM_Cyrillic', b'\x00\x8b\x03W'),
 (
  'encoding_OEM_Turkish', b'\x00\x8b\x03Y'),
 (
  'encoding_OEM_Portuguese', b'\x00\x8b\x03\\'),
 (
  'encoding_OEM_Icelandic', b'\x00\x8b\x03]'),
 (
  'encoding_OEM_Hebrew', b'\x00\x8b\x03^'),
 (
  'encoding_OEM_Canadian_French', b'\x00\x8b\x03_'),
 (
  'encoding_OEM_Arabic', b'\x00\x8b\x03`'),
 (
  'encoding_OEM_Nordic', b'\x00\x8b\x03a'),
 (
  'encoding_OEM_CyrillicII', b'\x00\x8b\x03b'),
 (
  'encoding_OEM_modern_Greek', b'\x00\x8b\x03e'),
 (
  'encoding_EUC_Japanese', b'\x00\x8b\xca\xdc'),
 (
  'encoding_EUC_Chinese_simplified_Chinese', b'\x00\x8b\xca\xe0'),
 (
  'encoding_EUC_Korean', b'\x00\x8b\xca\xed'),
 (
  'encoding_EUC_Taiwanese_traditional_Chinese', b'\x00\x8b\xca\xee'),
 (
  'encoding_Devanagari', b'\x00\x8b\xde\xaa'),
 (
  'encoding_Bengali', b'\x00\x8b\xde\xab'),
 (
  'encoding_Tamil', b'\x00\x8b\xde\xac'),
 (
  'encoding_Telugu', b'\x00\x8b\xde\xad'),
 (
  'encoding_Assamese', b'\x00\x8b\xde\xae'),
 (
  'encoding_Oriya', b'\x00\x8b\xde\xaf'),
 (
  'encoding_Kannada', b'\x00\x8b\xde\xb0'),
 (
  'encoding_Malayalam', b'\x00\x8b\xde\xb1'),
 (
  'encoding_Gujarati', b'\x00\x8b\xde\xb2'),
 (
  'encoding_Punjabi', b'\x00\x8b\xde\xb3'),
 (
  'encoding_Arabic_ASMO', b'\x00\x8b\x02\xc4'),
 (
  'encoding_Arabic_transparent_ASMO', b'\x00\x8b\x02\xd0'),
 (
  'encoding_Korean_Johab', b'\x00\x8b\x05Q'),
 (
  'encoding_Taiwan_CNS', b'\x00\x8bN '),
 (
  'encoding_Taiwan_TCA', b'\x00\x8bN!'),
 (
  'encoding_Taiwan_Eten', b'\x00\x8bN"'),
 (
  'encoding_Taiwan_IBM5550', b'\x00\x8bN#'),
 (
  'encoding_Taiwan_teletext', b'\x00\x8bN$'),
 (
  'encoding_Taiwan_Wang', b'\x00\x8bN%'),
 (
  'encoding_IA5IRV', b'\x00\x8bN\x89'),
 (
  'encoding_IA5_German', b'\x00\x8bN\x8a'),
 (
  'encoding_IA5_Swedish', b'\x00\x8bN\x8b'),
 (
  'encoding_IA5_Norwegian', b'\x00\x8bN\x8c'),
 (
  'encoding_US_ASCII', b'\x00\x8bN\x9f'),
 (
  'encoding_T61', b'\x00\x8bO%'),
 (
  'encoding_ISO6937_nonspacing_accent', b'\x00\x8bO-'),
 (
  'encoding_KOI8R', b'\x00\x8bQ\x82'),
 (
  'encoding_Ext_alpha_lowercase', b'\x00\x8bR#'),
 (
  'encoding_KOI8U', b'\x00\x8bUj'),
 (
  'encoding_Europa3', b'\x00\x8bqI'),
 (
  'encoding_HZGB_simplified_Chinese', b'\x00\x8b\xce\xc8'),
 (
  'encoding_UTF7', b'\x00\x8b\xfd\xe8'),
 (
  'encoding_UTF8', b'\x00\x8b\xfd\xe9'),
 (
  'command_bar', 'msCB'),
 (
  'command_bar_control', 'mCBC'),
 (
  'built_in_chart', b'\x01\xf6\x00\x15'),
 (
  'user_defined', b'\x01\xf6\x00\x16'),
 (
  'any_gallery', b'\x01\xf6\x00\x17'),
 (
  'color_index_automatic', b'\x01\xf6\xef\xf7'),
 (
  'color_index_none', b'\x01\xf6\xef\xd2'),
 (
  'a_color_index_integer', b'\x01\xf7\x00\x00'),
 (
  'cap', b'\x01\xf8\x00\x01'),
 (
  'no_cap', b'\x01\xf8\x00\x02'),
 (
  'by_columns', b'\x01\xf9\x00\x02'),
 (
  'by_rows', b'\x01\xf9\x00\x01'),
 (
  'scale_linear', b'\x01\xf9\xef\xdc'),
 (
  'scale_logarithmic', b'\x01\xf9\xef\xdb'),
 (
  'autofill_series', b'\x01\xfb\x00\x04'),
 (
  'chronological_series', b'\x01\xfb\x00\x03'),
 (
  'growth_series', b'\x01\xfb\x00\x02'),
 (
  'data_series_linear', b'\x01\xfa\xef\xdc'),
 (
  'axis_crosses_automatic', b'\x01\xfb\xef\xf7'),
 (
  'axis_crosses_custom', b'\x01\xfb\xef\xee'),
 (
  'axis_crosses_maximum', b'\x01\xfc\x00\x02'),
 (
  'axis_crosses_minimum', b'\x01\xfc\x00\x04'),
 (
  'primary_axis', b'\x01\xfd\x00\x01'),
 (
  'secondary_axis', b'\x01\xfd\x00\x02'),
 (
  'background_automatic', b'\x01\xfd\xef\xf7'),
 (
  'background_opaque', b'\x01\xfe\x00\x03'),
 (
  'background_transparent', b'\x01\xfe\x00\x02'),
 (
  'window_state_maximized', b'\x01\xfe\xef\xd7'),
 (
  'window_state_minimized', b'\x01\xfe\xef\xd4'),
 (
  'window_state_normal', b'\x01\xfe\xef\xd1'),
 (
  'category_axis', '\x02\x00\x00\x01'),
 (
  'series_axis', '\x02\x00\x00\x03'),
 (
  'value_axis', '\x02\x00\x00\x02'),
 (
  'arrowhead_length_long', '\x02\x01\x00\x03'),
 (
  'arrowhead_length_medium', b'\x02\x00\xef\xd6'),
 (
  'arrowhead_length_short', '\x02\x01\x00\x01'),
 (
  'valign_bottom', b'\x02\x01\xef\xf5'),
 (
  'valign_center', b'\x02\x01\xef\xf4'),
 (
  'valign_distributed', b'\x02\x01\xef\xeb'),
 (
  'valign_justify', b'\x02\x01\xef\xde'),
 (
  'valign_top', b'\x02\x01\xef\xc0'),
 (
  'tick_mark_cross', '\x02\x03\x00\x04'),
 (
  'tick_mark_inside', '\x02\x03\x00\x02'),
 (
  'tick_mark_none', b'\x02\x02\xef\xd2'),
 (
  'tick_mark_outside', '\x02\x03\x00\x03'),
 (
  'error_bar_direction_x', b'\x02\x03\xef\xb8'),
 (
  'error_bar_direction_y', '\x02\x04\x00\x01'),
 (
  'error_bar_include_both', '\x02\x05\x00\x01'),
 (
  'error_bar_include_minus_values', '\x02\x05\x00\x03'),
 (
  'error_bar_include_none', b'\x02\x04\xef\xd2'),
 (
  'error_bar_include_plus_values', '\x02\x05\x00\x02'),
 (
  'interpolated', '\x02\x06\x00\x03'),
 (
  'not_plotted', '\x02\x06\x00\x01'),
 (
  'zero', '\x02\x06\x00\x02'),
 (
  'arrowhead_style_closed', '\x02\x07\x00\x03'),
 (
  'arrowhead_style_double_closed', '\x02\x07\x00\x05'),
 (
  'arrowhead_style_double_open', '\x02\x07\x00\x04'),
 (
  'arrowhead_style_none', b'\x02\x06\xef\xd2'),
 (
  'arrowhead_style_open', '\x02\x07\x00\x02'),
 (
  'arrowhead_width_medium', b'\x02\x07\xef\xd6'),
 (
  'arrowhead_width_narrow', '\x02\x08\x00\x01'),
 (
  'arrowhead_width_wide', '\x02\x08\x00\x03'),
 (
  'horizontal_align_center', b'\x02\x08\xef\xf4'),
 (
  'horizontal_align_center_across_selection', '\x02\t\x00\x07'),
 (
  'horizontal_align_distributed', b'\x02\x08\xef\xeb'),
 (
  'horizontal_align_fill', '\x02\t\x00\x05'),
 (
  'horizontal_align_general', '\x02\t\x00\x01'),
 (
  'horizontal_align_justify', b'\x02\x08\xef\xde'),
 (
  'horizontal_align_left', b'\x02\x08\xef\xdd'),
 (
  'horizontal_align_right', b'\x02\x08\xef\xc8'),
 (
  'tick_label_position_high', b'\x02\t\xef\xe1'),
 (
  'tick_label_position_low', b'\x02\t\xef\xda'),
 (
  'tick_label_position_next_to_axis', '\x02\n\x00\x04'),
 (
  'tick_label_position_none', b'\x02\t\xef\xd2'),
 (
  'legend_position_bottom', b'\x02\n\xef\xf5'),
 (
  'legend_position_corner', '\x02\x0b\x00\x02'),
 (
  'legend_position_left', b'\x02\n\xef\xdd'),
 (
  'legend_position_right', b'\x02\n\xef\xc8'),
 (
  'legend_position_top', b'\x02\n\xef\xc0'),
 (
  'chart_picture_type_stack_scale', '\x02\x0c\x00\x03'),
 (
  'chart_picture_type_stack', '\x02\x0c\x00\x02'),
 (
  'chart_picture_type_stretch', '\x02\x0c\x00\x01'),
 (
  'sides', '\x02\r\x00\x01'),
 (
  'end_', '\x02\r\x00\x02'),
 (
  'end_sides', '\x02\r\x00\x03'),
 (
  'front', '\x02\r\x00\x04'),
 (
  'front_sides', '\x02\r\x00\x05'),
 (
  'front_end', '\x02\r\x00\x06'),
 (
  'all_faces', '\x02\r\x00\x07'),
 (
  'orientation_downward', b'\x02\r\xef\xb6'),
 (
  'orientation_horizontal', b'\x02\r\xef\xe0'),
 (
  'orientation_upward', b'\x02\r\xef\xb5'),
 (
  'orientation_vertical', b'\x02\r\xef\xba'),
 (
  'tick_label_orientation_automatic', b'\x02\x0e\xef\xf7'),
 (
  'tick_label_orientation_downward', b'\x02\x0e\xef\xb6'),
 (
  'tick_label_orientation_horizontal', b'\x02\x0e\xef\xe0'),
 (
  'tick_label_orientation_upward', b'\x02\x0e\xef\xb5'),
 (
  'tick_label_orientation_vertical', b'\x02\x0e\xef\xba'),
 (
  'border_weight_hairline', '\x02\x10\x00\x01'),
 (
  'border_weight_medium', b'\x02\x0f\xef\xd6'),
 (
  'border_weight_thick', '\x02\x10\x00\x04'),
 (
  'border_weight_thin', '\x02\x10\x00\x02'),
 (
  'series_date_day', '\x02\x11\x00\x01'),
 (
  'series_date_month', '\x02\x11\x00\x03'),
 (
  'series_date_weekday', '\x02\x11\x00\x02'),
 (
  'series_date_year', '\x02\x11\x00\x04'),
 (
  'underline_style_double', b'\x02\x11\xef\xe9'),
 (
  'underline_style_double_accounting', '\x02\x12\x00\x05'),
 (
  'underline_style_none', b'\x02\x11\xef\xd2'),
 (
  'underline_style_single', '\x02\x12\x00\x02'),
 (
  'underline_style_single_accounting', '\x02\x12\x00\x04'),
 (
  'error_bar_type_custom', b'\x02\x12\xef\xee'),
 (
  'error_bar_type_fixed_value', '\x02\x13\x00\x01'),
 (
  'error_bar_type_percent', '\x02\x13\x00\x02'),
 (
  'error_bar_type_standard_deviation', b'\x02\x12\xef\xc5'),
 (
  'error_bar_type_standard_error', '\x02\x13\x00\x04'),
 (
  'exponential', '\x02\x14\x00\x05'),
 (
  'linear', b'\x02\x13\xef\xdc'),
 (
  'logarithmic', b'\x02\x13\xef\xdb'),
 (
  'moving_average', '\x02\x14\x00\x06'),
 (
  'polynomial', '\x02\x14\x00\x03'),
 (
  'power', '\x02\x14\x00\x04'),
 (
  'continuous', '\x02\x15\x00\x01'),
 (
  'dash', b'\x02\x14\xef\xed'),
 (
  'dash_dot', '\x02\x15\x00\x04'),
 (
  'dash_dot_dot', '\x02\x15\x00\x05'),
 (
  'dot', b'\x02\x14\xef\xea'),
 (
  'double', b'\x02\x14\xef\xe9'),
 (
  'slant_dash_dot', '\x02\x15\x00\r'),
 (
  'line_style_none', b'\x02\x14\xef\xd2'),
 (
  'data_labels_show_none', b'\x02\x15\xef\xd2'),
 (
  'data_labels_show_value', '\x02\x16\x00\x02'),
 (
  'data_labels_show_percent', '\x02\x16\x00\x03'),
 (
  'data_labels_show_label', '\x02\x16\x00\x04'),
 (
  'data_labels_show_label_and_percent', '\x02\x16\x00\x05'),
 (
  'data_labels_show_bubble_sizes', '\x02\x16\x00\x06'),
 (
  'marker_style_automatic', b'\x02\x16\xef\xf7'),
 (
  'marker_style_circle', '\x02\x17\x00\x08'),
 (
  'marker_style_dash', b'\x02\x16\xef\xed'),
 (
  'marker_style_diamond', '\x02\x17\x00\x02'),
 (
  'marker_style_dot', b'\x02\x16\xef\xea'),
 (
  'marker_style_none', b'\x02\x16\xef\xd2'),
 (
  'marker_style_picture', b'\x02\x16\xef\xcd'),
 (
  'marker_style_plus', '\x02\x17\x00\t'),
 (
  'marker_style_square', '\x02\x17\x00\x01'),
 (
  'marker_style_star', '\x02\x17\x00\x05'),
 (
  'marker_style_triangle', '\x02\x17\x00\x03'),
 (
  'marker_style_x', b'\x02\x16\xef\xb8'),
 (
  'pattern_automatic', b'\x02\x18\xef\xf7'),
 (
  'pattern_checker', '\x02\x19\x00\t'),
 (
  'pattern_criss_cross', '\x02\x19\x00\x10'),
 (
  'pattern_down', b'\x02\x18\xef\xe7'),
 (
  'pattern_gray_16', '\x02\x19\x00\x11'),
 (
  'pattern_gray_25', b'\x02\x18\xef\xe4'),
 (
  'pattern_gray_50', b'\x02\x18\xef\xe3'),
 (
  'pattern_gray_75', b'\x02\x18\xef\xe2'),
 (
  'pattern_gray_8', '\x02\x19\x00\x12'),
 (
  'pattern_grid', '\x02\x19\x00\x0f'),
 (
  'pattern_horizontal', b'\x02\x18\xef\xe0'),
 (
  'pattern_light_down', '\x02\x19\x00\r'),
 (
  'pattern_light_horizontal', '\x02\x19\x00\x0b'),
 (
  'pattern_light_up', '\x02\x19\x00\x0e'),
 (
  'pattern_light_vertical', '\x02\x19\x00\x0c'),
 (
  'pattern_none', b'\x02\x18\xef\xd2'),
 (
  'pattern_semi_gray_75', '\x02\x19\x00\n'),
 (
  'pattern_solid', '\x02\x19\x00\x01'),
 (
  'pattern_up', b'\x02\x18\xef\xbe'),
 (
  'pattern_vertical', b'\x02\x18\xef\xba'),
 (
  'pattern_linear_gradient', b'\x02\x19\x0f\xa0'),
 (
  'pattern_rectangular_gradient', b'\x02\x19\x0f\xa1'),
 (
  'split_by_position', '\x02\x1a\x00\x01'),
 (
  'split_by_percent_value', '\x02\x1a\x00\x03'),
 (
  'split_by_custom_split', '\x02\x1a\x00\x04'),
 (
  'split_by_value', '\x02\x1a\x00\x02'),
 (
  'hundreds', b'\x02\x1a\xff\xfe'),
 (
  'thousands', b'\x02\x1a\xff\xfd'),
 (
  'ten_thousands', b'\x02\x1a\xff\xfc'),
 (
  'hundred_thousands', b'\x02\x1a\xff\xfb'),
 (
  'millions', b'\x02\x1a\xff\xfa'),
 (
  'ten_millions', b'\x02\x1a\xff\xf9'),
 (
  'hundred_millions', b'\x02\x1a\xff\xf8'),
 (
  'thousand_millions', b'\x02\x1a\xff\xf7'),
 (
  'million_millions', b'\x02\x1a\xff\xf6'),
 (
  'custom_display_unit', b'\x02\x1a\xef\xee'),
 (
  'label_position_center', b'\x02\x1b\xef\xf4'),
 (
  'label_position_above', '\x02\x1c\x00\x00'),
 (
  'label_position_below', '\x02\x1c\x00\x01'),
 (
  'label_position_left', b'\x02\x1b\xef\xdd'),
 (
  'label_position_right', b'\x02\x1b\xef\xc8'),
 (
  'label_position_outside_end', '\x02\x1c\x00\x02'),
 (
  'label_position_inside_end', '\x02\x1c\x00\x03'),
 (
  'label_position_inside_base', '\x02\x1c\x00\x04'),
 (
  'label_position_best_fit', '\x02\x1c\x00\x05'),
 (
  'label_position_mixed', '\x02\x1c\x00\x06'),
 (
  'label_position_custom', '\x02\x1c\x00\x07'),
 (
  'days', '\x02\x1d\x00\x00'),
 (
  'months', '\x02\x1d\x00\x01'),
 (
  'years', '\x02\x1d\x00\x02'),
 (
  'category_scale', '\x02\x1e\x00\x02'),
 (
  'time_scale', '\x02\x1e\x00\x03'),
 (
  'automatic_scale', b'\x02\x1d\xef\xf7'),
 (
  'box', '\x02\x1f\x00\x00'),
 (
  'pyramid_to_point', '\x02\x1f\x00\x01'),
 (
  'pyramid_to_max', '\x02\x1f\x00\x02'),
 (
  'cylinder', '\x02\x1f\x00\x03'),
 (
  'cone_to_point', '\x02\x1f\x00\x04'),
 (
  'cone_to_max', '\x02\x1f\x00\x05'),
 (
  'column_clustered', '\x02 \x003'),
 (
  'column_stacked', '\x02 \x004'),
 (
  'column_stacked_100', '\x02 \x005'),
 (
  'ThreeD_column_clustered', '\x02 \x006'),
 (
  'ThreeD_column_stacked', '\x02 \x007'),
 (
  'ThreeD_column_stacked_100', '\x02 \x008'),
 (
  'bar_clustered', '\x02 \x009'),
 (
  'bar_stacked', '\x02 \x00:'),
 (
  'bar_stacked_100', '\x02 \x00;'),
 (
  'ThreeD_bar_clustered', '\x02 \x00<'),
 (
  'ThreeD_bar_stacked', '\x02 \x00='),
 (
  'ThreeD_bar_stacked_100', '\x02 \x00>'),
 (
  'line_stacked', '\x02 \x00?'),
 (
  'line_stacked_100', '\x02 \x00@'),
 (
  'line_markers', '\x02 \x00A'),
 (
  'line_markers_stacked', '\x02 \x00B'),
 (
  'line_markers_stacked_100', '\x02 \x00C'),
 (
  'pie_of_pie', '\x02 \x00D'),
 (
  'pie_exploded', '\x02 \x00E'),
 (
  'ThreeD_pie_exploded', '\x02 \x00F'),
 (
  'bar_of_pie', '\x02 \x00G'),
 (
  'xy_scatter_smooth', '\x02 \x00H'),
 (
  'xy_scatter_smooth_no_markers', '\x02 \x00I'),
 (
  'xy_scatter_lines', '\x02 \x00J'),
 (
  'xy_scatter_lines_no_markers', '\x02 \x00K'),
 (
  'area_stacked', '\x02 \x00L'),
 (
  'area_stacked_100', '\x02 \x00M'),
 (
  'ThreeD_area_stacked', '\x02 \x00N'),
 (
  'ThreeD_area_stacked_100', '\x02 \x00O'),
 (
  'doughnut_exploded', '\x02 \x00P'),
 (
  'radar_markers', '\x02 \x00Q'),
 (
  'radar_filled', '\x02 \x00R'),
 (
  'surface', '\x02 \x00S'),
 (
  'surface_wireframe', '\x02 \x00T'),
 (
  'surface_top_view', '\x02 \x00U'),
 (
  'surface_top_view_wireframe', '\x02 \x00V'),
 (
  'bubble', '\x02 \x00\x0f'),
 (
  'bubble_ThreeD_effect', '\x02 \x00W'),
 (
  'stock_HLC', '\x02 \x00X'),
 (
  'stock_OHLC', '\x02 \x00Y'),
 (
  'stock_VHLC', '\x02 \x00Z'),
 (
  'stock_VOHLC', '\x02 \x00['),
 (
  'cylinder_column_clustered', '\x02 \x00\\'),
 (
  'cylinder_column_stacked', '\x02 \x00]'),
 (
  'cylinder_column_stacked_100', '\x02 \x00^'),
 (
  'cylinder_bar_clustered', '\x02 \x00_'),
 (
  'cylinder_bar_stacked', '\x02 \x00`'),
 (
  'cylinder_bar_stacked_100', '\x02 \x00a'),
 (
  'cylinder_column', '\x02 \x00b'),
 (
  'cone_column_clustered', '\x02 \x00c'),
 (
  'cone_column_stacked', '\x02 \x00d'),
 (
  'cone_column_stacked_100', '\x02 \x00e'),
 (
  'cone_bar_clustered', '\x02 \x00f'),
 (
  'cone_bar_stacked', '\x02 \x00g'),
 (
  'cone_bar_stacked_100', '\x02 \x00h'),
 (
  'cone_col', '\x02 \x00i'),
 (
  'pyramid_column_clustered', '\x02 \x00j'),
 (
  'pyramid_column_stacked', '\x02 \x00k'),
 (
  'pyramid_column_stacked_100', '\x02 \x00l'),
 (
  'pyramid_bar_clustered', '\x02 \x00m'),
 (
  'pyramid_bar_stacked', '\x02 \x00n'),
 (
  'pyramid_bar_stacked_100', '\x02 \x00o'),
 (
  'pyramid_column', '\x02 \x00p'),
 (
  'ThreeD_column', b'\x02\x1f\xef\xfc'),
 (
  'line_chart', '\x02 \x00\x04'),
 (
  'ThreeD_line', b'\x02\x1f\xef\xfb'),
 (
  'ThreeD_pie', b'\x02\x1f\xef\xfa'),
 (
  'pie_chart', '\x02 \x00\x05'),
 (
  'xyscatter', b'\x02\x1f\xef\xb7'),
 (
  'ThreeD_area', b'\x02\x1f\xef\xfe'),
 (
  'area_chart', '\x02 \x00\x01'),
 (
  'doughnut', b'\x02\x1f\xef\xe8'),
 (
  'radar', b'\x02\x1f\xef\xc9'),
 (
  'combination_chart', b'\x02\x1f\xef\xf1'),
 (
  'data_label', '\x02!\x00\x00'),
 (
  'a_chart_area', '\x02!\x00\x02'),
 (
  'a_series', '\x02!\x00\x03'),
 (
  'a_chart_title', '\x02!\x00\x04'),
 (
  'walls', '\x02!\x00\x05'),
 (
  'a_corners_object', '\x02!\x00\x06'),
 (
  'data_table', '\x02!\x00\x07'),
 (
  'trendline', '\x02!\x00\x08'),
 (
  'error_bars_object', '\x02!\x00\t'),
 (
  'xerror_bars', '\x02!\x00\n'),
 (
  'yerror_bars', '\x02!\x00\x0b'),
 (
  'legend_entry', '\x02!\x00\x0c'),
 (
  'legend_key', '\x02!\x00\r'),
 (
  'shape', '\x02!\x00\x0e'),
 (
  'major_gridlines', '\x02!\x00\x0f'),
 (
  'minor_gridlines', '\x02!\x00\x10'),
 (
  'axis_title', '\x02!\x00\x11'),
 (
  'up_bars', '\x02!\x00\x12'),
 (
  'plot_area', '\x02!\x00\x13'),
 (
  'down_bars', '\x02!\x00\x14'),
 (
  'axis', '\x02!\x00\x15'),
 (
  'series_lines', '\x02!\x00\x16'),
 (
  'floor', '\x02!\x00\x17'),
 (
  'legend', '\x02!\x00\x18'),
 (
  'hi_lo_lines', '\x02!\x00\x19'),
 (
  'drop_lines', '\x02!\x00\x1a'),
 (
  'radar_axis_labels', '\x02!\x00\x1b'),
 (
  'nothing', '\x02!\x00\x1c'),
 (
  'leader_lines', '\x02!\x00\x1d'),
 (
  'display_unit_label', '\x02!\x00\x1e'),
 (
  'size_is_width', '\x02"\x00\x02'),
 (
  'size_is_area', '\x02"\x00\x01'),
 (
  'shift_down', b'\x02"\xef\xe7'),
 (
  'shift_to_right', b'\x02"\xef\xbf'),
 (
  'shift_to_left', b'\x02#\xef\xc1'),
 (
  'shift_up', b'\x02#\xef\xbe'),
 (
  'toward_the_bottom', b'\x02$\xef\xe7'),
 (
  'toward_the_left', b'\x02$\xef\xc1'),
 (
  'toward_the_right', b'\x02$\xef\xbf'),
 (
  'toward_the_top', b'\x02$\xef\xbe'),
 (
  'do_average', b'\x02%\xef\xf6'),
 (
  'do_count', b'\x02%\xef\xf0'),
 (
  'do_count_numbers', b'\x02%\xef\xef'),
 (
  'do_maximum', b'\x02%\xef\xd8'),
 (
  'do_minimum', b'\x02%\xef\xd5'),
 (
  'do_product', b'\x02%\xef\xcb'),
 (
  'do_standard_deviation', b'\x02%\xef\xc5'),
 (
  'do_standard_deviation_p', b'\x02%\xef\xc4'),
 (
  'do_sum', b'\x02%\xef\xc3'),
 (
  'do_var', b'\x02%\xef\xbc'),
 (
  'do_var_p', b'\x02%\xef\xbb'),
 (
  'sheet_type_chart', b'\x02&\xef\xf3'),
 (
  'sheet_type_dialog_sheet', b'\x02&\xef\xec'),
 (
  'sheet_type_excel_4_intl_macro_sheet', "\x02'\x00\x04"),
 (
  'sheet_type_excel_4_macro_sheet', "\x02'\x00\x03"),
 (
  'sheet_type_worksheet', b'\x02&\xef\xb9'),
 (
  'column_header', b"\x02'\xef\xf2"),
 (
  'column_item', '\x02(\x00\x05'),
 (
  'data_header', '\x02(\x00\x03'),
 (
  'data_item', '\x02(\x00\x07'),
 (
  'page_header', '\x02(\x00\x02'),
 (
  'page_item', '\x02(\x00\x06'),
 (
  'row_header', b"\x02'\xef\xc7"),
 (
  'row_item', '\x02(\x00\x04'),
 (
  'table_body', '\x02(\x00\x08'),
 (
  'formulas', b'\x02(\xef\xe5'),
 (
  'comments', b'\x02(\xef\xd0'),
 (
  'values', b'\x02(\xef\xbd'),
 (
  'window_type_chart_as_window', '\x02*\x00\x05'),
 (
  'window_type_chart_in_place', '\x02*\x00\x04'),
 (
  'window_type_clipboard', '\x02*\x00\x03'),
 (
  'window_type_info', b'\x02)\xef\xdf'),
 (
  'window_type_workbook', '\x02*\x00\x01'),
 (
  'pivot_field_type_date', '\x02+\x00\x02'),
 (
  'pivot_field_type_number', b'\x02*\xef\xcf'),
 (
  'pivot_field_type_text', b'\x02*\xef\xc2'),
 (
  'bitmap', '\x02,\x00\x02'),
 (
  'picture', b'\x02+\xef\xcd'),
 (
  'consolidation', '\x02-\x00\x03'),
 (
  'database', '\x02-\x00\x01'),
 (
  'external', '\x02-\x00\x02'),
 (
  'pivot_table', b'\x02,\xef\xcc'),
 (
  'A1', '\x02.\x00\x01'),
 (
  'R1C1', b'\x02-\xef\xca'),
 (
  'Microsoft_Access', '\x02/\x00\x04'),
 (
  'Microsoft_Fox_Pro', '\x02/\x00\x05'),
 (
  'Microsoft_Mail', '\x02/\x00\x03'),
 (
  'Microsoft_PowerPoint', '\x02/\x00\x02'),
 (
  'Microsoft_Project', '\x02/\x00\x06'),
 (
  'Microsoft_Schedule_Plus', '\x02/\x00\x07'),
 (
  'Microsoft_Word', '\x02/\x00\x01'),
 (
  'no_button', '\x020\x00\x00'),
 (
  'primary_button', '\x020\x00\x01'),
 (
  'secondary_button', '\x020\x00\x02'),
 (
  'copy_mode', '\x021\x00\x01'),
 (
  'cut_mode', '\x021\x00\x02'),
 (
  'filter_copy', '\x023\x00\x02'),
 (
  'filter_in_place', '\x023\x00\x01'),
 (
  'down_then_over', '\x024\x00\x01'),
 (
  'over_then_down', '\x024\x00\x02'),
 (
  'link_type_Excel_links', '\x025\x00\x01'),
 (
  'link_type_OLE_links', '\x025\x00\x02'),
 (
  'column_then_row', '\x026\x00\x02'),
 (
  'row_then_column', '\x026\x00\x01'),
 (
  'cancel_key_disabled', '\x027\x00\x00'),
 (
  'error_handler', '\x027\x00\x02'),
 (
  'interrupt', '\x027\x00\x01'),
 (
  'page_break_automatic', b'\x027\xef\xf7'),
 (
  'page_break_manual', b'\x027\xef\xd9'),
 (
  'page_break_none', '\x028\x00\x00'),
 (
  'landscape', '\x02:\x00\x02'),
 (
  'portrait', '\x02:\x00\x01'),
 (
  'edition_date', '\x02;\x00\x02'),
 (
  'update_state', '\x02;\x00\x01'),
 (
  'command_underlines_automatic', b'\x02;\xef\xf7'),
 (
  'command_underlines_off', b'\x02;\xef\xce'),
 (
  'command_underlines_on', '\x02<\x00\x01'),
 (
  'verb_open', '\x02=\x00\x02'),
 (
  'verb_primary', '\x02=\x00\x01'),
 (
  'calculation_automatic', b'\x02=\xef\xf7'),
 (
  'calculation_manual', b'\x02=\xef\xd9'),
 (
  'calculation_semiautomatic', '\x02>\x00\x02'),
 (
  'workbook_read_only', '\x02?\x00\x03'),
 (
  'workbook_read_write', '\x02?\x00\x02'),
 (
  'fit_to_page', '\x02@\x00\x02'),
 (
  'full_page', '\x02@\x00\x03'),
 (
  'full_screen', '\x02@\x00\x01'),
 (
  'part', '\x02A\x00\x02'),
 (
  'whole', '\x02A\x00\x01'),
 (
  'MAPI', '\x02B\x00\x01'),
 (
  'no_mail_system', '\x02B\x00\x00'),
 (
  'power_talk', '\x02B\x00\x02'),
 (
  'link_info_olelinks', '\x02C\x00\x02'),
 (
  'link_info_publishers', '\x02C\x00\x05'),
 (
  'link_info_subscribers', '\x02C\x00\x06'),
 (
  'cell_type_blanks', '\x02F\x00\x04'),
 (
  'cell_type_constants', '\x02F\x00\x02'),
 (
  'cell_type_formulas', b'\x02E\xef\xe5'),
 (
  'cell_type_last_cell', '\x02F\x00\x0b'),
 (
  'cell_type_comments', b'\x02E\xef\xd0'),
 (
  'cell_type_visible', '\x02F\x00\x0c'),
 (
  'cell_type_all_format_conditions', b'\x02E\xef\xb4'),
 (
  'cell_type_same_format_conditions', b'\x02E\xef\xb3'),
 (
  'cell_type_all_validation', b'\x02E\xef\xb2'),
 (
  'cell_type_same_validation', b'\x02E\xef\xb1'),
 (
  'arrange_style_cascade', '\x02G\x00\x07'),
 (
  'arrange_style_horizontal', b'\x02F\xef\xe0'),
 (
  'arrange_style_tiled', '\x02G\x00\x01'),
 (
  'arrange_style_vertical', b'\x02F\xef\xba'),
 (
  'I_beam_cursor', '\x02H\x00\x03'),
 (
  'default_cursor', b'\x02G\xef\xd1'),
 (
  'northwest_arrow_cursor', '\x02H\x00\x01'),
 (
  'wait_cursor', '\x02H\x00\x02'),
 (
  'fill_copy', '\x02I\x00\x01'),
 (
  'fill_days', '\x02I\x00\x05'),
 (
  'fill_default', '\x02I\x00\x00'),
 (
  'fill_formats', '\x02I\x00\x03'),
 (
  'fill_months', '\x02I\x00\x07'),
 (
  'fill_series', '\x02I\x00\x02'),
 (
  'fill_values', '\x02I\x00\x04'),
 (
  'fill_weekdays', '\x02I\x00\x06'),
 (
  'fill_years', '\x02I\x00\x08'),
 (
  'growth_trend', '\x02I\x00\n'),
 (
  'linear_trend', '\x02I\x00\t'),
 (
  'autofilter_and', '\x02J\x00\x01'),
 (
  'bottom_10_items', '\x02J\x00\x04'),
 (
  'bottom_10_percent', '\x02J\x00\x06'),
 (
  'autofilter_or', '\x02J\x00\x02'),
 (
  'top_10_items', '\x02J\x00\x03'),
 (
  'top_10_percent', '\x02J\x00\x05'),
 (
  'filter_by_value', '\x02J\x00\x07'),
 (
  'filter_by_cell_color', '\x02J\x00\x08'),
 (
  'filter_by_font_color', '\x02J\x00\t'),
 (
  'filter_by_icon', '\x02J\x00\n'),
 (
  'filter_dynamic', '\x02J\x00\x0b'),
 (
  'filter_no_fill', '\x02J\x00\x0c'),
 (
  'filter_by_automatic_font_color', '\x02J\x00\r'),
 (
  'filter_by_no_icon', '\x02J\x00\x0e'),
 (
  'clipboard_format_biff', '\x02K\x00\x08'),
 (
  'clipboard_format_biff_2', '\x02K\x00\x12'),
 (
  'clipboard_format_biff_3', '\x02K\x00\x14'),
 (
  'clipboard_format_biff_4', '\x02K\x00\x1e'),
 (
  'clipboard_format_binary', '\x02K\x00\x0f'),
 (
  'clipboard_format_bitmap', '\x02K\x00\t'),
 (
  'clipboard_format_cgm', '\x02K\x00\r'),
 (
  'clipboard_format_csv', '\x02K\x00\x05'),
 (
  'clipboard_format_dif', '\x02K\x00\x04'),
 (
  'clipboard_format_dsp_text', '\x02K\x00\x0c'),
 (
  'clipboard_format_embedded_object', '\x02K\x00\x15'),
 (
  'clipboard_format_embed_source', '\x02K\x00\x16'),
 (
  'clipboard_format_link', '\x02K\x00\x0b'),
 (
  'clipboard_format_link_source', '\x02K\x00\x17'),
 (
  'clipboard_format_link_source_desc', '\x02K\x00 '),
 (
  'clipboard_format_movie', '\x02K\x00\x18'),
 (
  'clipboard_format_native', '\x02K\x00\x0e'),
 (
  'clipboard_format_object_desc', '\x02K\x00\x1f'),
 (
  'clipboard_format_object_link', '\x02K\x00\x13'),
 (
  'clipboard_format_owner_link', '\x02K\x00\x11'),
 (
  'clipboard_format_pict', '\x02K\x00\x02'),
 (
  'clipboard_format_print_pict', '\x02K\x00\x03'),
 (
  'clipboard_format_rtf', '\x02K\x00\x07'),
 (
  'clipboard_format_screen_pict', '\x02K\x00\x1d'),
 (
  'clipboard_format_standard_font', '\x02K\x00\x1c'),
 (
  'clipboard_format_standard_scale', '\x02K\x00\x1b'),
 (
  'clipboard_format_sylk', '\x02K\x00\x06'),
 (
  'clipboard_format_table', '\x02K\x00\x10'),
 (
  'clipboard_format_text', '\x02K\x00\x00'),
 (
  'clipboard_format_tool_face', '\x02K\x00\x19'),
 (
  'clipboard_format_tool_face_pict', '\x02K\x00\x1a'),
 (
  'clipboard_format_valu', '\x02K\x00\x01'),
 (
  'clipboard_format_wk_1', '\x02K\x00\n'),
 (
  'clipboard_format_unicode_text', '\x02K\x00.'),
 (
  'clipboard_format_style_text', '\x02K\x005'),
 (
  'clipboard_format_unicode_style_text', '\x02K\x007'),
 (
  'clipboard_format_biff_5', '\x02K\x00!'),
 (
  'clipboard_format_picture_build', '\x02K\x00"'),
 (
  'clipboard_format_odbc_conn', '\x02K\x00#'),
 (
  'clipboard_format_odbc_sql', '\x02K\x00$'),
 (
  'clipboard_format_3d_picture', '\x02K\x00%'),
 (
  'clipboard_format_unexpected_38', '\x02K\x00&'),
 (
  'clipboard_format_drawing_drag_drop', "\x02K\x00'"),
 (
  'clipboard_format_drawing', '\x02K\x00('),
 (
  'clipboard_format_unexpected_41', '\x02K\x00)'),
 (
  'clipboard_format_unexpected_42', '\x02K\x00*'),
 (
  'clipboard_format_unexpected_43', '\x02K\x00+'),
 (
  'clipboard_format_hyperlink', '\x02K\x00,'),
 (
  'clipboard_format_unexpected_45', '\x02K\x00-'),
 (
  'clipboard_format_windows_bitmap', '\x02K\x00/'),
 (
  'clipboard_format_uniform_resource_locator', '\x02K\x000'),
 (
  'clipboard_format_file_name', '\x02K\x001'),
 (
  'clipboard_format_unexpected_50', '\x02K\x002'),
 (
  'clipboard_format_unexpected_51', '\x02K\x003'),
 (
  'clipboard_format_hypertext_markup_language', '\x02K\x004'),
 (
  'clipboard_format_office_scrapbook_info', '\x02K\x006'),
 (
  'clipboard_format_portable_document_format', '\x02K\x008'),
 (
  'clipboard_format_excel_internal_shape', '\x02K\x009'),
 (
  'clipboard_format_office_art_shape', '\x02K\x00:'),
 (
  'CSV_file_format', b'\x02\xbc\x00\x06'),
 (
  'CSV_Mac_file_format', b'\x02\xbc\x00\x16'),
 (
  'CSV_MSDos_file_format', b'\x02\xbc\x00\x18'),
 (
  'CSV_Windows_file_format', b'\x02\xbc\x00\x17'),
 (
  'DBF3_file_format', b'\x02\xbc\x00\x08'),
 (
  'DBF4_file_format', b'\x02\xbc\x00\x0b'),
 (
  'DIF_file_format', b'\x02\xbc\x00\t'),
 (
  'Excel2_file_format', b'\x02\xbc\x00\x10'),
 (
  'Excel_2_east_asian_file_format', b'\x02\xbc\x00\x1b'),
 (
  'Excel3_file_format', b'\x02\xbc\x00\x1d'),
 (
  'Excel4_file_format', b'\x02\xbc\x00!'),
 (
  'Excel5_file_format', b"\x02\xbc\x00'"),
 (
  'Excel7_file_format', b"\x02\xbc\x00'"),
 (
  'Excel_4_workbook_file_format', b'\x02\xbc\x00#'),
 (
  'international_add_in_file_format', b'\x02\xbc\x00\x1a'),
 (
  'international_macro_file_format', b'\x02\xbc\x00\x19'),
 (
  'workbook_normal_file_format', b'\x02\xbb\xef\xd1'),
 (
  'SYLK_file_format', b'\x02\xbc\x00\x02'),
 (
  'current_platform_text_file_format', b'\x02\xbb\xef\xc2'),
 (
  'text_Mac_file_format', b'\x02\xbc\x00\x13'),
 (
  'text_MSDos_file_format', b'\x02\xbc\x00\x15'),
 (
  'text_printer_file_format', b'\x02\xbc\x00$'),
 (
  'text_windows_file_format', b'\x02\xbc\x00\x14'),
 (
  'HTML_file_format', b'\x02\xbc\x00,'),
 (
  'XML_spreadsheet_file_format', b'\x02\xbc\x00-'),
 (
  'PDF_file_format', b'\x02\xbc\x00.'),
 (
  'Excel_binary_file_format', b'\x02\xbc\x003'),
 (
  'Excel_XML_file_format', b'\x02\xbc\x004'),
 (
  'macro_enabled_XML_file_format', b'\x02\xbc\x005'),
 (
  'macro_enabled_template_file_format', b'\x02\xbc\x006'),
 (
  'template_file_format', b'\x02\xbc\x007'),
 (
  'add_in_file_format', b'\x02\xbc\x008'),
 (
  'Excel98to2004_file_format', b'\x02\xbc\x009'),
 (
  'Excel98to2004_template_file_format', b'\x02\xbc\x00\x11'),
 (
  'Excel98to2004_add_in_file_format', b'\x02\xbc\x00\x12'),
 (
  'twenty_four_hour_clock', '\x02M\x00!'),
 (
  'four_digit_years', '\x02M\x00+'),
 (
  'alternate_array_separator', '\x02M\x00\x10'),
 (
  'column_separator', '\x02M\x00\x0e'),
 (
  'country_code', '\x02M\x00\x01'),
 (
  'country_setting', '\x02M\x00\x02'),
 (
  'currency_before', '\x02M\x00%'),
 (
  'currency_code', '\x02M\x00\x19'),
 (
  'currency_digits', '\x02M\x00\x1b'),
 (
  'currency_leading_zeros', '\x02M\x00('),
 (
  'currency_minus_sign', '\x02M\x00&'),
 (
  'currency_negative', '\x02M\x00\x1c'),
 (
  'currency_space_before', '\x02M\x00$'),
 (
  'currency_trailing_zeros', "\x02M\x00'"),
 (
  'date_order', '\x02M\x00 '),
 (
  'date_separator', '\x02M\x00\x11'),
 (
  'day_code', '\x02M\x00\x15'),
 (
  'day_leading_zero', '\x02M\x00*'),
 (
  'decimal_separator', '\x02M\x00\x03'),
 (
  'general_format_name', '\x02M\x00\x1a'),
 (
  'hour_code', '\x02M\x00\x16'),
 (
  'left_brace', '\x02M\x00\x0c'),
 (
  'left_bracket', '\x02M\x00\n'),
 (
  'list_separator', '\x02M\x00\x05'),
 (
  'lower_case_column_letter', '\x02M\x00\t'),
 (
  'lower_case_row_letter', '\x02M\x00\x08'),
 (
  'mdy', '\x02M\x00,'),
 (
  'metric', '\x02M\x00#'),
 (
  'minute_code', '\x02M\x00\x17'),
 (
  'month_code', '\x02M\x00\x14'),
 (
  'month_leading_zero', '\x02M\x00)'),
 (
  'month_name_chars', '\x02M\x00\x1e'),
 (
  'noncurrency_digits', '\x02M\x00\x1d'),
 (
  'non_english_functions', '\x02M\x00"'),
 (
  'right_brace', '\x02M\x00\r'),
 (
  'right_bracket', '\x02M\x00\x0b'),
 (
  'row_separator', '\x02M\x00\x0f'),
 (
  'second_code', '\x02M\x00\x18'),
 (
  'thousands_separator', '\x02M\x00\x04'),
 (
  'time_leading_zero', '\x02M\x00-'),
 (
  'time_separator', '\x02M\x00\x12'),
 (
  'upper_case_column_letter', '\x02M\x00\x07'),
 (
  'upper_case_row_letter', '\x02M\x00\x06'),
 (
  'weekday_name_chars', '\x02M\x00\x1f'),
 (
  'year_code', '\x02M\x00\x13'),
 (
  'page_break_full', '\x02N\x00\x01'),
 (
  'page_break_partial', '\x02N\x00\x02'),
 (
  'overwrite_cells', '\x02O\x00\x00'),
 (
  'insert_delete_cells', '\x02O\x00\x01'),
 (
  'insert_entire_rows', '\x02O\x00\x02'),
 (
  'no_labels', b'\x02O\xef\xd2'),
 (
  'row_labels', '\x02P\x00\x01'),
 (
  'column_labels', '\x02P\x00\x02'),
 (
  'mixed_labels', '\x02P\x00\x03'),
 (
  'since_my_last_save', '\x02Q\x00\x01'),
 (
  'all_changes', '\x02Q\x00\x02'),
 (
  'not_yet_reviewed', '\x02Q\x00\x03'),
 (
  'no_indicator', '\x02R\x00\x00'),
 (
  'comment_indicator_only', b'\x02Q\xff\xff'),
 (
  'comment_and_indicator', '\x02R\x00\x01'),
 (
  'cell_value', '\x02S\x00\x01'),
 (
  'expression', '\x02S\x00\x02'),
 (
  'color_scale', '\x02S\x00\x03'),
 (
  'databar', '\x02S\x00\x04'),
 (
  'top_10', '\x02S\x00\x05'),
 (
  'icon_sets', '\x02S\x00\x06'),
 (
  'unique_values', '\x02S\x00\x07'),
 (
  'text_string', '\x02S\x00\t'),
 (
  'blanks_condition', '\x02S\x00\n'),
 (
  'time_period', '\x02S\x00\x0b'),
 (
  'above_average_condition', '\x02S\x00\x0c'),
 (
  'no_blanks_condition', '\x02S\x00\r'),
 (
  'errors_condition', '\x02S\x00\x10'),
 (
  'no_errors_condition', '\x02S\x00\x11'),
 (
  'operator_between', '\x02T\x00\x01'),
 (
  'operator_not_between', '\x02T\x00\x02'),
 (
  'operator_equal', '\x02T\x00\x03'),
 (
  'operator_not_equal', '\x02T\x00\x04'),
 (
  'operator_greater', '\x02T\x00\x05'),
 (
  'operator_less', '\x02T\x00\x06'),
 (
  'operator_greater_equal', '\x02T\x00\x07'),
 (
  'operator_less_equal', '\x02T\x00\x08'),
 (
  'no_restrictions', '\x02U\x00\x00'),
 (
  'unlocked_cells', '\x02U\x00\x01'),
 (
  'no_selection', b'\x02T\xef\xd2'),
 (
  'validate_input_only', '\x02V\x00\x00'),
 (
  'validate_whole_number', '\x02V\x00\x01'),
 (
  'validate_decimal', '\x02V\x00\x02'),
 (
  'validate_list', '\x02V\x00\x03'),
 (
  'validated_date', '\x02V\x00\x04'),
 (
  'validate_time', '\x02V\x00\x05'),
 (
  'validate_text_length', '\x02V\x00\x06'),
 (
  'validate_custom', '\x02V\x00\x07'),
 (
  'IME_mode_no_control', '\x02W\x00\x00'),
 (
  'IME_mode_on', '\x02W\x00\x01'),
 (
  'IME_mode_off', '\x02W\x00\x02'),
 (
  'IME_mode_disable', '\x02W\x00\x03'),
 (
  'IME_mode_hiragana', '\x02W\x00\x04'),
 (
  'IME_mode_katakana', '\x02W\x00\x05'),
 (
  'IME_mode_katakana_half', '\x02W\x00\x06'),
 (
  'IME_mode_alpha_full', '\x02W\x00\x07'),
 (
  'IME_mode_alpha', '\x02W\x00\x08'),
 (
  'IME_mode_hangul_full', '\x02W\x00\t'),
 (
  'IME_mode_hangul', '\x02W\x00\n'),
 (
  'valid_alert_none', b'\x02W\xff\xff'),
 (
  'valid_alert_stop', '\x02X\x00\x01'),
 (
  'valid_alert_warning', '\x02X\x00\x02'),
 (
  'valid_alert_information', '\x02X\x00\x03'),
 (
  'location_as_new_sheet', '\x02Y\x00\x01'),
 (
  'location_as_object', '\x02Y\x00\x02'),
 (
  'location_automatic', '\x02Y\x00\x03'),
 (
  'automatic', b'\x02Y\xef\xf7'),
 (
  'custom', b'\x02Y\xef\xee'),
 (
  'pivot_table_version_2000', b'\x03\x84\x00\x00'),
 (
  'pivot_table_version_10', b'\x03\x84\x00\x01'),
 (
  'pivot_table_version_11', b'\x03\x84\x00\x02'),
 (
  'pivot_table_version_12', b'\x03\x84\x00\x03'),
 (
  'pivot_table_version_14', b'\x03\x84\x00\x04'),
 (
  'pivot_table_version_current', b'\x03\x83\xff\xff'),
 (
  'compact_row', b'\x03\x85\x00\x00'),
 (
  'tabular_row', b'\x03\x85\x00\x01'),
 (
  'outline_row', b'\x03\x85\x00\x02'),
 (
  'at_top', b'\x03\x86\x00\x01'),
 (
  'at_bottom', b'\x03\x86\x00\x02'),
 (
  'manual_allocation', b'\x03\x87\x00\x01'),
 (
  'automatic_allocation', b'\x03\x87\x00\x02'),
 (
  'allocate_value', b'\x03\x88\x00\x01'),
 (
  'allocate_increment', b'\x03\x88\x00\x02'),
 (
  'equal_allocation', b'\x03\x89\x00\x01'),
 (
  'weight_allocation', b'\x03\x89\x00\x02'),
 (
  'do_not_repeat_labels', b'\x03\x8a\x00\x01'),
 (
  'repeat_labels', b'\x03\x8a\x00\x02'),
 (
  'missing_items_default', b'\x03\x8a\xff\xff'),
 (
  'missing_items_none', b'\x03\x8b\x00\x00'),
 (
  'missing_items_max', b'\x03\x8b~\xf4'),
 (
  'missing_items_max2', b'\x03\x9b\x00\x00'),
 (
  'pivot_cell_value', b'\x03\x8c\x00\x00'),
 (
  'pivot_cell_pivot_item', b'\x03\x8c\x00\x01'),
 (
  'pivot_cell_subtotal', b'\x03\x8c\x00\x02'),
 (
  'pivot_cell_grand_total', b'\x03\x8c\x00\x03'),
 (
  'pivot_cell_data_field', b'\x03\x8c\x00\x04'),
 (
  'pivot_cell_pivot_field', b'\x03\x8c\x00\x05'),
 (
  'pivot_cell_page_field_item', b'\x03\x8c\x00\x06'),
 (
  'pivot_cell_custom_subtotal', b'\x03\x8c\x00\x07'),
 (
  'pivot_cell_data_pivot_field', b'\x03\x8c\x00\x08'),
 (
  'pivot_cell_blank_cell', b'\x03\x8c\x00\t'),
 (
  'cell_not_changed', b'\x03\x8d\x00\x01'),
 (
  'cell_changed', b'\x03\x8d\x00\x02'),
 (
  'cell_change_applied', b'\x03\x8d\x00\x03'),
 (
  'tabular', b'\x03\x8e\x00\x00'),
 (
  'outline', b'\x03\x8e\x00\x01'),
 (
  'pivot_top_count', b'\x03\x8f\x00\x01'),
 (
  'pivot_bottom_count', b'\x03\x8f\x00\x02'),
 (
  'pivot_top_percent', b'\x03\x8f\x00\x03'),
 (
  'pivot_bottom_percent', b'\x03\x8f\x00\x04'),
 (
  'pivot_top_sum', b'\x03\x8f\x00\x05'),
 (
  'pivot_bottom_sum', b'\x03\x8f\x00\x06'),
 (
  'pivot_value_equals', b'\x03\x8f\x00\x07'),
 (
  'pivot_value_is_not_equal', b'\x03\x8f\x00\x08'),
 (
  'pivot_value_is_greater_than', b'\x03\x8f\x00\t'),
 (
  'pivot_value_is_greater_than_or_equal_to', b'\x03\x8f\x00\n'),
 (
  'pivot_value_is_less_than', b'\x03\x8f\x00\x0b'),
 (
  'pivot_value_is_less_than_or_equal_to', b'\x03\x8f\x00\x0c'),
 (
  'pivot_value_is_between', b'\x03\x8f\x00\r'),
 (
  'pivot_value_is_not_between', b'\x03\x8f\x00\x0e'),
 (
  'pivot_caption_equals', b'\x03\x8f\x00\x0f'),
 (
  'pivot_caption_does_not_equal', b'\x03\x8f\x00\x10'),
 (
  'pivot_caption_begins_with', b'\x03\x8f\x00\x11'),
 (
  'pivot_caption_does_not_begin_with', b'\x03\x8f\x00\x12'),
 (
  'pivot_caption_ends_with', b'\x03\x8f\x00\x13'),
 (
  'pivot_caption_does_not_end_with', b'\x03\x8f\x00\x14'),
 (
  'pivot_caption_contains', b'\x03\x8f\x00\x15'),
 (
  'pivot_caption_does_not_contain', b'\x03\x8f\x00\x16'),
 (
  'pivot_caption_is_greater_than', b'\x03\x8f\x00\x17'),
 (
  'pivot_caption_is_greater_than_or_equal_to', b'\x03\x8f\x00\x18'),
 (
  'pivot_caption_is_less_than', b'\x03\x8f\x00\x19'),
 (
  'pivot_caption_is_less_than_or_equal_to', b'\x03\x8f\x00\x1a'),
 (
  'pivot_caption_is_between', b'\x03\x8f\x00\x1b'),
 (
  'pivot_caption_is_now_between', b'\x03\x8f\x00\x1c'),
 (
  'pivot_specific_date', b'\x03\x8f\x00\x1d'),
 (
  'pivot_not_specific_date', b'\x03\x8f\x00\x1e'),
 (
  'pivot_before', b'\x03\x8f\x00\x1f'),
 (
  'pivot_before_or_equal_to', b'\x03\x8f\x00 '),
 (
  'pivot_after', b'\x03\x8f\x00!'),
 (
  'pivot_after_or_equal_to', b'\x03\x8f\x00"'),
 (
  'pivot_between', b'\x03\x8f\x00#'),
 (
  'pivot_not_between', b'\x03\x8f\x00$'),
 (
  'pivot_tomorrow', b'\x03\x8f\x00%'),
 (
  'pivot_today', b'\x03\x8f\x00&'),
 (
  'pivot_yesterday', b"\x03\x8f\x00'"),
 (
  'pivot_next_week', b'\x03\x8f\x00('),
 (
  'pivot_this_week', b'\x03\x8f\x00)'),
 (
  'pivot_last_week', b'\x03\x8f\x00*'),
 (
  'pivot_next_month', b'\x03\x8f\x00+'),
 (
  'pivot_this_month', b'\x03\x8f\x00,'),
 (
  'pivot_last_month', b'\x03\x8f\x00-'),
 (
  'pivot_next_quarter', b'\x03\x8f\x00.'),
 (
  'pivot_this_quarter', b'\x03\x8f\x00/'),
 (
  'pivot_last_quarter', b'\x03\x8f\x000'),
 (
  'pivot_next_year', b'\x03\x8f\x001'),
 (
  'pivot_this_year', b'\x03\x8f\x002'),
 (
  'pivot_last_year', b'\x03\x8f\x003'),
 (
  'pivot_year_to_date', b'\x03\x8f\x004'),
 (
  'pivot_all_dates_in_period_quarter1', b'\x03\x8f\x005'),
 (
  'pivot_all_dates_in_period_quarter2', b'\x03\x8f\x006'),
 (
  'pivot_all_dates_in_period_quarter3', b'\x03\x8f\x007'),
 (
  'pivot_all_dates_in_period_quarter4', b'\x03\x8f\x008'),
 (
  'pivot_all_dates_in_period_January', b'\x03\x8f\x009'),
 (
  'pivot_all_dates_in_period_Feberary', b'\x03\x8f\x00:'),
 (
  'pivot_all_dates_in_period_March', b'\x03\x8f\x00;'),
 (
  'pivot_all_dates_in_period_April', b'\x03\x8f\x00<'),
 (
  'pivot_all_dates_in_period_May', b'\x03\x8f\x00='),
 (
  'pivot_all_dates_in_period_June', b'\x03\x8f\x00>'),
 (
  'pivot_all_dates_in_period_July', b'\x03\x8f\x00?'),
 (
  'pivot_all_dates_in_period_August', b'\x03\x8f\x00@'),
 (
  'pivot_all_dates_in_period_September', b'\x03\x8f\x00A'),
 (
  'pivot_all_dates_in_period_October', b'\x03\x8f\x00B'),
 (
  'pivot_all_dates_in_period_November', b'\x03\x8f\x00C'),
 (
  'pivot_all_dates_in_period_December', b'\x03\x8f\x00D'),
 (
  'pivot_line_regular', b'\x03\x90\x00\x00'),
 (
  'pivot_line_subtotal', b'\x03\x90\x00\x01'),
 (
  'pivot_line_grandtotal', b'\x03\x90\x00\x02'),
 (
  'pivot_line_blank', b'\x03\x90\x00\x03'),
 (
  'hierarchy', b'\x03\x91\x00\x01'),
 (
  'measure', b'\x03\x91\x00\x02'),
 (
  'set', b'\x03\x91\x00\x03'),
 (
  'cube_hierarchy', b'\x03\x92\x00\x01'),
 (
  'cube_measure', b'\x03\x92\x00\x02'),
 (
  'cube_set', b'\x03\x92\x00\x03'),
 (
  'cube_attribute', b'\x03\x92\x00\x04'),
 (
  'cube_calculated_measure', b'\x03\x92\x00\x05'),
 (
  'cube_KPI_value', b'\x03\x92\x00\x06'),
 (
  'cube_KPI_goal', b'\x03\x92\x00\x07'),
 (
  'cube_KPI_status', b'\x03\x92\x00\x08'),
 (
  'cube_KPI_trend', b'\x03\x92\x00\t'),
 (
  'cube_KPI_weight', b'\x03\x92\x00\n'),
 (
  'display_property_in_pivot_table', b'\x03\x93\x00\x01'),
 (
  'display_property_in_tooltip', b'\x03\x93\x00\x02'),
 (
  'display_property_in_pivot_table_and_tooltip', b'\x03\x93\x00\x03'),
 (
  'calculated_member', b'\x03\x94\x00\x00'),
 (
  'calculated_set', b'\x03\x94\x00\x01'),
 (
  'connection_type_OLEDB', b'\x03\x95\x00\x01'),
 (
  'connection_type_ODBC', b'\x03\x95\x00\x02'),
 (
  'connection_type_XMLMAP', b'\x03\x95\x00\x03'),
 (
  'connection_type_TEXT', b'\x03\x95\x00\x04'),
 (
  'connection_type_WEB', b'\x03\x95\x00\x05'),
 (
  'paste_special_operation_add', '\x02[\x00\x02'),
 (
  'paste_special_operation_divide', '\x02[\x00\x05'),
 (
  'paste_special_operation_multiply', '\x02[\x00\x04'),
 (
  'paste_special_operation_none', b'\x02Z\xef\xd2'),
 (
  'paste_special_operation_subtract', '\x02[\x00\x03'),
 (
  'paste_all', b'\x02[\xef\xf8'),
 (
  'paste_all_using_source_theme', '\x02\\\x00\r'),
 (
  'paste_all_except_borders', '\x02\\\x00\x07'),
 (
  'paste_formats', b'\x02[\xef\xe6'),
 (
  'paste_formulas', b'\x02[\xef\xe5'),
 (
  'paste_comments', b'\x02[\xef\xd0'),
 (
  'paste_values', b'\x02[\xef\xbd'),
 (
  'paste_column_widths', '\x02\\\x00\x08'),
 (
  'paste_validation', '\x02\\\x00\x06'),
 (
  'paste_formulas_and_number_formats', '\x02\\\x00\x0b'),
 (
  'paste_values_and_number_formats', '\x02\\\x00\x0c'),
 (
  'phonetic_character_half_width_katakana', '\x02]\x00\x00'),
 (
  'phonetic_character_full_width_katakana', '\x02]\x00\x01'),
 (
  'phonetic_character_hiragana', '\x02]\x00\x02'),
 (
  'no_phonetic_character_conversion', '\x02]\x00\x03'),
 (
  'phonetic_align_no_control', '\x02^\x00\x00'),
 (
  'phonetic_align_left', '\x02^\x00\x01'),
 (
  'phonetic_align_center', '\x02^\x00\x02'),
 (
  'phonetic_align_distributed', '\x02^\x00\x03'),
 (
  'printer', '\x02_\x00\x02'),
 (
  'screen', '\x02_\x00\x01'),
 (
  'orient_as_column_field', '\x02`\x00\x02'),
 (
  'orient_as_data_field', '\x02`\x00\x04'),
 (
  'orient_as_hidden', '\x02`\x00\x00'),
 (
  'orient_as_page_field', '\x02`\x00\x03'),
 (
  'orient_as_row_field', '\x02`\x00\x01'),
 (
  'pivot_field_calculation_difference_from', '\x02a\x00\x02'),
 (
  'pivot_field_calculation_index', '\x02a\x00\t'),
 (
  'pivot_field_calculation_no_additional_calculation', b'\x02`\xef\xd1'),
 (
  'pivot_field_calculation_percent_difference_from', '\x02a\x00\x04'),
 (
  'pivot_field_calculation_percent_of', '\x02a\x00\x03'),
 (
  'pivot_field_calculation_percent_of_column', '\x02a\x00\x07'),
 (
  'pivot_field_calculation_percent_of_row', '\x02a\x00\x06'),
 (
  'pivot_field_calculation_percent_of_total', '\x02a\x00\x08'),
 (
  'pivot_field_calculation_running_total', '\x02a\x00\x05'),
 (
  'placement_free_floating', '\x02b\x00\x03'),
 (
  'placement_move', '\x02b\x00\x02'),
 (
  'placement_move_and_size', '\x02b\x00\x01'),
 (
  'Macintosh', '\x02c\x00\x01'),
 (
  'MSDos', '\x02c\x00\x03'),
 (
  'MSWindows', '\x02c\x00\x02'),
 (
  'print_sheet_end', '\x02d\x00\x01'),
 (
  'print_in_place', '\x02d\x00\x10'),
 (
  'print_no_comments', b'\x02c\xef\xd2'),
 (
  'priority_high', b'\x02d\xef\xe1'),
 (
  'priority_low', b'\x02d\xef\xda'),
 (
  'priority_normal', b'\x02d\xef\xd1'),
 (
  'selection_mode_label_only', '\x02f\x00\x01'),
 (
  'selection_mode_data_and_label', '\x02f\x00\x00'),
 (
  'selection_mode_data_only', '\x02f\x00\x02'),
 (
  'selection_mode_origin', '\x02f\x00\x03'),
 (
  'selection_mode_button', '\x02f\x00\x0f'),
 (
  'selection_mode_blanks', '\x02f\x00\x04'),
 (
  'range_autoformat_threeD_effects_1', '\x02g\x00\r'),
 (
  'range_autoformat_threeD_effects_2', '\x02g\x00\x0e'),
 (
  'range_autoformat_accounting_1', '\x02g\x00\x04'),
 (
  'range_autoformat_accounting_2', '\x02g\x00\x05'),
 (
  'range_autoformat_accounting_3', '\x02g\x00\x06'),
 (
  'range_autoformat_accounting_4', '\x02g\x00\x11'),
 (
  'range_autoformat_classic_1', '\x02g\x00\x01'),
 (
  'range_autoformat_classic_2', '\x02g\x00\x02'),
 (
  'range_autoformat_classic_3', '\x02g\x00\x03'),
 (
  'range_autoformat_color_1', '\x02g\x00\x07'),
 (
  'range_autoformat_color_2', '\x02g\x00\x08'),
 (
  'range_autoformat_color_3', '\x02g\x00\t'),
 (
  'range_autoformat_list_1', '\x02g\x00\n'),
 (
  'range_autoformat_list_2', '\x02g\x00\x0b'),
 (
  'range_autoformat_list_3', '\x02g\x00\x0c'),
 (
  'range_autoformat_local_format_1', '\x02g\x00\x0f'),
 (
  'range_autoformat_local_format_2', '\x02g\x00\x10'),
 (
  'range_autoformat_local_format_3', '\x02g\x00\x13'),
 (
  'range_autoformat_local_format_4', '\x02g\x00\x14'),
 (
  'range_autoformat_none', b'\x02f\xef\xd2'),
 (
  'range_autoformat_simple', b'\x02f\xef\xc6'),
 (
  'all_at_once', '\x02i\x00\x02'),
 (
  'one_after_another', '\x02i\x00\x01'),
 (
  'not_yet_routed', '\x02j\x00\x00'),
 (
  'routing_complete', '\x02j\x00\x02'),
 (
  'routing_in_progress', '\x02j\x00\x01'),
 (
  'auto_activate', '\x02k\x00\x03'),
 (
  'auto_close', '\x02k\x00\x02'),
 (
  'auto_deactivate', '\x02k\x00\x04'),
 (
  'auto_open', '\x02k\x00\x01'),
 (
  'exclusive', '\x02m\x00\x03'),
 (
  'no_change', '\x02m\x00\x01'),
 (
  'shared', '\x02m\x00\x02'),
 (
  'local_session_changes', '\x02n\x00\x02'),
 (
  'other_session_changes', '\x02n\x00\x03'),
 (
  'user_resolution', '\x02n\x00\x01'),
 (
  'search_next', '\x02o\x00\x01'),
 (
  'search_previous', '\x02o\x00\x02'),
 (
  'by_columns', '\x02p\x00\x02'),
 (
  'by_rows', '\x02p\x00\x01'),
 (
  'sheet_visible', b'\x02p\xff\xff'),
 (
  'sheet_hidden', '\x02q\x00\x00'),
 (
  'sheet_very_hidden', '\x02q\x00\x02'),
 (
  'pin_yin', '\x02r\x00\x01'),
 (
  'stroke', '\x02r\x00\x02'),
 (
  'sort_ascending', '\x02t\x00\x01'),
 (
  'sort_descending', '\x02t\x00\x02'),
 (
  'sort_manual', b'\x02s\xef\xd9'),
 (
  'sort_rows', '\x02u\x00\x02'),
 (
  'sort_columns', '\x02u\x00\x01'),
 (
  'sort_labels', '\x02v\x00\x02'),
 (
  'sort_values', '\x02v\x00\x01'),
 (
  'errors', '\x02w\x00\x10'),
 (
  'logical', '\x02w\x00\x04'),
 (
  'numbers', '\x02w\x00\x01'),
 (
  'text_values', '\x02w\x00\x02'),
 (
  'summary_above', '\x02x\x00\x00'),
 (
  'summary_below', '\x02x\x00\x01'),
 (
  'summary_on_left', b'\x02x\xef\xdd'),
 (
  'summary_on_right', b'\x02x\xef\xc8'),
 (
  'summary_pivot_table', b'\x02y\xef\xcc'),
 (
  'standard_summary', '\x02z\x00\x01'),
 (
  'delimited', '\x02|\x00\x01'),
 (
  'fixed_width', '\x02|\x00\x02'),
 (
  'text_qualifier_double_quote', '\x02}\x00\x01'),
 (
  'text_qualifier_none', b'\x02|\xef\xd2'),
 (
  'text_qualifier_single_quote', '\x02}\x00\x02'),
 (
  'chart', b'\x02}\xef\xf3'),
 (
  'Excel_4_intl_macro_sheet', '\x02~\x00\x04'),
 (
  'Excel_4_macro_sheet', '\x02~\x00\x03'),
 (
  'worksheet', b'\x02}\xef\xb9'),
 (
  'normal_view', '\x02\x7f\x00\x01'),
 (
  'page_layout_view', '\x02\x7f\x00\x03'),
 (
  'macro_type_command', b'\x02\x80\x00\x02'),
 (
  'macro_type_function', b'\x02\x80\x00\x01'),
 (
  'macro_type_not_XLM', b'\x02\x80\x00\x03'),
 (
  'header_guess', b'\x02\x81\x00\x00'),
 (
  'header_no', b'\x02\x81\x00\x02'),
 (
  'header_yes', b'\x02\x81\x00\x01'),
 (
  'display_shapes', b'\x02\x81\xef\xf8'),
 (
  'hide', b'\x02\x82\x00\x03'),
 (
  'placeholders', b'\x02\x82\x00\x02'),
 (
  'inside_horizontal', b'\x02\x83\x00\x0c'),
 (
  'inside_vertical', b'\x02\x83\x00\x0b'),
 (
  'diagonal_down', b'\x02\x83\x00\x05'),
 (
  'diagonal_up', b'\x02\x83\x00\x06'),
 (
  'edge_bottom', b'\x02\x83\x00\t'),
 (
  'edge_left', b'\x02\x83\x00\x07'),
 (
  'edge_right', b'\x02\x83\x00\n'),
 (
  'edge_top', b'\x02\x83\x00\x08'),
 (
  'border_bottom', b'\x02\x82\xef\xf5'),
 (
  'border_left', b'\x02\x82\xef\xdd'),
 (
  'border_right', b'\x02\x82\xef\xc8'),
 (
  'border_top', b'\x02\x82\xef\xc0'),
 (
  'no_button_changes', b'\x02\x84\x00\x01'),
 (
  'no_changes', b'\x02\x84\x00\x04'),
 (
  'no_docking_changes', b'\x02\x84\x00\x03'),
 (
  'toolbar_protection_none', b'\x02\x83\xef\xd1'),
 (
  'no_shape_changes', b'\x02\x84\x00\x02'),
 (
  'dialog_open', b'\x02\x85\x00\x01'),
 (
  'dialog_open_links', b'\x02\x85\x00\x02'),
 (
  'dialog_save_as', b'\x02\x85\x00\x05'),
 (
  'dialog_file_delete', b'\x02\x85\x00\x06'),
 (
  'dialog_page_setup', b'\x02\x85\x00\x07'),
 (
  'dialog_print', b'\x02\x85\x00\x08'),
 (
  'dialog_printer_setup', b'\x02\x85\x00\t'),
 (
  'dialog_arrange_all', b'\x02\x85\x00\x0c'),
 (
  'dialog_window_size', b'\x02\x85\x00\r'),
 (
  'dialog_window_move', b'\x02\x85\x00\x0e'),
 (
  'dialog_run', b'\x02\x85\x00\x11'),
 (
  'dialog_set_print_titles', b'\x02\x85\x00\x17'),
 (
  'dialog_font', b'\x02\x85\x00\x1a'),
 (
  'dialog_display', b'\x02\x85\x00\x1b'),
 (
  'dialog_protect_document', b'\x02\x85\x00\x1c'),
 (
  'dialog_calculation', b'\x02\x85\x00 '),
 (
  'dialog_extract', b'\x02\x85\x00#'),
 (
  'dialog_data_delete', b'\x02\x85\x00$'),
 (
  'dialog_sort', b"\x02\x85\x00'"),
 (
  'dialog_data_series', b'\x02\x85\x00('),
 (
  'dialog_table', b'\x02\x85\x00)'),
 (
  'dialog_format_number', b'\x02\x85\x00*'),
 (
  'dialog_alignment', b'\x02\x85\x00+'),
 (
  'dialog_style', b'\x02\x85\x00,'),
 (
  'dialog_border', b'\x02\x85\x00-'),
 (
  'dialog_cell_protection', b'\x02\x85\x00.'),
 (
  'dialog_column_width', b'\x02\x85\x00/'),
 (
  'dialog_clear', b'\x02\x85\x004'),
 (
  'dialog_paste_special', b'\x02\x85\x005'),
 (
  'dialog_edit_delete', b'\x02\x85\x006'),
 (
  'dialog_insert', b'\x02\x85\x007'),
 (
  'dialog_paste_names', b'\x02\x85\x00:'),
 (
  'dialog_define_name', b'\x02\x85\x00='),
 (
  'dialog_create_names', b'\x02\x85\x00>'),
 (
  'dialog_formula_goto', b'\x02\x85\x00?'),
 (
  'dialog_formula_find', b'\x02\x85\x00@'),
 (
  'dialog_gallery_area', b'\x02\x85\x00C'),
 (
  'dialog_gallery_bar', b'\x02\x85\x00D'),
 (
  'dialog_gallery_column', b'\x02\x85\x00E'),
 (
  'dialog_gallery_line', b'\x02\x85\x00F'),
 (
  'dialog_gallery_pie', b'\x02\x85\x00G'),
 (
  'dialog_gallery_scatter', b'\x02\x85\x00H'),
 (
  'dialog_combination', b'\x02\x85\x00I'),
 (
  'dialog_gridlines', b'\x02\x85\x00L'),
 (
  'dialog_axes', b'\x02\x85\x00N'),
 (
  'dialog_attach_text', b'\x02\x85\x00P'),
 (
  'dialog_patterns', b'\x02\x85\x00T'),
 (
  'dialog_main_chart', b'\x02\x85\x00U'),
 (
  'dialog_overlay', b'\x02\x85\x00V'),
 (
  'dialog_scale', b'\x02\x85\x00W'),
 (
  'dialog_format_legend', b'\x02\x85\x00X'),
 (
  'dialog_format_text', b'\x02\x85\x00Y'),
 (
  'dialog_parse', b'\x02\x85\x00['),
 (
  'dialog_unhide', b'\x02\x85\x00^'),
 (
  'dialog_workspace', b'\x02\x85\x00_'),
 (
  'dialog_activate', b'\x02\x85\x00g'),
 (
  'dialog_copy_picture', b'\x02\x85\x00l'),
 (
  'dialog_delete_name', b'\x02\x85\x00n'),
 (
  'dialog_delete_format', b'\x02\x85\x00o'),
 (
  'dialog_new', b'\x02\x85\x00w'),
 (
  'dialog_row_height', b'\x02\x85\x00\x7f'),
 (
  'dialog_format_move', b'\x02\x85\x00\x80'),
 (
  'dialog_format_size', b'\x02\x85\x00\x81'),
 (
  'dialog_formula_replace', b'\x02\x85\x00\x82'),
 (
  'dialog_select_special', b'\x02\x85\x00\x84'),
 (
  'dialog_apply_names', b'\x02\x85\x00\x85'),
 (
  'dialog_replace_font', b'\x02\x85\x00\x86'),
 (
  'dialog_split', b'\x02\x85\x00\x89'),
 (
  'dialog_outline', b'\x02\x85\x00\x8e'),
 (
  'dialog_save_workbook', b'\x02\x85\x00\x91'),
 (
  'dialog_copy_chart', b'\x02\x85\x00\x93'),
 (
  'dialog_format_font', b'\x02\x85\x00\x96'),
 (
  'dialog_note', b'\x02\x85\x00\x9a'),
 (
  'dialog_set_update_status', b'\x02\x85\x00\x9f'),
 (
  'dialog_color_palette', b'\x02\x85\x00\xa1'),
 (
  'dialog_change_link', b'\x02\x85\x00\xa6'),
 (
  'dialog_app_move', b'\x02\x85\x00\xaa'),
 (
  'dialog_app_size', b'\x02\x85\x00\xab'),
 (
  'dialog_main_chart_type', b'\x02\x85\x00\xb9'),
 (
  'dialog_overlay_chart_type', b'\x02\x85\x00\xba'),
 (
  'dialog_open_mail', b'\x02\x85\x00\xbc'),
 (
  'dialog_send_mail', b'\x02\x85\x00\xbd'),
 (
  'dialog_standard_font', b'\x02\x85\x00\xbe'),
 (
  'dialog_consolidate', b'\x02\x85\x00\xbf'),
 (
  'dialog_sort_special', b'\x02\x85\x00\xc0'),
 (
  'dialog_gallery_threeD_area', b'\x02\x85\x00\xc1'),
 (
  'dialog_gallery_threeD_column', b'\x02\x85\x00\xc2'),
 (
  'dialog_gallery_threeD_line', b'\x02\x85\x00\xc3'),
 (
  'dialog_gallery_threeD_pie', b'\x02\x85\x00\xc4'),
 (
  'dialog_view_threeD', b'\x02\x85\x00\xc5'),
 (
  'dialog_goal_seek', b'\x02\x85\x00\xc6'),
 (
  'dialog_workgroup', b'\x02\x85\x00\xc7'),
 (
  'dialog_fill_group', b'\x02\x85\x00\xc8'),
 (
  'dialog_update_link', b'\x02\x85\x00\xc9'),
 (
  'dialog_promote', b'\x02\x85\x00\xca'),
 (
  'dialog_demote', b'\x02\x85\x00\xcb'),
 (
  'dialog_show_detail', b'\x02\x85\x00\xcc'),
 (
  'dialog_object_properties', b'\x02\x85\x00\xcf'),
 (
  'dialog_save_new_object', b'\x02\x85\x00\xd0'),
 (
  'dialog_apply_style', b'\x02\x85\x00\xd4'),
 (
  'dialog_assign_to_object', b'\x02\x85\x00\xd5'),
 (
  'dialog_object_protection', b'\x02\x85\x00\xd6'),
 (
  'dialog_show_toolbar', b'\x02\x85\x00\xdc'),
 (
  'dialog_print_preview', b'\x02\x85\x00\xde'),
 (
  'dialog_edit_color', b'\x02\x85\x00\xdf'),
 (
  'dialog_format_main', b'\x02\x85\x00\xe1'),
 (
  'dialog_format_overlay', b'\x02\x85\x00\xe2'),
 (
  'dialog_edit_series', b'\x02\x85\x00\xe4'),
 (
  'dialog_define_style', b'\x02\x85\x00\xe5'),
 (
  'dialog_gallery_radar', b'\x02\x85\x00\xf9'),
 (
  'dialog_zoom', b'\x02\x85\x01\x00'),
 (
  'dialog_insert_object', b'\x02\x85\x01\x03'),
 (
  'dialog_size', b'\x02\x85\x01\x05'),
 (
  'dialog_move', b'\x02\x85\x01\x06'),
 (
  'dialog_format_auto', b'\x02\x85\x01\r'),
 (
  'dialog_gallery_threeD_bar', b'\x02\x85\x01\x10'),
 (
  'dialog_gallery_threeD_surface', b'\x02\x85\x01\x11'),
 (
  'dialog_customize_toolbar', b'\x02\x85\x01\x14'),
 (
  'dialog_workbook_add', b'\x02\x85\x01\x19'),
 (
  'dialog_workbook_move', b'\x02\x85\x01\x1a'),
 (
  'dialog_workbook_copy', b'\x02\x85\x01\x1b'),
 (
  'dialog_workbook_options', b'\x02\x85\x01\x1c'),
 (
  'dialog_save_workspace', b'\x02\x85\x01\x1d'),
 (
  'dialog_chart_wizard', b'\x02\x85\x01 '),
 (
  'dialog_assign_to_tool', b'\x02\x85\x01%'),
 (
  'dialog_placement', b'\x02\x85\x01,'),
 (
  'dialog_fill_workgroup', b'\x02\x85\x01-'),
 (
  'dialog_workbook_new', b'\x02\x85\x01.'),
 (
  'dialog_scenario_cells', b'\x02\x85\x011'),
 (
  'dialog_scenario_add', b'\x02\x85\x013'),
 (
  'dialog_scenario_edit', b'\x02\x85\x014'),
 (
  'dialog_scenario_summary', b'\x02\x85\x017'),
 (
  'dialog_pivot_table_wizard', b'\x02\x85\x018'),
 (
  'dialog_pivot_field_properties', b'\x02\x85\x019'),
 (
  'dialog_options_calculation', b'\x02\x85\x01>'),
 (
  'dialog_options_edit', b'\x02\x85\x01?'),
 (
  'dialog_options_view', b'\x02\x85\x01@'),
 (
  'dialog_add_in_manager', b'\x02\x85\x01A'),
 (
  'dialog_menu_editor', b'\x02\x85\x01B'),
 (
  'dialog_attach_toolbars', b'\x02\x85\x01C'),
 (
  'dialog_options_chart', b'\x02\x85\x01E'),
 (
  'dialog_vba_insert_file', b'\x02\x85\x01H'),
 (
  'dialog_vba_procedure_definition', b'\x02\x85\x01J'),
 (
  'dialog_routing_slip', b'\x02\x85\x01P'),
 (
  'dialog_mail_logon', b'\x02\x85\x01S'),
 (
  'dialog_insert_picture', b'\x02\x85\x01V'),
 (
  'dialog_gallery_doughnut', b'\x02\x85\x01X'),
 (
  'dialog_chart_trend', b'\x02\x85\x01^'),
 (
  'dialog_workbook_insert', b'\x02\x85\x01b'),
 (
  'dialog_options_transition', b'\x02\x85\x01c'),
 (
  'dialog_options_general', b'\x02\x85\x01d'),
 (
  'dialog_filter_advanced', b'\x02\x85\x01r'),
 (
  'dialog_mail_next_letter', b'\x02\x85\x01z'),
 (
  'dialog_data_label', b'\x02\x85\x01{'),
 (
  'dialog_insert_title', b'\x02\x85\x01|'),
 (
  'dialog_font_properties', b'\x02\x85\x01}'),
 (
  'dialog_macro_options', b'\x02\x85\x01~'),
 (
  'dialog_workbook_unhide', b'\x02\x85\x01\x80'),
 (
  'dialog_workbook_name', b'\x02\x85\x01\x82'),
 (
  'dialog_gallery_custom', b'\x02\x85\x01\x84'),
 (
  'dialog_add_chart_autoformat', b'\x02\x85\x01\x86'),
 (
  'dialog_chart_add_data', b'\x02\x85\x01\x88'),
 (
  'dialog_tab_order', b'\x02\x85\x01\x8a'),
 (
  'dialog_subtotal_create', b'\x02\x85\x01\x8e'),
 (
  'dialog_workbook_tab_split', b'\x02\x85\x01\x9f'),
 (
  'dialog_workbook_protect', b'\x02\x85\x01\xa1'),
 (
  'dialog_scrollbar_properties', b'\x02\x85\x01\xa4'),
 (
  'dialog_pivot_show_pages', b'\x02\x85\x01\xa5'),
 (
  'dialog_text_to_columns', b'\x02\x85\x01\xa6'),
 (
  'dialog_format_charttype', b'\x02\x85\x01\xa7'),
 (
  'dialog_pivot_field_group', b'\x02\x85\x01\xb1'),
 (
  'dialog_pivot_field_ungroup', b'\x02\x85\x01\xb2'),
 (
  'dialog_checkbox_properties', b'\x02\x85\x01\xb3'),
 (
  'dialog_label_properties', b'\x02\x85\x01\xb4'),
 (
  'dialog_listbox_properties', b'\x02\x85\x01\xb5'),
 (
  'dialog_editbox_properties', b'\x02\x85\x01\xb6'),
 (
  'dialog_open_text', b'\x02\x85\x01\xb9'),
 (
  'dialog_pushbutton_properties', b'\x02\x85\x01\xbd'),
 (
  'dialog_filter', b'\x02\x85\x01\xbf'),
 (
  'dialog_function_wizard', b'\x02\x85\x01\xc2'),
 (
  'dialog_save_copy_as', b'\x02\x85\x01\xc8'),
 (
  'dialog_options_lists_add', b'\x02\x85\x01\xca'),
 (
  'dialog_series_axes', b'\x02\x85\x01\xcc'),
 (
  'dialog_series_x', b'\x02\x85\x01\xcd'),
 (
  'dialog_series_y', b'\x02\x85\x01\xce'),
 (
  'dialog_errorbar_x', b'\x02\x85\x01\xcf'),
 (
  'dialog_errorbar_y', b'\x02\x85\x01\xd0'),
 (
  'dialog_format_chart', b'\x02\x85\x01\xd1'),
 (
  'dialog_series_order', b'\x02\x85\x01\xd2'),
 (
  'dialog_mail_edit_mailer', b'\x02\x85\x01\xd6'),
 (
  'dialog_standard_width', b'\x02\x85\x01\xd8'),
 (
  'dialog_scenario_merge', b'\x02\x85\x01\xd9'),
 (
  'dialog_properties', b'\x02\x85\x01\xda'),
 (
  'dialog_summary_info', b'\x02\x85\x01\xda'),
 (
  'dialog_find_file', b'\x02\x85\x01\xdb'),
 (
  'dialog_active_cell_font', b'\x02\x85\x01\xdc'),
 (
  'dialog_vba_make_add_in', b'\x02\x85\x01\xde'),
 (
  'dialog_file_sharing', b'\x02\x85\x01\xe1'),
 (
  'dialog_autocorrect', b'\x02\x85\x01\xe5'),
 (
  'dialog_custom_views', b'\x02\x85\x01\xed'),
 (
  'dialog_insert_name_label', b'\x02\x85\x01\xf0'),
 (
  'dialog_series_shape', b'\x02\x85\x01\xf8'),
 (
  'dialog_chart_options_data_labels', b'\x02\x85\x01\xf9'),
 (
  'dialog_chart_options_data_table', b'\x02\x85\x01\xfa'),
 (
  'dialog_set_background_picture', b'\x02\x85\x01\xfd'),
 (
  'dialog_data_validation', b'\x02\x85\x02\r'),
 (
  'dialog_chart_type', b'\x02\x85\x02\x0e'),
 (
  'dialog_chart_location', b'\x02\x85\x02\x0f'),
 (
  'dialog_chart_source_data', b'\x02\x85\x02\x1d'),
 (
  'dialog_series_options', b'\x02\x85\x02-'),
 (
  'dialog_pivot_table_options', b'\x02\x85\x027'),
 (
  'dialog_pivot_solve_order', b'\x02\x85\x028'),
 (
  'dialog_pivot_calculated_field', b'\x02\x85\x02:'),
 (
  'dialog_pivot_calculated_item', b'\x02\x85\x02<'),
 (
  'dialog_conditional_formatting', b'\x02\x85\x02G'),
 (
  'dialog_insert_hyperlink', b'\x02\x85\x02T'),
 (
  'dialog_protect_sharing', b'\x02\x85\x02l'),
 (
  'dialog_phonetic', b'\x02\x85\x02\x8b'),
 (
  'dialog_import_text_file', b'\x02\x85\x02\x9a'),
 (
  'dialog_web_options_general', b'\x02\x85\x02\xb4'),
 (
  'dialog_web_options_pictures', b'\x02\x85\x02\xb6'),
 (
  'dialog_web_options_files', b'\x02\x85\x02\xb5'),
 (
  'dialog_web_options_fonts', b'\x02\x85\x02\xb8'),
 (
  'dialog_web_options_encoding', b'\x02\x85\x02\xb7'),
 (
  'prompt', b'\x02\x86\x00\x00'),
 (
  'constant', b'\x02\x86\x00\x01'),
 (
  'range', b'\x02\x86\x00\x02'),
 (
  'param_type_unknown', b'\x02\x87\x00\x00'),
 (
  'param_type_char', b'\x02\x87\x00\x01'),
 (
  'param_type_numeric', b'\x02\x87\x00\x02'),
 (
  'param_type_decimal', b'\x02\x87\x00\x03'),
 (
  'param_type_number', b'\x02\x87\x00\x04'),
 (
  'param_type_small_int', b'\x02\x87\x00\x05'),
 (
  'param_type_float', b'\x02\x87\x00\x06'),
 (
  'param_type_real', b'\x02\x87\x00\x07'),
 (
  'param_type_double', b'\x02\x87\x00\x08'),
 (
  'param_type_var_char', b'\x02\x87\x00\x0c'),
 (
  'param_type_date', b'\x02\x87\x00\t'),
 (
  'param_type_time', b'\x02\x87\x00\n'),
 (
  'param_type_timestamp', b'\x02\x87\x00\x0b'),
 (
  'param_type_long_var_char', b'\x02\x86\xff\xff'),
 (
  'param_type_binary', b'\x02\x86\xff\xfe'),
 (
  'param_type_var_binary', b'\x02\x86\xff\xfd'),
 (
  'param_type_long_var_binary', b'\x02\x86\xff\xfc'),
 (
  'param_type_big_int', b'\x02\x86\xff\xfb'),
 (
  'param_type_tiny_int', b'\x02\x86\xff\xfa'),
 (
  'param_type_bit', b'\x02\x86\xff\xf9'),
 (
  'button_control', b'\x02\x88\x00\x00'),
 (
  'check_box', b'\x02\x88\x00\x01'),
 (
  'drop_down', b'\x02\x88\x00\x02'),
 (
  'edit_box', b'\x02\x88\x00\x03'),
 (
  'group_box', b'\x02\x88\x00\x04'),
 (
  'label', b'\x02\x88\x00\x05'),
 (
  'list_box', b'\x02\x88\x00\x06'),
 (
  'option_button', b'\x02\x88\x00\x07'),
 (
  'scroll_bar', b'\x02\x88\x00\x08'),
 (
  'spinner', b'\x02\x88\x00\t'),
 (
  'general_format', b'\x02\x89\x00\x01'),
 (
  'text_format', b'\x02\x89\x00\x02'),
 (
  'MDY_format', b'\x02\x89\x00\x03'),
 (
  'DMY_format', b'\x02\x89\x00\x04'),
 (
  'YMD_format', b'\x02\x89\x00\x05'),
 (
  'MYD_format', b'\x02\x89\x00\x06'),
 (
  'DYM_format', b'\x02\x89\x00\x07'),
 (
  'YDM_format', b'\x02\x89\x00\x08'),
 (
  'skip_column', b'\x02\x89\x00\t'),
 (
  'ODBC_query', b'\x02\x8a\x00\x01'),
 (
  'DAO_record_set', b'\x02\x8a\x00\x02'),
 (
  'web_query', b'\x02\x8a\x00\x04'),
 (
  'OLE_DB_query', b'\x02\x8a\x00\x05'),
 (
  'text_import', b'\x02\x8a\x00\x06'),
 (
  'ADO_recordset', b'\x02\x8a\x00\x07'),
 (
  'FileMaker_query', b'\x02\x8a\x00\x08'),
 (
  'cmd_cube', b'\x02\x8b\x00\x01'),
 (
  'cmd_sql', b'\x02\x8b\x00\x02'),
 (
  'cmd_table', b'\x02\x8b\x00\x03'),
 (
  'cmd_default', b'\x02\x8b\x00\x04'),
 (
  'cmd_list', b'\x02\x8b\x00\x05'),
 (
  'src_none', b'\x02\x8d\x00\x01'),
 (
  'src_range', b'\x02\x8d\x00\x02'),
 (
  'src_external', b'\x02\x8d\x00\x03'),
 (
  'criteria_equals', b'\x02\x91\x00\x00'),
 (
  'criteria_less_than_or_equal_to', b'\x02\x91\x00\x01'),
 (
  'criteria_greater_than_or_equal_to', b'\x02\x91\x00\x02'),
 (
  'criteria_less_than', b'\x02\x91\x00\x03'),
 (
  'criteria_greater_than', b'\x02\x91\x00\x04'),
 (
  'criteria_begins_with', b'\x02\x91\x00\x05'),
 (
  'criteria_ends_with', b'\x02\x91\x00\x06'),
 (
  'criteria_contains', b'\x02\x91\x00\x07'),
 (
  'no_condition', b'\x02\x92\x00\x00'),
 (
  'and_condition', b'\x02\x92\x00\x01'),
 (
  'or_condition', b'\x02\x92\x00\x02'),
 (
  'range_value_default', b'\x02\x93\x00\n'),
 (
  'range_value_XML_spreadsheet', b'\x02\x93\x00\x0b'),
 (
  'range_value_MS_persist_XML', b'\x02\x93\x00\x0c'),
 (
  'inches', b'\x02\x94\x00\x01'),
 (
  'centimeters', b'\x02\x94\x00\x02'),
 (
  'millimeters', b'\x02\x94\x00\x03'),
 (
  'subtotal_automatic', b'\x02\x95\x00\x01'),
 (
  'subtotal_sum', b'\x02\x95\x00\x02'),
 (
  'subtotal_count', b'\x02\x95\x00\x03'),
 (
  'subtotal_average', b'\x02\x95\x00\x04'),
 (
  'subtotal_max', b'\x02\x95\x00\x05'),
 (
  'subtotal_min', b'\x02\x95\x00\x06'),
 (
  'subtotal_product', b'\x02\x95\x00\x07'),
 (
  'subtotal_count_numbers', b'\x02\x95\x00\x08'),
 (
  'subtotal_standard_deviation', b'\x02\x95\x00\t'),
 (
  'subtotal_standard_deviation_p', b'\x02\x95\x00\n'),
 (
  'subtotal_variable', b'\x02\x95\x00\x0b'),
 (
  'subtotal_variable_p', b'\x02\x95\x00\x0c'),
 (
  'data_entry_on', b'\x02\x96\x00\x01'),
 (
  'data_entry_strict', b'\x02\x96\x00\x02'),
 (
  'data_entry_off', b'\x02\x95\xef\xce'),
 (
  'status_text', b'\x02\x96\xff\xff'),
 (
  'a_Boolean', b'\x02\x97\x00\x00'),
 (
  'excel_menus', b'\x02\x98\x00\x01'),
 (
  'left_to_right', b'\x02\x98\xecu'),
 (
  'right_to_left', b'\x02\x98\xect'),
 (
  'context', b'\x02\x98\xecv'),
 (
  'normal_cursor', b'\x02\x9a\x00\x00'),
 (
  'logical_cursor', b'\x02\x9a\x00\x01'),
 (
  'visual_cursor', b'\x02\x9a\x00\x02'),
 (
  'range_object', b'\x02\x9b\x00\x01'),
 (
  'A1_style_range_reference', b'\x02\x9b\x00\x02'),
 (
  'named_range', b'\x02\x9b\x00\x03'),
 (
  'automatic_subtotal', b'\x02\x9c\x00\x01'),
 (
  'sum_subtotal', b'\x02\x9c\x00\x02'),
 (
  'count_subtotal', b'\x02\x9c\x00\x03'),
 (
  'average_subtotal', b'\x02\x9c\x00\x04'),
 (
  'maximum_value', b'\x02\x9c\x00\x05'),
 (
  'minimum_value', b'\x02\x9c\x00\x06'),
 (
  'product_subtotal', b'\x02\x9c\x00\x07'),
 (
  'count_numbers_subtotal', b'\x02\x9c\x00\x08'),
 (
  'standard_deviation', b'\x02\x9c\x00\t'),
 (
  'standard_deviation_P', b'\x02\x9c\x00\n'),
 (
  'variance_subtotal', b'\x02\x9c\x00\x0b'),
 (
  'variance_P_subtotal', b'\x02\x9c\x00\x0c'),
 (
  'type_automatic', b'\x02\x9c\xef\xf7'),
 (
  'type_manual', b'\x02\x9c\xef\xd9'),
 (
  'position_top', b'\x02\x9d\xef\xc0'),
 (
  'position_bottom', b'\x02\x9d\xef\xf5'),
 (
  'scroll_tab_position_first', b'\x02\x9f\x00\x00'),
 (
  'scroll_tab_position_last', b'\x02\x9f\x00\x01'),
 (
  'range', b'\x02\xa0\x00\x00'),
 (
  'a_list_of_ranges', b'\x02\xa0\x00\x01'),
 (
  'report_name', b'\x02\xa0\x00\x02'),
 (
  'a_list_of_string_that_is_a_SQL_query', b'\x02\xa0\x00\x03'),
 (
  'built_in_chart_template', b'\x02\xa1\x00\x01'),
 (
  'format_name', b'\x02\xa1\x00\x02'),
 (
  'built_in_chart_type', b'\x02\xa2\x00\x15'),
 (
  'custom_chart', b'\x02\xa1\xef\xee'),
 (
  'range_object', b'\x02\xa3\x00\x01'),
 (
  'A1_style_range_reference', b'\x02\xa3\x00\x02'),
 (
  'named_range', b'\x02\xa3\x00\x03'),
 (
  'list_of_strings', b'\x02\xa3\x00\x04'),
 (
  'range_object', b'\x02\xa4\x00\x01'),
 (
  'A1_style_range_reference', b'\x02\xa4\x00\x02'),
 (
  'named_range', b'\x02\xa4\x00\x03'),
 (
  'input_default_as_string', b'\x02\xa4\x00\x04'),
 (
  'a_number', b'\x02\xa5\x00\x01'),
 (
  'input_type_as_string', b'\x02\xa5\x00\x02'),
 (
  'a_number_or_a_string', b'\x02\xa5\x00\x03'),
 (
  'a_bool', b'\x02\xa5\x00\x04'),
 (
  'range_object', b'\x02\xa5\x00\x08'),
 (
  'list_of_numbers', b'\x02\xa5\x00A'),
 (
  'list_of_strings', b'\x02\xa5\x00B'),
 (
  'list_of_number_or_string', b'\x02\xa5\x00C'),
 (
  'list_of_bools', b'\x02\xa5\x00D'),
 (
  'list_of_range_objects', b'\x02\xa5\x00H'),
 (
  'a_number', b'\x02\xa6\x00\x01'),
 (
  'a_bool', b'\x02\xa6\x00\x04'),
 (
  'range_object', b'\x02\xa7\x00\x01'),
 (
  'A1_style_range_reference', b'\x02\xa7\x00\x02'),
 (
  'named_range', b'\x02\xa7\x00\x03'),
 (
  'list_of_strings', b'\x02\xa7\x00\x04'),
 (
  'percentable', b'\x02\xa8\x00\x01'),
 (
  'a_bool', b'\x02\xa8\x00\x04'),
 (
  'script', b'\x02\xa9\x00\x01'),
 (
  'script_Text', b'\x02\xa9\x00\x02'),
 (
  'application', b'\x02\xaa\x00\x01'),
 (
  'worksheet', b'\x02\xaa\x00\x02'),
 (
  'A1_style_range_reference', b'\x02\xaa\x00\x03'),
 (
  'horizontal_aligment_bottom', b'\x02\xaa\xef\xf5'),
 (
  'horizontal_aligment_left', b'\x02\xaa\xef\xdd'),
 (
  'horizontal_aligment_right', b'\x02\xaa\xef\xc8'),
 (
  'horizontal_aligment_top', b'\x02\xaa\xef\xc0'),
 (
  'vertical_alignment_top', b'\x02\xab\xef\xc0'),
 (
  'vertical_alignment_center', b'\x02\xab\xef\xf4'),
 (
  'vertical_alignment_bottom', b'\x02\xab\xef\xf5'),
 (
  'vertical_alignment_justify', b'\x02\xab\xef\xde'),
 (
  'vertical_alignment_distributed', b'\x02\xab\xef\xeb'),
 (
  'checkbox_off', b'\x02\xac\xef\xce'),
 (
  'checkbox_on', b'\x02\xad\x00\x01'),
 (
  'checkbox_mixed', b'\x02\xad\x00\x02'),
 (
  'text', b'\x02\xad\xef\xc2'),
 (
  'a_number', b'\x02\xae\x00\x02'),
 (
  'xl_number', b'\x02\xad\xef\xcf'),
 (
  'reference', b'\x02\xae\x00\x04'),
 (
  'formula', b'\x02\xae\x00\x05'),
 (
  'select_none', b'\x02\xb1\xef\xd2'),
 (
  'select_simple', b'\x02\xb1\xef\xc6'),
 (
  'select_extended', b'\x02\xb2\x00\x03'),
 (
  'text_to_replace', b'\x02\xb3\x00\x01'),
 (
  'replacement_text', b'\x02\xb3\x00\x02'),
 (
  'range_object', b'\x02\xb4\x00\x01'),
 (
  'A1_style_range_reference', b'\x02\xb4\x00\x02'),
 (
  'named_range', b'\x02\xb4\x00\x03'),
 (
  'list_of_category_names', b'\x02\xb4\x00\x04'),
 (
  'do_not_update_links', b'\x02\xb6\x00\x00'),
 (
  'update_external_links_only', b'\x02\xb6\x00\x01'),
 (
  'update_remote_links_only', b'\x02\xb6\x00\x02'),
 (
  'update_remote_and_external_links', b'\x02\xb6\x00\x03'),
 (
  'tab_delimiter', b'\x02\xb7\x00\x01'),
 (
  'commas_delimiter', b'\x02\xb7\x00\x02'),
 (
  'spaces_delimiter', b'\x02\xb7\x00\x03'),
 (
  'semicolon_delimiter', b'\x02\xb7\x00\x04'),
 (
  'no_delimiter', b'\x02\xb7\x00\x05'),
 (
  'custom_character_delimiter', b'\x02\xb7\x00\x06'),
 (
  'vary_by_color', b'\x02\xb8\x00\x01'),
 (
  'vary_by_shade', b'\x02\xb8\x00\x02'),
 (
  'vary_by_grayscale', b'\x02\xb8\x00\x03'),
 (
  'vary_by_same_color', b'\x02\xb8\x00\x04'),
 (
  'range_object', b'\x02\xb9\x00\x01'),
 (
  'A1_style_range_reference', b'\x02\xb9\x00\x02'),
 (
  'named_range', b'\x02\xb9\x00\x03'),
 (
  'worksheet_object', b'\x02\xba\x00\x01'),
 (
  'worksheet_name', b'\x02\xba\x00\x02'),
 (
  'align_tick_label_center', b'\x02\xba\xef\xf4'),
 (
  'align_tick_label_left', b'\x02\xba\xef\xdd'),
 (
  'align_tick_label_right', b'\x02\xba\xef\xc8'),
 (
  'Basque', b'\x02\xbc\x04-'),
 (
  'Catalan', b'\x02\xbc\x04\x03'),
 (
  'Chinese', b'\x02\xbc\x08\x04'),
 (
  'Chinese_Taiwan', b'\x02\xbc\x04\x04'),
 (
  'Czech', b'\x02\xbc\x04\x05'),
 (
  'Danish', b'\x02\xbc\x04\x06'),
 (
  'Dutch', b'\x02\xbc\x04\x13'),
 (
  'English_US', b'\x02\xbc\x04\t'),
 (
  'English_AUS', b'\x02\xbc\x0c\t'),
 (
  'English_British', b'\x02\xbc\x08\t'),
 (
  'English_CAN', b'\x02\xbc\x10\t'),
 (
  'Finnish', b'\x02\xbc\x04\x0b'),
 (
  'French', b'\x02\xbc\x04\x0c'),
 (
  'French_Canadian', b'\x02\xbc\x0c\x0c'),
 (
  'German', b'\x02\xbc\x04\x07'),
 (
  'German_Austria', b'\x02\xbc\x0c\x07'),
 (
  'Swiss_German', b'\x02\xbc\x08\x07'),
 (
  'Greek', b'\x02\xbc\x04\x08'),
 (
  'Hungarian', b'\x02\xbc\x04\x0e'),
 (
  'Italian', b'\x02\xbc\x04\x10'),
 (
  'Japanese', b'\x02\xbc\x04\x11'),
 (
  'Korean', b'\x02\xbc\x04\x12'),
 (
  'Malaysian', b'\x02\xbc\x04>'),
 (
  'Norwegian_Bokmal', b'\x02\xbc\x04\x14'),
 (
  'Norwegian', b'\x02\xbc\x04,'),
 (
  'Polish', b'\x02\xbc\x04\x15'),
 (
  'Portuguese_Brazil', b'\x02\xbc\x04\x16'),
 (
  'Portuguese_Iberian', b'\x02\xbc\x08\x16'),
 (
  'Russian', b'\x02\xbc\x04\x19'),
 (
  'Slovak', b'\x02\xbc\x04\x1b'),
 (
  'Slovenian', b'\x02\xbc\x04$'),
 (
  'Spanish', b'\x02\xbc\x04\n'),
 (
  'Swedish', b'\x02\xbc\x04\x1d'),
 (
  'Turkish', b'\x02\xbc\x04\x1f'),
 (
  'sort_on_cell_value', b'\x02\xbd\x00\x00'),
 (
  'sort_on_cell_color', b'\x02\xbd\x00\x01'),
 (
  'sort_on_font_color', b'\x02\xbd\x00\x02'),
 (
  'sort_on_icon', b'\x02\xbd\x00\x03'),
 (
  'sort_normal', b'\x02\xbe\x00\x00'),
 (
  'sort_text_as_numbers', b'\x02\xbe\x00\x01'),
 (
  'none_totals_calc', b'\x02\xbf\x00\x00'),
 (
  'average_totals_calc', b'\x02\xbf\x00\x01'),
 (
  'count_totals_calc', b'\x02\xbf\x00\x02'),
 (
  'count_number_totals_calc', b'\x02\xbf\x00\x03'),
 (
  'max_totals_calc', b'\x02\xbf\x00\x04'),
 (
  'min_totals_calc', b'\x02\xbf\x00\x05'),
 (
  'sum_totals_calc', b'\x02\xbf\x00\x06'),
 (
  'deviation_totals_calc', b'\x02\xbf\x00\x07'),
 (
  'var_totals_calc', b'\x02\xbf\x00\x08'),
 (
  'custom_totals_calc', b'\x02\xbf\x00\t'),
 (
  'no_chart_title', b'\x03\x86\x00\x00'),
 (
  'chart_title_centered_overlay', b'\x03\x86\x00\x01'),
 (
  'chart_title_above_chart', b'\x03\x86\x00\x02'),
 (
  'no_legend', b'\x03\x86\x00d'),
 (
  'legend_right', b'\x03\x86\x00e'),
 (
  'legend_top', b'\x03\x86\x00f'),
 (
  'legend_left', b'\x03\x86\x00g'),
 (
  'legend_bottom', b'\x03\x86\x00h'),
 (
  'legend_right_overlay', b'\x03\x86\x00i'),
 (
  'legend_left_overlay', b'\x03\x86\x00j'),
 (
  'no_data_label', b'\x03\x86\x00\xc8'),
 (
  'show_data_label', b'\x03\x86\x00\xc9'),
 (
  'data_label_center', b'\x03\x86\x00\xca'),
 (
  'data_label_inside_end', b'\x03\x86\x00\xcb'),
 (
  'data_label_inside_base', b'\x03\x86\x00\xcc'),
 (
  'data_label_outside_end', b'\x03\x86\x00\xcd'),
 (
  'data_label_left', b'\x03\x86\x00\xce'),
 (
  'data_label_right', b'\x03\x86\x00\xcf'),
 (
  'data_label_top', b'\x03\x86\x00\xd0'),
 (
  'data_label_bottom', b'\x03\x86\x00\xd1'),
 (
  'data_label_best_fit', b'\x03\x86\x00\xd2'),
 (
  'no_primary_category_axis_title', b'\x03\x86\x01,'),
 (
  'primary_category_axis_title_adjacent_to_axis', b'\x03\x86\x01-'),
 (
  'primary_category_axis_title_below_axis', b'\x03\x86\x01.'),
 (
  'primary_category_axis_title_rotated', b'\x03\x86\x01/'),
 (
  'primary_category_axis_title_vertical', b'\x03\x86\x010'),
 (
  'primary_category_axis_title_horizontal', b'\x03\x86\x011'),
 (
  'no_primary_value_axis_title', b'\x03\x86\x012'),
 (
  'primary_value_axis_title_adjacent_to_axis', b'\x03\x86\x013'),
 (
  'primary_value_axis_title_below_axis', b'\x03\x86\x014'),
 (
  'primary_value_axis_title_rotated', b'\x03\x86\x015'),
 (
  'primary_value_axis_title_vertical', b'\x03\x86\x016'),
 (
  'primary_value_axis_title_horizontal', b'\x03\x86\x017'),
 (
  'no_secondary_category_axis_title', b'\x03\x86\x018'),
 (
  'secondary_category_axis_title_adjacent_to_axis', b'\x03\x86\x019'),
 (
  'secondary_category_axis_title_below_Axis', b'\x03\x86\x01:'),
 (
  'secondary_category_axis_title_rotated', b'\x03\x86\x01;'),
 (
  'secondary_category_axis_title_vertical', b'\x03\x86\x01<'),
 (
  'secondary_category_axis_title_horizontal', b'\x03\x86\x01='),
 (
  'no_secondary_value_axis_title', b'\x03\x86\x01>'),
 (
  'secondary_value_axis_title_Adjacent_to_axis', b'\x03\x86\x01?'),
 (
  'secondary_value_axis_title_below_axis', b'\x03\x86\x01@'),
 (
  'secondary_value_axis_title_rotated', b'\x03\x86\x01A'),
 (
  'secondary_value_axis_title_vertical', b'\x03\x86\x01B'),
 (
  'secondary_value_axis_title_horizontal', b'\x03\x86\x01C'),
 (
  'no_series_axis_title', b'\x03\x86\x01D'),
 (
  'series_axis_title_rotated', b'\x03\x86\x01E'),
 (
  'series_axis_title_vertical', b'\x03\x86\x01F'),
 (
  'series_axis_title_horizontal', b'\x03\x86\x01G'),
 (
  'no_primary_value_grid_lines', b'\x03\x86\x01H'),
 (
  'primary_value_grid_lines_minor', b'\x03\x86\x01I'),
 (
  'primary_value_grid_lines_major', b'\x03\x86\x01J'),
 (
  'primary_value_grid_lines_minor_major', b'\x03\x86\x01K'),
 (
  'no_primary_category_grid_lines', b'\x03\x86\x01L'),
 (
  'primary_category_grid_lines_minor', b'\x03\x86\x01M'),
 (
  'primary_category_grid_lines_major', b'\x03\x86\x01N'),
 (
  'primary_category_grid_lines_minor_major', b'\x03\x86\x01O'),
 (
  'no_secondary_value_grid_lines', b'\x03\x86\x01P'),
 (
  'secondary_value_grid_lines_minor', b'\x03\x86\x01Q'),
 (
  'secondary_value_grid_lines_major', b'\x03\x86\x01R'),
 (
  'secondary_value_grid_lines_minor_major', b'\x03\x86\x01S'),
 (
  'no_secondary_category_grid_lines', b'\x03\x86\x01T'),
 (
  'secondary_category_grid_lines_minor', b'\x03\x86\x01U'),
 (
  'secondary_category_grid_lines_major', b'\x03\x86\x01V'),
 (
  'secondary_category_grid_lines_minor_major', b'\x03\x86\x01W'),
 (
  'no_series_axis_grid_lines', b'\x03\x86\x01X'),
 (
  'series_axis_grid_lines_minor', b'\x03\x86\x01Y'),
 (
  'series_axis_grid_lines_major', b'\x03\x86\x01Z'),
 (
  'series_axis_grid_lines_minor_major', b'\x03\x86\x01['),
 (
  'no_primary_category_axis', b'\x03\x86\x01\\'),
 (
  'primary_category_axis_show', b'\x03\x86\x01]'),
 (
  'primary_category_axis_without_labels', b'\x03\x86\x01^'),
 (
  'primary_category_axis_reverse', b'\x03\x86\x01_'),
 (
  'no_primary_value_axis', b'\x03\x86\x01`'),
 (
  'show_primary_value_axis', b'\x03\x86\x01a'),
 (
  'primary_value_axis_thousands', b'\x03\x86\x01b'),
 (
  'primary_value_axis_millions', b'\x03\x86\x01c'),
 (
  'primary_value_axis_billions', b'\x03\x86\x01d'),
 (
  'primary_value_axis_log_scale', b'\x03\x86\x01e'),
 (
  'no_secondary_category_axis', b'\x03\x86\x01f'),
 (
  'show_secondary_category_axis', b'\x03\x86\x01g'),
 (
  'secondary_category_axis_without_labels', b'\x03\x86\x01h'),
 (
  'secondary_category_axis_reverse', b'\x03\x86\x01i'),
 (
  'no_secondary_value_axis', b'\x03\x86\x01j'),
 (
  'show_secondary_value_axis', b'\x03\x86\x01k'),
 (
  'secondary_value_axis_thousands', b'\x03\x86\x01l'),
 (
  'secondary_value_axis_millions', b'\x03\x86\x01m'),
 (
  'secondary_value_axis_billions', b'\x03\x86\x01n'),
 (
  'secondary_value_axis_log_scale', b'\x03\x86\x01o'),
 (
  'no_series_axis', b'\x03\x86\x01p'),
 (
  'show_series_axis', b'\x03\x86\x01q'),
 (
  'series_axis_without_labeling', b'\x03\x86\x01r'),
 (
  'series_axis_reverse', b'\x03\x86\x01s'),
 (
  'primary_category_axis_thousands', b'\x03\x86\x01t'),
 (
  'primary_category_axis_millions', b'\x03\x86\x01u'),
 (
  'primary_category_axis_billions', b'\x03\x86\x01v'),
 (
  'primary_category_axis_log_scale', b'\x03\x86\x01w'),
 (
  'secondary_category_axis_thousands', b'\x03\x86\x01x'),
 (
  'secondary_category_axis_millions', b'\x03\x86\x01y'),
 (
  'secondary_category_axis_billions', b'\x03\x86\x01z'),
 (
  'secondary_category_axis_log_scale', b'\x03\x86\x01{'),
 (
  'no_data_table', b'\x03\x86\x01\xf4'),
 (
  'show_data_table', b'\x03\x86\x01\xf5'),
 (
  'data_table_with_legend_keys', b'\x03\x86\x01\xf6'),
 (
  'no_Trendline', b'\x03\x86\x02X'),
 (
  'trendline_add_linear', b'\x03\x86\x02Y'),
 (
  'trendline_add_exponential', b'\x03\x86\x02Z'),
 (
  'trendline_add_linear_forecast', b'\x03\x86\x02['),
 (
  'trendline_add_two_period_moving_average', b'\x03\x86\x02\\'),
 (
  'no_error_bar', b'\x03\x86\x02\xbc'),
 (
  'error_bar_standard_error', b'\x03\x86\x02\xbd'),
 (
  'error_bar_percentage', b'\x03\x86\x02\xbe'),
 (
  'error_bar_standard_deviation', b'\x03\x86\x02\xbf'),
 (
  'no_line', b'\x03\x86\x03 '),
 (
  'line_drop_line', b'\x03\x86\x03!'),
 (
  'line_hiLo_line', b'\x03\x86\x03"'),
 (
  'line_series_line', b'\x03\x86\x03#'),
 (
  'line_drop_hilo_line', b'\x03\x86\x03$'),
 (
  'no_up_down_bars', b'\x03\x86\x03\x84'),
 (
  'show_up_down_bars', b'\x03\x86\x03\x85'),
 (
  'no_plot_area', b'\x03\x86\x03\xe8'),
 (
  'show_plot_area', b'\x03\x86\x03\xe9'),
 (
  'no_chart_wall', b'\x03\x86\x04L'),
 (
  'show_chart_wall', b'\x03\x86\x04M'),
 (
  'no_chart_floor', b'\x03\x86\x04\xb0'),
 (
  'show_chart_floor', b'\x03\x86\x04\xb1'),
 (
  'filter_above_average', b'\x03\x87\x00!'),
 (
  'filter_all_dates_in_april', b'\x03\x87\x00\x18'),
 (
  'filter_all_dates_in_august', b'\x03\x87\x00\x1c'),
 (
  'filter_all_dates_in_december', b'\x03\x87\x00 '),
 (
  'filter_all_dates_in_february', b'\x03\x87\x00\x16'),
 (
  'filter_all_dates_in_january', b'\x03\x87\x00\x15'),
 (
  'filter_all_dates_in_july', b'\x03\x87\x00\x1b'),
 (
  'filter_all_dates_in_june', b'\x03\x87\x00\x1a'),
 (
  'filter_all_dates_in_march', b'\x03\x87\x00\x17'),
 (
  'filter_all_dates_in_may', b'\x03\x87\x00\x19'),
 (
  'filter_all_dates_in_november', b'\x03\x87\x00\x1f'),
 (
  'filter_all_dates_in_october', b'\x03\x87\x00\x1e'),
 (
  'filter_all_dates_in_quarter1', b'\x03\x87\x00\x11'),
 (
  'filter_all_dates_in_quarter2', b'\x03\x87\x00\x12'),
 (
  'filter_all_dates_in_quarter3', b'\x03\x87\x00\x13'),
 (
  'filter_all_dates_in_quarter4', b'\x03\x87\x00\x14'),
 (
  'filter_all_dates_in_september', b'\x03\x87\x00\x1d'),
 (
  'filter_below_average', b'\x03\x87\x00"'),
 (
  'filter_last_month', b'\x03\x87\x00\x08'),
 (
  'filter_last_quarter', b'\x03\x87\x00\x0b'),
 (
  'filter_last_week', b'\x03\x87\x00\x05'),
 (
  'filter_last_year', b'\x03\x87\x00\x0e'),
 (
  'filter_next_month', b'\x03\x87\x00\t'),
 (
  'filter_next_quarter', b'\x03\x87\x00\x0c'),
 (
  'filter_next_week', b'\x03\x87\x00\x06'),
 (
  'filter_next_year', b'\x03\x87\x00\x0f'),
 (
  'filter_this_month', b'\x03\x87\x00\x07'),
 (
  'filter_this_quarter', b'\x03\x87\x00\n'),
 (
  'filter_this_week', b'\x03\x87\x00\x04'),
 (
  'filter_this_year', b'\x03\x87\x00\r'),
 (
  'filter_today', b'\x03\x87\x00\x01'),
 (
  'filter_tomorrow', b'\x03\x87\x00\x03'),
 (
  'filter_year_to_date', b'\x03\x87\x00\x10'),
 (
  'filter_yesterday', b'\x03\x87\x00\x02'),
 (
  'theme_font_index_none', b'\x02\xc0\x00\x00'),
 (
  'theme_font_index_major', b'\x02\xc0\x00\x01'),
 (
  'theme_font_index_minor', b'\x02\xc0\x00\x02'),
 (
  'color_index_none', b'\x02\xc0\xef\xd2'),
 (
  'first_dark_theme_color', b'\x02\xc1\x00\x01'),
 (
  'first_light_theme_color', b'\x02\xc1\x00\x02'),
 (
  'second_dark_theme_color', b'\x02\xc1\x00\x03'),
 (
  'second_light_theme_color', b'\x02\xc1\x00\x04'),
 (
  'first_accent_theme_color', b'\x02\xc1\x00\x05'),
 (
  'second_accent_theme_color', b'\x02\xc1\x00\x06'),
 (
  'third_accent_theme_color', b'\x02\xc1\x00\x07'),
 (
  'fourth_accent_theme_color', b'\x02\xc1\x00\x08'),
 (
  'fifth_accent_theme_color', b'\x02\xc1\x00\t'),
 (
  'sixth_accent_theme_color', b'\x02\xc1\x00\n'),
 (
  'hyperlink_theme_color', b'\x02\xc1\x00\x0b'),
 (
  'followed_hyperlink_theme_color', b'\x02\xc1\x00\x0c'),
 (
  'minor_version', b'\x02\xc4\x00\x00'),
 (
  'major_version', b'\x02\xc4\x00\x01'),
 (
  'overwrite_current_version', b'\x02\xc4\x00\x02'),
 (
  'entire_page', b'\x02\xc5\x00\x00'),
 (
  'all_tables', b'\x02\xc5\x00\x01'),
 (
  'specified_tables', b'\x02\xc5\x00\x02'),
 (
  'web_formatting_all', b'\x02\xc6\x00\x00'),
 (
  'web_formatting_rtf', b'\x02\xc6\x00\x01'),
 (
  'web_formatting_none', b'\x02\xc6\x00\x02'),
 (
  'as_required', b'\x02\xc7\x00\x00'),
 (
  'always', b'\x02\xc7\x00\x01'),
 (
  'never', b'\x02\xc7\x00\x02'),
 (
  'condition_value_none', b'\x02\xc7\xff\xff'),
 (
  'condition_value_number', b'\x02\xc8\x00\x00'),
 (
  'condition_value_lowest_value', b'\x02\xc8\x00\x01'),
 (
  'condition_value_highest_value', b'\x02\xc8\x00\x02'),
 (
  'condition_value_percent', b'\x02\xc8\x00\x03'),
 (
  'condition_value_formula', b'\x02\xc8\x00\x04'),
 (
  'condition_value_percentile', b'\x02\xc8\x00\x05'),
 (
  'condition_value_automatic_minimum', b'\x02\xc8\x00\x06'),
 (
  'condition_value_automatic_maximum', b'\x02\xc8\x00\x07'),
 (
  'pivot_condition_selection_scope', b'\x02\xc9\x00\x00'),
 (
  'pivot_condition_fields_scope', b'\x02\xc9\x00\x01'),
 (
  'pivot_condition_data_field_scope', b'\x02\xc9\x00\x02'),
 (
  'databar_fill_solid', b'\x02\xca\x00\x00'),
 (
  'databar_fill_gradient', b'\x02\xca\x00\x01'),
 (
  'databar_border_none', b'\x02\xcb\x00\x00'),
 (
  'databar_border_solid', b'\x02\xcb\x00\x01'),
 (
  'databar_axis_automatic', b'\x02\xcc\x00\x00'),
 (
  'databar_axis_midpoint', b'\x02\xcc\x00\x01'),
 (
  'databar_axis_none', b'\x02\xcc\x00\x02'),
 (
  'databar_automatic', b'\x02\xcd\x00\x00'),
 (
  'databar_positive_format', b'\x02\xcd\x00\x01'),
 (
  'databar_custom_format', b'\x02\xcd\x00\x02'),
 (
  'format_condition_icon_no_cell_icon', b'\x02\xcd\xff\xff'),
 (
  'format_condition_icon_green_up_arrow', b'\x02\xce\x00\x01'),
 (
  'format_condition_icon_yellow_side_arrow', b'\x02\xce\x00\x02'),
 (
  'format_condition_icon_red_down_arrow', b'\x02\xce\x00\x03'),
 (
  'format_condition_icon_gray_up_arrow', b'\x02\xce\x00\x04'),
 (
  'format_condition_icon_gray_side_arrow', b'\x02\xce\x00\x05'),
 (
  'format_condition_icon_gray_down_arrow', b'\x02\xce\x00\x06'),
 (
  'format_condition_icon_green_flag', b'\x02\xce\x00\x07'),
 (
  'format_condition_icon_yellow_flag', b'\x02\xce\x00\x08'),
 (
  'format_condition_icon_red_flag', b'\x02\xce\x00\t'),
 (
  'format_condition_icon_green_circle', b'\x02\xce\x00\n'),
 (
  'format_condition_icon_yellow_circle', b'\x02\xce\x00\x0b'),
 (
  'format_condition_icon_red_circle_with_border', b'\x02\xce\x00\x0c'),
 (
  'format_condition_icon_black_circle_with_border', b'\x02\xce\x00\r'),
 (
  'format_condition_icon_green_traffic_light', b'\x02\xce\x00\x0e'),
 (
  'format_condition_icon_yellow_traffic_light', b'\x02\xce\x00\x0f'),
 (
  'format_condition_icon_red_traffic_light', b'\x02\xce\x00\x10'),
 (
  'format_condition_icon_yellow_triangle', b'\x02\xce\x00\x11'),
 (
  'format_condition_icon_red_diamond', b'\x02\xce\x00\x12'),
 (
  'format_condition_icon_green_check_symbol', b'\x02\xce\x00\x13'),
 (
  'format_condition_icon_yellow_exclamation_symbol', b'\x02\xce\x00\x14'),
 (
  'format_condition_icon_red_cross_symbol', b'\x02\xce\x00\x15'),
 (
  'format_condition_icon_green_check', b'\x02\xce\x00\x16'),
 (
  'format_condition_icon_yellow_exclamation', b'\x02\xce\x00\x17'),
 (
  'format_condition_icon_red_cross', b'\x02\xce\x00\x18'),
 (
  'format_condition_icon_yellow_up_incline_arrow', b'\x02\xce\x00\x19'),
 (
  'format_condition_icon_yellow_down_incline_arrow', b'\x02\xce\x00\x1a'),
 (
  'format_condition_icon_gray_up_incline_arrow', b'\x02\xce\x00\x1b'),
 (
  'format_condition_icon_gray_down_incline_arrow', b'\x02\xce\x00\x1c'),
 (
  'format_condition_icon_red_circle', b'\x02\xce\x00\x1d'),
 (
  'format_condition_icon_pink_circle', b'\x02\xce\x00\x1e'),
 (
  'format_condition_icon_gray_circle', b'\x02\xce\x00\x1f'),
 (
  'format_condition_icon_black_circle', b'\x02\xce\x00 '),
 (
  'format_condition_icon_circle_with_one_white_quarter', b'\x02\xce\x00!'),
 (
  'format_condition_icon_circle_with_two_white_quarters', b'\x02\xce\x00"'),
 (
  'format_condition_icon_circle_with_three_white_quarters', b'\x02\xce\x00#'),
 (
  'format_condition_icon_white_circle_all_white_quarters', b'\x02\xce\x00$'),
 (
  'format_condition_icon_0_bars', b'\x02\xce\x00%'),
 (
  'format_condition_icon_1_bar', b'\x02\xce\x00&'),
 (
  'format_condition_icon_2_bars', b"\x02\xce\x00'"),
 (
  'format_condition_icon_3_bars', b'\x02\xce\x00('),
 (
  'format_condition_icon_4_bars', b'\x02\xce\x00)'),
 (
  'format_condition_icon_gold_star', b'\x02\xce\x00*'),
 (
  'format_condition_icon_half_gold_star', b'\x02\xce\x00+'),
 (
  'format_condition_icon_silver_star', b'\x02\xce\x00,'),
 (
  'format_condition_icon_green_up_triangle', b'\x02\xce\x00-'),
 (
  'format_condition_icon_yellow_dash', b'\x02\xce\x00.'),
 (
  'format_condition_icon_red_down_triangle', b'\x02\xce\x00/'),
 (
  'format_condition_icon_4_filled_boxes', b'\x02\xce\x000'),
 (
  'format_condition_icon_3_filled_boxes', b'\x02\xce\x001'),
 (
  'format_condition_icon_2_filled_boxes', b'\x02\xce\x002'),
 (
  'format_condition_icon_1_filled_box', b'\x02\xce\x003'),
 (
  'format_condition_icon_0_filled_boxes', b'\x02\xce\x004'),
 (
  'icon_set_custom', b'\x02\xce\xff\xff'),
 (
  'icon_set_3_arrows', b'\x02\xcf\x00\x01'),
 (
  'icon_set_3_arrows_gray', b'\x02\xcf\x00\x02'),
 (
  'icon_set_3_flags', b'\x02\xcf\x00\x03'),
 (
  'icon_set_3_traffic_lights_1', b'\x02\xcf\x00\x04'),
 (
  'icon_set_3_traffic_lights_2', b'\x02\xcf\x00\x05'),
 (
  'icon_set_3_signs', b'\x02\xcf\x00\x06'),
 (
  'icon_set_3_symbols', b'\x02\xcf\x00\x07'),
 (
  'icon_set_3_symbols_2', b'\x02\xcf\x00\x08'),
 (
  'icon_set_4_arrows', b'\x02\xcf\x00\t'),
 (
  'icon_set_4_arrows_gray', b'\x02\xcf\x00\n'),
 (
  'icon_set_4_red_to_black', b'\x02\xcf\x00\x0b'),
 (
  'icon_set_4_CRV', b'\x02\xcf\x00\x0c'),
 (
  'icon_set_4_traffic_lights', b'\x02\xcf\x00\r'),
 (
  'icon_set_5_arrows', b'\x02\xcf\x00\x0e'),
 (
  'icon_set_5_arrows_gray', b'\x02\xcf\x00\x0f'),
 (
  'icon_set_5_CRV', b'\x02\xcf\x00\x10'),
 (
  'icon_set_5_quarters', b'\x02\xcf\x00\x11'),
 (
  'icon_set_3_stars', b'\x02\xcf\x00\x12'),
 (
  'icon_set_3_triangles', b'\x02\xcf\x00\x13'),
 (
  'icon_set_5_boxes', b'\x02\xcf\x00\x14'),
 (
  'top_10_top', b'\x02\xd0\x00\x01'),
 (
  'top_10_bottom', b'\x02\xd0\x00\x00'),
 (
  'calc_for_all_values', b'\x02\xd1\x00\x00'),
 (
  'calc_for_row_groups', b'\x02\xd1\x00\x01'),
 (
  'calc_for_col_groups', b'\x02\xd1\x00\x02'),
 (
  'format_above_average', b'\x02\xd2\x00\x00'),
 (
  'format_below_average', b'\x02\xd2\x00\x01'),
 (
  'format_equal_above_average', b'\x02\xd2\x00\x02'),
 (
  'format_equal_below_average', b'\x02\xd2\x00\x03'),
 (
  'format_above_standard_deviation', b'\x02\xd2\x00\x04'),
 (
  'format_below_standard_deviation', b'\x02\xd2\x00\x05'),
 (
  'format_unique_values', b'\x02\xd3\x00\x00'),
 (
  'format_duplicate_values', b'\x02\xd3\x00\x01'),
 (
  'text_contains', b'\x02\xd4\x00\x00'),
 (
  'text_does_not_contain', b'\x02\xd4\x00\x01'),
 (
  'text_begins_with', b'\x02\xd4\x00\x02'),
 (
  'text_ends_with', b'\x02\xd4\x00\x03'),
 (
  'date_is_today', b'\x02\xd5\x00\x00'),
 (
  'date_is_yesterday', b'\x02\xd5\x00\x01'),
 (
  'date_is_within_the_last_seven_days', b'\x02\xd5\x00\x02'),
 (
  'date_is_this_week', b'\x02\xd5\x00\x03'),
 (
  'date_is_last_week', b'\x02\xd5\x00\x04'),
 (
  'date_is_last_month', b'\x02\xd5\x00\x05'),
 (
  'date_is_tomorrow', b'\x02\xd5\x00\x06'),
 (
  'date_is_next_week', b'\x02\xd5\x00\x07'),
 (
  'date_is_next_month', b'\x02\xd5\x00\x08'),
 (
  'date_is_this_month', b'\x02\xd5\x00\t'),
 (
  'databar_color_type_color', b'\x02\xd6\x00\x00'),
 (
  'databar_color_type_same_as_positive', b'\x02\xd6\x00\x01'),
 (
  'window', 'cwin'),
 (
  'pane', 'X189'),
 (
  'sheet', 'X128'),
 (
  'workbook', 'X141'),
 (
  'application', 'capp'),
 (
  'button', 'Xbtn'),
 (
  'checkbox', 'Xckb'),
 (
  'option_button', 'XObn'),
 (
  'groupbox', 'XGBc'),
 (
  'label', 'Xlbl'),
 (
  'textbox', 'XTbx'),
 (
  'scrollbar', 'XSrl'),
 (
  'listbox', 'XLbx'),
 (
  'dropdown', 'XdpD'),
 (
  'spinner', 'XSpn'),
 (
  'dialog', 'X165'),
 (
  'scenario', 'X191'),
 (
  'format_condition', 'X227'),
 (
  'color_scale_format_condition', 'X325'),
 (
  'databar_format_condition', 'X312'),
 (
  'icon_set_format_condition', 'X315'),
 (
  'top_10_format_condition', 'X321'),
 (
  'above_average_format_condition', 'X322'),
 (
  'unique_values_format_condition', 'X323'),
 (
  'pivot_table', 'X155'),
 (
  'pivot_field', 'X157'),
 (
  'cube_field', 'X900'),
 (
  'calculated_member', 'X901'),
 (
  'pivot_filter', 'X903'),
 (
  'value_change', 'X905'),
 (
  'pivot_item', 'X160'),
 (
  'pivot_cache', 'X151'),
 (
  'query_table', 'X231'),
 (
  'display_format', 'X306'),
 (
  'overflow', b'\x02\xc2\x00\x00'),
 (
  'clip', b'\x02\xc2\x00\x01'),
 (
  'ellipsis', b'\x02\xc2\x00\x02'),
 (
  'overflow', b'\x02\xc3\x00\x00'),
 (
  'clip', b'\x02\xc3\x00\x01'),
 (
  'callout_format', 'X101'),
 (
  'callout', 'cD00'),
 (
  'rectangle', 'XRct'),
 (
  'oval', 'XOvl'),
 (
  'arc', 'Xarc'),
 (
  'line', 'Xlne'),
 (
  'shape', 'pShp'),
 (
  'chart_fill_format', 'X253'),
 (
  'chart_title', 'X256'),
 (
  'axis_title', 'X257'),
 (
  'series_point', 'X262'),
 (
  'series', 'X263'),
 (
  'data_label', 'X265'),
 (
  'legend_key', 'X269'),
 (
  'down_bars', 'X279'),
 (
  'floor', 'X280'),
 (
  'walls', 'X281'),
 (
  'plot_area', 'X283'),
 (
  'chart_area', 'X284'),
 (
  'legend', 'X285'),
 (
  'display_unit_label', 'X299'),
 (
  'trendline', 'X271'),
 (
  'error_bars', 'X286'),
 (
  'chart', 'X119'),
 (
  'chart_object', 'X221'),
 (
  'axis', 'X255')]
properties = [
 (
  'class_', 'pcls'),
 (
  'properties', 'pALL'),
 (
  'frontmost', 'pisf'),
 (
  'name', 'pnam'),
 (
  'version', 'vers'),
 (
  'modified', 'imod'),
 (
  'bounds', 'pbnd'),
 (
  'closeable', 'hclb'),
 (
  'titled', 'ptit'),
 (
  'entry_index', 'pidx'),
 (
  'floating', 'isfl'),
 (
  'modal', 'pmod'),
 (
  'position', 'posn'),
 (
  'resizable', 'prsz'),
 (
  'zoomable', 'iszm'),
 (
  'zoomed', 'pzum'),
 (
  'visible', 'pvis'),
 (
  'collapsable', 'iscp'),
 (
  'collapsed', 'wshd'),
 (
  'sheet', 'issh'),
 (
  'copies', 'lwcp'),
 (
  'collating', 'lwcl'),
 (
  'starting_page', 'lwfp'),
 (
  'ending_page', 'lwlp'),
 (
  'pages_across', 'lwla'),
 (
  'pages_down', 'lwld'),
 (
  'requested_print_time', 'lwqt'),
 (
  'error_handling', 'lweh'),
 (
  'fax_number', 'faxn'),
 (
  'target_printer', 'trpr'),
 (
  'button_face_is_default', 'BTBi'),
 (
  'button_state', 'BTST'),
 (
  'button_style', 'BTSy'),
 (
  'face_id', 'BTFi'),
 (
  'combobox_style', 'CBSy'),
 (
  'combobox_text', 'CBtX'),
 (
  'drop_down_lines', 'CBdd'),
 (
  'drop_down_width', 'CBdw'),
 (
  'list_index', 'CBlI'),
 (
  'begin_group', 'BCbg'),
 (
  'built_in', 'pBtN'),
 (
  'control_type', 'cBcT'),
 (
  'description_text', 'BCDt'),
 (
  'enabled', 'enbl'),
 (
  'entry_index', 'MSix'),
 (
  'height', 'hght'),
 (
  'help_context_ID', 'BCHi'),
 (
  'help_file', 'BCHf'),
 (
  'id', 'BCId'),
 (
  'left_position', 'plft'),
 (
  'parameter', 'BCPa'),
 (
  'priority', 'BCPr'),
 (
  'tag', 'BCTg'),
 (
  'tooltip_text', 'BCTt'),
 (
  'top', 'ptop'),
 (
  'width', 'pwid'),
 (
  'bar_position', 'bPos'),
 (
  'bar_type', 'bTyp'),
 (
  'context', 'CbCT'),
 (
  'embeddable', 'pMbl'),
 (
  'embedded', 'pMbd'),
 (
  'local_name', 'CbNL'),
 (
  'protection', 'CBPt'),
 (
  'row_index', 'CBRi'),
 (
  'document_property_type', 'mDty'),
 (
  'link_source', 'DPLs'),
 (
  'link_to_content', 'DPLc'),
 (
  'value', 'DPVu'),
 (
  'fixed_width_font', 'WFfw'),
 (
  'fixed_width_font_size', 'WFfs'),
 (
  'proportional_font', 'WFpf'),
 (
  'proportional_font_size', 'WFps'),
 (
  'author', '2123'),
 (
  'shape_object', '2124'),
 (
  'error_string', '1920'),
 (
  'sql_state', '2167'),
 (
  'allow_deleting_columns', '2442'),
 (
  'allow_deleting_rows', '2443'),
 (
  'allow_filtering', '2445'),
 (
  'allow_formatting_cells', '2436'),
 (
  'allow_formatting_columns', '2437'),
 (
  'allow_formatting_rows', '2438'),
 (
  'allow_inserting_columns', '2439'),
 (
  'allow_inserting_hyperlinks', '2441'),
 (
  'allow_inserting_rows', '2440'),
 (
  'allow_sorting', '2444'),
 (
  'allow_using_pivot_table', '2446'),
 (
  'above_or_below', '2604'),
 (
  'applies_to', '2568'),
 (
  'calc_for', '2603'),
 (
  'font_object', 'XftO'),
 (
  'format_condition_priority', '2566'),
 (
  'format_condition_type', '2119'),
 (
  'interior_object', 'XitO'),
 (
  'number_format', '1593'),
 (
  'number_of_standard_deviations', '2605'),
 (
  'pivot_condition_scope_type', '2574'),
 (
  'pivot_table_condition', '2573'),
 (
  'stop_if_true', '2567'),
 (
  'full_name', '1773'),
 (
  'installed', '1774'),
 (
  'path', '1289'),
 (
  'AutoFormatAsYouTypeReplaceHyperlinks', 'LLnm'),
 (
  'Excel_cursor', '1219'),
 (
  'ODBC_timeout', '1282'),
 (
  'active_cell', '1104'),
 (
  'active_chart', '1105'),
 (
  'active_printer', '1170'),
 (
  'active_sheet', '1107'),
 (
  'active_window', '1171'),
 (
  'active_workbook', '1172'),
 (
  'alert_before_overwriting', '1201'),
 (
  'alt_startup_path', '1202'),
 (
  'arbitrary_XML_support_available', 'LLnp'),
 (
  'ask_to_update_links', '1203'),
 (
  'autocorrect_object', 'XocO'),
 (
  'automation_security', 'Xaso'),
 (
  'build', '1206'),
 (
  'calculate_before_save', '1207'),
 (
  'calculation', '1208'),
 (
  'calculation_version', '1339'),
 (
  'caption', '1108'),
 (
  'cell_drag_and_drop', '1210'),
 (
  'command_underlines', '1215'),
 (
  'copy_objects_with_cells', '1218'),
 (
  'custom_list_count', '1220'),
 (
  'cut_copy_mode', '1221'),
 (
  'data_entry_mode', '1222'),
 (
  'default_file_path', '1234'),
 (
  'default_save_format', '1314'),
 (
  'default_web_options_object', '1332'),
 (
  'display_alerts', '1238'),
 (
  'display_comment_indicator', '1242'),
 (
  'display_excel_4_menus', '1243'),
 (
  'display_formula_bar', 'XdFb'),
 (
  'display_full_screen', '1240'),
 (
  'display_function_tooltips', 'XdfT'),
 (
  'display_insert_options', 'XdIo'),
 (
  'display_note_indicator', '1241'),
 (
  'display_recent_files', '1244'),
 (
  'display_scroll_bars', '1245'),
 (
  'display_status_bar', '1246'),
 (
  'edit_directly_in_cell', '1248'),
 (
  'enable_animations', '1204'),
 (
  'enable_autocomplete', '1249'),
 (
  'enable_cancel_key', '1250'),
 (
  'enable_events', '1331'),
 (
  'enable_formula_autocomplete', 'fAcm'),
 (
  'enable_formula_type_ahead', 'fTyp'),
 (
  'enable_sound', '1251'),
 (
  'extend_list', '1335'),
 (
  'fixed_decimal', '1255'),
 (
  'fixed_decimal_places', '1256'),
 (
  'formula_autocomplete_wait', 'typW'),
 (
  'include_empty_cells_in_lists', 'XiEc'),
 (
  'iteration', '1267'),
 (
  'keep_four_digit_years', '1333'),
 (
  'keyboard_script', 'kbSc'),
 (
  'library_path', '1268'),
 (
  'localized_language', 'LLng'),
 (
  'math_coprocessor_available', '1270'),
 (
  'max_change', '1271'),
 (
  'max_iterations', '1272'),
 (
  'measurement_unit', '1342'),
 (
  'memory_free', '1273'),
 (
  'memory_total', '1274'),
 (
  'memory_used', '1275'),
 (
  'move_after_return', '1277'),
 (
  'move_after_return_direction', '1278'),
 (
  'network_templates_path', '1280'),
 (
  'operating_system', '1287'),
 (
  'organization_name', '1288'),
 (
  'path_separator', '1290'),
 (
  'pivot_table_selection', '1292'),
 (
  'prompt_for_summary_info', '1293'),
 (
  'reference_style', '1297'),
 (
  'ribbon_expanded', 'EPRB'),
 (
  'roll_zoom', '1301'),
 (
  'save_interval', '1341'),
 (
  'screen_updating', '1303'),
 (
  'selection', 'sele'),
 (
  'sheets_in_new_workbook', '1305'),
 (
  'show_chart_tip_names', '1306'),
 (
  'show_chart_tip_values', '1307'),
 (
  'show_ribbon', 'SHRB'),
 (
  'show_tool_tips', '1313'),
 (
  'spelling_options', 'xlsp'),
 (
  'standard_font', '1308'),
 (
  'standard_font_size', '1309'),
 (
  'startup_dialog', '1337'),
 (
  'startup_path', '1310'),
 (
  'status_bar', '1311'),
 (
  'templates_path', '1312'),
 (
  'this_cell', 'LLnn'),
 (
  'transition_menu_key', '1315'),
 (
  'transition_menu_key_action', '1316'),
 (
  'two_digit_cutoff_year', '1334'),
 (
  'usable_height', '1143'),
 (
  'usable_width', '1144'),
 (
  'user_name', '1320'),
 (
  'autofiltermode', '2530'),
 (
  'range_object', '2180'),
 (
  'sort_object', '2533'),
 (
  'color', 'colr'),
 (
  'color_index', '1098'),
 (
  'line_style', 'XlnS'),
 (
  'line_weight', 'XlnW'),
 (
  'theme_color', 'DThC'),
 (
  'tint_and_shade', '2535'),
 (
  'weight', '1031'),
 (
  'accelerator', '1996'),
 (
  'add_indent', '1514'),
 (
  'auto_scale_font', '1992'),
 (
  'auto_size', '1993'),
 (
  'bottom_right_cell', '1983'),
 (
  'cancel_button', '1997'),
 (
  'control_text', 'XcTx'),
 (
  'default_button', '1998'),
 (
  'dismiss_button', '1999'),
 (
  'formula', '1562'),
 (
  'help_button', '2000'),
 (
  'horizontal_alignment', '1575'),
 (
  'locked', '1584'),
 (
  'locked_text', '1994'),
 (
  'on_action', 'BCOa'),
 (
  'orientation', '1596'),
 (
  'phonetic_accelerator', '2001'),
 (
  'placement', '1986'),
 (
  'print_object', '1987'),
 (
  'reading_order', '1639'),
 (
  'top_left_cell', '1989'),
 (
  'vertical_alignment', '1631'),
 (
  'wrap_auto_text', '1995'),
 (
  'z_order_position', '2364'),
 (
  '_default_', 'CL12'),
 (
  'display_folder', 'CL15'),
 (
  'dynamic', 'CL14'),
 (
  'flatten_hierarchies', 'CL17'),
 (
  'formula', 'CL08'),
 (
  'hierarchize_distinct', 'CL16'),
 (
  'is_valid', 'CL11'),
 (
  'name', 'CL07'),
 (
  'solve_order', 'CL10'),
 (
  'source_name', '1954'),
 (
  'type', 'CL13'),
 (
  'border', 'X251'),
 (
  'display_threeD_shading', '2002'),
 (
  'linked_cell', '2003'),
 (
  'color_scale_criterion_index', '2575'),
 (
  'color_scale_criterion_type', '2576'),
 (
  'color_scale_criterion_value', '2577'),
 (
  'format_color', 'X307'),
 (
  'color_scale_criteria', 'X310'),
 (
  'color_scale_type', '2609'),
 (
  'colorstop_position', '2548'),
 (
  'condition_value_type', '2564'),
 (
  'condition_value_value', '2565'),
 (
  'all_items_visible', 'CL00'),
 (
  'cube_field_sub_type', 'CK99'),
 (
  'cube_field_type', 'CK80'),
 (
  'current_page_name', 'CL02'),
 (
  'drag_to_column', '1962'),
 (
  'drag_to_data', '1966'),
 (
  'drag_to_hide', '1963'),
 (
  'drag_to_page', '1964'),
 (
  'drag_to_row', '1965'),
 (
  'enable_multiple_page_items', 'CK94'),
 (
  'flatten_hierarchies', 'CL05'),
 (
  'has_member_properties', 'CK91'),
 (
  'hierarchize_distinct', 'CL06'),
 (
  'include_new_items_in_filter', 'CK98'),
 (
  'is_date', 'CL03'),
 (
  'layout_form', 'CK92'),
 (
  'layout_subtotal_location', 'CK95'),
 (
  'name', 'CK81'),
 (
  'orientation', 'CK83'),
 (
  'position', 'CK84'),
 (
  'show_in_field_list', 'CK96'),
 (
  'treeview_control', 'CK85'),
 (
  'value', 'CK82'),
 (
  'custom_view_print_settings', '2116'),
 (
  'row_col_settings', '2117'),
 (
  'databar_border_color', '2589'),
 (
  'databar_border_type', '2588'),
 (
  'databar_axis_color', '2587'),
 (
  'databar_axis_position', '2586'),
 (
  'databar_bar_color', '2582'),
 (
  'databar_border', 'X313'),
 (
  'databar_direction', '2584'),
 (
  'databar_fill_type', '2585'),
 (
  'format_condition_show_value', '2583'),
 (
  'max_point_condition_value', '2579'),
 (
  'max_point_percent', '2581'),
 (
  'min_point_condition_value', '2578'),
 (
  'min_point_percent', '2580'),
 (
  'negative_bar_format', 'X314'),
 (
  'allow_png', '2400'),
 (
  'always_save_in_default_encoding', '2405'),
 (
  'encoding', '2404'),
 (
  'location_of_components', '2403'),
 (
  'pixels_per_inch', '2402'),
 (
  'screen_size', '2401'),
 (
  'update_links_on_save', '2395'),
 (
  'formula_hidden', '1565'),
 (
  'indent_level', '1576'),
 (
  'merge_cells', '1588'),
 (
  'shrink_to_fit', '1618'),
 (
  'style_object', '1029'),
 (
  'text_orientation', 'XtOr'),
 (
  'wrap_text', '1633'),
 (
  'drop_down_lines', '2021'),
 (
  'list_fill_range', '2015'),
 (
  'number_of_items_in_list', 'XnIL'),
 (
  'criteria1', '2191'),
 (
  'criteria2', '2192'),
 (
  'filter_on', '2190'),
 (
  'operator', '2120'),
 (
  'format_condition_icon_index', '2598'),
 (
  'icon_set_id', '2599'),
 (
  'condition_operator', 'XfcO'),
 (
  'format_condition_date_operator', '2608'),
 (
  'format_condition_text', 'XfcT'),
 (
  'format_condition_text_operator', '2607'),
 (
  'formula_1', '2121'),
 (
  'formula_2', '2122'),
 (
  'brightness', '1037'),
 (
  'color_type', '1038'),
 (
  'contrast', '1039'),
 (
  'crop_bottom', '1040'),
 (
  'crop_left', '1041'),
 (
  'crop_right', '1042'),
 (
  'crop_top', '1043'),
 (
  'file_name', 'AFLN'),
 (
  'lock_aspect_ratio', '2207'),
 (
  'extent', '1725'),
 (
  'horizontal_page_break_type', '1726'),
 (
  'location', '1694'),
 (
  'address', '2182'),
 (
  'email_subject', '2185'),
 (
  'hyperlink_type', '2183'),
 (
  'screen_tip', '2186'),
 (
  'sub_address', '2181'),
 (
  'text_to_display', '2187'),
 (
  'icon_criterion_icon', '2597'),
 (
  'icon_criterion_index', '2594'),
 (
  'icon_criterion_type', '2595'),
 (
  'icon_criterion_value', '2596'),
 (
  'format_condition_icon_set', 'X319'),
 (
  'icon_criteria', 'X316'),
 (
  'percentile_values', '2592'),
 (
  'reverse_icon_set_order', '2591'),
 (
  'show_icon_only', '2593'),
 (
  'enable_selection', '1740'),
 (
  'colorstops', '2541'),
 (
  'linear_gradient_degree', '2540'),
 (
  'cell_table', '2193'),
 (
  'index', '2508'),
 (
  'total_row', '2194'),
 (
  'totals_calculation', '2499'),
 (
  'active', '2504'),
 (
  'autofilter_object', 'AfOj'),
 (
  'comment', '2501'),
 (
  'default', '2503'),
 (
  'display_name', '2500'),
 (
  'display_right_to_left', '2505'),
 (
  'header_row', '2506'),
 (
  'insert_row', '2507'),
 (
  'query_table', 'X231'),
 (
  'show_autofilter', '2198'),
 (
  'show_headers', '2502'),
 (
  'show_table_style_column_stripes', 'CJ39'),
 (
  'show_table_style_first_column', 'SJ30'),
 (
  'show_table_style_last_column', 'CJ37'),
 (
  'show_table_style_row_stripes', 'CJ38'),
 (
  'source_type', '2509'),
 (
  'table_style', '1936'),
 (
  'total', '2196'),
 (
  'multi_select', '2017'),
 (
  'category', '2092'),
 (
  'category_local', '2094'),
 (
  'macro_type', '2095'),
 (
  'name_local', '1772'),
 (
  'reference_local', '2101'),
 (
  'reference_local_r1c1', '2104'),
 (
  'reference_r1c1', '2102'),
 (
  'reference_range', '2105'),
 (
  'references', '2098'),
 (
  'shortcut_key', '2100'),
 (
  'negative_bar_border_color_type', '2590'),
 (
  'negative_bar_color_type', '2585'),
 (
  'group_box', '2004'),
 (
  'automatic_styles', '2048'),
 (
  'summary_column', '2050'),
 (
  'summary_row', '2051'),
 (
  'black_and_white', '2055'),
 (
  'bottom_margin', '2056'),
 (
  'center_footer', '2057'),
 (
  'center_footer_picture', '2087'),
 (
  'center_header', '2058'),
 (
  'center_header_picture', '2086'),
 (
  'center_horizontally', '2059'),
 (
  'center_vertically', '2060'),
 (
  'chart_size', '2061'),
 (
  'draft', '2062'),
 (
  'first_page_number', '2063'),
 (
  'fit_to_pages_tall', '2064'),
 (
  'fit_to_pages_wide', '2065'),
 (
  'footer_margin', '2066'),
 (
  'header_margin', '2067'),
 (
  'left_footer', '2068'),
 (
  'left_footer_picture', '2089'),
 (
  'left_header', '2069'),
 (
  'left_header_picture', '2088'),
 (
  'left_margin', '2070'),
 (
  'order', '2071'),
 (
  'page_orientation', 'XPgO'),
 (
  'print_Excel_comments', '2085'),
 (
  'print_area', '2073'),
 (
  'print_gridlines', '2074'),
 (
  'print_headings', '2075'),
 (
  'print_notes', '2076'),
 (
  'print_quality', 'XVpQ'),
 (
  'print_title_columns', '2079'),
 (
  'print_title_rows', '2080'),
 (
  'right_footer', '2081'),
 (
  'right_footer_picture', '2091'),
 (
  'right_header', '2082'),
 (
  'right_header_picture', '2090'),
 (
  'right_margin', '2083'),
 (
  'top_margin', '2084'),
 (
  'zoom', '1148'),
 (
  'scroll_column', '1131'),
 (
  'scroll_row', '1132'),
 (
  'visible_range', '1145'),
 (
  'character_type', '2336'),
 (
  'phonetic_alignment', 'XpoA'),
 (
  'phonetic_text', 'phTx'),
 (
  'ADO_connection', 'CJ78'),
 (
  'OLAP', 'CJ81'),
 (
  'SQL_query', '1886'),
 (
  'background_query', '1878'),
 (
  'command_text', '1889'),
 (
  'command_type', 'CJ69'),
 (
  'connection', '1879'),
 (
  'enable_refresh', '1880'),
 (
  'is_connected', 'CJ79'),
 (
  'local_connection', 'CJ75'),
 (
  'maintain_connection', 'CJ71'),
 (
  'missing_items_limit', 'CJ83'),
 (
  'optimize_cache', '1881'),
 (
  'query_type', '2155'),
 (
  'record_count', '1882'),
 (
  'refresh_date', '1883'),
 (
  'refresh_name', '1884'),
 (
  'refresh_on_file_open', '1885'),
 (
  'refresh_period', 'CJ72'),
 (
  'robust_connect', 'CJ85'),
 (
  'save_password', '1887'),
 (
  'source_connection_file', 'CJ84'),
 (
  'source_data', '1888'),
 (
  'source_type', 'CJ82'),
 (
  'upgrade_on_refresh', 'CJ89'),
 (
  'use_local_connection', 'CJ77'),
 (
  'version', 'CJ88'),
 (
  'workbook_connection', 'CJ87'),
 (
  'MDX', 'CK06'),
 (
  'cell_changed', 'CK05'),
 (
  'custom_subtotal_function', 'CJ99'),
 (
  'data_field', 'CJ93'),
 (
  'data_source_value', 'CK04'),
 (
  'pivot_cell_type', 'CJ91'),
 (
  'pivot_column_line', 'CK01'),
 (
  'pivot_field', 'CJ94'),
 (
  'pivot_item', 'CJ95'),
 (
  'pivot_row_line', 'CK00'),
 (
  'pivot_table', 'CJ92'),
 (
  'range', 'CJ98'),
 (
  'row_items', 'CJ96'),
 (
  'all_items_visible', 'CK40'),
 (
  'auto_show_count', '1975'),
 (
  'auto_show_field', '1976'),
 (
  'auto_show_range', '1974'),
 (
  'auto_show_type', '1973'),
 (
  'auto_sort_custom_subtotal', 'CK37'),
 (
  'auto_sort_field', '1972'),
 (
  'auto_sort_order', '1971'),
 (
  'auto_sort_pivot_line', 'CK36'),
 (
  'base_field', '1957'),
 (
  'base_item', '1958'),
 (
  'child_field', '1941'),
 (
  'cube_field', 'CK14'),
 (
  'current_page', '1943'),
 (
  'current_page_list', 'CK23'),
 (
  'current_page_name', 'CK15'),
 (
  'data_range', '1944'),
 (
  'database_sort', 'CK18'),
 (
  'display_as_caption', 'CK31'),
 (
  'display_as_tooltip', 'CK29'),
 (
  'display_in_report', 'CK30'),
 (
  'drilled_down', 'CK13'),
 (
  'enable_item_selection', 'CK22'),
 (
  'enable_multiple_page_items', 'CK39'),
 (
  'function', '1946'),
 (
  'group_level', '1947'),
 (
  'hidden', '1574'),
 (
  'hidden_items_list', 'CK17'),
 (
  'include_new_items_in_filter', 'CK33'),
 (
  'is_calculated', '1967'),
 (
  'is_member_property', 'CK19'),
 (
  'label_range', '1949'),
 (
  'layout_blank_line', 'CK07'),
 (
  'layout_compact_row', 'CK32'),
 (
  'layout_form', 'CK10'),
 (
  'layout_pagebreak', 'CK09'),
 (
  'layout_subtotal_location', 'CK08'),
 (
  'member_property_caption', 'CK28'),
 (
  'parent_field', '1951'),
 (
  'pivot_field_data_type', 'XpfT'),
 (
  'pivot_field_orientation', 'XpfO'),
 (
  'property_order', 'CK21'),
 (
  'property_parent_field', 'CK20'),
 (
  'repeat_labels', 'CK48'),
 (
  'server_based', '1968'),
 (
  'show_all_items', '1950'),
 (
  'show_detail', '1615'),
 (
  'showing_in_axis', 'CK38'),
 (
  'source_caption', 'CK46'),
 (
  'standard_formula', 'CK16'),
 (
  'subtotal_name', 'CK11'),
 (
  'total_levels', '1959'),
 (
  'use_member_property_as_caption', 'CK27'),
 (
  'visible_items', 'PFvi'),
 (
  'visible_items_list', 'CK34'),
 (
  'active', 'CK64'),
 (
  'data_cube_field', 'CK67'),
 (
  'data_field', 'CK66'),
 (
  'description', 'CK62'),
 (
  'filter_type', 'CK50'),
 (
  'is_member_property_filter', 'CK71'),
 (
  'member_property_field', 'CK70'),
 (
  'name', 'CK61'),
 (
  'order', 'CK49'),
 (
  'pivot_field', 'CK65'),
 (
  'value1', 'CK68'),
 (
  'value2', 'DPV2'),
 (
  'standard_formula', 'CK72'),
 (
  'drilled_down', 'CK74'),
 (
  'parent_item', 'XPIp'),
 (
  'parent_show_detail', '1978'),
 (
  'source_name_standard', 'CK76'),
 (
  'standard_formula', 'CK75'),
 (
  'line_type', 'CK77'),
 (
  'pivot_line_cells', 'CK79'),
 (
  'position', 'CK78'),
 (
  'CompactRowIndent', 'CJ28'),
 (
  'allocation', 'CJ52'),
 (
  'allocation_method', 'CJ54'),
 (
  'allocation_value', 'CJ53'),
 (
  'allocation_weight_expression', 'CJ55'),
 (
  'allow_multiple_filters', 'CJ43'),
 (
  'alternative_text', 'CJ63'),
 (
  'cache_index', '1913'),
 (
  'calculated_members_in_filters', 'CJ67'),
 (
  'change_list', 'CJ61'),
 (
  'column_grand', '1892'),
 (
  'column_range', '1893'),
 (
  'compact_layout_column_header', 'CJ45'),
 (
  'compact_layout_row_header', 'CJ44'),
 (
  'data_body_range', '1895'),
 (
  'data_label_range', '1897'),
 (
  'data_pivot_field', 'CJ07'),
 (
  'display_context_tooltips', 'CJ26'),
 (
  'display_empty_column', 'CJ20'),
 (
  'display_empty_row', 'CJ19'),
 (
  'display_error_string', '1915'),
 (
  'display_field_captions', 'CJ30'),
 (
  'display_immediate_items', 'CJ13'),
 (
  'display_member_property_tooltips', 'CJ25'),
 (
  'display_null_string', '1916'),
 (
  'enable_data_value_editing', 'CJ08'),
 (
  'enable_drilldown', '1917'),
 (
  'enable_field_dialog', '1918'),
 (
  'enable_field_list', 'CJ14'),
 (
  'enable_wizard', '1919'),
 (
  'enable_writeback', 'CJ51'),
 (
  'file_list_sort_ascending', 'CJ46'),
 (
  'grand_total_name', 'CJ02'),
 (
  'has_autoformat', '1898'),
 (
  'in_grid_drop_zones', 'CJ34'),
 (
  'inner_detail', '1900'),
 (
  'layout_row_default', 'CJ29'),
 (
  'location', 'CJ50'),
 (
  'manual_update', '1923'),
 (
  'mdx', 'CJ10'),
 (
  'merge_labels', '1924'),
 (
  'null_string', '1925'),
 (
  'page_field_order', '1929'),
 (
  'page_field_style', '1930'),
 (
  'page_field_wrap_count', '1931'),
 (
  'page_range', '1902'),
 (
  'page_range_cells', '1903'),
 (
  'pivot_cache', 'X151'),
 (
  'pivot_column_axis', 'CJ21'),
 (
  'pivot_row_axis', 'CJ22'),
 (
  'pivot_selection', '1934'),
 (
  'pivot_selection_standard', 'CJ05'),
 (
  'preserve_formatting', '1932'),
 (
  'print_drill_indicators', 'Cj24'),
 (
  'print_titles', 'CJ00'),
 (
  'repeat_items_on_each_printed_page', 'CJ03'),
 (
  'row_grand', '1907'),
 (
  'row_range', '1908'),
 (
  'save_data', '1909'),
 (
  'selection_mode', '1935'),
 (
  'show_drill_indicators', 'CJ23'),
 (
  'show_page_multiple_label', 'CJ16'),
 (
  'show_table_style_column_headers', 'CJ41'),
 (
  'show_table_style_row_headers', 'CJ40'),
 (
  'show_values_row', 'CJ66'),
 (
  'small_grid', '1940'),
 (
  'sort_using_custom_lists', 'CJ47'),
 (
  'subtotal_hidden_page_items', '1928'),
 (
  'summary', '1622'),
 (
  'table_range1', '1910'),
 (
  'table_range2', '1911'),
 (
  'table_style2', 'CJ36'),
 (
  'totals_annotation', 'CJ04'),
 (
  'vacated_style', '1939'),
 (
  'version', 'CJ17'),
 (
  'view_calculated_members', 'CJ11'),
 (
  'visual_totals', 'CJ15'),
 (
  'visual_totals_for_sets', 'CJ65'),
 (
  'FileMaker_fields', '2158'),
 (
  'FileMaker_num_criteria', '2159'),
 (
  'FileMaker_use_table', '2212'),
 (
  'adjust_column_width', '2141'),
 (
  'command_type', 'CmTe'),
 (
  'destination', '2134'),
 (
  'enable_editing', '2140'),
 (
  'fetched_row_overflow', '2131'),
 (
  'field_names', '2127'),
 (
  'fill_adjacent_formulas', '2129'),
 (
  'post_text', '2135'),
 (
  'refresh_style', '2133'),
 (
  'refreshing', '2130'),
 (
  'result_range', '2136'),
 (
  'row_numbers', '2128'),
 (
  'sql', '1886'),
 (
  'tables_only_from_html', '2139'),
 (
  'text_file_column_data_types', '2152'),
 (
  'text_file_comma_delimiter', '2149'),
 (
  'text_file_consecutive_delimiter', '2146'),
 (
  'text_file_decimal_separator', '2156'),
 (
  'text_file_fixed_column_widths', '2153'),
 (
  'text_file_other_delimiter', '2151'),
 (
  'text_file_parse_type', '2144'),
 (
  'text_file_platform', '2142'),
 (
  'text_file_prompt_on_refresh', '2154'),
 (
  'text_file_semicolon_delimiter', '2148'),
 (
  'text_file_space_delimiter', '2150'),
 (
  'text_file_start_row', '2143'),
 (
  'text_file_tab_delimiter', '2147'),
 (
  'text_file_text_qualifier', '2145'),
 (
  'text_file_thousands_separator', '2157'),
 (
  'use_list_object', '2162'),
 (
  'rectangular_gradient_bottom', '2542'),
 (
  'rectangular_gradient_left', '2543'),
 (
  'rectangular_gradient_right', '2544'),
 (
  'rectangular_gradient_top', '2545'),
 (
  'Excel_comment', 'X229'),
 (
  'changing_cells', '2023'),
 (
  'large_change', '2010'),
 (
  'maximum_value', 'XSMv'),
 (
  'minimum_value', 'XSmv'),
 (
  'small_change', '2009'),
 (
  'autofilter_mode', '1732'),
 (
  'circular_reference', '1734'),
 (
  'consolidation_function', '1736'),
 (
  'consolidation_options', 'COPT'),
 (
  'consolidation_sources', '1738'),
 (
  'display_page_breaks', '1760'),
 (
  'enable_autofilter', '1739'),
 (
  'enable_calculation', '1733'),
 (
  'enable_outlining', '1741'),
 (
  'enable_pivot_table', '1742'),
 (
  'filter_mode', '1743'),
 (
  'next_', '1591'),
 (
  'outline_object', '1745'),
 (
  'page_setup_object', '1654'),
 (
  'previous_', '1606'),
 (
  'protect_contents', '1656'),
 (
  'protect_drawing_objects', '1657'),
 (
  'protection_mode', '1658'),
 (
  'protection_object', '2447'),
 (
  'scroll_area', '1749'),
 (
  'sheet_tab', '2551'),
 (
  'standard_height', '1752'),
 (
  'standard_width', '1753'),
 (
  'transition_expression_evaluation', '1731'),
 (
  'used_range', '1756'),
 (
  'worksheet_type', '1755'),
 (
  'match_case', '2512'),
 (
  'sort_header', '2513'),
 (
  'sort_method', '2515'),
 (
  'sort_orientation', '2514'),
 (
  'sortfields', 'Xsfs'),
 (
  'sortrange', '2511'),
 (
  'custom_order', '2524'),
 (
  'sort_data_option', '2525'),
 (
  'sort_key', '2522'),
 (
  'sort_on', '2520'),
 (
  'sort_on_values', '2521'),
 (
  'sort_order', '2523'),
 (
  'sort_priority', '2526'),
 (
  'has_format', '2610'),
 (
  'namelocal', '2611'),
 (
  'show_as_available_pivot_table_style', '2613'),
 (
  'show_as_available_table_style', '2612'),
 (
  'rounded_corners', '2028'),
 (
  'shadow', 'shad'),
 (
  'string_value', 'XRgt'),
 (
  'top_10_percentage', '2602'),
 (
  'top_10_rank', '2601'),
 (
  'top_or_bottom', '2600'),
 (
  'drilled', 'CK25'),
 (
  'duplicate_or_unique', '2606'),
 (
  'IME_mode', '2171'),
 (
  'alert_style', '2169'),
 (
  'error_message', '2173'),
 (
  'error_title', '2174'),
 (
  'formula1', '2121'),
 (
  'formula2', '2122'),
 (
  'ignore_blank', '2170'),
 (
  'in_cell_dropdown', '2172'),
 (
  'input_message', '2175'),
 (
  'input_title', '2176'),
 (
  'show_error', '2177'),
 (
  'show_input', '2178'),
 (
  'validation_operator', 'XlVo'),
 (
  'validation_type', '2179'),
 (
  'allocation_method', 'CL30'),
 (
  'allocation_value', 'CL29'),
 (
  'allocation_weight_expression', 'CL31'),
 (
  'order', 'CL22'),
 (
  'pivot_cell', 'CL24'),
 (
  'tuple', 'CL27'),
 (
  'value', 'CL28'),
 (
  'visible_in_pivot_table', 'CL23'),
 (
  'vertical_page_break_type', '1724'),
 (
  'web_page_keywords', '2410'),
 (
  'web_page_title', '2409'),
 (
  'active_pane', '1106'),
 (
  'date_grouping', '2534'),
 (
  'display_formulas', '1110'),
 (
  'display_gridlines', '1111'),
 (
  'display_headings', '1112'),
 (
  'display_horizontal_scroll_bar', '1113'),
 (
  'display_outline', '1114'),
 (
  'display_vertical_scroll_bar', '1116'),
 (
  'display_workbook_tabs', '1117'),
 (
  'display_zeros', '1118'),
 (
  'enable_resize', '1119'),
 (
  'freeze_panes', '1120'),
 (
  'gridline_color', '1121'),
 (
  'gridline_color_index', '1122'),
 (
  'range_selection', '1130'),
 (
  'selected_sheets', '1134'),
 (
  'split', '1136'),
 (
  'split_column', '1137'),
 (
  'split_horizontal', '1138'),
 (
  'split_row', '1139'),
 (
  'split_vertical', '1140'),
 (
  'tab_ratio', '1141'),
 (
  'view', '1149'),
 (
  'window_number', '1146'),
 (
  'window_state', '1147'),
 (
  'window_type', '1142'),
 (
  '_default_', 'CL20'),
 (
  'description', 'CL19'),
 (
  'name', 'CL18'),
 (
  'ranges', 'CL24'),
 (
  'type', 'CL21'),
 (
  'accept_labels_in_formulas', '1796'),
 (
  'accuracy_version', '1340'),
 (
  'auto_update_frequency', '1797'),
 (
  'auto_update_save_changes', '1798'),
 (
  'change_history_duration', '1799'),
 (
  'conflict_resolution', '1805'),
 (
  'create_backup', '1807'),
 (
  'date_1904', '1809'),
 (
  'default_pivottable_style', '2619'),
 (
  'default_table_style', 'DTS3'),
 (
  'display_drawing_objects', '1811'),
 (
  'enable_auto_recover', '2557'),
 (
  'excel_8_compatibility_mode', '2562'),
 (
  'file_format', '1813'),
 (
  'full_name_urlencoded', '2558'),
 (
  'has_password', '1814'),
 (
  'has_vb_project', '2561'),
 (
  'highlight_changes_on_screen', '1857'),
 (
  'inactive_list_border_visible', '2559'),
 (
  'is_add_in', '1816'),
 (
  'keep_change_history', '1858'),
 (
  'list_changes_on_new_sheet', '1859'),
 (
  'multi_user_editing', '1820'),
 (
  'password', '1872'),
 (
  'personal_view_list_settings', '1822'),
 (
  'personal_view_print_settings', '1823'),
 (
  'precision_as_displayed', '1826'),
 (
  'protect_structure', '1828'),
 (
  'protect_windows', '1829'),
 (
  'read_only', '1830'),
 (
  'read_only_recommended', '1874'),
 (
  'remove_personal_information', '1870'),
 (
  'revision_number', '1835'),
 (
  'save_link_values', '1843'),
 (
  'saved', '1842'),
 (
  'show_conflict_history', '1845'),
 (
  'template_remove_external_data', '1855'),
 (
  'theme', 'pThm'),
 (
  'update_remote_references', '1850'),
 (
  'user_status', '1851'),
 (
  'web_options', 'X301'),
 (
  'workbook_comments', 'XWBc'),
 (
  'write_password', '1873'),
 (
  'write_reserved', '1853'),
 (
  'write_reserved_by', '1854'),
 (
  'protect_scenarios', '1730'),
 (
  'dictionary_lang', 'dila'),
 (
  'adjustment_value', 'mAjv'),
 (
  'bullet_character', 'BtCh'),
 (
  'bullet_font', 'OblF'),
 (
  'bullet_number', 'BlNm'),
 (
  'bullet_start_value', 'bSvu'),
 (
  'bullet_style', 'bStl'),
 (
  'bullet_type', 'BLty'),
 (
  'relative_size', 'BRlS'),
 (
  'use_text_color', 'ButC'),
 (
  'use_text_font', 'bUtf'),
 (
  'accent', '1007'),
 (
  'angle', '1008'),
 (
  'auto_attach', '1009'),
 (
  'auto_length', '1010'),
 (
  'callout_format_length', '1015'),
 (
  'callout_format_type', '1016'),
 (
  'drop', '1012'),
 (
  'drop_type', '1013'),
 (
  'gap', '1014'),
 (
  'callout_format', 'X101'),
 (
  'callout_type', 'coTY'),
 (
  'begin_connected', '2381'),
 (
  'begin_connected_shape', '2382'),
 (
  'begin_connection_site', '2383'),
 (
  'connector_format_type', '2387'),
 (
  'end_connected', '2384'),
 (
  'end_connected_shape', '2385'),
 (
  'end_connection_site', '2386'),
 (
  'back_color', '1019'),
 (
  'back_color_theme_index', 'fBCT'),
 (
  'fill_format_type', '1095'),
 (
  'fore_color', '1027'),
 (
  'fore_color_theme_index', 'fFCT'),
 (
  'gradient_color_type', '1087'),
 (
  'gradient_degree', '1088'),
 (
  'gradient_style', 'XgSy'),
 (
  'gradient_variant', '1090'),
 (
  'pattern', '1028'),
 (
  'preset_gradient_type', '1091'),
 (
  'preset_texture', '1092'),
 (
  'rotate_with_object', 'SsRo'),
 (
  'texture_alignment', 'FfTa'),
 (
  'texture_horizontal_scale', 'pTsX'),
 (
  'texture_name', '1093'),
 (
  'texture_offset_X', 'pToX'),
 (
  'texture_offset_Y', 'pToY'),
 (
  'texture_tile', 'FfTt'),
 (
  'texture_type', '1094'),
 (
  'texture_vertical_scale', 'pTsY'),
 (
  'transparency', '1030'),
 (
  'color_theme_index', 'DThC'),
 (
  'radius', 'GRad'),
 (
  'begin_arrowhead_length', '1020'),
 (
  'begin_arrowhead_style', '1021'),
 (
  'begin_arrowhead_width', '1022'),
 (
  'dash_style', '1023'),
 (
  'end_arrowhead_length', '1024'),
 (
  'end_arrowhead_style', '1025'),
 (
  'end_arrowhead_width', '1026'),
 (
  'arrowhead_length', '2025'),
 (
  'arrowhead_style', '2026'),
 (
  'arrowhead_width', '2027'),
 (
  'theme_color_scheme', 'DTcS'),
 (
  'theme_effect_scheme', 'DTeS'),
 (
  'theme_font_scheme', 'DTfS'),
 (
  'alignment', '1053'),
 (
  'baseline_alignment', 'BlAg'),
 (
  'bullet', 'xbf2'),
 (
  'east_asian_line_break_level', 'FelB'),
 (
  'first_line_indent', 'fLIn'),
 (
  'hanging_punctuation', 'Hfpu'),
 (
  'left_indent', 'IndL'),
 (
  'line_rule_after', 'lRAr'),
 (
  'line_rule_before', 'lRB4'),
 (
  'line_rule_within', 'lRwI'),
 (
  'right_indent', 'IndR'),
 (
  'space_after', 'SpcA'),
 (
  'space_before', 'SpcB'),
 (
  'space_within', 'SpcW'),
 (
  'text_direction', 'txTD'),
 (
  'word_wrap', 'PfWW'),
 (
  'transparency_color', '1044'),
 (
  'transparent_background', '1045'),
 (
  'link_to_file', 'l2Fl'),
 (
  'picture_format', 'X106'),
 (
  'save_with_document', 'SwFl'),
 (
  'reflection_type', 'ReFT'),
 (
  'first_margin', '1Mar'),
 (
  'left_margin', 'lMar'),
 (
  'blur', '1035'),
 (
  'obscured', '1048'),
 (
  'offset_X', '1049'),
 (
  'offset_Y', '1050'),
 (
  'rotate_with_shape', 'SsRs'),
 (
  'shadow_style', 'Swss'),
 (
  'shadow_type', '1051'),
 (
  'size', 'SwSs'),
 (
  'connector_format', 'X294'),
 (
  'connector_type', 'CFTy'),
 (
  'ASCII_name', 'fANm'),
 (
  'auto_rotate_numbers', 'FarN'),
 (
  'base_line_offset', 'fBlO'),
 (
  'bold', 'bold'),
 (
  'caps_type', 'fSCf'),
 (
  'east_asian_name', 'FEnm'),
 (
  'embedable', 'fEbD'),
 (
  'embedded', 'fEbF'),
 (
  'equalize_character_height', 'fEQu'),
 (
  'fill_format', 'X110'),
 (
  'font_color', 'Fclr'),
 (
  'font_color_theme_index', 'FCTI'),
 (
  'font_name', '1056'),
 (
  'font_name_other', 'FNor'),
 (
  'font_size', 'ptsz'),
 (
  'glow_format', 'DGoF'),
 (
  'highlight_color', 'fHlC'),
 (
  'highlight_color_theme_index', 'fHCT'),
 (
  'italic', 'ital'),
 (
  'kerning', 'fKrn'),
 (
  'line_format', 'X103'),
 (
  'reflection_format', 'DReF'),
 (
  'shadow_format', 'X107'),
 (
  'soft_edge_type', 'SeFT'),
 (
  'spacing', 'fSpc'),
 (
  'strike_type', 'fSTf'),
 (
  'subscript', 'sbsc'),
 (
  'superscript', 'spsc'),
 (
  'underline_color', 'fUlC'),
 (
  'underline_color_theme_index', 'fUCT'),
 (
  'underline_style', 'fUls'),
 (
  'word_art_styles_format', 'TEpE'),
 (
  'begin_line_X', 'wLBx'),
 (
  'begin_line_Y', 'wLBy'),
 (
  'end_line_X', 'wLex'),
 (
  'end_line_Y', 'wLey'),
 (
  'has_text', 'TFht'),
 (
  'horizontal_anchor', 'TfHA'),
 (
  'margin_bottom', '2371'),
 (
  'margin_left', '2372'),
 (
  'margin_right', '2373'),
 (
  'margin_top', '2374'),
 (
  'path_format', 'TfPF'),
 (
  'ruler', 'xRul'),
 (
  'text_column', 'Tcl2'),
 (
  'text_range', 'TObj'),
 (
  'threeD_format', 'X109'),
 (
  'vertical_anchor', 'TfVA'),
 (
  'warp_format', 'TfWF'),
 (
  'word_wrap', 'TfWW'),
 (
  'wordart_auto_size', '2427'),
 (
  'wordart_format', 'TEpE'),
 (
  'alternative_text', 'atxt'),
 (
  'auto_shape_type', '2349'),
 (
  'background_style', 'sHBs'),
 (
  'black_white_mode', '2366'),
 (
  'chart', 'X119'),
 (
  'child', 'sHCl'),
 (
  'connection_site_count', '2351'),
 (
  'connector', '2352'),
 (
  'has_chart', 'fCrt'),
 (
  'horizontal_flip', '2355'),
 (
  'hyperlink', 'X239'),
 (
  'parentgroup', 'prng'),
 (
  'rotation', '1703'),
 (
  'shape_on_action', 'ShOa'),
 (
  'shape_style', 'sHSs'),
 (
  'shape_text_frame', 'X295'),
 (
  'shape_type', '2361'),
 (
  'soft_edge_format', 'DSeF'),
 (
  'text_frame', 'X293'),
 (
  'vertical_flip', '2362'),
 (
  'word_art_format', 'X108'),
 (
  'tab_position', 'TSPn'),
 (
  'tab_stop_type', 'TSty'),
 (
  'column_number', 'T2Nm'),
 (
  'auto_margins', '2376'),
 (
  'horizontal_overflow', 'hzno'),
 (
  'vertical_overflow', 'vrto'),
 (
  'RGB', 'tRGB'),
 (
  'theme_color_scheme_index', 'TCSi'),
 (
  'Z_distance', 'TfZd'),
 (
  'bevel_bottom_depth', 'TfBd'),
 (
  'bevel_bottom_inset', 'TfBi'),
 (
  'bevel_bottom_type', 'TfBb'),
 (
  'bevel_top_depth', 'TfTd'),
 (
  'bevel_top_inset', 'TfTi'),
 (
  'bevel_top_type', 'TfBt'),
 (
  'contour_color', 'TfCc'),
 (
  'contour_color_theme_index', 'cCTi'),
 (
  'contour_width', 'TfCw'),
 (
  'depth', '1068'),
 (
  'extrusion_color', '1069'),
 (
  'extrusion_color_theme_index', 'eCTi'),
 (
  'extrusion_color_type', '1070'),
 (
  'field_of_view', 'TfFv'),
 (
  'light_angle', 'TfLa'),
 (
  'perspective', '1071'),
 (
  'preset_camera', 'TfSp'),
 (
  'preset_extrusion_direction', '1072'),
 (
  'preset_lighting_direction', '1073'),
 (
  'preset_lighting_rig', 'TfPl'),
 (
  'preset_lighting_softness', '1074'),
 (
  'preset_material', '1075'),
 (
  'preset_threeD_format', '1076'),
 (
  'project_text', 'TfPt'),
 (
  'rotation_X', '1077'),
 (
  'rotation_Y', '1078'),
 (
  'rotation_Z', 'TfZr'),
 (
  'kerned_pairs', '1057'),
 (
  'normalized_height', '1058'),
 (
  'preset_shape', '1059'),
 (
  'preset_word_art_effect', '4028'),
 (
  'rotated_chars', '1061'),
 (
  'tracking', '1062'),
 (
  'word_art_text', 'XWAt'),
 (
  'content', 'XtCt'),
 (
  'phonetic_characters', '1979'),
 (
  'font_background', 'XfBg'),
 (
  'font_color_index', 'XfcI'),
 (
  'font_style', '1099'),
 (
  'outline_font', '1100'),
 (
  'strikethrough', 'strk'),
 (
  'theme_font_index', '2550'),
 (
  'underline', 'undl'),
 (
  'include_alignment', '1766'),
 (
  'include_border', '1767'),
 (
  'include_font', '1768'),
 (
  'include_number', '1769'),
 (
  'include_patterns', '1770'),
 (
  'include_protection', '1771'),
 (
  'merged_cells', '1588'),
 (
  'number_format_local', '1594'),
 (
  'bound_height', 'TRbh'),
 (
  'bound_left', 'TRlb'),
 (
  'bound_top', 'TRtb'),
 (
  'bound_width', 'TRbw'),
 (
  'font', 'X111'),
 (
  'paragraph_format', 'xpf2'),
 (
  'text_length', 'TRln'),
 (
  'text_start', 'TRst'),
 (
  'areas', '1520'),
 (
  'column_width', '1536'),
 (
  'count_large', 'XCcs'),
 (
  'current_array', '1541'),
 (
  'current_region', '1542'),
 (
  'dependents', '1548'),
 (
  'direct_dependents', '1550'),
 (
  'direct_precedents', '1551'),
 (
  'display_format', 'X306'),
 (
  'entire_column', '1553'),
 (
  'entire_row', '1554'),
 (
  'first_column_index', 'XfcX'),
 (
  'first_row_index', 'XfrX'),
 (
  'formula_array', '1563'),
 (
  'formula_label', '1564'),
 (
  'formula_local', '1566'),
 (
  'formula_r1c1', '1567'),
 (
  'formula_r1c1_local', '1568'),
 (
  'has_array', '1572'),
 (
  'has_formula', '1573'),
 (
  'list_header_rows', '1581'),
 (
  'list_object', 'X244'),
 (
  'location_in_table', '1583'),
 (
  'merge_area', '1587'),
 (
  'named_item', 'X220'),
 (
  'outline_level', '1597'),
 (
  'page_break', '1598'),
 (
  'phonetic_object', '1637'),
 (
  'pivot_field', 'X157'),
 (
  'pivot_item', 'X160'),
 (
  'pivot_table', 'X155'),
 (
  'precedents', '1604'),
 (
  'prefix_character', '1605'),
 (
  'row_height', '1611'),
 (
  'use_standard_height', '1625'),
 (
  'use_standard_width', '1626'),
 (
  'validation', 'X237'),
 (
  'worksheet_object', '1632'),
 (
  'Automatically_expand_tables_as_I_type', 'Expd'),
 (
  'Automatically_fill_formulas', 'AtFF'),
 (
  'correct_caps_lock', '2216'),
 (
  'correct_days', '2209'),
 (
  'correct_initial_caps', '2214'),
 (
  'correct_sentence_caps', '2215'),
 (
  'replace_text', '2213'),
 (
  'axis_title_text', 'AtTx'),
 (
  'chart_fill_format_object', 'XCFf'),
 (
  'include_in_layout', '1985'),
 (
  'axis_between_categories', '2223'),
 (
  'axis_group', 'AgOb'),
 (
  'axis_title', 'X257'),
 (
  'axis_type', 'XAty'),
 (
  'base_unit', '2250'),
 (
  'base_unit_is_auto', '2251'),
 (
  'category_names', '2226'),
 (
  'category_type', '2254'),
 (
  'chart_format', 'X115'),
 (
  'crosses', '2227'),
 (
  'crosses_at', '2228'),
 (
  'display_unit', '2255'),
 (
  'display_unit_custom', '2256'),
 (
  'display_unit_label', 'X299'),
 (
  'has_display_unit_label', '2257'),
 (
  'has_major_gridlines', '2229'),
 (
  'has_minor_gridlines', '2230'),
 (
  'has_title', '1689'),
 (
  'log_base', '2258'),
 (
  'major_gridlines', '2231'),
 (
  'major_tick_mark', '2232'),
 (
  'major_unit', '2233'),
 (
  'major_unit_is_auto', '2234'),
 (
  'major_unit_scale', '2252'),
 (
  'maximum_scale', '2235'),
 (
  'maximum_scale_is_auto', '2236'),
 (
  'minimum_scale', '2237'),
 (
  'minimum_scale_is_auto', '2238'),
 (
  'minor_gridlines', '2239'),
 (
  'minor_tick_mark', '2240'),
 (
  'minor_unit', '2241'),
 (
  'minor_unit_is_auto', '2242'),
 (
  'minor_unit_scale', '2253'),
 (
  'reverse_plot_order', '2243'),
 (
  'scale_type', '2244'),
 (
  'tick_label_position', '2245'),
 (
  'tick_label_spacing', '2247'),
 (
  'tick_label_spacing_is_auto', '2259'),
 (
  'tick_labels', 'X282'),
 (
  'tick_mark_spacing', '2248'),
 (
  'background_scheme_color', 'bgSC'),
 (
  'chart_fill_format_type', '2221'),
 (
  'foreground_scheme_color', 'fgSC'),
 (
  'bubble_scale', '2277'),
 (
  'doughnut_hole_size', '2260'),
 (
  'down_bars_object', 'XdbO'),
 (
  'drop_lines_object', 'XdlO'),
 (
  'first_slice_angle', '2263'),
 (
  'gap_width', '2264'),
 (
  'has_drop_lines', '2265'),
 (
  'has_hi_lo_lines', '2266'),
 (
  'has_radar_axis_labels', '2267'),
 (
  'has_series_lines', '2268'),
 (
  'has_threeD_shading', '2282'),
 (
  'has_up_down_bars', '2269'),
 (
  'hilo_lines_Object', 'XhlO'),
 (
  'overlap', '2271'),
 (
  'radar_axis_labels', '2272'),
 (
  'second_plot_size', '2281'),
 (
  'series_lines_object', 'XslO'),
 (
  'show_negative_bubbles', '2278'),
 (
  'size_represents', '2276'),
 (
  'split_type', '2279'),
 (
  'split_value', '2280'),
 (
  'up_bars_object', 'XubO'),
 (
  'vary_by_categories', '2275'),
 (
  'protect_chart_object', '2107'),
 (
  'chart_title_text', 'XctT'),
 (
  'area_threeD_group', '1663'),
 (
  'auto_scaling', '1665'),
 (
  'back_wall', '2429'),
 (
  'bar_shape', '1713'),
 (
  'bar_threeD_group', '1668'),
 (
  'chart_area_object', '1670'),
 (
  'chart_style', '2433'),
 (
  'chart_title', 'X256'),
 (
  'chart_type', '1708'),
 (
  'column_threeD_group', '1675'),
 (
  'corners_object', 'XcrO'),
 (
  'data_table_object', '1678'),
 (
  'depth_percent', '1679'),
 (
  'display_blanks_as', '1681'),
 (
  'elevation', '1683'),
 (
  'floor_object', '1455'),
 (
  'gap_depth', '1684'),
 (
  'has_data_table', '1687'),
 (
  'has_legend', '1688'),
 (
  'height_percent', '1690'),
 (
  'legend_object', '1691'),
 (
  'line_threeD_group', 'C3DG'),
 (
  'pie_threeD_group', '1697'),
 (
  'plot_area_object', '1699'),
 (
  'plot_by', '1714'),
 (
  'plot_visible_only', '1700'),
 (
  'protect_data', '1716'),
 (
  'protect_formatting', '1715'),
 (
  'protect_goal_seek', '1717'),
 (
  'protect_selection', '1718'),
 (
  'right_angle_axes', '1702'),
 (
  'show_data_labels_over_maximum', '2434'),
 (
  'show_window', '1706'),
 (
  'side_wall', '2428'),
 (
  'size_with_window', '1705'),
 (
  'surface_group', '1707'),
 (
  'walls_and_gridlines_twoD', '1711'),
 (
  'walls_object', '1710'),
 (
  'auto_text', '2313'),
 (
  'data_label_text', 'XdlT'),
 (
  'data_label_type', '2316'),
 (
  'number_format_linked', '2314'),
 (
  'show_legend_key', '2315'),
 (
  'has_border_horizontal', '2333'),
 (
  'has_border_outline', '2335'),
 (
  'has_border_vertical', '2334'),
 (
  'display_label_unit_text', 'DLuT'),
 (
  'end_style', '2332'),
 (
  'picture_type', '2292'),
 (
  'thickness', 'Thck'),
 (
  'invert_if_negative', '2218'),
 (
  'linear_gradient', 'X302'),
 (
  'pattern_color', '2219'),
 (
  'pattern_color_index', '2220'),
 (
  'pattern_theme_color', '2536'),
 (
  'pattern_tint_and_shade', '2537'),
 (
  'rectangular_gradient', 'X303'),
 (
  'legend_key', 'X269'),
 (
  'marker_background_color', '2286'),
 (
  'marker_background_color_index', '2287'),
 (
  'marker_foreground_color', '2288'),
 (
  'marker_foreground_color_index', '2289'),
 (
  'marker_size', '2290'),
 (
  'marker_style', '2291'),
 (
  'picture_unit', '2293'),
 (
  'smooth', '2304'),
 (
  'inside_height', '2330'),
 (
  'inside_left', '2327'),
 (
  'inside_top', '2328'),
 (
  'inside_width', '2329'),
 (
  'apply_pict_to_end', '2296'),
 (
  'apply_pict_to_front', '2295'),
 (
  'apply_pict_to_sides', '2294'),
 (
  'data_label_object', 'XdlO'),
 (
  'explosion', '2284'),
 (
  'has_data_label', '2285'),
 (
  'has_threeD_effect', '2310'),
 (
  'secondary_plot', '2297'),
 (
  'apply_picture_to_end', '2296'),
 (
  'apply_picture_to_front', '2295'),
 (
  'apply_picture_to_sides', '2294'),
 (
  'bubble_sizes', '2309'),
 (
  'error_bars', 'X286'),
 (
  'has_data_labels', '2301'),
 (
  'has_error_bars', '2302'),
 (
  'has_leader_lines', '2311'),
 (
  'leader_lines', 'X277'),
 (
  'plot_color_index', 'pcli'),
 (
  'plot_order', '2303'),
 (
  'series_values', 'XsrV'),
 (
  'xvalues', '2308'),
 (
  'multi_level', '2312'),
 (
  'offset', '2326'),
 (
  'tick_alignment', 'XtAl'),
 (
  'backward', '2318'),
 (
  'display_R_squared', '2320'),
 (
  'display_equation', '2319'),
 (
  'forward', '2321'),
 (
  'intercept', '1481'),
 (
  'intercept_is_auto', '2322'),
 (
  'name_is_auto', '2323'),
 (
  'period', '2324'),
 (
  'trendline_type', '2325')]
elements = [
 (
  'base_documents', 'bDoc'),
 (
  'basic_windows', 'bwin'),
 (
  'command_bar_buttons', 'mCBB'),
 (
  'command_bar_comboboxes', 'mCBX'),
 (
  'command_bar_controls', 'mCBC'),
 (
  'command_bar_popups', 'mCBP'),
 (
  'command_bars', 'msCB'),
 (
  'custom_document_properties', 'mCDP'),
 (
  'document_properties', 'mDPr'),
 (
  'Excel_comments', 'X229'),
 (
  'ODBC_errors', 'X235'),
 (
  'active_filters', 'Y903'),
 (
  'add_ins', 'X133'),
 (
  'applications', 'capp'),
 (
  'autofilters', 'X240'),
 (
  'borders', 'X251'),
 (
  'buttons', 'Xbtn'),
 (
  'calculated_fields', 'XPFc'),
 (
  'calculated_items', 'XPIi'),
 (
  'calculated_members', 'X901'),
 (
  'checkboxes', 'Xckb'),
 (
  'child_items', 'XPIc'),
 (
  'column_fields', 'XPFn'),
 (
  'column_items', 'XPIo'),
 (
  'cube_fields', 'X900'),
 (
  'custom_views', 'X225'),
 (
  'data_fields', 'XPFd'),
 (
  'dialogs', 'X165'),
 (
  'documents', 'docu'),
 (
  'dropdowns', 'XdpD'),
 (
  'filters', 'X242'),
 (
  'format_conditions', 'X227'),
 (
  'graphics', 'X308'),
 (
  'groupboxes', 'XGBc'),
 (
  'hidden_fields', 'XPFh'),
 (
  'hidden_items', 'XPIh'),
 (
  'horizontal_page_breaks', 'X122'),
 (
  'hyperlinks', 'X239'),
 (
  'international_macro_sheets', 'XiSH'),
 (
  'labels', 'Xlbl'),
 (
  'list_columns', 'X248'),
 (
  'list_objects', 'X244'),
 (
  'list_rows', 'X246'),
 (
  'listboxes', 'XLbx'),
 (
  'macro_sheets', 'XmSH'),
 (
  'named_items', 'X220'),
 (
  'option_buttons', 'XObn'),
 (
  'outlines', 'X212'),
 (
  'page_fields', 'XPFp'),
 (
  'page_setups', 'X218'),
 (
  'panes', 'X189'),
 (
  'parent_items', 'XPIp'),
 (
  'phonetics', 'X288'),
 (
  'pivot_caches', 'X151'),
 (
  'pivot_fields', 'X157'),
 (
  'pivot_filters', 'X903'),
 (
  'pivot_formulas', 'X153'),
 (
  'pivot_items', 'X160'),
 (
  'pivot_lines', 'X907'),
 (
  'pivot_tables', 'X155'),
 (
  'query_tables', 'X231'),
 (
  'recent_files', 'X125'),
 (
  'row_fields', 'XPFr'),
 (
  'row_items', 'XPIr'),
 (
  'scenarios', 'X191'),
 (
  'scrollbars', 'XSrl'),
 (
  'sheets', 'X128'),
 (
  'slicers', 'X906'),
 (
  'spinners', 'XSpn'),
 (
  'table_style_elements', 'TSET'),
 (
  'table_styles', '1936'),
 (
  'textboxes', 'XTbx'),
 (
  'validations', 'X237'),
 (
  'vertical_page_breaks', 'X121'),
 (
  'windows', 'cwin'),
 (
  'workbooks', 'X141'),
 (
  'worksheets', 'XwSH'),
 (
  'adjustments', 'mAdj'),
 (
  'arcs', 'Xarc'),
 (
  'callout_formats', 'X101'),
 (
  'callouts', 'cD00'),
 (
  'connector_formats', 'X294'),
 (
  'fill_formats', 'X110'),
 (
  'gradient_stops', 'GrdS'),
 (
  'line_formats', 'X103'),
 (
  'lines', 'Xlne'),
 (
  'major_theme_fonts', '1ThF'),
 (
  'minor_theme_fonts', '2ThF'),
 (
  'ovals', 'XOvl'),
 (
  'picture_formats', 'X106'),
 (
  'pictures', 'cD04'),
 (
  'rectangles', 'XRct'),
 (
  'ruler_levels', 'xRlL'),
 (
  'shadow_formats', 'X107'),
 (
  'shape_connectors', 'cD01'),
 (
  'shape_lines', 'cD12'),
 (
  'shape_text_frames', 'X295'),
 (
  'shape_textboxes', 'cD07'),
 (
  'shapes', 'pShp'),
 (
  'tab_stops', 'Tab2'),
 (
  'text_frames', 'X293'),
 (
  'theme_fonts', 'DThF'),
 (
  'threeD_formats', 'X109'),
 (
  'word_art_formats', 'X108'),
 (
  'characters', 'cha '),
 (
  'fonts', 'X111'),
 (
  'paragraphs', 'cpar'),
 (
  'sentences', 'csen'),
 (
  'styles', 'X129'),
 (
  'text_flows', 'cflo'),
 (
  'text_range_characters', 'TrCh'),
 (
  'text_range_lines', 'TrLn'),
 (
  'words', 'cwor'),
 (
  'cells', 'ccel'),
 (
  'columns', 'ccol'),
 (
  'ranges', 'X117'),
 (
  'rows', 'crow'),
 (
  'area_groups', 'cg01'),
 (
  'axis_titles', 'X257'),
 (
  'axes', 'X255'),
 (
  'bar_groups', 'cg05'),
 (
  'chart_areas', 'X284'),
 (
  'chart_fill_formats', 'X253'),
 (
  'chart_groups', 'X258'),
 (
  'chart_objects', 'X221'),
 (
  'chart_sheets', 'XcSH'),
 (
  'chart_titles', 'X256'),
 (
  'charts', 'X119'),
 (
  'column_groups', 'cg04'),
 (
  'data_labels', 'X265'),
 (
  'data_tables', 'X287'),
 (
  'display_unit_labels', 'X299'),
 (
  'doughnut_groups', 'cg03'),
 (
  'floors', 'X280'),
 (
  'interiors', 'X252'),
 (
  'legend_entries', 'X267'),
 (
  'legend_keys', 'X269'),
 (
  'legends', 'X285'),
 (
  'line_groups', 'cg02'),
 (
  'pie_groups', 'cg06'),
 (
  'plot_areas', 'X283'),
 (
  'radar_groups', 'cg07'),
 (
  'series_points', 'X262'),
 (
  'series_collection', 'X263'),
 (
  'trendlines', 'X271'),
 (
  'walls_collection', 'X281'),
 (
  'xy_groups', 'cg09'),
 (
  'xlspelling_options', 'Xspo'),
 (
  'error_bars', 'X286'),
 (
  'pivot_cell', 'X908'),
 (
  'up_bars', 'X278'),
 (
  'tick_labels', 'X282'),
 (
  'rectangular_gradient', 'X303'),
 (
  'format_color', 'X307'),
 (
  'icon_criterion', 'X317'),
 (
  'theme_effect_scheme', 'DTeS'),
 (
  'format_condition_icon_object', 'X318'),
 (
  'workbook_connection', 'X904'),
 (
  'databar_border', 'X313'),
 (
  'web_page_font', 'mWPF'),
 (
  'soft_edge_format', 'DSeF'),
 (
  'databar_format_condition', 'X312'),
 (
  'negative_bar_format', 'X314'),
 (
  'default_web_options', 'X300'),
 (
  'color_scale_criterion', 'X311'),
 (
  'sort', 'Xsrt'),
 (
  'treeview_control', 'X911'),
 (
  'autocorrect', 'X250'),
 (
  'reflection_format', 'DReF'),
 (
  'down_bars', 'X279'),
 (
  'theme_color', 'DThC'),
 (
  'text_column', 'Tcl2'),
 (
  'format_condition_icon_sets', 'X320'),
 (
  'colorstops', 'X304'),
 (
  'unique_values_format_condition', 'X323'),
 (
  'office_theme', 'DOfT'),
 (
  'ruler', 'xRul'),
 (
  'theme_font_scheme', 'DTfS'),
 (
  'corners', 'X272'),
 (
  'above_average_format_condition', 'X322'),
 (
  'leader_lines', 'X277'),
 (
  'color_scale_format_condition', 'X325'),
 (
  'drop_lines', 'X276'),
 (
  'chart_format', 'X115'),
 (
  'sortfields', 'Xsfs'),
 (
  'paragraph_format', 'xpf2'),
 (
  'colorstop', 'X305'),
 (
  'linear_gradient', 'X302'),
 (
  'Protection', 'Xpot'),
 (
  'display_format', 'X306'),
 (
  'format_condition_icon_set', 'X319'),
 (
  'condition_value', 'X324'),
 (
  'base_application', 'cbap'),
 (
  'icon_criteria', 'X316'),
 (
  'base_object', 'oItm'),
 (
  'bullet_format', 'xbf2'),
 (
  'value_change', 'X905'),
 (
  'tab', 'Xtab'),
 (
  'web_options', 'X301'),
 (
  'print_settings', 'pset'),
 (
  'text_range', 'TObj'),
 (
  'pivot_axis', 'X902'),
 (
  'glow_format', 'DGoF'),
 (
  'top_10_format_condition', 'X321'),
 (
  'color_scale_criteria', 'X310'),
 (
  'shape_font', 'Fon2'),
 (
  'gridlines', 'X275'),
 (
  'icon_set_format_condition', 'X315'),
 (
  'series_lines', 'X273'),
 (
  'sortfield', 'Xsfd'),
 (
  'theme_color_scheme', 'DTcS'),
 (
  'hilo_lines', 'X274')]
commands = [
 (
  'protect_workbook',
  'smXLXPTw',
  [
   (
    'password', '5236'), ('structure', '5293'), ('windows', '1192')]),
 (
  'preset_drop', 'sDRw1006', [('drop_type', '5004')]),
 (
  'intersect',
  'smXL1182',
  [
   (
    'range1', 'XLr1'),
   (
    'range2', 'XLr2'),
   (
    'range3', 'XLr3'),
   (
    'range4', 'XLr4'),
   (
    'range5', 'XLr5'),
   (
    'range6', 'XLr6'),
   (
    'range7', 'XLr7'),
   (
    'range8', 'XLr8'),
   (
    'range9', 'XLr9'),
   (
    'range10', 'Xr10'),
   (
    'range11', 'Xr11'),
   (
    'range12', 'Xr12'),
   (
    'range13', 'Xr13'),
   (
    'range14', 'Xr14'),
   (
    'range15', 'Xr15'),
   (
    'range16', 'Xr16'),
   (
    'range17', 'Xr17'),
   (
    'range18', 'Xr18'),
   (
    'range19', 'Xr19'),
   (
    'range20', 'Xr20'),
   (
    'range21', 'Xr21'),
   (
    'range22', 'Xr22'),
   (
    'range23', 'Xr23'),
   (
    'range24', 'Xr24'),
   (
    'range25', 'Xr25'),
   (
    'range26', 'Xr26'),
   (
    'range27', 'Xr27'),
   (
    'range28', 'Xr28'),
   (
    'range29', 'Xr29'),
   (
    'range30', 'Xr30')]),
 (
  'get_end', 'sTBL1552', [('direction', '5165')]),
 (
  'delete_chart_autoformat', 'smXL1235', [('name', 'pnam')]),
 (
  'quit', 'aevtquit', [('saving', 'savo')]),
 (
  'chart_one_color_gradient',
  'sCRTXc1c',
  [
   (
    'gradient_style', 'XgSy'), ('variant', '5008'), ('degree', '5009')]),
 (
  'user_textured', 'sDRw1086', [('texture_file', '5013')]),
 (
  'select', 'coreslct', []),
 (
  'get_international', 'smXL1266', [('data_type', '5216')]),
 (
  'apply_layout', 'sCRTACLo', [('layout', '5358'), ('chart_type', '5359')]),
 (
  'check_spelling_for',
  'smXLXcsW',
  [
   (
    'text_to_check', '5080'),
   (
    'custom_dictionary', '5081'),
   (
    'ignore_uppercase', '5082')]),
 (
  'change_link',
  'smXL1802',
  [
   (
    'name', 'pnam'), ('new_name', '5289'), ('type', '5103')]),
 (
  'load_theme_font_scheme', 'sDRwlTFS', [('file_name', '5015')]),
 (
  'update', 'smXL1938', []),
 (
  'find_previous', 'sTBL1560', [('after_', '5167')]),
 (
  'chart_patterned', 'sCRT1080', [('pattern', '1028')]),
 (
  'link_info',
  'smXL1817',
  [
   (
    'name', 'pnam'), ('link_info', '1817'), ('type', '5103')]),
 (
  'cancel_refresh', 'smXL2132', []),
 (
  'get_file_converters', 'smXL1252', []),
 (
  'add_chart_autoformat',
  'smXL1199',
  [
   (
    'chart', '5075'), ('name', 'pnam'), ('description', '5076')]),
 (
  'print_preview', 'smXL1129', [('enable_changes', '5029')]),
 (
  'merge_workbook', 'smXL1819', [('file_name', '5016')]),
 (
  'remove_user', 'smXL1834', [('entry_index', 'MSix')]),
 (
  'remove_item', 'smXLXrMI', [('entry_index', 'MSix'), ('count', '1000')]),
 (
  'apply', 'sDRw2337', []),
 (
  'subtotal_location', 'smXLCJ32', [('location', '6038')]),
 (
  'clear_circles', 'smXL1762', []),
 (
  'activate_previous', 'smXL1103', []),
 (
  'discard_change', 'smXLCK03', []),
 (
  'load_theme_color_scheme', 'sDRwlTCS', [('file_name', '5016')]),
 (
  'autofit', 'sTBL1524', []),
 (
  'ungroup', 'sDRw1624', []),
 (
  'parse', 'sTBL1599', [('parse_line', '5190'), ('destination', '5134')]),
 (
  'clear_colorstops', 'smXL2547', []),
 (
  'get', 'coregetd', [('as_', 'rtyp')]),
 (
  'allocate_change', 'smXLCK02', []),
 (
  'calculate_full', 'smXL1338', []),
 (
  'user_picture', 'sDRw1085', [('picture_file', '5012')]),
 (
  'clear_to_match_style', 'sCRT2434', []),
 (
  'get_dialog', 'smXLXgDg', []),
 (
  'exclusive_access', 'smXL1812', []),
 (
  'auto_show',
  'smXL1970',
  [
   (
    'type', '5103'),
   (
    'range', '5312'),
   (
    'count', '1000'),
   (
    'field', '5135')]),
 (
  'set', 'coresetd', [('to', 'data')]),
 (
  'add_item_to_list',
  'smXLXAIL',
  [
   (
    'item_text', 'DITx'), ('entry_index', 'MSix')]),
 (
  'run_XLM_Macro',
  'smXL1186',
  [
   (
    'arg1', '5040'),
   (
    'arg2', '5041'),
   (
    'arg3', '5042'),
   (
    'arg4', '5043'),
   (
    'arg5', '5044'),
   (
    'arg6', '5045'),
   (
    'arg7', '5046'),
   (
    'arg8', '5047'),
   (
    'arg9', '5048'),
   (
    'arg10', '5049'),
   (
    'arg11', '5050'),
   (
    'arg12', '5051'),
   (
    'arg13', '5052'),
   (
    'arg14', '5053'),
   (
    'arg15', '5054'),
   (
    'arg16', '5055'),
   (
    'arg17', '5056'),
   (
    'arg18', '5057'),
   (
    'arg19', '5058'),
   (
    'arg20', '5059'),
   (
    'arg21', '5060'),
   (
    'arg22', '5061'),
   (
    'arg23', '5062'),
   (
    'arg24', '5063'),
   (
    'arg25', '5064'),
   (
    'arg26', '5065'),
   (
    'arg27', '5066'),
   (
    'arg28', '5067'),
   (
    'arg29', '5068'),
   (
    'arg30', '5069')]),
 (
  'modify_condition_value',
  'smXL2563',
  [
   (
    'type', '5103'), ('condition_value', '5389')]),
 (
  'protect_chart',
  'sCRTXPTc',
  [
   (
    'password', '5236'),
   (
    'drawing_objects', '5237'),
   (
    'chart_contents', 'XcCt'),
   (
    'user_interface_only', '5240')]),
 (
  'clear_outline', 'sTBL1534', []),
 (
  'modify_sort_key', 'smXL2528', [('rng', '5385')]),
 (
  'duplicate', 'coreclon', [('to', 'insh')]),
 (
  'error_bar',
  'sCRT2299',
  [
   (
    'direction', '5165'),
   (
    'include', '5337'),
   (
    'type', '5103'),
   (
    'amount', '5338'),
   (
    'minus_values', '5339')]),
 (
  'create_cube_file',
  'smXLCJ18',
  [
   (
    'file', '6032'),
   (
    'measures', '6033'),
   (
    'levels', '6034'),
   (
    'members', '6035'),
   (
    'properties', '6036')]),
 (
  'pick_up', 'sDRw2342', []),
 (
  'Excel_comment_text',
  'smXLXCmT',
  [
   (
    'text', 'ctxt'), ('start', '5144'), ('over_write', '5321')]),
 (
  'refresh', 'smXL1722', []),
 (
  'commit_changes', 'smXLCJ57', []),
 (
  'create_new_document',
  'smXL2188',
  [
   (
    'file_name', '5262'), ('edit_now', '5328'), ('overwrite', '5321')]),
 (
  'remove_subtotal', 'sTBL1608', []),
 (
  'insert_into_range', 'sTBLXiiR', [('shift', '5164')]),
 (
  'group',
  'sTBL1571',
  [
   (
    'start', '5144'),
   (
    'end_', '5180'),
   (
    'by', '5181'),
   (
    'periods', '5182')]),
 (
  'run_XLM_macro',
  'sTBL1186',
  [
   (
    'arg1', '5040'),
   (
    'arg2', '5041'),
   (
    'arg3', '5042'),
   (
    'arg4', '5043'),
   (
    'arg5', '5044'),
   (
    'arg6', '5045'),
   (
    'arg7', '5046'),
   (
    'arg8', '5047'),
   (
    'arg9', '5048'),
   (
    'arg10', '5049'),
   (
    'arg11', '5050'),
   (
    'arg12', '5051'),
   (
    'arg13', '5052'),
   (
    'arg14', '5053'),
   (
    'arg15', '5054'),
   (
    'arg16', '5055'),
   (
    'arg17', '5056'),
   (
    'arg18', '5057'),
   (
    'arg19', '5058'),
   (
    'arg20', '5059'),
   (
    'arg21', '5060'),
   (
    'arg22', '5061'),
   (
    'arg23', '5062'),
   (
    'arg24', '5063'),
   (
    'arg25', '5064'),
   (
    'arg26', '5065'),
   (
    'arg27', '5066'),
   (
    'arg28', '5067'),
   (
    'arg29', '5068'),
   (
    'arg30', '5069')]),
 (
  'help_',
  'smXL1262',
  [
   (
    'help_file', '5099'), ('help_context_id', '5100')]),
 (
  'apply_names',
  'sTBL1518',
  [
   (
    'names', '1183'),
   (
    'ignore_relative_absolute', '5128'),
   (
    'use_row_column_names', '5129'),
   (
    'omit_column', '5130'),
   (
    'omit_row', '5131'),
   (
    'order', '5132'),
   (
    'append_last', '5133')]),
 (
  'merge', 'sTBL1585', [('across', '5184')]),
 (
  'unprotect', 'smXL1660', [('password', '5236')]),
 (
  'union',
  'smXL1191',
  [
   (
    'range1', 'XLr1'),
   (
    'range2', 'XLr2'),
   (
    'range3', 'XLr3'),
   (
    'range4', 'XLr4'),
   (
    'range5', 'XLr5'),
   (
    'range6', 'XLr6'),
   (
    'range7', 'XLr7'),
   (
    'range8', 'XLr8'),
   (
    'range9', 'XLr9'),
   (
    'range10', 'Xr10'),
   (
    'range11', 'Xr11'),
   (
    'range12', 'Xr12'),
   (
    'range13', 'Xr13'),
   (
    'range14', 'Xr14'),
   (
    'range15', 'Xr15'),
   (
    'range16', 'Xr16'),
   (
    'range17', 'Xr17'),
   (
    'range18', 'Xr18'),
   (
    'range19', 'Xr19'),
   (
    'range20', 'Xr20'),
   (
    'range21', 'Xr21'),
   (
    'range22', 'Xr22'),
   (
    'range23', 'Xr23'),
   (
    'range24', 'Xr24'),
   (
    'range25', 'Xr25'),
   (
    'range26', 'Xr26'),
   (
    'range27', 'Xr27'),
   (
    'range28', 'Xr28'),
   (
    'range29', 'Xr29'),
   (
    'range30', 'Xr30')]),
 (
  'copy_text_range', 'sTXTPytr', []),
 (
  'clear_combobox', 'sMSOZCCB', []),
 (
  'chart_user_textured', 'sCRTXuTd', [('texture_file', '5013')]),
 (
  'fill_up', 'sTBL1558', []),
 (
  'remove_all_items', 'smXLXrAi', []),
 (
  'clear', 'sCRT1530', []),
 (
  'change_connection', 'smXLCJ48', [('connection', '6040')]),
 (
  'paste_text_range', 'sTXTPStr', []),
 (
  'get_rotated_text_bounds', 'sTXTTRRb', []),
 (
  'begin_connect',
  'sDRw2377',
  [
   (
    'connected_shape', '5345'), ('connection_site', '5346')]),
 (
  'end_connect',
  'sDRw2379',
  [
   (
    'connected_shape', '5345'), ('connection_site', '5346')]),
 (
  'add_periods_to', 'sTXTTRaP', []),
 (
  'create_pivot_fields', 'smXLCL02', []),
 (
  'web_page_preview', 'smXL1868', []),
 (
  'get_address_local',
  'sTBL1516',
  [
   (
    'row_absolute', '5121'),
   (
    'column_absolute', '5122'),
   (
    'reference_style', '1297'),
   (
    'external', '5123'),
   (
    'relative_to', '5087')]),
 (
  'custom_drop', 'sDRw1004', [('drop', '5002')]),
 (
  'insert_indent', 'sTBL1577', [('insert_amount', '5183')]),
 (
  'get_pivot_data',
  'smXLCJ06',
  [
   (
    'data_field', '6000'),
   (
    'field1', '6001'),
   (
    'item1', '6002'),
   (
    'field2', '6003'),
   (
    'item2', '6004'),
   (
    'field3', '6005'),
   (
    'item3', '6006'),
   (
    'field4', '6007'),
   (
    'item4', '6008'),
   (
    'field5', '6009'),
   (
    'item5', '6010'),
   (
    'field6', '6011'),
   (
    'item6', '6012'),
   (
    'field7', '6013'),
   (
    'item7', '6014'),
   (
    'field8', '6015'),
   (
    'item8', '6016'),
   (
    'field9', '6017'),
   (
    'item9', '6018'),
   (
    'field10', '6019'),
   (
    'item10', '6020'),
   (
    'field11', '6021'),
   (
    'item11', '6022'),
   (
    'field12', '6023'),
   (
    'item12', '6024'),
   (
    'field13', '6025'),
   (
    'item13', '6026'),
   (
    'field14', '6027'),
   (
    'item14', '6028')]),
 (
  'change_pivot_cache', 'smXLCJ49', [('pivot_cache', '6041')]),
 (
  'data_series',
  'sTBL1544',
  [
   (
    'rowcol', '5158'),
   (
    'data_series_type', 'XdsT'),
   (
    'date', '5159'),
   (
    'increment', 'XBzo'),
   (
    'stop', 'XBny'),
   (
    'trend', '1370')]),
 (
  'modify_applies_to_range', 'smXL2572', [('range', '5387')]),
 (
  'delete_custom_list', 'smXL1236', [('list_num', '5088')]),
 (
  'activate_object', 'smXLxACT', []),
 (
  'update_from_file', 'smXL1848', []),
 (
  'move', 'coremove', [('to', 'insh')]),
 (
  'list_names', 'sTBL1582', []),
 (
  'clear_arrows', 'smXL1735', []),
 (
  'chart_two_color_gradient',
  'sCRTXc2G',
  [
   (
    'gradient_style', 'XgSy'), ('variant', '5008')]),
 (
  'data_table',
  'sTBLXdtF',
  [
   (
    'row_input', '5214'), ('column_input', '5215')]),
 (
  'convert_to_formulas', 'smXLCJ42', [('convert_filters', '6039')]),
 (
  'sort_special',
  'sTBL1620',
  [
   (
    'sort_method', '5206'),
   (
    'key1', '5198'),
   (
    'order1', '5199'),
   (
    'type', '5103'),
   (
    'key2', '5200'),
   (
    'order2', '5201'),
   (
    'key3', '5202'),
   (
    'order3', '5203'),
   (
    'header', '5204'),
   (
    'order_custom', '5205'),
   (
    'match_case', '5172'),
   (
    'orientation', '1596'),
   (
    'dataoption1', '5376'),
   (
    'dataoption2', '5377'),
   (
    'dataoption3', '5378')]),
 (
  'preset_textured', 'sDRw1082', [('preset_texture', '5011')]),
 (
  'chart_location', 'sCRTXcLo', [('where', '5260'), ('name', 'pnam')]),
 (
  'check_out', 'smXL2555', [('file_name', 'Cofn')]),
 (
  'send_to_back', 'smXL1988', []),
 (
  'highlight_changes_options',
  'smXL1856',
  [
   (
    'when', '5298'), ('who', '5299'), ('where', '5260')]),
 (
  'save_workbook_as',
  'smXLxSwA',
  [
   (
    'filename', '5016'),
   (
    'file_format', '1813'),
   (
    'password', '5236'),
   (
    'write_reservation_password', '5242'),
   (
    'read_only_recommended', '5243'),
   (
    'create_backup', '5244'),
   (
    'access_mode', '5296'),
   (
    'conflict_resolution', '1805'),
   (
    'add_to_most_recently_used_list', '5245'),
   (
    'overwrite', '5321')]),
 (
  'apply_filter', 'smXL2531', []),
 (
  'get_border', 'smXLXBtr', [('which_border', 'wWbr')]),
 (
  'row_axis_layout', 'smXLCJ31', [('layout', '6037')]),
 (
  'fill_right', 'sTBL1557', []),
 (
  'paste', 'sCRT1696', []),
 (
  'clear_formats', 'sCRT1532', []),
 (
  'print_out',
  'smXL1128',
  [
   (
    'from_', '5022'),
   (
    'to', '5023'),
   (
    'copies', '5024'),
   (
    'preview', '5025'),
   (
    'active_printer', '5026'),
   (
    'print_to_file', '5027'),
   (
    'collate', '5028')]),
 (
  'send_html_mail', 'smXLSeHM', []),
 (
  'set_sort_range', 'smXL2516', [('rng', '5379')]),
 (
  'cut_range', 'sTBL1543', [('destination_of_cut', '5134')]),
 (
  'text_to_columns',
  'sTBL1623',
  [
   (
    'destination', '5134'),
   (
    'data_type', '5216'),
   (
    'text_qualifier', '5217'),
   (
    'consecutive_delimiter', '5218'),
   (
    'tab', '5219'),
   (
    'semicolon', '5220'),
   (
    'comma', '5221'),
   (
    'space', '5222'),
   (
    'use_other', 'XuOr'),
   (
    'other_char', '5224'),
   (
    'field_info', '5225'),
   (
    'decimal_separator', '5226'),
   (
    'thousands_separator', '5227')]),
 (
  'solid', 'sDRw1083', []),
 (
  'execute', 'sMSOmEXC', []),
 (
  'scroll_workbook_tabs',
  'smXL1133',
  [
   (
    'sheets', '5030'), ('position', '5031')]),
 (
  'get_combobox_item', 'sMSOZGCI', [('entry_index', 'MSix')]),
 (
  'large_scroll',
  'smXL1124',
  [
   (
    'down', '5018'),
   (
    'up', '5019'),
   (
    'to_right', '5020'),
   (
    'to_left', '5021')]),
 (
  'set_background_picture', 'smXL1667', [('picture_file_name', 'XpFN')]),
 (
  'find_next', 'sTBL1559', [('after_', '5167')]),
 (
  'get_list_item', 'smXLXgLi', [('entry_index', 'MSix')]),
 (
  'make',
  'corecrel',
  [
   (
    'new', 'kocl'),
   (
    'at', 'insh'),
   (
    'with_data', 'data'),
   (
    'with_properties', 'prdt')]),
 (
  'add_sortfield',
  'smXL2518',
  [
   (
    'key', '5380'),
   (
    'sorton', '5381'),
   (
    'order', '5382'),
   (
    'customorder', '5383'),
   (
    'dataoption', '5384')]),
 (
  'save_as',
  'smXL1659',
  [
   (
    'filename', '5016'),
   (
    'file_format', '1813'),
   (
    'password', '5236'),
   (
    'write_reservation_password', '5242'),
   (
    'read_only_recommended', '5243'),
   (
    'create_backup', '5244'),
   (
    'add_to_most_recently_used_list', '5245'),
   (
    'overwrite', '5321'),
   (
    'save_as_local_language', 'locl')]),
 (
  'set_subtotals',
  'smXL1956',
  [
   (
    'subtotal_index', 'XSTT'), ('value', 'XSTv')]),
 (
  'refresh_data_source_values', 'smXLCJ59', []),
 (
  'set_first_priority', 'smXL2569', []),
 (
  'run_VB_macro',
  'sTBL2620',
  [
   (
    'arg1', '5040'),
   (
    'arg2', '5041'),
   (
    'arg3', '5042'),
   (
    'arg4', '5043'),
   (
    'arg5', '5044'),
   (
    'arg6', '5045'),
   (
    'arg7', '5046'),
   (
    'arg8', '5047'),
   (
    'arg9', '5048'),
   (
    'arg10', '5049'),
   (
    'arg11', '5050'),
   (
    'arg12', '5051'),
   (
    'arg13', '5052'),
   (
    'arg14', '5053'),
   (
    'arg15', '5054'),
   (
    'arg16', '5055'),
   (
    'arg17', '5056'),
   (
    'arg18', '5057'),
   (
    'arg19', '5058'),
   (
    'arg20', '5059'),
   (
    'arg21', '5060'),
   (
    'arg22', '5061'),
   (
    'arg23', '5062'),
   (
    'arg24', '5063'),
   (
    'arg25', '5064'),
   (
    'arg26', '5065'),
   (
    'arg27', '5066'),
   (
    'arg28', '5067'),
   (
    'arg29', '5068'),
   (
    'arg30', '5069')]),
 (
  'protect_sharing',
  'smXL1827',
  [
   (
    'file_name', '5016'),
   (
    'password', '5236'),
   (
    'write_reservation_password', '5242'),
   (
    'read_only_recommended', '5243'),
   (
    'create_backup', '5244'),
   (
    'sharing_password', '5294'),
   (
    'file_format', '5388')]),
 (
  'paste_series', 'sCRTXsPt', []),
 (
  'insert_text_text_range',
  'sTXTTRIt',
  [
   (
    'insert_where', 'epiP'), ('new_text', 'epNT')]),
 (
  'clear_all_filters', 'smXLCJ35', []),
 (
  'fill_down', 'sTBL1555', []),
 (
  'get_resize',
  'sTBL1609',
  [
   (
    'row_size', '5195'), ('column_size', '5196')]),
 (
  'save_as_picture',
  'sDRwOSaP',
  [
   (
    'picture_type', '5016'), ('file_name', '5015')]),
 (
  'end_disconnect', 'sDRw2380', []),
 (
  'double_click', 'smXL1247', []),
 (
  'activate_next', 'smXL1102', []),
 (
  'advanced_filter',
  'sTBL1517',
  [
   (
    'action', '5124'),
   (
    'criteria_range', '5125'),
   (
    'copy_to_range', '5126'),
   (
    'unique', '5127')]),
 (
  'paste_chart', 'sCRTXprt', [('format', '5140')]),
 (
  'copy_worksheet', 'smXLXcpW', [('before_', '5235'), ('after_', '5167')]),
 (
  'get_count_of_combobox_items', 'sMSOZCCi', []),
 (
  'navigate_arrow',
  'sTBL1589',
  [
   (
    'toward_precedent', '5185'),
   (
    'arrow_number', '5186'),
   (
    'link_number', '5187')]),
 (
  'run_VB_Macro',
  'smXL2620',
  [
   (
    'arg1', '5040'),
   (
    'arg2', '5041'),
   (
    'arg3', '5042'),
   (
    'arg4', '5043'),
   (
    'arg5', '5044'),
   (
    'arg6', '5045'),
   (
    'arg7', '5046'),
   (
    'arg8', '5047'),
   (
    'arg9', '5048'),
   (
    'arg10', '5049'),
   (
    'arg11', '5050'),
   (
    'arg12', '5051'),
   (
    'arg13', '5052'),
   (
    'arg14', '5053'),
   (
    'arg15', '5054'),
   (
    'arg16', '5055'),
   (
    'arg17', '5056'),
   (
    'arg18', '5057'),
   (
    'arg19', '5058'),
   (
    'arg20', '5059'),
   (
    'arg21', '5060'),
   (
    'arg22', '5061'),
   (
    'arg23', '5062'),
   (
    'arg24', '5063'),
   (
    'arg25', '5064'),
   (
    'arg26', '5065'),
   (
    'arg27', '5066'),
   (
    'arg28', '5067'),
   (
    'arg29', '5068'),
   (
    'arg30', '5069')]),
 (
  'autofill', 'sTBL1522', [('destination', '5134'), ('type', '5103')]),
 (
  'one_color_gradient',
  'sDRw1079',
  [
   (
    'gradient_style', 'XgSy'), ('variant', '5008'), ('degree', '5009')]),
 (
  'reroute_connections', 'sDRw2343', []),
 (
  'get_open_filename',
  'smXL1259',
  [
   (
    'file_filter', '5091'),
   (
    'button_text', '5094'),
   (
    'multi_select', '5095')]),
 (
  'show_pages', 'smXL1894', [('page_field', '5311')]),
 (
  'clear_range', 'sTBLXrgC', []),
 (
  'get_values', 'smXL2024', []),
 (
  'follow',
  'smXL2184',
  [
   (
    'new_window', '1125'),
   (
    'extra_info', '5304'),
   (
    'method', '5305'),
   (
    'header_info', '5306')]),
 (
  'unmerge', 'sTBL1586', []),
 (
  'convert_formula',
  'smXL1217',
  [
   (
    'formula_to_convert', '5083'),
   (
    'from_reference_style', '5084'),
   (
    'to_reference_style', '5085'),
   (
    'to_absolute', '5086'),
   (
    'relative_to', '5087')]),
 (
  'send_mail', 'smXLSeML', []),
 (
  'can_check_in', 'smXL2553', []),
 (
  'preset_gradient',
  'sDRw1081',
  [
   (
    'gradient_style', 'XgSy'),
   (
    'variant', '5008'),
   (
    'preset_gradient_type', '5010')]),
 (
  'link_sources', 'smXL1818', [('type', '5103')]),
 (
  'open_links',
  'smXL1821',
  [
   (
    'name', 'pnam'), ('read_only', '5291'), ('type', '5103')]),
 (
  'reset_rotation', 'sDRw1065', []),
 (
  'clear_contents', 'smXL1531', []),
 (
  'deselect', 'sCRT1680', []),
 (
  'count', 'corecnte', [('each', 'kocl')]),
 (
  'get_registered_functions', 'smXL1298', []),
 (
  'calculate_full_rebuild', 'smXLLLni', []),
 (
  'add_item_to_combobox',
  'sMSOZAIB',
  [
   (
    'combobox_item', 'Z001'), ('entry_index', 'MSix')]),
 (
  'get_webpage_font', 'smXLwGwF', []),
 (
  'clear_label_filters', 'smXLCK44', []),
 (
  'consolidate',
  'sTBL1537',
  [
   (
    'sources', '5150'),
   (
    'consolidation_function', 'XcdF'),
   (
    'top_row', '5152'),
   (
    'left_column', '5153'),
   (
    'create_links', '5154')]),
 (
  'auto_outline', 'sTBL1526', []),
 (
  'add_data_validation',
  'smXL2168',
  [
   (
    'type', '5103'),
   (
    'alert_style', '5327'),
   (
    'operator', '2120'),
   (
    'formula1', '2121'),
   (
    'formula2', '2122')]),
 (
  'modify_condition',
  'smXLXMFc',
  [
   (
    'type', '5103'),
   (
    'operator', '5137'),
   (
    'formula1', '5319'),
   (
    'formula2', '5320'),
   (
    'string', '5390'),
   (
    'operator2', '5391')]),
 (
  'z_order', 'sDRw1990', [('z_order_command', '5344')]),
 (
  'save', 'coresave', [('in_', 'kfil'), ('as_', 'fltp')]),
 (
  'save_theme_color_scheme', 'sDRwsTCS', [('file_name', '5016')]),
 (
  'list_formulas', 'smXL1922', []),
 (
  'resize', 'smXL2510', [('range', '5387')]),
 (
  'apply_data_labels',
  'sCRT1662',
  [
   (
    'type', '5103'),
   (
    'legend_key', '5248'),
   (
    'auto_text', '5249'),
   (
    'has_leader_lines', '5250'),
   (
    'show_series_name', '5352'),
   (
    'show_category_name', '5353'),
   (
    'show_value', '5354'),
   (
    'show_percentage', '5355'),
   (
    'show_bubble_size', '5356'),
   (
    'separator', '5357')]),
 (
  'delete_colorstop', 'smXL2549', []),
 (
  'update_link', 'smXL1849', [('name', 'pnam'), ('type', '5103')]),
 (
  'use_default_folder_suffix', 'smXL2408', []),
 (
  'fill_left', 'sTBL1556', []),
 (
  'copy_object', 'smXLXcpO', []),
 (
  'dirty', 'sTBLXCcv', []),
 (
  'clear_sortfields', 'smXL2519', []),
 (
  'change_file_access',
  'smXL1801',
  [
   (
    'mode', '1500'), ('write_password', '5287'), ('notify', '5288')]),
 (
  'replace',
  'sTBL1393',
  [
   (
    'what', '5166'),
   (
    'replacement', '5194'),
   (
    'look_at', '5169'),
   (
    'search_order', '5170'),
   (
    'match_case', '5172'),
   (
    'match_byte', '5173'),
   (
    'match_control_characters', '5174'),
   (
    'match_diacritics', '5175')]),
 (
  'modify',
  'smXL2118',
  [
   (
    'type', '5103'),
   (
    'alert_style', '2169'),
   (
    'operator', '2120'),
   (
    'formula1', '2121'),
   (
    'formula2', '2122')]),
 (
  'close', 'coreclos', [('saving', 'savo'), ('saving_in', 'kfil')]),
 (
  'arrange_windows',
  'smXLXaWs',
  [
   (
    'arrange_style', 'XaSy'),
   (
    'active_workbook', '1172'),
   (
    'sync_horizontal', 'XAsh'),
   (
    'sync_vertical', 'XAsV')]),
 (
  'flip', 'sDRw2338', [('flip_cmd', '5340')]),
 (
  'allocate_changes', 'smXLCJ56', []),
 (
  'create_pivot_table',
  'smXLCJ76',
  [
   (
    'table_destination', '6043'),
   (
    'table_name', '6044'),
   (
    'read_data', '6045'),
   (
    'default_version', '6046')]),
 (
  'begin_disconnect', 'sDRw2378', []),
 (
  'discard_changes', 'smXLCJ58', []),
 (
  'auto_sort',
  'smXL1969',
  [
   (
    'sort_order', 'XsrO'), ('sort_field', 'XsrF')]),
 (
  'open_xml',
  'smXLXCdq',
  [
   (
    'filename', 'BoPf'),
   (
    'style_sheets', 'BoGf'),
   (
    'load_option', 'BoKf')]),
 (
  'get_clipboard_formats', 'smXL1213', []),
 (
  'get_previous_selections', 'smXL1291', []),
 (
  'inches_to_points', 'smXL1263', [('inches', '5101')]),
 (
  'preset_chart_textured',
  'sCRTXpCt',
  [
   (
    'preset_texture_for_chart', '5011')]),
 (
  'item_selected', 'smXLXLis', [('entry_index', 'MSix')]),
 (
  'Excel_repeat', 'smXL1300', []),
 (
  'scale_width',
  'sDRwsScW',
  [
   (
    'factor', 'ep01'),
   (
    'relative_to_original_size', 'ep02'),
   (
    'scale', 'ep03')]),
 (
  'special_cells', 'sTBL1621', [('type', '5103'), ('value', 'DPVu')]),
 (
  'border_around',
  'sTBL1527',
  [
   (
    'line_style', '5143'),
   (
    'weight', '1031'),
   (
    'color_index', '1098'),
   (
    'color', 'colr')]),
 (
  'remove_periods_from', 'sTXTTRrP', []),
 (
  'get_custom_list_contents', 'smXL1257', [('list_num', '5088')]),
 (
  'new_window_on_workbook', 'smXLXnWw', []),
 (
  'change_scenario',
  'smXL2022',
  [
   (
    'changing_cells', '5313'), ('values', '5314')]),
 (
  'reset_timer', 'smXLQtRt', []),
 (
  'input_box',
  'smXL1264',
  [
   (
    'prompt', '5102'),
   (
    'title', '5093'),
   (
    'default', '1233'),
   (
    'left_position', 'plft'),
   (
    'top', 'ptop'),
   (
    'type', '5103')]),
 (
  'open_text_file',
  'smXLXoTx',
  [
   (
    'filename', '5016'),
   (
    'origin', 'XoDw'),
   (
    'start_row', 'XoSW'),
   (
    'data_type', '5216'),
   (
    'text_qualifier', '5217'),
   (
    'consecutive_delimiter', '5218'),
   (
    'tab', '5219'),
   (
    'semicolon', '5220'),
   (
    'comma', '5221'),
   (
    'space', '5222'),
   (
    'use_other', 'XuOr'),
   (
    'other_char', '5224'),
   (
    'field_info', '5225'),
   (
    'decimal_separator', '5226'),
   (
    'thousands_separator', '5227')]),
 (
  'clear_value_filters', 'smXLCK43', []),
 (
  'two_color_gradient',
  'sDRw1084',
  [
   (
    'gradient_style', 'XgSy'), ('variant', '5008')]),
 (
  'toggle_forms_design', 'smXLXPTz', []),
 (
  'chart_user_picture',
  'sCRTXcup',
  [
   (
    'picture_file', '5012'),
   (
    'picture_format', '5334'),
   (
    'picture_stack_unit', '5335'),
   (
    'picture_placement', '5336')]),
 (
  'apply_custom_chart_type',
  'sCRTXAcC',
  [
   (
    'chart_type', '1708'), ('chart_name', '5261')]),
 (
  'show_all', 'smXL2532', []),
 (
  'set_bullet_picture', 'sDRwBlPc', [('FileName', 'xpBF')]),
 (
  'remove_an_item_from_combobox', 'sMSOZRCI', [('entry_index', 'MSix')]),
 (
  'get_address',
  'sTBL1515',
  [
   (
    'row_absolute', '5121'),
   (
    'column_absolute', '5122'),
   (
    'reference_style', '1297'),
   (
    'external', '5123'),
   (
    'relative_to', '5087')]),
 (
  'create_summary_for_scenarios',
  'smXLXcSs',
  [
   (
    'report_type', 'XRpT'), ('result_cells', 'XRtC')]),
 (
  'toggle_vertical_text', 'sDRw1052', []),
 (
  'reset_colors', 'smXL1863', []),
 (
  'protect_worksheet',
  'smXLXPTs',
  [
   (
    'password', '5236'),
   (
    'drawing_objects', '5237'),
   (
    'worksheet_contents', 'XwsC'),
   (
    'scenarios', '5239'),
   (
    'user_interface_only', '5240'),
   (
    'allow_formatting_cells', '5362'),
   (
    'allow_formatting_columns', '5363'),
   (
    'allow_formatting_rows', '5364'),
   (
    'allow_inserting_columns', '5365'),
   (
    'allow_inserting_rows', '5366'),
   (
    'allow_inserting_hyperlinks', '5367'),
   (
    'allow_deleting_columns', '5368'),
   (
    'allow_deleting_rows', '5369'),
   (
    'allow_sorting', '5370'),
   (
    'allow_filtering', '5371'),
   (
    'allow_using_pivot_table', '5372')]),
 (
  'purge_change_history_now',
  'smXL1860',
  [
   (
    'days', '5300'), ('sharing_password', '5294')]),
 (
  'row_differences', 'sTBL1610', [('comparison', '5149')]),
 (
  'copy_range', 'sTBLXcpR', [('destination', '5134')]),
 (
  'get_pivot_table_data', 'smXL1921', [('name', 'pnam')]),
 (
  'clear_manual_filter', 'smXLCK41', []),
 (
  'show_levels',
  'smXL2049',
  [
   (
    'row_levels', '5316'), ('column_levels', '5317')]),
 (
  'show_errors', 'sTBL1616', []),
 (
  'get_FileMaker_criteria', 'smXL2161', [('criteria_index', '5323')]),
 (
  'save_as_ODC',
  'smXLCJ86',
  [
   (
    'ODC_file_name', '6047'),
   (
    'description', '6048'),
   (
    'keywords', '6049')]),
 (
  'set_combobox_item',
  'sMSOZSCI',
  [
   (
    'entry_index', 'MSix'), ('combobox_item', 'Z001')]),
 (
  'get_visible_fields', 'smXL1912', []),
 (
  'accept_all_changes',
  'smXL1861',
  [
   (
    'when', '5298'), ('who', '5299'), ('where', '5260')]),
 (
  'check_in',
  'smXL2552',
  [
   (
    'save_changes', 'Spc1'),
   (
    'comments', 'Spc2'),
   (
    'make_public', 'Spc3')]),
 (
  'clear_table', 'smXLCJ27', []),
 (
  'data_size', 'coredsiz', [('as_', 'rtyp')]),
 (
  'exists', 'coredoex', []),
 (
  'function_wizard', 'sTBL1569', []),
 (
  'autofilter_range',
  'sTBL1523',
  [
   (
    'field', '5135'),
   (
    'criteria1', '5136'),
   (
    'operator', '5137'),
   (
    'criteria2', '5138'),
   (
    'visible_drop_down', '5139')]),
 (
  'subtotal',
  'sTBL1506',
  [
   (
    'group_by', '5210'),
   (
    'function', '5151'),
   (
    'total_list', '5211'),
   (
    'replace', '1393'),
   (
    'page_breaks', '5212'),
   (
    'summary_below_data', '5213')]),
 (
  'bring_to_front', 'smXL1984', []),
 (
  'print',
  'aevtpdoc',
  [
   (
    'with_properties', 'prdt'), ('print_dialog', 'pdlg')]),
 (
  'set_list_item',
  'smXLXSli',
  [
   (
    'entry_index', 'MSix'), ('item_text', '5038')]),
 (
  'insert_into', 'sTXT1578', [('string', '5039')]),
 (
  'clear_Excel_comments', 'sTBL1636', []),
 (
  'reject_all_changes',
  'smXL1862',
  [
   (
    'when', '5298'), ('who', '5299'), ('where', '5260')]),
 (
  'delete_sortfield', 'smXL2527', []),
 (
  'copy_picture', 'smXL1539', [('appearance', '5155'), ('format', '5140')]),
 (
  'change_case', 'sTXTTRcc', [('to', 'p#CC')]),
 (
  'repeat_all_labels', 'smXLCJ60', [('repeat', '6042')]),
 (
  'show_precedents', 'sTBL1617', [('remove', '5197')]),
 (
  'set_XML_value', 'sTBL1629', [('range_value', 'XrgV')]),
 (
  'automatic_length', 'sDRw1003', []),
 (
  'sort',
  'sTBL1619',
  [
   (
    'key1', '5198'),
   (
    'order1', '5199'),
   (
    'key2', '5200'),
   (
    'sort_type', 'Styp'),
   (
    'order2', '5201'),
   (
    'key3', '5202'),
   (
    'order3', '5203'),
   (
    'header', '5204'),
   (
    'order_custom', '5205'),
   (
    'match_case', '5172'),
   (
    'orientation', '1596'),
   (
    'sort_method', '5206'),
   (
    'ignore_control_characters', '5207'),
   (
    'ignore_diacritics', '5208'),
   (
    'dataoption1', '5373'),
   (
    'dataoption2', '5374'),
   (
    'dataoption3', '5375')]),
 (
  'clear_range_formats', 'sTBL1532', []),
 (
  'add_colorstop', 'smXL2546', [('position', 'posn')]),
 (
  'delete_gradient_stop', 'sDRwdGrd', [('stop_index', 'igSI')]),
 (
  'paste_special',
  'sTBL1600',
  [
   (
    'what', '5166'),
   (
    'operation', '5192'),
   (
    'skip_blanks', '5193'),
   (
    'transpose', '1383')]),
 (
  'clear_hyperlinks', 'sTBLXCcw', []),
 (
  'justify', 'sTBL1580', []),
 (
  'merge_scenarios', 'smXLXMss', [('merge_source', 'XmSr')]),
 (
  'load_theme_effect_scheme', 'sDRwlTES', [('file_name', '5015')]),
 (
  'convert_to_range', 'smXL2201', []),
 (
  'get_axis', 'sCRTXGAx', [('axis_type', 'XAty'), ('which_axis', '5251')]),
 (
  'calculate_row_major_order', 'sTBLXCcu', []),
 (
  'apply_sort', 'smXL2517', []),
 (
  'scale_height',
  'sDRwsScH',
  [
   (
    'factor', 'ep01'),
   (
    'relative_to_original_size', 'ep02'),
   (
    'scale', 'ep03')]),
 (
  'circle_invalid', 'smXL1763', []),
 (
  'set_last_priority', 'smXL2570', []),
 (
  'save_theme_font_scheme', 'sDRwsTFS', [('file_name', '5015')]),
 (
  'delete_replacement', 'sPRF2210', [('what', '5166')]),
 (
  'reset', 'sMSOmFBr', []),
 (
  'cut', 'smXL1543', []),
 (
  'delete_number_format', 'smXL1810', [('number_format', '1593')]),
 (
  'refresh_all', 'smXL1831', []),
 (
  'show', 'smXL1613', []),
 (
  'delete', 'coredelo', []),
 (
  'show_data_form', 'smXL1751', []),
 (
  'delete_range', 'sTBLXdRg', [('shift', '5164')]),
 (
  'paste_special_on_worksheet',
  'smXLXpsW',
  [
   (
    'format', '5140'),
   (
    'link', '5265'),
   (
    'display_as_icon', '5266'),
   (
    'icon_file_name', '5267'),
   (
    'icon_index', '5268'),
   (
    'icon_label', '5269'),
   (
    'no_HTML_formatting', 'nofm')]),
 (
  'add_data_field',
  'smXLCJ09',
  [
   (
    'field', '6029'), ('caption', '6030'), ('function', '6031')]),
 (
  'undo', 'smXL1318', []),
 (
  'show_dependents', 'sTBL1614', [('remove', '5197')]),
 (
  'chart_solid', 'sCRTXcSd', []),
 (
  'next_Excel_comment', 'smXLXnxC', []),
 (
  'can_check_out', 'smXL2556', [('file_name', 'Cofn')]),
 (
  'get_has_axis',
  'sCRT1685',
  [
   (
    'axis_type', 'XAty'), ('axis_group', '5251')]),
 (
  'add_page_item', 'smXLCK24', [('item', '6053'), ('clear_list', '6054')]),
 (
  'apply_theme', 'smXLxlTh', [('file_name', '5015')]),
 (
  'add_fields_to_pivot_table',
  'smXL1890',
  [
   (
    'row_fields', '5307'),
   (
    'column_fields', '5308'),
   (
    'page_fields', '5309'),
   (
    'add_to_table', '5310')]),
 (
  'open_workbook',
  'smXL1169',
  [
   (
    'workbook_file_name', 'WbFN'),
   (
    'update_links', 'XOul'),
   (
    'read_only', '5291'),
   (
    'format', '5140'),
   (
    'password', '5236'),
   (
    'write_reserved_password', 'XoRP'),
   (
    'ignore_read_only_recommended', 'XoiR'),
   (
    'origin', 'XoDw'),
   (
    'delimiter', 'XoDL'),
   (
    'editable', 'XoEd'),
   (
    'notify', '5288'),
   (
    'converter', 'XoCV'),
   (
    'add_to_mru', '5245')]),
 (
  'reset_all_page_breaks', 'smXL1744', []),
 (
  'goal_seek', 'sTBL1570', [('goal', '5178'), ('changing_cell', '5179')]),
 (
  'add_comment', 'sTBL1634', [('comment_text', 'XCmT')]),
 (
  'on_key',
  'smXL1283',
  [
   (
    'key', '5110'),
   (
    'command_key_pressed', 'XcKP'),
   (
    'shift_key_pressed', 'XsKP'),
   (
    'option_key_pressed', 'XoKP'),
   (
    'control_key_pressed', 'XrKP'),
   (
    'procedure', '5111')]),
 (
  'cut_text_range', 'sTXTpCtr', []),
 (
  'set_source_data', 'sCRT1720', [('source', '5252'), ('plot_by', '1714')]),
 (
  'preset_chart_gradient',
  'sCRTXpCg',
  [
   (
    'gradient_style', 'XgSy'),
   (
    'variant', '5008'),
   (
    'preset_gradient_type', '5010')]),
 (
  'goto', 'smXL1261', [('reference', '5097'), ('scroll', '5098')]),
 (
  'autoformat',
  'sTBL1525',
  [
   (
    'format', '5140'),
   (
    'include_number', '5141'),
   (
    'font', '5142'),
   (
    'alignment', '1053'),
   (
    'border', '1011'),
   (
    'pattern', '1028'),
   (
    'width', 'pwid')]),
 (
  'get_custom_list_num', 'smXL1258', [('list_array', '5077')]),
 (
  'evaluate', 'smXL2435', [('name', 'pnam')]),
 (
  'insert_gradient_stop',
  'sDRwiGrd',
  [
   (
    'custom_color', 'igCC'),
   (
    'position', 'posn'),
   (
    'transparency', 'igTR'),
   (
    'stop_index', 'igSI')]),
 (
  'refresh_table', 'smXL1905', []),
 (
  'patterned', 'sDRw1080', [('pattern', '1028')]),
 (
  'get_offset',
  'sTBL1595',
  [
   (
    'row_offset', '5188'), ('column_offset', '5189')]),
 (
  'get_subtotals', 'smXL1955', [('subtotal_index', 'XSTT')]),
 (
  'register_xll', 'smXL1299', [('filename', '5016')]),
 (
  'column_differences', 'sTBL1535', [('comparison', '5149')]),
 (
  'get_XML_value', 'sTBL1628', []),
 (
  'remove_duplicates', 'sTBLXCcr', []),
 (
  'previous_Excel_comment', 'smXLXpvC', []),
 (
  'follow_hyperlink',
  'smXL1865',
  [
   (
    'address', '5301'),
   (
    'sub_address', '5302'),
   (
    'new_window', '1125'),
   (
    'extra_info', '5304'),
   (
    'method', '5305'),
   (
    'header_info', '5306')]),
 (
  'open_data_base',
  'smXLOpdb',
  [
   (
    'filename', 'BoDf'),
   (
    'command_text', 'BoDe'),
   (
    'rcommand_type', 'BoDg'),
   (
    'back_ground_query', 'BoDh'),
   (
    'import_data_as', 'BoDi')]),
 (
  'custom_length', 'sDRw1005', [('length', '5003')]),
 (
  'check_spelling',
  'smXL1212',
  [
   (
    'custom_dictionary', '5081'),
   (
    'ignore_uppercase', '5082'),
   (
    'always_suggest', '5145')]),
 (
  'find',
  'sTBL1395',
  [
   (
    'what', '5166'),
   (
    'after_', '5167'),
   (
    'look_in', '5168'),
   (
    'look_at', '5169'),
   (
    'search_order', '5170'),
   (
    'search_direction', '5171'),
   (
    'match_case', '5172'),
   (
    'match_byte', '5173')]),
 (
  'get_chart_element', 'sCRT1719', [('x', '5230'), ('y', '5231')]),
 (
  'delete_object', 'sCRTXdel', []),
 (
  'check_in_with_version',
  'smXL2554',
  [
   (
    'save_changes', 'Spc1'),
   (
    'comments', 'Spc2'),
   (
    'make_public', 'Spc3'),
   (
    'version_type', 'Spc4')]),
 (
  'autocomplete', 'sTBL1521', [('string', '5039')]),
 (
  'calculate', 'smXL1175', []),
 (
  'get_custom_color', 'sDRwtGCC', [('name', 'pnam')]),
 (
  'add_member_property_field',
  'smXLCK97',
  [
   (
    'property', '6062'),
   (
    'property_order', '6063'),
   (
    'property_displayed_in', '6064')]),
 (
  'unprotect_sharing', 'smXL1847', [('sharing_password', '5294')]),
 (
  'open', 'aevtodoc', []),
 (
  'pivot_select', 'smXL1933', [('name', 'pnam'), ('mode', '1500')]),
 (
  'small_scroll',
  'smXL1135',
  [
   (
    'down', '5018'),
   (
    'up', '5019'),
   (
    'to_right', '5020'),
   (
    'to_left', '5021')]),
 (
  'show_all_data', 'smXL1750', []),
 (
  'add_replacement',
  'sPRF2208',
  [
   (
    'text_to_replace', 'Xt2R'), ('replacement_text', 'XRtx')]),
 (
  'set_shapes_default_properties', 'sDRw2346', []),
 (
  'centimeters_to_points', 'smXL1211', [('centimeters', '5079')]),
 (
  'refresh_query_table', 'smXLXrQT', [('background_query', '1878')]),
 (
  'create_names',
  'sTBL1540',
  [
   (
    'top', 'ptop'),
   (
    'left_position', 'plft'),
   (
    'bottom', '5156'),
   (
    'right', '5157')]),
 (
  'set_FileMaker_criteria',
  'smXL2160',
  [
   (
    'criteria_index', '5323'),
   (
    'field_name', '5324'),
   (
    'operator', '2120'),
   (
    'clause_text', '5325'),
   (
    'condition', '5326')]),
 (
  'break_link', 'smXL1871', [('name', 'pnam'), ('type', '5103')]),
 (
  'save_workspace', 'smXL1302', [('workspace_file_name', 'WsFN')]),
 (
  'get_save_as_filename',
  'smXL1260',
  [
   (
    'initial_filename', '5096'),
   (
    'file_filter', '5091'),
   (
    'filter_index', '5092'),
   (
    'button_text', '5094')]),
 (
  'open_FileMaker_file', 'smXLXoFM', [('filename', '5016')]),
 (
  'paste_worksheet',
  'smXL1696',
  [
   (
    'destination', '5134'), ('link', '5265')]),
 (
  'set_chart_element', 'sCRT2432', [('chart_element', '5360')]),
 (
  'apply_outline_styles', 'sTBL1519', []),
 (
  'set_has_axis',
  'sCRT1686',
  [
   (
    'axis_exists', 'XAXt'), ('axis_type', 'XAty'), ('axis_group', '5251')]),
 (
  'make_connection', 'smXLCJ80', []),
 (
  'copy_chart_as_picture',
  'sCRTXCcp',
  [
   (
    'appearance', '5155'), ('format', '5140'), ('output_size', 'XopZ')]),
 (
  'add_custom_list',
  'smXL1200',
  [
   (
    'list_array', '5077'), ('by_row', '5078')]),
 (
  'drill_to', 'smXLCK26', [('field', '6055')]),
 (
  'get_replacement_list', 'sPRF2211', []),
 (
  'chart_wizard',
  'sCRT1674',
  [
   (
    'source', '5252'),
   (
    'gallery', '5118'),
   (
    'format', '5140'),
   (
    'plot_by', '5253'),
   (
    'category_labels', '5254'),
   (
    'series_labels', '5255'),
   (
    'has_legend', '5256'),
   (
    'title', '5093'),
   (
    'category_title', '5257'),
   (
    'value_title', '5258'),
   (
    'extra_title', '5259')]),
 (
  'show_custom_view', 'smXLXsCv', [])]