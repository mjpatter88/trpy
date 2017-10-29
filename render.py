import math
import sys
import random
from PIL import Image
from model import Model

WIDTH = 800
HEIGHT = 800

pixels = [0] * WIDTH * HEIGHT

def transpose(point):
    return point[1], point[0]

def draw_point(point, color):
    x = min(int(point[0]), WIDTH-1)
    y = min(int(point[1]), HEIGHT-1)
    new_point = x + (y * WIDTH)
    pixels[new_point] = color

def line_to_pixels(start, end):
    pix = []
    start = round((start[0])), round((start[1]))
    end = round((end[0])), round((end[1]))
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
    # If line starts and stops on the same point, just return that point
    if x0 == x1:
        pix.append((x0,y0))
    else:
        for x in range(x0, x1+1):
            step = (x-x0)/(x1-x0)
            y = round((y0*(1-step) + y1*step))
            if steep:
                x, y = transpose((x,y))
            pix.append((x,y))
    return pix

def draw_line(start, end, color):
    for pixel in line_to_pixels(start, end):
        draw_point(pixel, color)

def draw_hor_line(start, end, color):
    x1 = min(start[0], end[0])
    x2 = max(start[0], end[0])
    for x in range(x1, x2):
        draw_point((x, start[1]), color)

def draw_between_sides(side_1, side_2, color):
    side_1 = {point[1]:point[0] for point in side_1}
    side_2 = {point[1]:point[0] for point in side_2}
    for y in side_1:
        if y in side_2:
            draw_hor_line((side_1[y], y), (side_2[y], y), color)

def draw_triangle(points, color):
    draw_line(points[0], points[1], color)
    draw_line(points[1], points[2], color)
    draw_line(points[0], points[2], color)

def fill_triangle(points, color):
    side_1 = line_to_pixels(points[0], points[1])
    side_2 = line_to_pixels(points[1], points[2])
    side_3 = line_to_pixels(points[0], points[2])

    draw_between_sides(side_1, side_2, color)
    draw_between_sides(side_2, side_3, color)
    draw_between_sides(side_1, side_3, color)

"""
Do a basic matrix cross product
"""
def get_face_normal(face):
    p1 = face[0]
    p2 = face[1]
    p3 = face[2]
    side1 = (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
    side2 = (p3[0]-p2[0], p3[1]-p2[1], p3[2]-p2[2])

    x_index = 0
    y_index = 1
    z_index = 2
    x = side1[y_index]*side2[z_index] - side1[z_index]*side2[y_index]
    y = side1[z_index]*side2[x_index] - side1[x_index]*side2[z_index]
    z = side1[x_index]*side2[y_index] - side1[y_index]*side2[x_index]

    return (x, y, z)

def normalize(n):
    fact = math.sqrt(n[0]*n[0] + n[1]*n[1] + n[2]*n[2])
    return (n[0]/fact, n[1]/fact, n[2]/fact)

"""
The intensity of illumination is equal to the scalar product of the light vector and the normal
to the given triangle
"""
def get_face_intensity(face):
    light_vec = [0, 0, 1]
    n = get_face_normal(face)
    n = normalize(n)
    return n[0]*light_vec[0] + n[1]*light_vec[1] + n[2]*light_vec[2]

def world_to_screen(face, width, height):
    return [((vert[0] + 1) * (width/2), (vert[1] + 1) * (height/2)) for vert in face]

def draw_model_wireframe():
    model_file = 'models/african_head.obj'
    width = WIDTH
    height = HEIGHT
    color = (255, 255, 255)
    out_file_name = 'out_render.png'

    if len(sys.argv) > 1:
        model_file = sys.argv[1]

    image = Image.new('RGB', (width, height))
    model = Model(model_file, width, height)

    for face in model.get_faces():
        intensity = get_face_intensity(face)

        screen_face = world_to_screen(face, width, height)
        # If intensity < 0, polygon is not visible (roughly speaking)
        if intensity > 0:
            color = (int(intensity*255), int(intensity*255), int(intensity*255))
            fill_triangle(screen_face, color)
            # draw_triangle(image, screen_face, (color[0], 0, 0))

    image.putdata(pixels)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(out_file_name)


if __name__ == '__main__':
    draw_model_wireframe()

