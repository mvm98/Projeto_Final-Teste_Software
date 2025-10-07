# test_game_logic.py
import pytest
import numpy as np
from game_logic import SudokuGame

class TestSudokuGame:
    def test_init(self):
        """Testa inicialização da classe SudokuGame"""
        game = SudokuGame()
        assert game.grid.shape == (9, 9)
        assert game.numeros == list(range(1, 10))
        assert game.original is None
        assert game.change is None
        assert game.n_remove == 40

    def test_pode_colocar_valid(self):
        """Testa se pode_colocar retorna True para posição válida"""
        game = SudokuGame()
        game.grid[0][0] = 1
        # Testa posição onde número pode ser colocado
        assert game.pode_colocar(1, 1, 2) == True

    def test_pode_colocar_linha_invalida(self):
        """Testa se pode_colocar retorna False para número na mesma linha"""
        game = SudokuGame()
        game.grid[0][0] = 1
        assert game.pode_colocar(0, 1, 1) == False

    def test_pode_colocar_coluna_invalida(self):
        """Testa se pode_colocar retorna False para número na mesma coluna"""
        game = SudokuGame()
        game.grid[0][0] = 1
        assert game.pode_colocar(1, 0, 1) == False

    def test_pode_colocar_bloco_invalido(self):
        """Testa se pode_colocar retorna False para número no mesmo bloco 3x3"""
        game = SudokuGame()
        game.grid[0][0] = 1
        assert game.pode_colocar(1, 1, 1) == False

    def test_generate_creates_valid_puzzle(self):
        """Testa se generate cria um puzzle válido"""
        game = SudokuGame(n_remove=5)
        game.generate()
        
        assert game.original is not None
        assert game.change is not None
        assert np.array_equal(game.original, game.grid)
        
        # Verifica se foram removidas células
        zeros_count = np.count_nonzero(game.change == 0)
        assert zeros_count == 5

    def test_generate_with_custom_n_remove(self):
        """Testa generate com valor personalizado de n_remove"""
        game = SudokuGame(n_remove=10)
        game.generate(n_remove=15)
        zeros_count = np.count_nonzero(game.change == 0)
        assert zeros_count == 15

    def test_is_solved_by_player_true(self):
        """Testa is_solved_by_player com grid correto"""
        game = SudokuGame()
        game.generate(n_remove=5)
        assert game.is_solved_by_player(game.original) == True

    def test_is_solved_by_player_false(self):
        """Testa is_solved_by_player com grid incorreto"""
        game = SudokuGame()
        game.generate(n_remove=5)
        wrong_grid = game.original.copy()
        wrong_grid[0][0] = 0
        assert game.is_solved_by_player(wrong_grid) == False

    def test_is_solved_by_player_none_original(self):
        """Testa is_solved_by_player quando original é None"""
        game = SudokuGame()
        assert game.is_solved_by_player(np.zeros((9, 9))) == False

    def test_resolver_grid_completes_sudoku(self):
        """Testa se resolver_grid completa o Sudoku corretamente"""
        game = SudokuGame()
        game.grid = np.zeros((9, 9), dtype=int)
        result = game.resolver_grid()
        
        assert result == True
        # Verifica se todas as células estão preenchidas
        assert np.all(game.grid != 0)
        
        # Verifica validade da solução
        for i in range(9):
            for j in range(9):
                num = game.grid[i][j]
                game.grid[i][j] = 0
                assert game.pode_colocar(i, j, num) == True
                game.grid[i][j] = num