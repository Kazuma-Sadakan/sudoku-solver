import time
import pygame
import copy
import requests

"""
board: 9x9 grid cells 
boxes: each cells 
units: 3x3 squares 
peers: boxes in the row, the col, and units which the particular box belongs 
"""

pygame.init()
WHITE = pygame.Color("White")
BLACK = pygame.Color("Black")
ORANGE = pygame.Color("Orange")
RED = pygame.Color("Red")
BOX_SIZE = 50
WIDTH = 450
MARGIN = 50
PADDING = 15
font = pygame.font.SysFont("ubuntu", 25)


def display(board):
    for row in range(len(board)):
        st = ""
        for col in range(len(board[0])):
            if not col % 3 and not col == 0: 
                st += " | " 
            st += str(board[row][col])
        print(st)
        if not (row + 1) % 3:
            st = "-" * 15
            print(st)

class Block:
    def __init__(self, window, row, col, value, color = BLACK):
        self.row = row
        self.col = col
        self.value = value if value != 0 else ""
        self.color = color
        self.window = window
        self.x = self.col * BOX_SIZE 
        self.y = self.row * BOX_SIZE 

    def draw_box(self):
        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.x + BOX_SIZE, self.y + BOX_SIZE), 1)

    def set_color(self, color):
        self.color = color 

    def insert_value(self, value):
        self.value = value 

    def update(self):
        self.draw_box()
        number = font.render(str(self.value), True, BLACK)
        self.window.blit(number, pygame.Vector2((PADDING + self.x, PADDING + self.y)))
        self.draw_box()
   

class Sudoku:
    difficulty = "easy"
    url = f"https://sugoku.herokuapp.com/board?difficulty={difficulty}"

    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("Sudoku")
        self.window.fill(WHITE) 
        self.values = None
        self.box_list = []

    def initialize(self):
        self.reset()
        self.update()

    def get_values(self):
        response = requests.get(Sudoku.url)
        self.values = response.json()['board']

    def set_values(self):
        for row in range(len(self.values)):
            for col in range(len(self.values[0])):
                self.box_list[row][col] = Block(self.window, row, col, self.values[row][col])

    def reset(self):
        self.window.fill(WHITE) 
        self.get_values()
        self.box_list = copy.deepcopy(self.values)
        self.set_values()
        display(self.values)

    def update(self):
        self.window.fill(WHITE) 
        for row in range(len(self.values)):
            for col in range(len(self.values[0])):
                self.box_list[row][col].update()
        pygame.display.flip()

    def _get_empty_cell(self):
        for row in range(9):
            for col in range(9):
                if self.values[row][col] == 0:
                    return row, col
        return None, None

    def _is_valid(self, value, row, col):
        if value in self.values[row]:
            return False 

        if value in [row[col] for row in self.values]:
            return False 

        block = ((row // 3)*3, (col//3)*3)
        for grid_row in self.values[block[0]: block[0] + 3]:
            if value in grid_row[block[1]: block[1] + 3]:
                return False 

        return True

    def solve(self):
        row, col = self._get_empty_cell() 
        if row is None and col is None:
            display(self.values)
            return True

        for val in range(1, 10):
            if self._is_valid(val, row, col):
                self.values[row][col] = val
                self.box_list[row][col].insert_value(val)
                time.sleep(0.001)

                self.update()

                if self.solve():
                    return True

            self.values[row][col] = 0
            self.box_list[row][col].insert_value("")
            self.update()
            
        return False 


