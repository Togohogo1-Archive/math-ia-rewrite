import numpy as np
from matplotlib import pyplot as plt
from math import ceil, exp, pi, sqrt as r
from PIL import Image, ImageOps

# Setting up image
im = Image.open("figures/figure12.png")
gray_im = ImageOps.grayscale(im)
width, height = gray_im.size  # x, y
pixels = gray_im.load()  # Img[x, y]

y_line = 100
intensity = []
derivative = [0]
blur_arr = []


# Smoothing out intensity profile with 1D Gaussian or average
def blur(x):
    sigma = 25
    coef = 1 / (r(2*pi)*sigma)
    tot = 0
    blur = ceil(sigma*3)

    for i in range(-blur, blur+1):
        if 0 <= x+i < width:
            tot += pixels[x+i, y_line] * coef * exp(-(((i)**2) / (2*sigma**2)))
            """ tot += pixels[x+i, y_line] """
        else:
            return None  # Ignoring edges

    return tot


for x in range(width):
    intensity.append(blur(x))
    """ intensity.append(pixels[x, y_line]) """

# Generating the derivative
for x in range(1, width-1):
    try:
        derivative.append(intensity[x+1] - intensity[x-1])
    except:
        derivative.append(None)

x = np.arange(width)

plt.title("Plot of I[x] blurred with σ = 5")
plt.xlabel(f"Pixels along x")
plt.ylabel("Intensity")
plt.plot(x, intensity)
plt.show()
