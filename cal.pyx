import numpy as np
from bezier import Bezier as Bz

cdef class Cal:
    cpdef object mesh 

    def __init__(self, mesh):
        self.mesh = mesh

    cpdef update_mesh(self, list start, list end, list pos):
        cpdef list res = []
        cpdef list points_1
        cpdef list points_2
        cpdef list vertices
        cpdef list indices
        cpdef int _i 
        cpdef int x
        cpdef int y

        points_1 = [[-1000, -1000], start, [pos[0] / 2, pos[1] / 2], pos]
        points_2 = [
            pos,
            [pos[0] / 2, (end[1] + pos[1]) / 2],
            end,
            [-1000, end[1] + 1000],
        ]
        res.extend(points_1)
        res.extend(points_2)

        t_points = np.arange(0, 1, 0.01)
        points1 = np.array(res)
        curve = Bz.Curve(t_points, points1)

        vertices = []
        indices = []
        _i = 0
        for x, y in curve:
            vertices.extend([x, y, 0, 0])
            indices.append(_i)
            _i += 1
        self.mesh.indices = indices
        self.mesh.vertices = vertices
