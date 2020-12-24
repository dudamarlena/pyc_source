# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/MEEGbuddy/gif_combine.py
# Compiled at: 2018-10-01 21:56:47
# Size of source mod 2**32: 2602 bytes


def combine_gifs(output_fname, fps, *gif_fnames):
    global axs
    global fig
    global gifs
    global ims
    import numpy as np, matplotlib.pyplot as plt
    from matplotlib import animation, rc
    from PIL import Image
    n = len(gif_fnames)
    dim1 = np.ceil(n ** 0.5)
    dim2 = np.ceil(n / dim1)
    fig, axs = plt.subplots(int(dim1), int(dim2))
    fig.set_size_inches(dim1 * 4, dim2 * 4)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0,
      hspace=0)
    axs = axs.flatten()
    for ax in axs:
        ax.axis('off')

    gifs = [Image.open(fname) for fname in gif_fnames]

    def determine_len(gif):
        t = 0
        test = True
        while test:
            try:
                gif.seek(t)
                t += 1
            except:
                test = False
                t -= 1

        return t

    lens = [determine_len(gif) for gif in gifs]
    if not all([l == lens[0] for l in lens]):
        raise ValueError('mismatched gif lengths')
    frames = lens[0] - 1

    def initGifs():
        ims = []
        for ax, gif in zip(axs[:len(gifs)], gifs):
            plt.axis('off')
            im = ax.imshow(gif.copy().convert('RGB'))
            ims.append(im)

        return ims

    ims = initGifs()

    def animate(i):
        for im, gif in zip(ims, gifs):
            gif.seek(i)
            im.set_data(gif.copy().convert('RGB'))

        return ims

    anim = animation.FuncAnimation(fig, animate, frames=frames, interval=10, blit=True)
    anim.save(output_fname, fps=fps, writer='imagemagick', savefig_kwargs={'facecolor': 'black'})
    return anim


if __name__ == '__main__':
    import sys
    output_fname = sys.argv[1]
    fps = int(sys.argv[2])
    combine_gifs(output_fname, fps, *sys.argv[3:])