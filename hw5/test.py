from PIL import Image

image = Image.new("RGB",(500,500),(255,255,255))
im = image.load()
(width, height) = image.size

for i in range(0, 250):
    for j in range(0, height):
        color1 = (i)*255//height
        color2 = (j)*255//width
        im[i,j] = (color1,color2,0)

image.save("pixel_result.jpg")