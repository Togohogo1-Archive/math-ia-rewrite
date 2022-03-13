from pprint import pprint
from math import ceil, exp, floor, pi
from PIL import Image, ImageOps

# Setting up image
im = Image.open("figures/figure12.png")
gray_im = ImageOps.grayscale(im)
width, height = gray_im.size  # x, y
pixels = gray_im.load()  # Img[x, y]

image_arr = [[pixels[x, y] for y in range(height)] for x in range(width)]

# 2D Gaussian parameters
sigma = 2
ker_size = ceil(sigma)*6 + 1
rad = ker_size // 2


# Initializing 2D Gaussian kernel
def init():
    arr = [[0 for _ in range(ker_size)] for _ in range(ker_size)]
    coef = 1 / (2*pi*sigma**2)

    for xx in range(-rad, rad+1):
        for yy in range(-rad, rad+1):
            arr[xx+rad][yy+rad] = coef * exp(-((xx**2+yy**2) / (2*sigma**2)))

    return arr


# Smoothing out image with 2D Gaussian kernel
def gaussian(x, y, kernel):
    num = 0

    for xx in range(ker_size):
        for yy in range(ker_size):
            # Ignoring edges
            try:
                num += image_arr[x+(yy-rad)][y+(xx-rad)] * kernel[xx][yy]
            except:
                pass

    # Ok if < 0, intensity relative to all values
    return int(num)


gauss = init()

for x in range(width):
    for y in range(height):
        pixels[x, y] = gaussian(x, y, gauss)

gray_im.show()
