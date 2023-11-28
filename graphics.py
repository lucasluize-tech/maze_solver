from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed")

    def close(self):
        self.__running = False

    def clear(self):
        self.__canvas.delete("all")

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point({},{})".format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __add__(self, point):
        x = self.x + point.x
        y = self.y + point.y
        return Point(x, y)

    def __sub__(self, point):
        x = self.x - point.x
        y = self.y - point.y
        return Point(x, y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, color):
        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y
        canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        canvas.pack(fill=BOTH, expand=True)


class Wall:
    def __init__(self, left=True, right=True, top=True, bottom=True):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.walls = [self.left, self.right, self.top, self.bottom]

    def __str__(self):
        return f"Wall(left: {self.left}\n,right: {self.right}\n,top: {self.top}\n, bottom{self.bottom}\n)"

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        for i in range(4):
            yield self.walls[i]

    def _add_or_remove_wall(self, wall_side, case):
        if case == "remove":
            if wall_side == "left":
                self.left = False
            elif wall_side == "right":
                self.right = False
            elif wall_side == "top":
                self.top = False
            elif wall_side == "bottom":
                self.bottom = False

        elif case == "add":
            if wall_side == "left":
                self.left = True
            elif wall_side == "right":
                self.right = True
            elif wall_side == "top":
                self.top = True
            elif wall_side == "bottom":
                self.bottom = True
        else:
            raise ValueError(f"Invalid wall_side: {wall_side}")


class Cell:
    def __init__(self, row, col, walls, points, window, maze):
        self.row = row
        self.col = col
        self.walls = walls
        self._x1, self._x2 = points[0], points[1]
        self._y1, self._y2 = points[2], points[3]
        self._win = window
        self.visited = False
        self.adjacent = []

    def __str__(self):
        return f"Cell({self.row},{self.col})"

    def __repr__(self):
        return self.__str__()

    def draw(self, color="black"):
        left, right = Line(self._x1, self._y1), Line(self._x2, self._y2)
        top, bottom = Line(self._y1, self._y2), Line(self._x1, self._x2)

        # !- this is just for the entry and exit cells to be all white
        if color == "white":
            self._win.draw_line(left, color)
            self._win.draw_line(right, color)
            self._win.draw_line(top, color)
            self._win.draw_line(bottom, color)
            return

        if self.walls.left == True:
            self._win.draw_line(left, color)
        if self.walls.right == True:
            self._win.draw_line(right, color)
        if self.walls.top == True:
            self._win.draw_line(top, color)
        if self.walls.bottom == True:
            self._win.draw_line(bottom, color)

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        # undo is used to draw the path back to the previous cell
        color = "red" if not undo else "gray"

        half_height = (self._x1.y - self._y1.y) / 2
        half_width = (self._x2.x - self._x1.x) / 2

        from_point = Point(self._x1.x + half_width, self._y1.y + half_height)
        to_point = Point(to_cell._x1.x + half_width, to_cell._y1.y + half_height)
        # print(f"going from : {from_point} to {to_point}")

        if undo:
            from_point, to_point = to_point, from_point
            # print(f"{to_point} back to {from_point}")
            self._win.draw_line(Line(from_point, to_point), color)
            return

        # print(f"going from : {from_point} to {to_point}")
        self._win.draw_line(Line(from_point, to_point), color)
        return

    def _adjacent_cells(self, maze):
        if self.row == 0:
            if self.col == 0:
                self.adjacent.append(maze._cells[self.row][self.col + 1])
                self.adjacent.append(maze._cells[self.row + 1][self.col])
                return self.adjacent
            if maze._num_cols - 1 == self.col:
                self.adjacent.append(maze._cells[self.row][self.col - 1])
                self.adjacent.append(maze._cells[self.row + 1][self.col])
                return self.adjacent
            else:
                self.adjacent.append(maze._cells[self.row][self.col + 1])
                self.adjacent.append(maze._cells[self.row][self.col - 1])
                self.adjacent.append(maze._cells[self.row + 1][self.col])
                return self.adjacent

        elif self.row == maze._num_rows - 1:
            if self.col == 0:
                self.adjacent.append(maze._cells[self.row][self.col + 1])
                self.adjacent.append(maze._cells[self.row - 1][self.col])
                return self.adjacent
            elif self.col == maze._num_cols - 1:
                self.adjacent.append(maze._cells[self.row][self.col - 1])
                self.adjacent.append(maze._cells[self.row - 1][self.col])
                return self.adjacent
            else:
                self.adjacent.append(maze._cells[self.row][self.col + 1])
                self.adjacent.append(maze._cells[self.row][self.col - 1])
                self.adjacent.append(maze._cells[self.row - 1][self.col])
                return self.adjacent
        else:
            if self.col == 0:
                self.adjacent.append(maze._cells[self.row][self.col + 1])
                self.adjacent.append(maze._cells[self.row + 1][self.col])
                self.adjacent.append(maze._cells[self.row - 1][self.col])
                return self.adjacent
            elif self.col == maze._num_cols - 1:
                self.adjacent.append(maze._cells[self.row][self.col - 1])
                self.adjacent.append(maze._cells[self.row + 1][self.col])
                self.adjacent.append(maze._cells[self.row - 1][self.col])
                return self.adjacent
            else:
                self.adjacent.append(maze._cells[self.row][self.col + 1])
                self.adjacent.append(maze._cells[self.row][self.col - 1])
                self.adjacent.append(maze._cells[self.row + 1][self.col])
                self.adjacent.append(maze._cells[self.row - 1][self.col])
                return self.adjacent
