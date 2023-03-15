import sys
from PIL import Image
import random
import math
from collections import deque

# sys.setrecursionlimit(10**6)
n = 768
yellow, red, black, green, blue, white = (255, 255, 0), (255, 0, 0), (0, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)
colors = [yellow, red, black, green, blue]
color_names = {yellow: 'Y', red: 'R', black: 'K', green: 'G', blue: 'B'}

graph = None
mark = [None] * n
flag_start = [None]*n
mark_val = 0
full_credit = 1

dots = dict()
cnt_colors = {yellow: 0, red: 0, black: 0, green: 0, blue: 0}
circles = {yellow: [], red: [], black: [], green: [], blue: []}
all_circles = []
other_shapes = []


class Circle:
    def __init__(self, x, y, color, r):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.intersect = {yellow: 0, red: 0, black: 0, green: 0, blue: 0}
        self.removed = False


def print_subtask1():
    print('Y', cnt_colors[yellow])
    print('B', cnt_colors[blue])
    print('K', cnt_colors[black])
    print('G', cnt_colors[green])
    print('R', cnt_colors[red])


def flag_dots(dots, is_circle):
    global graph
    # color = (random.randint(50,200), random.randint(50,200),random.randint(50,200))
    for dot in dots:
        flag_start[dot[0]][dot[1]] = True
        # if not is_circle:
        # graph[dot[0], dot[1]] = color


def clear_map():
    for color in colors:
        dots[color] = []


def two_point_distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))


def ok(x, y, mark_val):
    global graph, mark
    return x >= 0 and x < n and y >= 0 and y < n and graph[x,y] != white and mark[x][y] != mark_val


def bfs(x, y, color, dots, credit, mark_val):
    global graph
    queue = deque()
    queue.append((x, y, credit))
    dots.append([x,y])
    while len(queue) > 0:
        (x_t, y_t, credit_t) = queue.popleft()
        mark[x_t][y_t] = mark_val
        for dx in range(-1, 2):
            for dy in range(-1,2):
                if dx == 0 and dy == 0:
                    continue
                if not ok(x_t + dx, y_t + dy, mark_val):
                    continue

                if graph[x_t + dx, y_t + dy] == color:
                    mark[x_t+dx][y_t+dy] = mark_val

                    queue.append((x_t + dx, y_t + dy, full_credit))
                    dots.append([x_t + dx, y_t + dy])
                elif credit > 0:
                    mark[x_t+dx][y_t+dy] = mark_val
                    queue.append((x_t + dx, y_t + dy, credit_t - 1))


def find_circle(x, y, color):
    global mark_val, other_shapes, all_circles, circles
    mark_val += 1
    dots = []
    mark_val += 1
    bfs(x, y, color, dots, full_credit, mark_val)
    sumX, sumY = 0, 0
    if len(dots) == 0:
        return
    for dot in dots:
        sumX += dot[0]
        sumY += dot[1]
    centerX, centerY = round(sumX / len(dots)), round(sumY / len(dots))
    r = -1
    for i in range(min(150, len(dots))):
        rand_index = random.randint(0, len(dots)-1)
        dist = round(two_point_distance(centerX, centerY, dots[rand_index][0], dots[rand_index][1]))
        if r == -1:
            r = dist
        elif abs(r - dist) > 1:
            flag_dots(dots, False)
            other_shapes.append(dots)
            return False

    new_circle = Circle(centerX, centerY, color, r)
    all_circles.append(new_circle)
    circles[color].append(new_circle)
    flag_dots(dots, True)
    return True


def remove_circle(circle: Circle):
    if circle.removed:
        return
    circle.removed = True
    circles[circle.color].remove(circle)


def good_circle(circle: Circle):
    if circle.color == blue:
        return circle.intersect[blue] == 0 and circle.intersect[yellow] <= 1 and circle.intersect[black] == 0 \
           and circle.intersect[green] == 0 and circle.intersect[red] == 0
    if circle.color == yellow:
        return circle.intersect[blue] <= 1 and circle.intersect[yellow] == 0 and circle.intersect[black] <= 1 \
           and circle.intersect[green] == 0 and circle.intersect[red] == 0
    if circle.color == black:
        return circle.intersect[blue] == 0 and circle.intersect[yellow] <= 1 and circle.intersect[black] == 0 \
           and circle.intersect[green] <= 1 and circle.intersect[red] == 0
    if circle.color == green:
        return circle.intersect[blue] == 0 and circle.intersect[yellow] == 0 and circle.intersect[black] <= 1 \
           and circle.intersect[green] == 0 and circle.intersect[red] <= 1
    if circle.color == red:
        return circle.intersect[blue] == 0 and circle.intersect[yellow] == 0 and circle.intersect[black] == 0 \
           and circle.intersect[green] <= 1 and circle.intersect[red] == 0
    return False


def totally_good_circle(circle: Circle):
    if circle.color == blue:
        return circle.intersect[blue] == 0 and circle.intersect[yellow] == 1 and circle.intersect[black] == 0 \
           and circle.intersect[green] == 0 and circle.intersect[red] == 0
    if circle.color == yellow:
        return circle.intersect[blue] == 1 and circle.intersect[yellow] == 0 and circle.intersect[black] == 1 \
           and circle.intersect[green] == 0 and circle.intersect[red] == 0
    if circle.color == black:
        return circle.intersect[blue] == 0 and circle.intersect[yellow] == 1 and circle.intersect[black] == 0 \
           and circle.intersect[green] == 1 and circle.intersect[red] == 0
    if circle.color == green:
        return circle.intersect[blue] == 0 and circle.intersect[yellow] == 0 and circle.intersect[black] == 1 \
           and circle.intersect[green] == 0 and circle.intersect[red] == 1
    if circle.color == red:
        return circle.intersect[blue] == 0 and circle.intersect[yellow] == 0 and circle.intersect[black] == 0 \
           and circle.intersect[green] == 1 and circle.intersect[red] == 0
    return False


def add_intersection(circle1: Circle, circle2: Circle):
    circle1.intersect[circle2.color] += 1
    circle2.intersect[circle1.color] += 1
    if not good_circle(circle1) or not good_circle(circle2):
        remove_circle(circle1)
        remove_circle(circle2)


def intersect(circle1: Circle, circle2: Circle):
    return two_point_distance(circle1.x, circle1.y, circle2.x, circle2.y) < circle1.r + circle2.r


def check_other_shapes_intersection(circle):
    global other_shapes
    outside = False
    inside = False
    for shape in other_shapes:
        for dot in shape:
            if two_point_distance(circle.x, circle.y, dot[0], dot[1]) <= circle.r:
                inside = True
            else:
                outside = True
            if inside and outside:
                return True

    return False


def clear_false_circles():
    global all_circles
    for i in range(len(all_circles)):
        for j in range(i+1, len(all_circles)):
            if intersect(all_circles[i], all_circles[j]):
                add_intersection(all_circles[i], all_circles[j])

    for circle in all_circles:
        if not totally_good_circle(circle) or check_other_shapes_intersection(circle):
            remove_circle(circle)


logos = []


def find_olympic_logo():
    global logos
    clear_false_circles()
    for blue_c in circles[blue]:
        for yellow_c in circles[yellow]:
            if intersect(blue_c, yellow_c):
                for black_c in circles[black]:
                    if intersect(yellow_c, black_c):
                        for green_c in circles[green]:
                            if intersect(black_c, green_c):
                                for red_c in circles[red]:
                                    if intersect(green_c, red_c):
                                        logos.append((yellow_c, blue_c, black_c, green_c, red_c))


if __name__ == '__main__':
    line = sys
    im = None
    for line in sys.stdin:
        path = line.strip()

        im = Image.open(path).convert('RGB')
        graph = im.load()
        break

    for i in range(n):
        t = 0
        clear_map()
        mark[i] = [0] * n
        flag_start[i] = [False] * n
        for j in range(n):
            if graph[i,j] in colors:
                cnt_colors[graph[i,j]] += 1
                dots[graph[i,j]].append((i,j))
    print_subtask1()


    for x in range(n):
        for y in range(n):
            if graph[x,y] in colors and not flag_start[x][y]:
                find_circle(x, y, graph[x, y])

    find_olympic_logo()

    print(len(logos))

    for i in range(len(logos)):
        for circle in logos[i]:
            print(color_names[circle.color], circle.x, circle.y)

    # im.save('res.png')