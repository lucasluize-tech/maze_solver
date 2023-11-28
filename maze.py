import random
from graphics import Cell, Point, Wall
import time
from tkinter import messagebox


class Maze:
    def __init__(self, x1, y1, rows, cols, cell_size_x, cell_size_y, window, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = rows
        self._num_cols = cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._window = window
        self.width = self._num_rows * cell_size_x
        self.height = self._num_cols * cell_size_y
        self._cells = [[] for _ in range(self._num_rows)]
        self.cells_dict = {}
        self._create_cells()
        self.seed = random.seed(seed) if seed is None else None

    def __str__(self):
        formatted_cells = "[\n"
        for _ in range(self._num_rows):
            formatted_cells += f"{self._cells[_]}\n"
            if _ == self._num_rows - 1:
                formatted_cells += "]"

        return f"Maze\norigin: {self._x1},{self._y1}\nrows: {self._num_rows}, columns: {self._num_cols}\ncell_size:(width: {self._cell_size_x}, height: {self._cell_size_y})\n\nlist of cells: {formatted_cells}\n"

    def _create_cells(self):
        for row in range(self._num_rows):
            for col in range(self._num_cols):
                cell = self._draw_cell(row, col)
                self.cells_dict[(row, col)] = cell
                self._cells[row].append(cell)
                cell.draw()
                self._animate()

    def _redraw(self):
        # first set canvas back to white and empty
        self._window.clear()
        for row in range(self._num_rows):
            for col in range(self._num_cols):
                cell = self._cells[row][col]
                cell.draw()
                self._animate()

    def create_cell_points(self, x, y):
        width, height = self._cell_size_x, self._cell_size_y
        points = [
            Point(x, y + height),  # x1.x, x1.y
            Point(x + width, y + height),  # x2.x, x2.y
            Point(x, y),  # y1.x y1.y
            Point(x + width, y),  # y2.x ,y2.y
        ]
        return points

    def _draw_cell(self, row, col):
        x = self._x1 + (col * self._cell_size_x)
        y = self._y1 + (row * self._cell_size_y)
        cell = Cell(
            row,
            col,
            Wall(),  # !Empty Will draw all sides
            self.create_cell_points(x, y),
            self._window,
            self,
        )

        return cell

    def _reset_cells_visited(self):
        cells = self._cells
        for cell in cells:
            for c in cell:
                c.visited = False

    def _animate(self, t=0):
        self._window.redraw()
        time.sleep(t)

    def _break_entrance_and_exit(self):
        entry_cell = self._cells[0][0]
        exit_cell = self._cells[self._num_rows - 1][self._num_cols - 1]

        entry_cell.walls._add_or_remove_wall("right", "remove")
        entry_cell.walls._add_or_remove_wall("bottom", "remove")
        entry_cell.walls._add_or_remove_wall("left", "remove")
        entry_cell.walls._add_or_remove_wall("top", "remove")

        exit_cell.walls._add_or_remove_wall("left", "remove")
        exit_cell.walls._add_or_remove_wall("top", "remove")
        exit_cell.walls._add_or_remove_wall("right", "remove")
        exit_cell.walls._add_or_remove_wall("bottom", "remove")
        (f" drawing entry and exit")
        entry_cell.draw(color="white")
        exit_cell.draw(color="white")
        self._animate()

    def _break_walls_r(self, row, col):
        current = self._cells[row][col]
        current.visited = True
        adjacents = current._adjacent_cells(self)

        while True:
            to_visit = []
            for cell in adjacents:
                if not cell.visited:
                    to_visit.append(cell)
            if len(to_visit) < 1:
                current.draw()
                break
            else:
                cell_choice = random.choice(to_visit)
                """
                Knock down the wall between the last cell and the chosen cell.
                
                Ex: cell[0,0] has a wall on the right side[1,0] a wall on the bottom side[0,1] , so if we choose right, we knock down the right wall, if we choose bottom, we knock down the bottom wall.
                
                """

                # - [0,0] , choice [0,1] => remove right wall from [0,0] and left wall from [0,1]
                if current.col + 1 == cell_choice.col:
                    current.walls._add_or_remove_wall("right", "remove")
                    cell_choice.walls._add_or_remove_wall("left", "remove")

                # - [5,7], choice [5,6] => remove left wall from [5,7] and right wall from [5,6]
                elif current.col - 1 == cell_choice.col:
                    current.walls._add_or_remove_wall("left", "remove")
                    cell_choice.walls._add_or_remove_wall("right", "remove")

                # - [1,0] , choice [0,0] => remove top wall from [1,0] and bottom wall from [0,0]
                elif current.row == cell_choice.row + 1:
                    current.walls._add_or_remove_wall("top", "remove")
                    cell_choice.walls._add_or_remove_wall("bottom", "remove")

                # - [4,7], choice [5,7] => remove top wall from [5,7] and bottom wall from [4,7]
                elif current.row == cell_choice.row - 1:
                    current.walls._add_or_remove_wall("bottom", "remove")
                    cell_choice.walls._add_or_remove_wall("top", "remove")

                self._break_walls_r(cell_choice.row, cell_choice.col)

        return

    def solve(self, row, col):
        self._animate(0.05)
        current = self._cells[row][col]
        current.visited = True

        if current == self._cells[self._num_rows - 1][self._num_cols - 1]:
            return True

        movements = [
            (0, 1, "right"),  # move right
            (0, -1, "left"),  # move left
            (1, 0, "bottom"),  # move down
            (-1, 0, "top"),  # move up
        ]
        adjacents = current._adjacent_cells(self)
        for cell in adjacents:
            if not cell.visited:
                for dir_row, dir_col, direction in movements:
                    next_row = current.row + dir_row
                    next_col = current.col + dir_col
                    if (
                        cell.row == next_row
                        and cell.col == next_col
                        and not getattr(current.walls, direction)
                    ):
                        current.draw_move(cell)
                        if self.solve(cell.row, cell.col):
                            return True
                        current.draw_move(cell, undo=True)
        return False

    def prompt_solve_maze(self):
        response = messagebox.askyesno("Solve Maze", "Do you want to solve the maze?")
        if response:
            self.solve(0, 0)
        return
