import sys
import math

cube_map = dict()
sidex = dict()
sidey = dict()
sidez = dict()

cubes = []
side_cubes = []

eps = 0.027
R = 0

class Field:
    def __init__(self, k1, k2, k3):
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.mark = False

    def __str__(self):
        return "Field " + str(self.k1) + " " + str(self.k2) + " " + str(self.k3)


class Line:
    def __init__(self, x1, y1, x2):
        self.x = x1
        self.y = y1
        if x1 == x2:
            self.type = 'v'
        else:
            self.type = 'h'


class Data:
    def __init__(self):
        self.min_x = 0.5
        self.min_y = 0.5
        self.max_x = 0.5
        self.max_y = 0.5

    def update_x(self, x):
        if self.min_x == 0.5:
            self.min_x = x
            self.max_x = x
        else:
            self.min_x = min(self.min_x, x)
            self.max_x = max(self.max_x, x)

    def update_y(self, y):
        if self.min_y == 0.5:
            self.min_y = y
            self.max_y = y
        else:
            self.min_y = min(self.min_y, y)
            self.max_y = max(self.max_y, y)


def point_distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2))


def dist_from_line(xr, yr, line: Line):
    x1, y1, x2, y2 = line.x, line.y, line.x+1, line.y
    if line.type == 'v':
        x2, y2 = x1, y1 + 1
    d = min(point_distance(xr, yr, x1, y1), point_distance(xr, yr, x2, y2))
    if min(x1, x2) <= xr <= max(x1, x2):
        d = min(d, abs(yr-y1))
    elif min(y1, y2) <= yr <= max(y1, y2):
        d = min(d, abs(xr - x1))
    return d


def get_r(x, y, lines):
    global R
    res = 9999999999
    for line in lines:
        res = min(res, dist_from_line(x, y, line))
        if res < R:
            return 0
    return res


def check_if_in_polygon(x, y, v_lines):
    br = 0
    for line in v_lines:
        if x >= line.x or y >= line.y+1 or y < line.y: # ako zahvatam odozgo lagano
            continue
        br += 1
    return br % 2 == 1


def count_sides(cube):
    global cubes
    br = 0
    for c in cubes:
        if c == cube:
            continue
        if (c[0] == cube[0] and c[1] == cube[1] and abs(c[2] - cube[2]) == 1) or \
            (c[0] == cube[0] and c[2] == cube[2] and abs(c[1] - cube[1]) == 1) or \
            (c[2] == cube[2] and c[1] == cube[1] and abs(c[0] - cube[0]) == 1):
            br += 1
    return 6 - br


def add_to_axis(k1, k2, k3, axis, field_map):
    if k3 not in axis:
        axis[k3] = []
    new_field = Field(k1, k2, k3)
    axis[k3].append(new_field)
    if k3 not in field_map:
        field_map[k3] = dict()

    if (k1, k2) not in field_map[k3]:
        field_map[k3][(k1, k2)] = new_field


neighboors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
for_lines = [(0,0,0,1), (1,0,1,1), (0,0,1,0), (0,1,1,1)]


def dfs(field: Field, field_map, lines, data):
    field.mark = True
    br = 0
    for i in range(len(neighboors)):
        n = neighboors[i]
        diff_lines = for_lines[i]
        # print(field.k1 + n[0], field.k2 + n[1])
        # print(field.k3 in field_map)
        if (field.k1 + n[0], field.k2 + n[1]) in field_map[field.k3]:

            if not field_map[field.k3][(field.k1 + n[0], field.k2 + n[1])].mark:
                br += dfs(field_map[field.k3][(field.k1 + n[0], field.k2 + n[1])], field_map, lines, data)

        else:
            lines.append(Line(field.k1+diff_lines[0], field.k2+diff_lines[1], field.k1+diff_lines[2]))
            data.update_x(field.k1+diff_lines[0])
            data.update_x(field.k1 + diff_lines[2])
            data.update_y(field.k2 + diff_lines[1])
            data.update_y(field.k2 + diff_lines[3])

    return br + 1


def determine_area(group_axis, field_map):
    global R, eps
    max_area = 0
    for k3 in group_axis:
        for field in group_axis[k3]:
            if not field.mark:
                lines = []
                data = Data()
                max_area = max(max_area, dfs(field, field_map, lines, data))
                v_lines = []
                for line in lines:
                    if line.type == 'v':
                        v_lines.append(line)
                if len(lines) == 0:
                    continue
                start_x = data.min_x+eps
                while start_x < data.max_x:
                    start_y = data.min_y + eps
                    while start_y < data.max_y:
                        if check_if_in_polygon(start_x, start_y, v_lines):
                            R = max(R, get_r(start_x, start_y, lines))
                        start_y += eps
                    start_x += eps

    return max_area


def for_every_side(side, s):
    # print(s, side)
    group_axis_min = dict()
    field_map_min = dict()
    group_axis_max = dict()
    field_map_max = dict()
    for key in side:
        k1, k2, k3_min, k3_max = key[0], key[1], side[key][0], side[key][1]
        add_to_axis(k1, k2, k3_min, group_axis_min, field_map_min)
        add_to_axis(k1, k2, k3_max, group_axis_max, field_map_max)

    # for g in group_axis_min:
    #     print(g)
    #     for field in group_axis_min[g]:
    #         print(field)
    return max(determine_area(group_axis_min, field_map_min), determine_area(group_axis_max, field_map_max))


if __name__ == '__main__':
    for line in sys.stdin:
        line = line.strip()
        if line == "exit":
            break
        line = line[1:]
        line = line[:-1]
        line = line.replace(" ", "")
        arr = line.split(",")
        x, y, z = int(arr[0]), int(arr[1]), int(arr[2])
        cubes.append((x, y, z))
        if (x, y) not in sidez:
            sidez[(x, y)] = (z, z)
        else:
            sidez[(x, y)] = (min(z, sidez[(x, y)][0]), max(z, sidez[(x, y)][1]))

        if (y, z) not in sidex:
            sidex[(y, z)] = (x, x)
        else:
            sidex[(y, z)] = (min(x, sidex[(y, z)][0]), max(x, sidex[(y, z)][1]))

        if (x, z) not in sidey:
            sidey[(x, z)] = (y, y)
        else:
            sidey[(x, z)] = (min(y, sidey[(x, z)][0]), max(y, sidey[(x, z)][1]))
    sum = 0
    for cube in cubes:
        sum += count_sides(cube)
    print(sum, max(for_every_side(sidex, "x"), for_every_side(sidey, "y"), for_every_side(sidez, "z")), R*R*3.1415926535)
