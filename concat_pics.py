import sys
import numpy as np
from PIL import Image


DESKTOP = 'C:\\Users\\Ant\\Desktop\\'

def concat_pics(lst, stacking='-v'):
    imgs = [Image.open(DESKTOP + i) for i in lst]

    max_shape = sorted([(np.sum(i.size), i.size) for i in imgs], reverse=True)[0][1]
    
    if stacking == '-v':
        imgs_comb = np.vstack((np.asarray(i.resize(max_shape, Image.LANCZOS)) for i in imgs))
    else:
        imgs_comb = np.hstack((np.asarray(i.resize(max_shape, Image.LANCZOS)) for i in imgs))
    
    Image.fromarray(imgs_comb).save('concat_result.png')


def concat_pics_1(lst, stacking='-v'):
    imgs = [Image.open(DESKTOP + i) for i in lst]
    max_width, max_height = map(max, zip(*(i.size for i in imgs)))

    imgs = [im.resize((max_width, max_height), Image.LANCZOS) for im in imgs]

    if stacking == '-v':
        new_im = Image.new('RGB', (max_width, len(lst) * max_height))

        for y_offset, im in enumerate(imgs):
            new_im.paste(im, (0, y_offset * max_height))
    else:
        new_im = Image.new('RGB', (len(lst) * max_width, max_height))

        for x_offset, im in enumerate(imgs):
            new_im.paste(im, (x_offset * max_width, 0))

    new_im.save(DESKTOP + 'concat_result.png')


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("""Syntax: python concat_pics.py [OPTION] [FILE]...
    -v    concatenate vertically
    -h    concatenate horizontally""")
        sys.exit(1)
    else:
        concat_pics_1(sys.argv[2:], sys.argv[1])
