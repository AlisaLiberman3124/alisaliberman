import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку"""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток"""
        grid = self.life.curr_generation
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                smile = "+" if grid[row][col] == 1 else " "
                screen.addstr(row, col, smile)

    def run(self) -> None:
        screen = curses.initscr()  # type:ignore
        # PUT YOUR CODE HERE
        self.draw_borders(screen)
        self.draw_grid(screen)

        while not self.life.is_max_generations_exceeded and self.life.is_changing:
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(0.2)
        curses.endwin()  # type:ignore


scr = curses.initscr()  # type:ignore
size = scr.getmaxyx()
curses.endwin()  # type:ignore

life = GameOfLife((size[0] - 10, size[1] - 10), max_generations=100)
ui = Console(life)
ui.run()
