import random as rn
import numpy
from PIL import Image


im = Image.open('C:\\Users\\Ant\\Desktop\\randrei\\156578363.jpeg')
a = [tuple(rn.randint(0, 255) for _ in range(3)) for i in range(10)]
print(a)

# img = Image.open().convert('L')
# im = numpy.array(img)
# fft_mag = numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(im)))
# visual = numpy.log(fft_mag)
# visual = (visual - visual.min())/(visual.max() - visual.min())
# result = Image.fromarray((visual * 255).astype(numpy.uint8))
# result.save
