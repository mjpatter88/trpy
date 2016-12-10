from PIL import Image


def draw_point(image, point, color):
    new_point = int(point[0]), int(point[1])
    image.putpixel(new_point, color)

def draw_line(image, start, end, color):
    const = 100
    for i in range(0, 100):
        x = start[0]*(1-i/100) + end[0]*i/100
        y = start[1]*(1-i/100) + end[1]*i/100
        draw_point(image, (x,y), color)


image = Image.new('RGB', (100, 100))

draw_point(image, (52, 41), (255,0,0))
draw_line(image, (0,0), (50,20), (0, 255, 0))

image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.save('test.png')


