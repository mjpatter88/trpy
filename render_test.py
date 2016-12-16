from render import transpose, draw_point, draw_hor_line


def test_transpose():
    point = (0,1)
    point = transpose(point)

    assert point == (1, 0)

def test_draw_point():
    p = [[(0,0,0) for x in range(5)] for y in range(5)]
    color = (255,255,255)
    draw_point(p, (2,3), color)

    assert p[2][3] == color

def test_draw_hor_line():
    p = [[(0,0,0) for x in range(10)] for y in range(10)]
    color = (255,255,255)

    draw_hor_line(p, (2,3), (5,3), color)

    assert p[2][3] == color
    assert p[3][3] == color
    assert p[4][3] == color
    assert p[5][3] == color

def test_draw_hor_line_backwards():
    p = [[(0,0,0) for x in range(10)] for y in range(10)]
    color = (255,255,255)

    draw_hor_line(p, (5,4), (2,4), color)

    assert p[2][4] == color
    assert p[3][4] == color
    assert p[4][4] == color
    assert p[5][4] == color

