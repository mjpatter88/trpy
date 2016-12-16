from render import transpose


def test_transpose():
    point = (0,1)
    point = transpose(point)

    assert point == (1, 0)
