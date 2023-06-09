import pathlib
import typing as tp
from random import randint
from typing import Optional, Tuple

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, size: Tuple[int, int], randomize: bool = True, max_generations: Optional[int] = None) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток

        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                x, y = cell[0] + i, cell[1] + j
                if -1 < y < self.cols and -1 < x < self.rows:
                    if bool(i) + bool(j):
                        neighbors.append(self.curr_generation[x][y])
        return neighbors

    def get_next_generation(self) -> Grid:
        next_grid = self.create_grid()
        grid = self.curr_generation
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                s = sum(self.get_neighbours((row, col)))
                next_grid[row][col] = 1 if (s in (2, 3)) and grid[row][col] == 1 or s == 3 else 0
        return next_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.generations += 1
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return self.generations >= self.max_generations
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r+") as f:
            lines = list(f)
            lines = list(map(lambda x: x[:-2].split(), lines))  # type:ignore
            grid = [list(map(int, i)) for i in lines]
            size = (len(grid), len(grid[0]))
            return GameOfLife(size, False)

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w+") as f:
            for _ in self.curr_generation:
                for x in _:
                    f.write(str(x) + " ")
                f.write("\n")



