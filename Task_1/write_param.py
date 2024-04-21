import numpy as np
import csv

class ModelCalculator:
    def __init__(self, file_path):
        self.vertices, self.faces = self.load_model_obj(file_path)

    def load_model_obj(self, file_path):
        vertices = []
        faces = []
        part = -1
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('# object'):
                    part += 1
                elif line.startswith('v '):
                    vertex = [float(v) for v in line.split()[1:]]
                    vertices.append(vertex)
                elif line.startswith('f '):
                    face = [int(v) for v in line.split()[1:]]
                    faces.append(face)
        return vertices, faces

    def calculate_triangle_area(self, face):
        v1 = np.array(self.vertices[face[0] - 1])
        v2 = np.array(self.vertices[face[1] - 1])
        v3 = np.array(self.vertices[face[2] - 1])
        a = np.linalg.norm(v2 - v1)
        b = np.linalg.norm(v3 - v2)
        c = np.linalg.norm(v1 - v3)
        s = (a + b + c) / 2
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        return area

    def calculate_element_areas(self):
        areas = []
        for face in self.faces:
            area = self.calculate_triangle_area(face)
            areas.append(area)
        return areas

    def write_csv(self, data, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)

    def calculate_and_write_areas(self, par_file_path='parameters.csv', temp_file_path='temperature.csv'):
        element_areas = self.calculate_element_areas()

        # 384 faces, 194 vertices - 1
        # 384 faces, 194 vertices - 2
        # 384 faces, 194 vertices - 4
        # 224 faces, 114 vertices - 3
        # 192 faces, 98 vertices - 5

        s_1 = sum(element_areas[:384])
        s_2 = sum(element_areas[384:768])
        s_4 = sum(element_areas[768:1152])
        s_3 = sum(element_areas[1152:1376])
        s_5 = sum(element_areas[1376:])

        faces12 = self.faces[:112]
        element_areas12 = [self.calculate_triangle_area(face) for face in faces12]
        s_12 = sum(element_areas12)

        faces23 = self.faces[384:496]
        element_areas23 = [self.calculate_triangle_area(face) for face in faces23]
        s_23 = sum(element_areas23)

        faces34 = self.faces[768:880]
        element_areas34 = [self.calculate_triangle_area(face) for face in faces34]
        s_34 = sum(element_areas34)

        faces45 = self.faces[1040:1152]
        element_areas45 = [self.calculate_triangle_area(face) for face in faces45]
        s_45 = sum(element_areas45)

        par = [[0.1, 0.1, 0.05, 0.02, 0.05],
               [900, 900, 520, 1930, 520],
               [0, 240, 0, 0, 0],
               [0, 0, 130, 0, 0],
               [0, 0, 0, 118, 0],
               [0, 0, 0, 0, 10.5],
               [0, 0, 0, 0, 0],
               [s_1, s_2, s_3, s_4, s_5],
               [0, s_12, 0, 0, 0],
               [0, 0, s_23, 0, 0],
               [0, 0, 0, s_34, 0],
               [0, 0, 0, 0, s_45],
               [0, 0, 0, 0, 0],
               [2000]]

        temp = [[10, 20, 70, 50, 5]]

        self.write_csv(par, par_file_path)
        self.write_csv(temp, temp_file_path)
