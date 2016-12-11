
class Model():

    def __init__(self, filename, width, height):
        self.verts = []
        self.faces = []

        width = width - 1
        height = height - 1
        # wavefront obj files start indexing at 1
        self.verts.append(None)
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    items = line.split(' ')
                    x = (float(items[1]) + 1) * (width / 2)
                    y = (float(items[2]) + 1) * (height / 2)
                    self.verts.append((x, y))
                elif line.startswith('f '):
                    item_set = line.split(' ')
                    face = []
                    for item in item_set[1:]:
                        face.append(int(item[0:item.index('/')]))

                    self.faces.append(face)

        print("{} vertices.".format(len(self.verts)))
        print("{} faces.".format(len(self.faces)))

    def get_faces(self):
        for face in self.faces:
            yield [self.verts[index] for index in face]
