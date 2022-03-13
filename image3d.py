import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageOps

# Setting up image
im = Image.open("figures/figure12.png")
gray_im = ImageOps.grayscale(im)
pixels = gray_im.load()  # Img[x, y]

corner_xy = 120  # Size of the N by N intensity map
img3d = np.zeros((corner_xy, corner_xy))

for x in range(corner_xy):
    for y in range(corner_xy):
        img3d[x][y] = pixels[x, y]

x = np.arange(corner_xy)
y = np.arange(corner_xy)
x, y = np.meshgrid(x, y)

ax = plt.axes(projection="3d")
ax.set_title("Image intensity map")
ax.set_xlabel("Pixels along y")
ax.set_ylabel("Pixels along x")
ax.set_zlabel("Intensity")
ax.view_init(45, 45)
ax.plot_surface(x, y, img3d, cmap="gray")

plt.show()
