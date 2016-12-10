from PIL import Image


def transpose(point):
    return point[1], point[0]

def draw_point(image, point, color):
    new_point = int(point[0]), int(point[1])
    image.putpixel(new_point, color)

def draw_line(image, start, end, color):
    steep = False;
    if abs(start[0] - end[0]) < abs(start[1] - end[1]):
        steep = True
        start = transpose(start)
        end = transpose(end)

    # Always draw from left to right
    if start[0] > end[0]:
        start, end = end, start

    x0, y0 = start
    x1, y1 = end
    for x in range(x0, x1):
        step = (x-x0)/(x1-x0)
        y = y0*(1-step) + y1*step
        if steep:
            x, y = transpose((x,y))
        draw_point(image, (x,y), color)


image = Image.new('RGB', (100, 100))

draw_line(image, (13,20), (80,40), (255, 255, 255))
draw_line(image, (20,13), (40,80), (255, 0, 0))
draw_line(image, (80,40), (13,20), (255, 0, 0))
draw_line(image, (20,80), (40,20), (255, 0, 0))

image = image.transpose(Image.FLIP_TOP_BOTTOM)
image.save('test.png')


