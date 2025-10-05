import pygame
import sys
import numpy as np
import random

# ---------- Sudoku logic (classe) ----------
class SudokuGame:
    def __init__(self):
        self.grid = np.zeros((9, 9), dtype=int)  # usada pelo solver para construir solução
        self.numeros = list(range(1, 10))
        self.original = None  # solução completa (preenchida)
        self.change = None    # puzzle com buracos (visível ao jogador)

    def pode_colocar(self, linha, coluna, numero):
        # verifica linha e coluna
        if numero in self.grid[linha]:
            return False
        if numero in self.grid[:, coluna]:
            return False
        # verifica bloco 3x3
        start_row, start_col = linha - (linha % 3), coluna - (coluna % 3)
        if numero in self.grid[start_row:start_row+3, start_col:start_col+3]:
            return False
        return True

    def resolver_grid(self):
        # backtracking para preencher self.grid (solução completa)
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    random.shuffle(self.numeros)
                    for num in self.numeros:
                        if self.pode_colocar(i, j, num):
                            self.grid[i][j] = num
                            if self.resolver_grid():
                                return True
                            self.grid[i][j] = 0
                    return False
        return True

    def generate(self, n_remove=30):
        # gera solução completa e depois remove números para criar puzzle
        self.grid[:] = 0
        self.resolver_grid()
        self.original = self.grid.copy()
        # create change (puzzle)
        self.change = self.original.copy()
        to_remove = n_remove
        # remove unique positions
        positions = [(i, j) for i in range(9) for j in range(9)]
        # shuffle positions and pop first to_remove
        random.shuffle(positions)
        for (i, j) in positions[:to_remove]:
            self.change[i][j] = 0

    def is_solved_by_player(self, player_grid):
        # verifica se player_grid == original solução
        if self.original is None:
            return False
        return np.array_equal(player_grid, self.original)