from typing import Tuple

import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        # ...
        super().__init__(life)

        self.cell_size = cell_size
        self.height = self.cell_size * self.life.rows
        self.width = self.cell_size * self.life.cols
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.life.cols * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for row in range(len(self.life.curr_generation)):
            for col in range(len(self.life.curr_generation[0])):
                clr = pygame.Color("green") if self.life.curr_generation[row][col] == 1 else pygame.Color("white")

                pygame.draw.rect(
                    self.screen, clr, (self.cell_size * col, self.cell_size * row, self.cell_size, self.cell_size)
                )

    def change(self, pos: Tuple) -> None:
        x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
        if self.life.curr_generation[y][x] == 0:
            self.life.curr_generation[y][x] = 1
        else:
            self.life.curr_generation[y][x] = 0

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.change(pos)

            if pause is False:
                self.life.step()

            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)



life = GameOfLife(size=(20, 30), randomize=True)
gui = GUI(life, cell_size=15)
gui.run()


