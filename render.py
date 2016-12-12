import sys
from PIL import Image
from model import Model


def transpose(point):
    return point[1], point[0]

def draw_point(image, point, color):
    new_point = int(point[0]), int(point[1])
    image.putpixel(new_point, color)

def draw_line(image, start, end, color):
    start = int(start[0]), int(start[1])
    end = int(end[0]), int(end[1])
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
        y = int(y0*(1-step) + y1*step)
        if steep:
            x, y = transpose((x,y))
        draw_point(image, (x,y), color)

def draw_triangle(image, points, color):
    draw_line(image, points[0], points[1], color)
    draw_line(image, points[1], points[2], color)
    draw_line(image, points[0], points[2], color)

def draw_model_wireframe():
    model_file = 'models/african_head.obj'
    width = 500
    height = 500
    color = (255, 255, 255)
    out_file_name = 'render.png'

    if len(sys.argv) > 1:
        model_file = sys.argv[1]
    if len(sys.argv) > 3:
        width = int(sys.argv[2])
        height = int(sys.argv[3])

    image = Image.new('RGB', (width, height))
    model = Model(model_file, width, height)

    for face in model.get_faces():
        draw_triangle(image, face, color)

    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(out_file_name)


if __name__ == '__main__':
    width = 200
    height = 200
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    out_file_name = 'out_render.png'

    image = Image.new('RGB', (width, height))

    draw_triangle(image, ((10, 70), (50, 160), (70, 80)), red)
    draw_triangle(image, ((180, 50), (150, 1), (70, 180)), white)
    draw_triangle(image, ((180, 150), (120, 160), (130, 180)), green)

    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(out_file_name)
