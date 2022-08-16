from pprint import pprint
from PIL import Image, ImageOps

# Setting up image
im = Image.open("Images/valve.png")
gray_im = ImageOps.grayscale(im)
width, height = gray_im.size  # x, y
pixels = gray_im.load() # Img[x, y]

# Testing purposes
print(pixels[0, height-1], "Bottom left")
print(pixels[width-1, 0], "Top right")
print(pixels[width-1, height-1], "Bottom right")

image_arr = [[pixels[x, y] for y in range(height)] for x in range(width)]

ker_size = 11
box = [[1 for _ in range(ker_size)] for _ in range(ker_size)]

def blur(x, y, kernel):
    rad = ker_size // 2
    num = 0

    for xx in range(ker_size):
        for yy in range(ker_size):
            # Ignoring pixels when kernel goes offscreen
            try:
                num +=  (1/ker_size**2) * image_arr[x+(yy-rad)][y+(xx-rad)] * kernel[xx][yy]
            except:
                pass

    # Ok if < 0, intensity relative to all values
    return int(num)


for x in range(width):
    for y in range(height):
        pixels[x, y] = blur(x, y, box)

# Show the new picture without saving
gray_im.show()
