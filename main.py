from graphics import Window
from maze import Maze


def main():
    # - Let's create a Maze !
    window = Window(800, 600)
    maze = Maze(20, 20, 10,14, 80,50, window)

    # * Let's break some walls !
    maze._break_walls_r(0, 0)
    maze._redraw()
    maze._reset_cells_visited()

    # ? should we solve the maze?

    maze._break_entrance_and_exit()
    maze.prompt_solve_maze()

    # //  just close the window
    window.wait_for_close()


main()
