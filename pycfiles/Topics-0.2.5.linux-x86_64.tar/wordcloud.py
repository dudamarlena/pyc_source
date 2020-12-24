# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Topics/visualization/wordcloud.py
# Compiled at: 2013-03-01 14:55:06
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
from Topics.visualization.query_integral_image import query_integral_image
FONT_PATH = '/usr/share/fonts/truetype/droid/DroidSansMono.ttf'

def make_wordcloud(words, counts, fname, font_path=None, width=400, height=200, margin=5, ranks_only=False):
    """Build word cloud using word counts, store in image.

    Parameters
    ----------
    words : numpy array of strings
        Words that will be drawn in the image.

    counts : numpy array of word counts
        Word counts or weighting of words. Determines the size of the word in
        the final image.
        Will be normalized to lie between zero and one.

    font_path : string
        Font path to the font that will be used.
        Defaults to DroidSansMono path.

    fname : sting
        Output filename. Extension determines image type
        (written with PIL).

    width : int (default=400)
        Width of the word cloud image.

    height : int (default=200)
        Height of the word cloud image.

    ranks_only : boolean (default=False)
        Only use the rank of the words, not the actual counts.

    Notes
    -----
    Larger Images with make the code significantly slower.
    If you need a large image, you can try running the algorithm at a lower
    resolution and then drawing the result at the desired resolution.

    In the current form it actually just uses the rank of the counts,
    i.e. the relative differences don't matter.
    Play with setting the font_size in the main loop vor differnt styles.

    Colors are used completely at random. Currently the colors are sampled
    from HSV space with a fixed S and V.
    Adjusting the percentages at the very end gives differnt color ranges.
    Obviously you can also set all at random - haven't tried that.

    """
    if len(counts) <= 0:
        print 'We need at least 1 word to plot a word cloud, got %d.' % len(counts)
    if font_path is None:
        font_path = FONT_PATH
    counts = counts / float(counts.max())
    inds = np.argsort(counts)[::-1]
    counts = counts[inds]
    words = words[inds]
    img_grey = Image.new('L', (width, height))
    draw = ImageDraw.Draw(img_grey)
    integral = np.zeros((height, width), dtype=np.uint32)
    img_array = np.asarray(img_grey)
    font_sizes, positions, orientations = [], [], []
    font_size = 1000
    for word, count in zip(words, counts):
        if not ranks_only:
            font_size = min(font_size, int(100 * np.log(count + 100)))
        while True:
            font = ImageFont.truetype(font_path, font_size)
            orientation = random.choice([None, Image.ROTATE_90])
            transposed_font = ImageFont.TransposedFont(font, orientation=orientation)
            draw.setfont(transposed_font)
            box_size = draw.textsize(word)
            result = query_integral_image(integral, box_size[1] + margin, box_size[0] + margin)
            if result is not None or font_size == 0:
                break
            font_size -= 1

        if font_size == 0:
            break
        x, y = np.array(result) + margin // 2
        draw.text((y, x), word, fill='white')
        positions.append((x, y))
        orientations.append(orientation)
        font_sizes.append(font_size)
        img_array = np.asarray(img_grey)
        partial_integral = np.cumsum(np.cumsum(img_array[x:, y:], axis=1), axis=0)
        if x > 0:
            if y > 0:
                partial_integral += integral[x - 1, y:] - integral[(x - 1, y - 1)]
            else:
                partial_integral += integral[x - 1, y:]
        if y > 0:
            partial_integral += integral[x:, y - 1][:, np.newaxis]
        integral[x:, y:] = partial_integral

    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    everything = zip(words, font_sizes, positions, orientations)
    for word, font_size, position, orientation in everything:
        font = ImageFont.truetype(font_path, font_size)
        transposed_font = ImageFont.TransposedFont(font, orientation=orientation)
        draw.setfont(transposed_font)
        draw.text((position[1], position[0]), word, fill='hsl(%d' % random.randint(0, 255) + ', 80%, 50%)')

    img.show()
    img.save(fname)
    return


if __name__ == '__main__':
    import os, sys
    from sklearn.feature_extraction.text import CountVectorizer
    if '-' in sys.argv:
        lines = sys.stdin.readlines()
        sources = ['stdin']
    else:
        sources = [ arg for arg in sys.argv[1:] if os.path.exists(arg) ] or [
         'constitution.txt']
        lines = []
        for s in sources:
            with open(s) as (f):
                lines.extend(f.readlines())

    text = ('').join(lines)
    cv = CountVectorizer(min_df=1, charset_error='ignore', stop_words='english', max_features=200)
    counts = cv.fit_transform([text]).toarray().ravel()
    words = np.array(cv.get_feature_names())
    words = words[(counts > 1)]
    counts = counts[(counts > 1)]
    output_filename = os.path.splitext(os.path.basename(sources[0]))[0] + '_.png'
    counts = make_wordcloud(words, counts, output_filename)