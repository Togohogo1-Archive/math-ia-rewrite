from pprint import pprint
from math import sqrt as r, pi, exp, atan
from PIL import Image, ImageOps
from matplotlib.pyplot import gray

# Setting up image, assumes it has already been gaussian blurred
im = Image.open("figures/figure12.png")
gray_im = ImageOps.grayscale(im)
width, height = gray_im.size  # x, y
pixels = gray_im.load() # Img[x, y]

# All in upright orientation
image_arr = [[pixels[x, y] for x in range(width)] for y in range(height)]
sobelx_arr = [[pixels[x, y] for x in range(width)] for y in range(height)]
sobely_arr = [[pixels[x, y] for x in range(width)] for y in range(height)]
grad_mag_arr = [[pixels[x, y] for x in range(width)] for y in range(height)]
nms_arr = [[0 for x in range(width)] for y in range(height)]

sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]


def sobel(x, y, kernel):
    num = 0

    for xx in range(3):
        for yy in range(3):
            try:  # Ignoring edges
                num += image_arr[x+(xx-1)][y+(yy-1)] * kernel[xx][yy]
            except:
                pass

    ## Ok if < 0, intensity relative to all values
    return num


def get_orientation(delx, dely):
    angle = 0

    try:
        angle = atan(dely/delx)*(180/pi)

        if dely == 0:
            angle = 180
        # return atan(dely/delx)
    except:
        if dely == 0 and delx == 0:
            angle = 0
        else:
            angle = 90 * (dely)/abs(dely)

    if angle < 0:
        angle += 180

    # return angle

    # if delx > 0 and dely > 0:
    #     ...
    # elif delx < 0 and dely > 0:
    #     return 180+angle
    # elif delx < 0 and dely < 0:
    #     return angle
    # elif delx > 0 and dely < 0:
    #     return 180+angle

    return abs(angle)


def non_max_supp(x, y, theta):
    epsilon = -0.01
    try:
        if 0 <= theta <= 22.5 or 157.5 < theta <= 180:
            if grad_mag_arr[x-1][y] <= grad_mag_arr[x][y] <= grad_mag_arr[x+1][y]:
                nms_arr[x][y] = 255
            # return "_"
        elif 22.5 < theta <= 67.5:
            if grad_mag_arr[x-1][y+1] <= grad_mag_arr[x][y] <= grad_mag_arr[x+1][y-1]:
                nms_arr[x][y] = 255
            # return "/"
        elif 67.5 < theta <= 112.5:
            if grad_mag_arr[x][y+1] <= grad_mag_arr[x][y] <= grad_mag_arr[x][y-1]:
                nms_arr[x][y] = 255
            # return "|"
        elif 112.5 < theta <= 157.5:
            if grad_mag_arr[x-1][y-1] <= grad_mag_arr[x][y] <= grad_mag_arr[x+1][y+1]:
                nms_arr[x][y] = 255
            # return "\\"
    except IndexError:
        pass



for x in range(height):
    for y in range(width):
        sobelx_arr[x][y] = sobel(x, y, sobelx)
        sobely_arr[x][y] = sobel(x, y, sobely)
        grad_mag_arr[x][y] = int(r(sobelx_arr[x][y]**2 + sobely_arr[x][y]**2))  # Gradient magnitude
        # pixels[y, x] = sobely_arr[x][y]
        # print((sx, sy), end=", ")


for x in range(height):
    for y in range(width):
        theta = get_orientation(sobelx_arr[x][y], sobely_arr[x][y])
        # print(f"{get_orientation(sobelx_arr[x][y], sobely_arr[x][y]):.2f}", end=" ")
        # print(non_max_supp(x, y, theta), end=" ")
        non_max_supp(x, y, theta)
        pixels[y, x] = nms_arr[x][y]
    print()
gray_im.show()

'''
rotate left
>>> a = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
>>> a
[[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
>>> pprint(a)
[[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
>>> b = [[a[i][j] for i in range(3)] for j in range(3)]

rorate right
>>> d = [[a[2-i][j] for i in range(3)] for j in range(3)]
>>> d
[[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
'''
