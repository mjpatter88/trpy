from PIL import Image


image = Image.new('RGB', (100, 100))

image.putpixel((52, 41),(255,0,0))

image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.save('test.png')
