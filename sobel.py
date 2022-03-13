from pprint import pprint
from math import exp, pi, sqrt as r
from PIL import Image, ImageOps

# Setting up image
im = Image.open("figures/figure12.png")
gray_im = ImageOps.grayscale(im)
width, height = gray_im.size  # x, y
pixels = gray_im.load()  # Img[x, y]

# Not upright image, but it's not a big deal
image_arr = [[pixels[x, y] for y in range(height)] for x in range(width)]
sobelx_arr = [[pixels[x, y] for y in range(height)] for x in range(width)]
sobely_arr = [[pixels[x, y] for y in range(height)] for x in range(width)]

# Filters
sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
delx = [[0, 0, 0], [-1, 0, 1], [0, 0, 0]]
dely = [[0, 1, 0], [0, 0, 0], [0, -1, 0]]


def sobel(x, y, kernel):
    num = 0

    for xx in range(3):
        for yy in range(3):
            # Ignoring edges
            try:
                num += image_arr[x+(yy-1)][y+(xx-1)] * kernel[xx][yy]
            except:
                pass

    # Ok if < 0, intensity relative to all values
    return num


max_int = pixels[0, 0]
min_int = pixels[0, 0]

for x in range(width):
    for y in range(height):
        # Applying filter
        sobelx_arr[x][y] = sobel(x, y, sobelx)
        sobely_arr[x][y] = sobel(x, y, sobely)

        # For normalizing
        max_int = max(max_int, sobely_arr[x][y])
        min_int = min(min_int, sobely_arr[x][y])

diff = max_int - min_int

for x in range(width):
    for y in range(height):
        pixels[x, y] = int(r(sobelx_arr[x][y]**2 + sobely_arr[x][y]**2))
        """
        pixels[x, y] = sobely_arr[x][y]
        pixels[x, y] = int((sobelx_arr[x][y]-min_int)*(255/(max_int-min_int)))
        """

gray_im.show()
