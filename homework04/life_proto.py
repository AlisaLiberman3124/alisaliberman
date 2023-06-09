import typing as tp
from pprint import pprint as pp
from random import randint

import pygame  # type: ignore
from pygame.locals import *  # type: ignore

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return [[randint(0, 1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                clr = pygame.Color("green") if self.grid[row][col] == 1 else pygame.Color("white")

                pygame.draw.rect(
                    self.screen, clr, (self.cell_size * col, self.cell_size * row, self.cell_size, self.cell_size)
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        res = []
        row = cell[0]
        col = cell[1]
        if row - 1 >= 0:
            res.append(self.grid[row - 1][col])
            if col - 1 >= 0:
                res.append(self.grid[row - 1][col - 1])
            if col + 1 <= len(self.grid[0]) - 1:
                res.append(self.grid[row - 1][col + 1])
        if row + 1 <= len(self.grid) - 1:
            res.append(self.grid[row + 1][col])
            if col - 1 >= 0:
                res.append(self.grid[row + 1][col - 1])
            if col + 1 <= len(self.grid[0]) - 1:
                res.append(self.grid[row + 1][col + 1])
        if col - 1 >= 0:
            res.append(self.grid[row][col - 1])
        if col + 1 <= len(self.grid[0]) - 1:
            res.append(self.grid[row][col + 1])
        return res

    def get_next_generation(self) -> Grid:
        next_grid = self.create_grid()
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                s = sum(self.get_neighbours((row, col)))
                if (s in (2, 3)) and self.grid[row][col] == 1:
                    next_grid[row][col] = 1
                elif s == 3:
                    next_grid[row][col] = 1
                else:
                    next_grid[row][col] = 0
        return next_grid

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife(400, 400, 10)
    game.run()
    # grid = game.create_grid(randomize=True)
    # pp(grid)
    # pp(game.get_next_generation())
    game.grid = [
        [1, 1, 0, 0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1],
    ]
    pp(game.get_next_generation())


