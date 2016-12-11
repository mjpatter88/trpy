
class Model():

    def __init__(self, filename, width, height):
        self.verts = []
        self.faces = []

        width = width - 1
        height = height - 1
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    items = line.split(' ')
                    self.verts.append([float(items[1]), float(items[2])])
                elif line.startswith('f '):
                    item_set = line.split(' ')
                    face = []
                    for item in item_set[1:]:
                        face.append(int(item[0:item.index('/')]))

                    self.faces.append(face)

        print("{} vertices.".format(len(self.verts)))
        print("{} faces.".format(len(self.faces)))
        
        x = max(abs(vert[0]) for vert in self.verts)
        y = max(abs(vert[1]) for vert in self.verts)
        biggest = max((x, y))
        scale_x = width / biggest
        scale_y = height / biggest
        
        for vert in self.verts:
            vert[0] = (vert[0] + biggest) * (scale_x / 2)
            vert[1] = (vert[1] + biggest) * (scale_y / 2)

        

    def get_faces(self):
        for face in self.faces:
            # wavefront obj files start indexing at 1
            yield [self.verts[index-1] for index in face]
