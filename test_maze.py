import unittest
from maze import Maze
from graphics import Window


class Tests(unittest.TestCase):
    rows, cols = 6, 8
    window = Window(800, 600)
    x, y = 0, 0
    cell_x, cell_y = 50, 30
    seed = 0  # ! removes randomness
    maze = Maze(x, y, rows, cols, cell_x, cell_y, window, seed)

    # - Testing Maze class
    def test_maze_create_cells(self):
        # ! Test if maze creates correct number of cells
        self.assertEqual(len(self.maze._cells), self.rows)
        self.assertEqual(len(self.maze._cells[0]), self.cols)

    def test_maze_cell_size(self):
        # ! test maze cells sizes are correct
        self.assertEqual(self.maze._cell_size_x, self.cell_x)
        self.assertEqual(self.maze._cell_size_y, self.cell_y)

    def test_maze_entry_and_exit(self):
        # ! test maze entry and exit
        self.assertTrue(self.maze._cells[0][0].walls.left)
        self.assertTrue(
            self.maze._cells[self.maze._num_rows - 1][
                self.maze._num_cols - 1
            ].walls.right
        )
        # call for _break_entrance_and_exit
        self.maze._break_entrance_and_exit()

        self.assertFalse(self.maze._cells[0][0].walls.left)
        self.assertFalse(self.maze._cells[0][0].walls.bottom)

        self.assertFalse(
            self.maze._cells[self.maze._num_rows - 1][
                self.maze._num_cols - 1
            ].walls.right
        )
        self.assertFalse(
            self.maze._cells[self.maze._num_rows - 1][self.maze._num_cols - 1].walls.top
        )

    def test_adjacent_cells(self):
        # ! - test adjacent cells of each cell
        i, j = 3, 4  # middle of the maze
        first_cell = self.maze._cells[0][0]
        middle_of_row_cell = self.maze._cells[0][j]
        middle_of_col_cell = self.maze._cells[i][0]
        last_cell = self.maze._cells[self.maze._num_rows - 1][self.maze._num_cols - 1]

        # testing number of adjacent cells
        self.assertEqual(len(first_cell._adjacent_cells(self.maze)), 2)
        self.assertEqual(len(last_cell._adjacent_cells(self.maze)), 2)
        self.assertEqual(len(self.maze._cells[i][j]._adjacent_cells(self.maze)), 4)
        self.assertEqual(len(middle_of_row_cell._adjacent_cells(self.maze)), 3)
        self.assertEqual(len(middle_of_col_cell._adjacent_cells(self.maze)), 3)

        # testing if adjacent cells are correct
        self.assertTrue(self.maze._cells[0][1] in first_cell._adjacent_cells(self.maze))
        self.assertTrue(
            self.maze._cells[self.maze._num_rows - 1][self.maze._num_cols - 2]
            in last_cell._adjacent_cells(self.maze)
        )

    def test_maze_reset_cells(self):
        # ! - test reseting cells visited
        self.maze._cells[0][0].visited = True
        self.maze._cells[0][1].visited = True
        self.maze._cells[0][2].visited = True
        self.maze._reset_cells_visited()
        self.assertFalse(self.maze._cells[0][0].visited)
        self.assertFalse(self.maze._cells[0][1].visited)
        self.assertFalse(self.maze._cells[0][2].visited)


if __name__ == "__main__":
    unittest.main()
