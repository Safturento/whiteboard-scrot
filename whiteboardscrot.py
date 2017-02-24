from PIL import Image
import sys
from math import tan,degrees,radians
import numpy

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

image = Image.open('Capture.png')

width,height = image.size

angle = 27
d = int(height*tan(radians(angle)))

coeffs = find_coeffs(
	[(0, 0), (width, 0), (width, height), (0, height)],
	[(-d, 0), (width+d, 0), (width, height), (0, height)])

skewed = image.transform((width,height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
skewed.save('Skewed.png')

# I need to find out what these numbers do mathematically
cropped = skewed.crop((.65*d,0,width-.65*d,height))
cropped.save('Cropped.png')