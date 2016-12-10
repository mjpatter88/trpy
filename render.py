from PIL import Image


def draw_point(image, point, color):
    new_point = int(point[0]), int(point[1])
    image.putpixel(new_point, color)

def draw_line(image, start, end, color):
    step = 10
    for x in range(start[0], end[0]):
        step = (x-start[0])/(end[0]-start[0])
        y = start[1]*(1-step) + end[1]*step
        draw_point(image, (x,y), color)


image = Image.new('RGB', (100, 100))

draw_point(image, (52, 41), (255,0,0))
draw_line(image, (13,20), (80,40), (255, 255, 255))
draw_line(image, (20,13), (40,80), (255, 0, 0))
draw_line(image, (80,40), (13,20), (255, 0, 0))

image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.save('test.png')


