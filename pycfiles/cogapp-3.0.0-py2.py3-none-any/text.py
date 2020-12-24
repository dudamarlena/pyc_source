# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/cogandmem/text.py
# Compiled at: 2018-06-23 15:24:19
__doc__ = '\nFunctions for displaying text to the screen.\n\nText rendering in pygame does not allow for line breaks. This can lead to\nissues when attempting to render text, particularly if one is unsure of the\nwidth and height of a to-be-rendered string in a given font. The functions\nhere handle these difficulties.\n\nThis module includes the following functions (see the docstrings for more\ninformation):\n    tallest_letter: returns the height in pixels of the tallest letter when\nrendered in a given font.\n    text_to_sentences: convert a string into a list of sentences.\n    screen_dimensions: returns the dimensions of the active display surface.\n    longest_string_to_render: return the string in a list that will take up\nthe most horizontal space in pixels (this will usually, but not necessarily,\nbe the string with the most characters).\n    height_of_strings: return the height of a list of strings when rendered in\na given font.\n    wrap_text: break a string into lines on a screen.\n    string_to_screens_and_lines: break a string into screens and lines.\n    render_string: get pygame.Surface and pygame.Rect objects for a string.\n    render_lines: return pygame.Surface and pygame.Rect objects for a list of\nstrings.\n    string_to_surface_and_rect: return pygame.Surface and pygame.Rect objects\nfor a string, given constraints on the pixel dimensions of the screen.\n    display_text_until_keypress: present text to the screen until the user\npresses a specific key (or any specific key from a list).\n    ask_question: display a question to the screen and return the response.\n'
from __future__ import division
import sys, pygame
from pygame.locals import *
import experiment, generic
LETTERS = (
 K_a, K_b, K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, K_m,
 K_n, K_o, K_p, K_q, K_r, K_s, K_t, K_u, K_v, K_w, K_x, K_y, K_z)
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
NUMBERS = (
 K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9)
PUNCTUATION = (
 K_PERIOD, K_COMMA, K_QUESTION, K_QUOTE, K_EXCLAIM, K_COLON, K_SEMICOLON)

def tallest_letter(font):
    """
    Get the height, in pixels, of the tallest letter in the alphabet when
    rendered with a given font.
    """
    return font.size(ALPHABET)[1]


def text_to_sentences(text, terminators=('.', '?', '!', '."', '?"', '!"'), exclude=('Mr.', 'Ms.', 'Mrs.', 'Dr.', 'e.g.', 'i.e.')):
    """
    Break text into a list of sentences.
    
    This is a highly imperfect function that takes a passage of text and
    breaks it into a list of sentences. The main stumbling block for the
    function is that there are numerous words that could indicate either the
    end of a sentence or the end of an abbreviation. I do not know of an
    effective solution to this problem.
    
    NB: The assumption is made that line breaks always denote the end of a
    sentence, regardless of the preceding character.
    
    Parameters:
        text: the passage to break into sentences.
    
    Keyword Parameters:
        terminators: strings that denote the end of a sentence.
        exclude: exceptions to the terminators.
    
    Returns:
        sentences: a list of sentences in text.
    """
    sentences = []
    text_as_paragraphs = text.split('\n')
    paragraphs_as_words = []
    for paragraph in text_as_paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            paragraphs_as_words.append([])
            continue
        words = paragraph.split(' ')
        paragraphs_as_words.append(words)

    for paragraph in paragraphs_as_words:
        if not paragraph:
            sentences.append('')
            continue
        sentence = ''
        for word in paragraph:
            if sentence:
                sentence = sentence + ' ' + word
            else:
                sentence = word
            try:
                ends_with_terminator = word.endswith(terminators)
            except TypeError:
                terminators = tuple(terminators)
                ends_with_terminator = word.endswith(terminators)

            if ends_with_terminator and word not in exclude:
                sentences.append(sentence)
                sentence = ''

        if sentence:
            sentences.append(sentence)

    return sentences


def screen_dimensions():
    """
    Get the width and height of the active display surface. If no display
    surface has been set, get the first element in pygame.display.list_modes().
    """
    screen_surface = pygame.display.get_surface()
    try:
        w, h = screen_surface.get_size()
    except AttributeError:
        w, h = pygame.display.list_modes()[0]

    return (w, h)


def longest_string_to_render(strings, f):
    """
    Get the longest string to render from a list.
    
    Parameters:
        strings: a list or tuple of strings.
        f: the pygame.font.Font object used for rendering.
    
    Returns:
        s: the longest string to render with f; if there is a tie, s is set to
            the string occurring earlier in the strings list.
        n: the number of pixel columns needed to render s.
    """
    s = ''
    n = 0
    for string in strings:
        w = f.size(string)[0]
        if w > n:
            n = w
            s = string

    return (
     s, n)


def height_of_strings(strings, f, line_size):
    """
    Compute the height of a list of strings when rendered with a given font,
    taking into account the line size (i.e., the number of pixel rows
    interpolated between the bottom of one line of text and the top of the
    next).
    
    Parameters:
        strings: the list of strings whose height is measured; assumes that
            each string is a separate line.
        f: the pygame.font.Font object in which text is to be rendered.
        line_size: the number of pixel rows between lines; must be positive.
    
    Returns:
        h: the height of strings when rendered.
    """
    h = 0
    for string in strings:
        line_height = f.size(string)[1]
        h = h + line_height

    h = h + line_size * (len(strings) - 1)
    return h


def wrap_text(new_text, width, f, old_text=[], start_new_line=False, return_height=False, line_height=None):
    """
    Break a string into lines on a screen.
    
    Parameters:
        new_text: words to convert to lines; if list or tuple, each element is
            a list of words from a paragraph, with line breaks automatically
            following an element; if str, split() is used to make into
            paragraphs and then individual words; if new_text evaluates to
            False in a Boolean context, a blank line is returned
        width: maximum pixels per line (width > 0).
        f: the font object to use.
    
    Keyword Parameters:
         return_height: whether the height of the rendered lines is returned;
            defaults to False.
        old_text: optional list of lines to which new_text is added; each
            element in old_text is assumed to be a single line; its legality
            given width is not checked; defaults to an empty list.
        start_new_line: only applies if old_text evaluates to True in a
            Boolean context; indicates whether a new line should start (i.e.,
            whether new_text should begin a new line); defaults to False.
        line_size: only applies if return_height is True; enotes the pixels
            interpolated between lines of text; if not set but line_size is
            needed, it is obtained from f.
    
    Returns:
        lines: old_text with new_text added.
        optionally:
            height: the height of lines when rendered with f.
    """
    if new_text:
        try:
            new_text_as_paragraphs = new_text.split('\n')
            new_text = []
            for paragraph in new_text_as_paragraphs:
                paragraph_list = paragraph.split(' ')
                new_text.append(paragraph_list)

        except AttributeError:
            pass

        new_lines = list(old_text)
        if old_text and not start_new_line:
            line = old_text[(-1)]
            del new_lines[-1]
        else:
            line = ''
        line_width = f.size(line)[0]
        for paragraph in new_text:
            for word in paragraph:
                if line:
                    word_width = f.size(' ' + word)[0]
                else:
                    word_width = f.size(word)[0]
                line_width = line_width + word_width
                if line_width < width:
                    if line:
                        line = line + ' ' + word
                    else:
                        line = word
                elif line_width == width:
                    line = line + ' ' + word
                    new_lines.append(line)
                    line = ''
                    line_width = 0
                else:
                    new_lines.append(line)
                    line = word
                    word_width = f.size(word)[0]
                    line_width = word_width

            if line:
                new_lines.append(line)
                line = ''
                line_width = 0

    else:
        new_lines = list(old_text)
        new_lines.append('')
    if return_height:
        if not line_height:
            line_height = f.get_linesize()
        height = height_of_strings(new_lines, f, line_height)
        return (
         new_lines, height)
    return new_lines


def string_to_screens_and_lines(source, allowed_width, allowed_height, f, pixels_between_lines=None, end_screens_with=(), do_not_include=()):
    """
    Convert a string to screens and lines.
    
    Pygame does not allow line breaks ("
") when rendering text. The purpose
    of this function is to break a string into lines and screens given a font
    and screen dimensions.
    
    The following two assumptions are made:
        1. Line breaks ("
") in source denote the start of a new paragraph.
            Therefore, to have an actual blank line (i.e., an empty string)
            appear in the returned array, add another "
" immediately
            following the first.
        2. Spaces denote the end of a word.
    
    Parameters:
        source: the string to divide into screens and lines.
        allowed_width: the width, in pixels, permitted for lines; can be a
            number of pixels or a proportion of the active screen's width.
        allowed_height: same as allowed_width but for the height of a single
            screen.
        f: the font with which source is measured.
    
    Keyword Parameters:
        pixels_between_lines: blank pixel rows between lines of text; defaults
            to None, in which case it is obtained from f.
        end_screens_with: a restricted set of characters that may end a
            screen; defaults to an empty tuple, in which case any character
            ending a word can end a screen.
        do_not_include: words that are exceptions to the end_screens_with
            words (e.g., "Mrs." ends in a period but should not end a screen)
    
    Returns:
        screens: a multidimensional list of screens and lines.
    """
    if 0 < allowed_width <= 1 and 0 < allowed_height <= 1:
        allowed_width, allowed_height = screen_dimensions()
    else:
        if not 0 < allowed_width <= 1:
            if 0 < allowed_height <= 1:
                raise ValueError('Both or neither of allowed_width and allowed_height can be between 0 and 1.')
            if not pixels_between_lines:
                pixels_between_lines = f.get_linesize()
            else:
                assert pixels_between_lines > 0, 'pixels_between_lines must be positive.'
            assert f.size(source)[1] <= allowed_height, 'allowed_height cannot accommodate source.'
            screens = []
            paragraphs = source.split('\n')
            single_words = []
            for paragraph in paragraphs:
                individual_words = paragraph.split(' ')
                widest_word, pixels = longest_string_to_render(individual_words, f)
                assert pixels < allowed_width, ('{:s} in source is too long for allowed_width.').format(widest_word)
                single_words.append(individual_words)

            lines_of_text, total_height = end_screens_with or wrap_text(single_words, allowed_width, f, return_height=True, line_height=pixels_between_lines)
            if total_height <= allowed_height:
                screens.append(lines_of_text)
            else:
                screen = []
                screen_height = 0
                for line in lines_of_text:
                    line_height = f.size(line)[1]
                    screen_height = screen_height + line_height + pixels_between_lines
                    if screen_height < allowed_height:
                        screen.append(line)
                    elif screen_height == allowed_height or screen_height - pixels_between_lines < allowed_height:
                        screen.append(line)
                        screens.append(screen)
                        screen = []
                        screen_height = 0
                    else:
                        screens.append(screen)
                        screen = [line]
                        screen_height = line_height + pixels_between_lines

                if screen:
                    screens.append(screen)
        else:
            sentences = []
            for paragraph in paragraphs:
                if sentences:
                    sentences.append('')
                if paragraph:
                    paragraph_as_sentences = text_to_sentences(paragraph, terminators=end_screens_with, exclude=do_not_include)
                    sentences = sentences + paragraph_as_sentences
                else:
                    sentences.append('')

            screen = []
            for sentence in sentences:
                if screen:
                    last_line = screen[(-1)]
                    if last_line:
                        next_line = False
                    else:
                        next_line = True
                else:
                    next_line = False
                possible_screen, screen_height = wrap_text(sentence, allowed_width, f, old_text=screen, start_new_line=next_line, return_height=True, line_height=pixels_between_lines)
                if screen_height <= allowed_height:
                    screen = possible_screen
                elif screen:
                    screens.append(screen)
                    screen, current_height = wrap_text(sentence, allowed_width, f, return_height=True, line_height=pixels_between_lines)
                    if current_height > allowed_height:
                        text_to_add = ''
                        for line in screen:
                            text_to_add = text_to_add + line + ''

                        text_to_add = text_to_add + sentence
                        multiple_screens = string_to_screens_and_lines(text_to_add, allowed_width, allowed_height, f, pixels_between_lines=pixels_between_lines)
                        for s in multiple_screens:
                            screens.append(s)

                else:
                    multiple_screens = string_to_screens_and_lines(sentence, allowed_width, allowed_height, f, pixels_between_lines=pixels_between_lines)
                    for s in multiple_screens:
                        screens.append(s)

        if screen:
            screens.append(screen)
    return screens


def render_string(s, f, colour, background, antialiasing=True):
    """
    Create pygame.Surface and pygame.Rect objects for a string, using a
    given font (f) and colour.
    
    Parameters:
        s: the string to render.
        f: the font in which to render s.
        colour: the colour of text to use, expressed as an RGB list or tuple.
        background: the background colour.
    
    Keyword Parameters:
        antialiasing: indicates whether text is rendered with antialiasing;
            defaults to True.
    
    Returns:
        s: the pygame.Surface object.
        r: the pygame.Rect object.
    """
    s = f.render(s, antialiasing, colour, background)
    r = s.get_rect()
    return (
     s, r)


def render_lines(lines, f, text_colour, background_colour, line_size=None, use_antialiasing=True):
    """
    Create pygame.Surface and pygame.Rect objects for a list of strings.
    
    Parameters:
        lines: the lines to render; "" is treated as a blank line.
        f: the font in which to render text.
        text_colour: an RGB list or tuple for the colour of the text.
        background_colour: RGB for background.
    
    Keyword Parameters:
        line_size: the number of pixel rows between lines; defaults to None,
            in which case it is set from f.
        use_antialiasing: indicates whether lines are rendered with
            antialiasing; defaults to True.
    
    Returns:
        surf: the pygame.Surface object.
        rect: the pygame.Rect object.
    """
    height = 0
    surfaces = []
    rects = []
    for line in lines:
        s, r = render_string(line, f, text_colour, background_colour, antialiasing=use_antialiasing)
        surfaces.append(s)
        rects.append(r)
        height = height + r.height

    try:
        height = height + line_size * (len(surfaces) - 1)
    except TypeError:
        line_size = f.get_linesize()
        height = height + line_size * (len(surfaces) - 1)

    width = rects[0].width
    for rect in rects[1:]:
        if rect.width > width:
            width = rect.width

    surf = pygame.Surface((width, height))
    surf.fill(background_colour)
    top = 0
    for i in range(len(surfaces)):
        s = surfaces[i]
        r = rects[i]
        r.topleft = (0, top)
        surf.blit(s, r)
        top = top + r.height + line_size

    rect = surf.get_rect()
    return (
     surf, rect)


def string_to_surface_and_rect(s, f, colour, background, max_width, max_height, max_screens=1, line_size=None, antialiasing=True):
    """
    Create a surface and rect from a string given a maximum pixel width for
    each line and a maximum pixel height for each screen.
    
    Parameters:
        s: the string.
        f: the font to use.
        colour: RGB for the text colour.
        background: RGB for the background colour.
        max_width: the maximum pixel width for each line.
        max_height: the maximum pixel height for each screen.
    
    Keyword Parameters:
        line_size: pixels between lines of text; defaults to None, in which
            case it is obtained from f.
        antialiasing: Boolean indicating whether antialiasing is used.
    
    Returns:
        surfaces: list of the pygame.Surface objects.
        rects: the list of pygame.Rect objects.
    """
    surfaces = []
    rects = []
    lines = string_to_screens_and_lines(s, max_width, max_height, f, line_size)
    assert len(lines) <= max_screens, 's is too long.'
    for screen in lines:
        surf, rect = render_lines(screen, f, colour, background, line_size=line_size, use_antialiasing=antialiasing)
        surfaces.append(surf)
        rects.append(rect)

    return (surfaces, rects)


def display_text_until_keypress(main_text, main_font, text_colour, background, antialias=True, proportion_width=0.95, proportion_height=0.95, main_line=None, break_sentences=False, sentence_terminators=('.', '!', '?'), terminator_exceptions=(), gap=1, bottom_message='Press the space bar to continue.', bottom_font=None, bottom_line=None, advance_keys=(K_SPACE,), reverse_keys=(K_LEFT, K_BACKSPACE), quit_keys=(K_ESCAPE,), ticker=None, frame_rate=30, files=()):
    """
    Display text to the screen and wait for the user to advance. If the text
    exceeds a single screen, users can move back and forth between the
    screens.
    
    Parameters:
        main_text: the text to be displayed, excluding the advance message.
        main_font: the font used for main_text.
        text_colour: RGB list/tuple for the colour of text.
        background: RGB list/tuple for main_text's background.
    
    Keyword Parameters:
        antialias: Boolean indicating whether antialiasing is used in text
            rendering; defaults to True.
        proportion_width: proportion of the main display surface's width used
            for text rendering (default = 0.95).
        proportion_height: proportion of the main display surface's height
            used for text rendering (default = 0.95).
        main_line: pixel rows between lines of text; taken from main_font if
            not set.
        break_sentences: Boolean indicating whether sentences can be broken
            across screens; defaults to False.
            NB: Sentences may be broken across screens even if
                False if they cannot fit on a single screen.
        sentence_terminators: strings that end a sentence.
            terminator_exceptions: exceptions to the strings in
            sentence_terminators.
        gap: the number of line breaks between the bottom of the main text and
            the top of bottom_message (default = 1).
        bottom_message: text at the end of each screen; defaults to "Press the
            space bar to continue.", but should be changed if advance_keys
            does not include K_SPACE.
        bottom_font: font to use for bottom_message; if left as None,
            main_font is used.
        bottom_line: same as main_line for bottom_line; taken from bottom_font
            if not set.
        advance_keys: keys to move through the screens; defaults to
            (K_SPACE,).
        reverse_keys: keys to move backward through the screens; defaults to
            (K_LEFT, K_BACKSPACE); to disable the user's ability to move
            backward, pass an empty tuple.
        quit_keys: keys to exit the program; set as an empty tuple to disable.
        ticker: a pygame.time.Clock object for controlling frame rate; one is
            created if one is not passed.
        frame_rate: the maximum frames per second; defaults to 30.
        files: an optional list/tuple of open files to close in case the user
            quits.
    """
    if not main_line:
        main_line = main_font.get_linesize()
    if not bottom_font:
        bottom_font = main_font
    if not bottom_line:
        bottom_line = bottom_font.get_linesize()
    window_surface = pygame.display.get_surface()
    try:
        window_rect = window_surface.get_rect()
    except AttributeError:
        window_surface = pygame.display.set_mode(pygame.display.list_modes()[0])
        window_rect = window_surface.get_rect()

    window_surface.fill(background)
    window_width, window_height = window_surface.get_size()
    pixel_columns = int(proportion_width * window_width)
    pixel_rows = int(proportion_height * window_height)
    surfaces = []
    rects = []
    bottom_lines = string_to_screens_and_lines(bottom_message, pixel_columns, pixel_rows, f=bottom_font, pixels_between_lines=bottom_line)
    assert len(bottom_lines) == 1, 'The bottom_message parameter cannot exceed a single screen.'
    bottom_lines = bottom_lines[0]
    bottom_surface, bottom_rect = render_lines(bottom_lines, bottom_font, text_colour, background, line_size=bottom_line, use_antialiasing=antialias)
    main_height = pixel_rows - bottom_rect.height - gap * main_line
    if break_sentences:
        main_lines = string_to_screens_and_lines(main_text, pixel_columns, main_height, main_font, pixels_between_lines=main_line, end_screens_with=sentence_terminators, do_not_include=terminator_exceptions)
    else:
        main_lines = string_to_screens_and_lines(main_text, pixel_columns, main_height, main_font, pixels_between_lines=main_line)
    for screen in main_lines:
        main_surface, main_rect = render_lines(screen, main_font, text_colour, background, line_size=main_line, use_antialiasing=antialias)
        bottom_rect_copy = pygame.Rect(bottom_rect)
        surfaces_combined = pygame.Surface((pixel_columns, pixel_rows))
        rects_combined = surfaces_combined.get_rect()
        surfaces_combined.fill(background)
        if main_rect.width >= bottom_rect.width:
            left_coordinate = (pixel_columns - main_rect.width) // 2
        else:
            left_coordinate = (pixel_columns - bottom_rect.width) // 2
        main_rect.topleft = (
         left_coordinate, 0)
        bottom_rect_copy.topleft = (left_coordinate, main_rect.bottom + gap * main_line)
        surfaces_combined.blit(main_surface, main_rect)
        surfaces_combined.blit(bottom_surface, bottom_rect_copy)
        rects_combined.center = window_rect.center
        surfaces.append(surfaces_combined)
        rects.append(rects_combined)

    i = 0
    surface_i = surfaces[i]
    rect_i = rects[i]
    window_surface.blit(surface_i, rect_i)
    keep_looping = True
    pygame.display.update()
    while keep_looping:
        for event in pygame.event.get():
            if event.type == KEYUP and event.key in quit_keys or event.type == QUIT:
                generic.terminate(files)
            elif event.type == KEYUP and event.key in reverse_keys and i > 0:
                i = i - 1
                surface_i = surfaces[i]
                rect_i = rects[i]
                window_surface.blit(surface_i, rect_i)
                pygame.display.update(rect_i)
            elif event.type == KEYUP and event.key in advance_keys and i < len(surfaces) - 1:
                i = i + 1
                surface_i = surfaces[i]
                rect_i = rects[i]
                window_surface.blit(surface_i, rect_i)
                pygame.display.update(rect_i)
            elif event.type == KEYUP and event.key in advance_keys and i == len(surfaces) - 1:
                keep_looping = False

        try:
            ticker.tick(frame_rate)
        except AttributeError:
            ticker = pygame.time.Clock()
            ticker.tick(frame_rate)


def ask_question(question, f, text_colour, background, antialiasing=True, w=0.95, h=0.95, line_size=None, gap=1, continue_message='Press the down arrow key to advance.', continue_font=None, continue_line_size=None, min_response=1, max_response=None, allowed_keys=LETTERS + NUMBERS + PUNCTUATION + (K_SPACE,), move_ahead=(K_DOWN,), move_back=(K_UP,), finished=(K_RETURN,), quit_keys=(K_ESCAPE,), allow_changes=True, ticker=None, frame_rate=30, files=()):
    """
    Display a question and return the user's typed response.
    
    Parameters:
        question: the question to which the user responds.
        f: the font used.
        text_colour: RGB list/tuple for text.
        background: RGB list/tuple for background.
    
    Keyword Parameters:
        antialiasing: Boolean indicating whether antialiasing is used in text
            rendering; defaults to True.
        w: the proportion of the active display surface's width allowed for
            text rendering (default = 0.95).
        h: the proportion of the active display surface's height allowed for
            text rendering (default = 0.95).
        line_size: pixel rows between lines of text; if not set, obtained from
            f.
        gap: line breaks between question and continue_message or the user's
            response (default = 1).
        continue_message: applies only if question exceeds a single screen;
            the message prompting the user to press a key to advance (default
            = "Press the down arrow key to advance.")
        continue_font: font used instead of f for continue_message; f used if
            not set.
        continue_line_size: same as line_size but for continue_message.
        min_response: the minimum length of the user's response (default = 1).
        max_response: the maximum length of the user's response; (default =
            None).
        allowed_keys: keys that can be used for responding.
        move_ahead: keys that move to the next screen; only applicable if
            question takes up more than one screen.
        move_back: keys that move to the previous screen.
        finished: keys to press when the response is finished; defaults to
            return, but can be empty if min_response and max_response are
            equal.
        quit_keys: keys for closing the program.
        allow_changes: Boolean guiding whether input can be deleted once
            typed; defaults to True.
        ticker: pygame.time.Clock object; one is created if none is passed.
        frame_rate: the maximum frames per second (default = 30).
        files: files to close if terminate() is called.
    
    Returns:
        r: the user's response.
    """
    if not line_size:
        line_size = f.get_linesize()
    r = ''
    window_surface = pygame.display.get_surface()
    try:
        window_rect = window_surface.get_rect()
    except AttributeError:
        window_surface = pygame.display.set_mode(pygame.display.list_modes()[0])

    window_surface.fill(background)
    window_width, window_height = window_rect.size
    pixel_columns = int(w * window_width)
    pixel_rows = int(h * window_height)
    surfaces = []
    rects = []
    question_height = pixel_rows - (gap + 1) * line_size
    question_screens = string_to_screens_and_lines(question, pixel_columns, question_height, f, pixels_between_lines=line_size)
    if len(question_screens) == 1:
        question_screens = question_screens[0]
        question_surface, question_rect = render_lines(question_screens, f, text_colour, background, line_size=line_size, use_antialiasing=antialiasing)
        main_surface = pygame.Surface((pixel_columns, pixel_rows))
        main_rect = main_surface.get_rect()
        question_rect.center = (
         pixel_columns // 2, question_height // 2)
        response_position = (
         question_rect.left + (window_width - pixel_columns) // 2,
         question_rect.bottom + gap * line_size + (window_height - pixel_rows) // 2)
        main_surface.fill(background)
        main_surface.blit(question_surface, question_rect)
        main_rect.center = window_rect.center
        surfaces.append(main_surface)
        rects.append(main_rect)
    else:
        if not continue_font:
            continue_font = f
        if not continue_line_size:
            continue_line_size = continue_font.get_linesize()
        continue_lines = string_to_screens_and_lines(continue_message, pixel_columns, pixel_rows, continue_font, pixels_between_lines=continue_line_size)
        assert len(continue_lines) == 1, 'continue_message is too long; it takes up multiple screens.'
        continue_lines = continue_lines[0]
        continue_surface, continue_rect = render_lines(continue_lines, continue_font, text_colour, background, line_size=continue_line_size, use_antialiasing=antialiasing)
        if continue_rect.height != line_size:
            for i in range(question_height, 0, -1):
                question_screens = string_to_screens_and_lines(question, pixel_columns, i, f, pixels_between_lines=line_size)
                if len(question_screens) > 1:
                    break

            last_screen = question_screens[(-1)]
            last_screen_height = height_of_strings(last_screen, f, line_size)
            if last_screen_height + (gap + 1) * line_size > pixel_rows:
                final_line = last_screen[(-1)]
                del last_screen[-1]
                new_last_screen = [final_line]
                question_screens.append(new_last_screen)
        for i in range(len(question_screens)):
            question_screen = question_screens[i]
            question_surface, question_rect = render_lines(question_screen, f, text_colour, background, line_size=line_size, use_antialiasing=antialiasing)
            current_surface = pygame.Surface((pixel_columns, pixel_rows))
            current_surface.fill(background)
            current_rect = current_surface.get_rect()
            if i == len(question_screens) - 1:
                question_rect.topleft = ((pixel_columns - question_rect.width) // 2, 0)
                response_position = (
                 question_rect.left + (window_width - pixel_columns),
                 question_rect.bottom + gap * line_size + (window_height - pixel_rows) // 2)
                current_surface.blit(question_surface, question_rect)
            else:
                if question_rect.width >= continue_rect.width:
                    left_coordinate = (pixel_columns - question_rect.width) // 2
                else:
                    left_coordinate = (pixel_columns - continue_rect.width) // 2
                question_rect.topleft = (
                 left_coordinate, 0)
                continue_rect.topleft = (
                 left_coordinate, question_rect.bottom + gap * line_size)
                current_surface.blit(question_surface, question_rect)
                current_surface.blit(continue_surface, continue_rect)
            current_rect.center = window_rect.center
            surfaces.append(current_surface)
            rects.append(current_rect)

        i = 0
        surface_i = surfaces[i]
        rect_i = rects[i]
        window_surface.blit(surface_i, rect_i)
        answer_obtained = False
        pygame.display.update()
        while not answer_obtained:
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYUP and event.key in quit_keys:
                    generic.terminate(files)
                elif i < len(surfaces) - 1 and event.type == KEYUP and event.key in move_ahead:
                    i = i + 1
                    window_surface.fill(background, rect_i)
                    surface_i = surfaces[i]
                    rect_i = rects[i]
                    window_surface.blit(surface_i, rect_i)
                    pygame.display.update(rect_i)
                elif i > 0 and event.type == KEYUP and event.key in move_back:
                    i = i - 1
                    window_surface.fill(background, rect_i)
                    surface_i = surfaces[i]
                    rect_i = rects[i]
                    window_surface.blit(surface_i, rect_i)
                    pygame.display.update(rect_i)
                elif event.type == KEYUP and event.key in allowed_keys and (len(r) < max_response or not max_response):
                    character = pygame.key.name(event.key)
                    r = r + character
                    if not finished and len(r) == max_response:
                        answer_obtained = True
                    else:
                        surface_r, rect_r = render_string(r, f, text_colour, background, antialiasing)
                        rect_r.topleft = response_position
                        window_surface.fill(background, rect_r)
                        window_surface.blit(surface_r, rect_r)
                        pygame.display.update(rect_r)
                elif event.type == KEYUP and event.key == K_BACKSPACE and allow_changes and r and i == len(surfaces) - 1:
                    r = r[:len(r) - 1]
                    update_rect = rect_r
                    surface_r, rect_r = render_string(r, f, text_colour, background, antialiasing)
                    rect_r.topleft = response_position
                    window_surface.fill(background, update_rect)
                    window_surface.blit(surface_r, rect_r)
                    pygame.display.update(update_rect)
                elif event.type == KEYUP and event.key in finished and i == len(surfaces) - 1 and len(r) >= min_response:
                    answer_obtained = True

            try:
                ticker.tick(frame_rate)
            except AttributeError:
                ticker = pygame.time.Clock()
                ticker.tick(frame_rate)

    return r