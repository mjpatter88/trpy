import sys
import random
from PIL import Image
from model import Model


def transpose(point):
    return point[1], point[0]

def draw_point(pixels, point, color):
    x, y = int(point[0]), int(point[1])
    pixels[x][y] = color

def line_to_pixels(start, end):
    pixels = []
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
        pixels.append((x,y))
    return pixels

def draw_line(pixels, start, end, color):
    for pixel in line_to_pixels(start, end):
        draw_point(pixels, pixel, color)

def draw_hor_line(pixels, start, end, color):
    x1 = min(start[0], end[0])
    x2 = max(start[0], end[0])
    for x in range(x1, x2 + 1):
        draw_point(pixels, (x, start[1]), color)

def draw_between_sides(pixels, side_1, side_2, color):
    side_1 = {point[1]:point[0] for point in side_1}
    side_2 = {point[1]:point[0] for point in side_2}
    for y in side_1:
        if y in side_2:
            draw_hor_line(pixels, (side_1[y], y), (side_2[y], y), color)

def draw_triangle(pixels, points, color):
    draw_line(pixels, points[0], points[1], color)
    draw_line(pixels, points[1], points[2], color)
    draw_line(pixels, points[0], points[2], color)

def fill_triangle(pixels, points, color):
    side_1 = line_to_pixels(points[0], points[1])
    side_2 = line_to_pixels(points[1], points[2])
    side_3 = line_to_pixels(points[0], points[2])

    draw_between_sides(pixels, side_1, side_2, color)
    draw_between_sides(pixels, side_2, side_3, color)
    draw_between_sides(pixels, side_1, side_3, color)


def render_model_wireframe(model_file, width, height, pixels):
    model = Model(model_file, width, height)

    for face in model.get_faces():
        color = (int(random.random()*255), int(random.random()*255), int(random.random()*255))
        fill_triangle(pixels, face, color)

def write_pixels_to_image_file(width, height, pixels, out_file_name):
    import itertools
    im = Image.new('RGB', (width, height), "black")
    im_pixels = im.load()

    for x,y in itertools.product(range(im.height), range(im.width)):
        im_pixels[x, y] = pixels[x][y]

    im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im.save(out_file_name)


if __name__ == '__main__':
    model_file = 'models/african_head.obj'
    width = 500
    height = 500
    out_file_name = 'out_render.png'

    if len(sys.argv) > 1:
        model_file = sys.argv[1]
    if len(sys.argv) > 3:
        width = int(sys.argv[2])
        height = int(sys.argv[3])

    pixels = [[(0,0,0) for x in range(width)] for y in range(height)]
    render_model_wireframe(model_file, width, height, pixels)
    write_pixels_to_image_file(width, height, pixels, out_file_name)


